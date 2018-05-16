import htxlib,GPIB,time,os,time,glob
import pyodbc
from winioport import *
logPath_station = os.getcwd() + "\\Station.Cal"
if not os.path.isdir(logPath_station):
   os.system("mkdir %s"%logPath_station)
execfile("system.ini")
ds_LPT1 = 0x378
#ds_LPT2 = 0x378

default_LPT1_val = 0
#default_LPT2_val = 0 
date = time.localtime()[:3]
class Except:
    """    example:
        try:
            if ....:
                raise Except("Error!!")
        except Except, msg:
            print msg    """
    def __init__(self,msg):
        self.value = msg
    def __str__(self):
        return self.value
    def __repr__(self):
        return self.value            
      
def GetAttnValue(filename,path=""):
    result = list()
    flag = 0
    if not path:
        path = "."
    if path[-1] not in ["/","\\"]: path += "/"
    fs = glob.glob(path+filename)
    if not fs:
        print "Can't read %s%s.*"%(path,filename)
        flag = 0
    else:
        fs.sort()
        print "Read Attn value from:",fs[-1]
        for i in open(fs[-1]).readlines():
            if "Attn" in i:
                attn = round(float(i.split("Attn =")[-1].strip()))
                print "Atenuation = %d"%attn
                return attn
            else:
                print "Can't read Attn value"
                flag = 0
    #raise Except("Can't read Attn value")
    return flag

def lReadEquipmentOffsetTable(filename,path=""):
    import glob

    result = []
    if not path:
        path = "."
    if path[-1] not in ["/","\\"]: path += "/"
    fs = glob.glob(path+filename+".*")
    if not fs:
        print "Can't read %s%s.*"%(path,filename)
    else:
        fs.sort()
        print "Read Compensation from:",fs[-1]
        for i in open(fs[-1]).readlines():
            if not i.strip(): continue
            if i.strip()[0]=='#' or i.strip()[0]=='F': continue
            freq,power,offset = i.split(',')
            result.append((int(float(freq)*1000),
                           float(power),
                           float(offset)))
    return result
    
def lDownstreamFrequencyPower(freqPwrOffsetTab,freq): 
    freq=float(freq) 
    for i in freqPwrOffsetTab:
        if int(i[0])== int(freq*1000):
            return i[1]                

def lReadEquipmentUSTable(filename,path=""):
    import glob
    result = []
    if not path:
        path = "."
    if path[-1] not in ["/","\\"]: path += "/"
    fs = glob.glob(path+filename+".*")
    if not fs:
        print "Can't read %s%s.*"%(path,filename)
    else:
        fs.sort()
        print "Read Compensation from:",fs[-1]
        for i in open(fs[-1]).readlines():
            if not i.strip(): continue
            if i.strip()[0]=='#' or i.strip()[0]=='F': continue
            index,freq,power,repower,offset = i.split(',')
            result.append((int(index),
                           int(freq), 
                           float(power),
                           float(repower),
                           float(offset)))
    return result    

def NS2SA(m540,bw,freq_plan,ds_freqs,noise_path,log):
    #pportOut(default_LPT2_val,ds_LPT2)
    gpib = GPIB.SICL_GPIB()        
    pportOut(default_LPT1_val,ds_LPT1)    
    freqs=list()
    powers=list()
    gpib.SetD3StationCal(bw)    
    try:
        if noise_path>1:
           if not os.path.isfile(logPath_station+'\\%s_%ddbmv_%sMHz_1.%04d%02d%02d'%(freq_plan,m540,bw,date[0],date[1],date[2])):
              msg="No Chain 1 table"
              return (False,msg)
           attn=int(GetAttnValue('%s_%ddbmv_%sMHz_1.%04d%02d%02d'%(freq_plan,m540,bw,date[0],date[1],date[2]),logPath_station))
           if not attn: return (False,'Plz check chain 1 table')
           else:
              msg = logPath_station+'\\%s_%ddbmv_%sMHz_%s.%04d%02d%02d'%(freq_plan,m540,bw,noise_path,date[0],date[1],date[2])
              log.set(msg,1)
              Log=open(logPath_station+'\\%s_%ddbmv_%sMHz_%s.%04d%02d%02d'%(freq_plan,m540,bw,noise_path,date[0],date[1],date[2]),'w')           
        else:
           msg = logPath_station+'\\%s_%ddbmv_%sMHz_%s.%04d%02d%02d'%(freq_plan,m540,bw,noise_path,date[0],date[1],date[2])
           log.set(msg,1)
           Log=open(logPath_station+'\\%s_%ddbmv_%sMHz_%s.%04d%02d%02d'%(freq_plan,m540,bw,noise_path,date[0],date[1],date[2]),'w')       
           for i in range(10): 
               base_pwr=gpib.ReadD3StationCalPower(refer_freq)
               if abs(base_pwr-m540)< 1: break
               attn=int((round(base_pwr-m540))) + default_LPT1_val
               pportOut(attn,ds_LPT1) 
               time.sleep(0.5)              
           if abs(base_pwr-m540)>1: 
              msg='Please check the digital ATTN'
              log.set(msg,2)
              Log.write(msg+'\n')
              return (False,msg)
        
        pportOut(attn,ds_LPT1)
        base_pwr=gpib.ReadD3StationCalPower(refer_freq)
        msg = "Freq = %dMHz, Power = %.2f , Attn = %.1f"%(refer_freq,base_pwr,attn)
        log.set(msg,2)
        Log.write(msg+'\n')
        for freq in ds_freqs:
            pwr =  gpib.ReadD3StationCalPower(freq) 
            freqs.append(freq)
            powers.append(pwr)
            msg = "Freq = %dMHz, Power = %.2f, Delta = %.2f"%(freq,pwr,base_pwr-pwr)
            log.set(msg,2)
            Log.write("%d,%.2f,%.2f\n"%(freq,pwr,base_pwr-pwr))   
        Log.close()
        return (True,freqs,powers)
    except Except,msg:
           return(False,'%s'%msg)  
    except Exception,e:
        msg='SA connection failure'
        if e.message:
           msg=e.message
        return (False,msg)


def CMTS(term,port,freq,bw):
    try:
         gpib = GPIB.SICL_GPIB()
         gpib.SetD3StationCal(bw)
         freq_dspower={}
         freqs=[] 
         powers=[]
         for i in range(4):
              freqs.append(freq+bw*i)
              #freq_dspower_EU.append({})
         data = lWaitCmdTerm(term,'exit','exit',3)
         if 'No CB at'in data:
            raise Except('%s'%data)
         sn=lWaitCmdTerm(term,'sn','sn',3).split()[-1]
         print 'CB SN :'+sn
         lWaitCmdTerm(term,"rf %s c"%port,"OK",5,2)
         ports=['1','2','3','4']
         ports.remove(str(port))
         for p in ports:
             lWaitCmdTerm(term,'rf %s n'%p,'OK',5,2)
             
         for freq in freqs: 
             r=gpib.ReadD3StationCalPower(freq)
             powers.append(r)
             freq_dspower[freq]=r
             print "%s:%.2f,"%(freq,r)
             
         station.write('\ndspower_%s_%s_%s = %s '%(bw,sn,port,repr(freq_dspower)))
         
         return (True,freqs,powers)
    except Except,msg:
           return(False,'%s'%msg)  
    except Exception,e:
           msg='***SA connection failure***'
           if e.message:
              msg=e.message
              return (False,msg)

def UploadDST(term,BasePower,BandWidth,ds_freqs):
    try: 
        attns=[]
        xattns=[]
        powers=[]
        freqs=''
        ps=[[],[],[],[]]
        #ds_freqs=range(88,1002,12)
        data = lWaitCmdTerm(term,'exit','exit',3)
        if 'No CB at'in data:
            raise Except('%s'%data)
        sn=lWaitCmdTerm(term,'sn','sn',3).split()[-1]
        print 'CB SN : %s'%sn
        for i in range(1,5):   
            attns.append(GetAttnValue("NoiseSource_%sdbmv_%sMHz_%s_%s"%(BasePower,BandWidth,sn,i),"C:\\Cal"))
            gSA_offset=lReadEquipmentOffsetTable("NoiseSource_%sdbmv_%sMHz_%s_%s"%(BasePower,BandWidth,sn,i),"C:\\Cal")
            power=''
            for freq in ds_freqs:
                ps[i-1].append(lDownstreamFrequencyPower(gSA_offset,freq))
                power+='%0.2f '%lDownstreamFrequencyPower(gSA_offset,freq)
            power=power.strip()
            #print power
            #print len(power)
            if len(power.split())<>len(ds_freqs):
                raise Except("Read Ds Table Fali for Port %s"%i)
            powers.append(power)
        Cattn=attns[0][0]
        xattns.append(attns[0][1])
        for i in range(3):
            if attns[i][0] <> attns[i+1][0]:
               raise Except('Check Cattn Failed : %s'%str(attns))     
            xattns.append(attns[i+1][1])
        for freq in ds_freqs:
            freqs+='%s '%freq
        freqs=freqs.strip()
        print 'insert data into db'
        if not InsertDSTable(sn,BandWidth,BasePower,freqs,powers,Cattn,xattns):
           raise Except('insert db failed')
        print 'insert data finsh' 
        return True,ds_freqs,ps  
    except Except,msg:
           return(False,'%s'%msg)  
    except Exception,e:
           msg='***SA connection failure***'
           if e.message:
              msg=e.message
              return (False,msg)

def InsertDSTable(sn,bw,basepower,freqs,powers,cattn,xattns):
    logserver='172.28.206.253'
    if '172.28.206' not in os.popen('ipconfig').read():logserver='172.28.209.253'       
    db = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(logserver,'test','test','test')) 
    db.autocommit=True
    cursor = db.cursor()
    tmp = time.localtime(time.time())
    testtime =  "%d/%d/%d %d:%d:%d"%tmp[:6]
    pa=[sn,basepower,bw,freqs,]+xattns+powers+[cattn,testtime]
    sql="insert into NoiseSource_table (module_ID,BasePower,BandSpan,Freqs,Attn1_01dB_1,Attn1_01dB_2,Attn1_01dB_3,\
Attn1_01dB_4,powers_1,powers_2,powers_3,powers_4,Attn2_1dB,DateTime) values ('%s','%s','%s','%s','%s','%s','%s',\
'%s','%s','%s','%s','%s','%s','%s')"%tuple(pa)
    cursor.execute(sql)
    time.sleep(2)
    cursor.execute("select module_ID from NoiseSource_table where DateTime = '%s'"%testtime)
    data = cursor.fetchone()
    if data:
       return data[0]
    else:
       return 0

      
    
     
