import sys,os,time,traceback,ConfigParser,thread,threading
from testlibs import *
from testlibs.toolslib import *
from htx import Win32Message
from testlibs.tftp import tftpcfg, tftp_engine
import wx
import random
import serial,glob
from ctypes import *
import win32com.client
import pythoncom
execfile("system.ini")
config_path=os.getcwd()+'\\testlibs\\model\\%s\\config.ini'%dut_model
execfile(config_path)
if os.path.isfile('c:\\station.ini'):
    execfile('c:\\station.ini')

#gpib = GPIB.SICL_GPIB()
mac_list=list()

#print os.popen("regsvr32 /s mcl_pm.dll")
#pm=win32com.client.Dispatch("MCL_PM.USB_PM")
#pm_id=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch,pm)
#sdk = win32com.client.Dispatch("MCL_PM.USB_PM")

def GetMacAddress(parent,dut_id):
    global mac_list
    val = eval('parent.MAC%d'%dut_id).GetValue()
    try:
        #if len(val) == 12 and int(val,16):
        #if (len(val) == 12 or len(val) == 10):
           #return val
        if val not in mac_list:
           mac_list.append(val)
           return val
    except ValueError:
           pass
    raise Except("Input MAC Error: %s !"%val)

def GetSN(parent,dut_id):
    val = eval('parent.SN%d'%dut.id).GetValue()
    try:
        #if len(val) == 12 and int(val,16):
        if (len(val) == 12 or len(val) == 1):
           return val 
    except ValueError:
           pass
    raise Except("Input Label Error %s !"%val)

def Check_boot(parent,dut_id,term,log):
    parent.SendMessage(dut_id,"Waitting for DUT bootup...\n",log)
    term.write('qu\n')
    test_time_=time.time()
    while 1:
       #term.write('\n')
       data=term.read(term.inWaiting()); print data
       if 'lan0' in data: lWaitCmdTerm(term,"kill `pidof osssidpgrm`","#",5); break
       else: time.sleep(2); term.write('ifconfig\n')
       if time.time()-test_time_ > 30: raise Except("FAIL: DUT Boot Fail")  
    #if not IsConnect(target,100):  raise Except("FAIL: DUT Boot Fail") 
    parent.SendMessage(dut_id,"DUT bootup success...\n",log)
    
def Check_boot_testmode(parent,dut_id,term,log):
    parent.SendMessage(dut_id,"Waitting for DUT bootup...\n",log)
    test_time_=time.time()
    flag=0
    while 1:
       data=term.read(term.inWaiting()); print data
       if not len(data): flag+=1; time.sleep(2); print flag
       else: flag=0       
       if time.time()-test_time_ > 20 or flag>3: 
          lWaitCmdTerm(term,"qu","#",5)
          data=lWaitCmdTerm(term,"ifconfig","#",5)
          if 'lo' not in data: raise Except("FAIL: DUT Boot Fail")
          else: break
    parent.SendMessage(dut_id,"DUT bootup success...\n",log)       

def Enter_Testmode(parent,dut_id,term,log):
    lWaitCmdTerm(term,'testmode',"#",20)
    lWaitCmdTerm(term,'cli',">",10)
    lWaitCmdTerm(term,'logger',"logger>",15)
    lWaitCmdTerm(term,'AllModulesConfig 1 0',"logger>",3)
    lWaitCmdTerm(term,'ModuleConfig 1 51 1',"logger>",3)
    lWaitCmdTerm(term,'ComponentConfig 1 1',"logger>",3)
    lWaitCmdTerm(term,'exit\n',">",3)

def ClitoCal(parent,dut_id,term,log):
    lWaitCmdTerm(term,"top",">",3)
    lWaitCmdTerm(term,"docsis","sis>",3)
    lWaitCmdTerm(term,"Prod","ion>",3) 
    lWaitCmdTerm(term,"Test","Test>",3)
    lWaitCmdTerm(term,"testmode","Test>",30)
    lWaitCmdTerm(term,"exit","ion>",3)
    lWaitCmdTerm(term,"Cali","ion>",3)
    
def ParameterSetup(parent,dut_id,term,mac,sn,log):
    test_time = time.time()
    parent.SendMessage(dut_id,"Set NVM Parameter Start...\n" ,log)
    lWaitCmdTerm(term,"cli","mainMenu>",5)
    lWaitCmdTerm(term,"docsis","docsis>",5) 
    lWaitCmdTerm(term,"Manu","Manufacture>",3)
    lWaitCmdTerm(term,"macAddr %s"%mac,"Manufacture>",3)
    parent.SendMessage(dut_id,"Set MAC Address: %s \n"%mac ,log)    
    lWaitCmdTerm(term,"setSN %s"%sn,"Manufacture>",3)
    parent.SendMessage(dut_id,"Set Serial Number: %s \n"%sn ,log)    
    parent.SendMessage(dut_id,"Set NVM Parameter time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)

class UsCalthread(threading.Thread):
      def __init__(self,parent,pm_id,dut_id,term,diplexer_list,us_freqs,log):
          threading.Thread.__init__(self)
          self.parent=parent
          self.dut_id=dut_id
          self.pm_id=pm_id
          self.term=term
          self.diplexer_list=diplexer_list
          self.us_freqs=us_freqs
          self.log=log
          self.test_flag=None
          self.msg=str()
          self.running=True
          self.mainrunning=True
      def run(self):
          pid.acquire()
          print 'Dut[%s] start the test'%self.dut_id
          pythoncom.CoInitialize()
          sdk = win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(self.pm_id,pythoncom.IID_IDispatch))
          for t in xrange(5):
            sdk.Init_PM()
            if not sdk.GetStatus() and t == 4: 
              pythoncom.CoUninitialize(); time.sleep(2)
              pid.release(); #time.sleep(2)
              self.running=False
              self.test_flag=1
              self.msg="USB PowerMeter not ready"
              raise Except('USB PowerMeter not ready')
            elif sdk.GetStatus(): print sdk.GetStatus(); break
            else: time.sleep(1) 
          sdk.SetFasterMode(1)
          sdk.AvgCount=10; sdk.AVG=1
          for diplexer in self.diplexer_list:     
            us_table=dict()
            diplexer_index=self.us_freqs[diplexer][0]
            for i in range(5):
              data=lWaitCmdTerm(self.term,"setDiplexer %s"%diplexer_index,">",5)
              if diplexer in data: self.parent.SendMessage(self.dut_id,"\nswithch to %s\n"%diplexer,self.log); break
              elif i == 4: 
                pythoncom.CoUninitialize(); time.sleep(2)
                pid.release(); #time.sleep(2)
                self.running=False
                self.test_flag=1
                self.msg="Fail to switch %s"%diplexer 
                raise Except('Fail: switch to %s'%diplexer)  
            freq_range=self.us_freqs[diplexer][1]
            self.parent.SendMessage(self.dut_id,"Upstream Frequencies:%s\n"%freq_range,self.log)
            lWaitCmdTerm(self.term,"Up",">",5)
            if int(diplexer_index) == 1:
              for i in range(8):
                lWaitCmdTerm(self.term,"upstream %s 0"%i,"ion>",5)
              lWaitCmdTerm(self.term,"er 0",">",5,2)
              lWaitCmdTerm(self.term,"freq 0 20",">",5)
              lWaitCmdTerm(self.term,"modulation 0 1",">",5)
              lWaitCmdTerm(self.term,"symb 0 1",">",10)
              lWaitCmdTerm(self.term,"cont 0 1",">",5)
              lWaitCmdTerm(self.term,"sdattn 0 0",">",5)
              lWaitCmdTerm(self.term,"uf\n",">",5)   
              lWaitCmdTerm(self.term,"er 2\n",">",5,2)
              lWaitCmdTerm(self.term,"upstream 0 1",">",5)
              lWaitCmdTerm(self.term,"gain %s"%pga_gain,">",5)
              for index,f in enumerate(freq_range):          
                sdk.Freq='%s'%f
                for try_ in range(1):
                  lWaitCmdTerm(self.term,"freq 0 %f"%f,">",5)
                  r=float('%.3f'%(sdk.ReadPower()+54.35)); print r
                  #r = gpib.ReadUSQPSKPower(f,200,400)+0.2; r=float('%.2f'%r)
                  msg = "Freq=%.1f measure=%.3f (%.3f ~ %.3f)"%(f,r,self.us_freqs[diplexer][2][index]-self.us_freqs[diplexer][3][index],self.us_freqs[diplexer][2][index]+self.us_freqs[diplexer][3][index])
                  if r<self.us_freqs[diplexer][2][index]-self.us_freqs[diplexer][3][index] or r>self.us_freqs[diplexer][2][index]+self.us_freqs[diplexer][3][index]:
                     msg = "Freq=%.1f measure=%.3f (%.3f ~ %.3f) --- fail"%(f,r,self.us_freqs[diplexer][2][index]-self.us_freqs[diplexer][3][index],self.us_freqs[diplexer][2][index]+self.us_freqs[diplexer][3][index])
                     if run_flow:
                       self.parent.SendMessage(self.dut_id,"%s\n"%msg,self.log)
                       self.test_flag=1
                     else:
                      lWaitCmdTerm(self.term,"upstream 0 0",">",5)
                      pythoncom.CoUninitialize(); time.sleep(2)
                      pid.release(); #time.sleep(2)
                      self.running=False                       
                      self.test_flag=1
                      self.msg=msg
                      raise Except('%s\n'%msg)                
                  else:
                     self.parent.SendMessage(self.dut_id,"%s\n"%msg,self.log); break              
                lWaitCmdTerm(self.term,"sfreq %.3f %.3f"%(f,r),">",5,3)       
                us_table.update([(float(f),r)])
              lWaitCmdTerm(self.term,"uf",">",5)
              USCal_Table_Verify(self.parent,self.dut_id,freq_range,us_table,self.term,self.log)
              lWaitCmdTerm(self.term,"exit",">",5)
            else:
              lWaitCmdTerm(self.term,"uf",">",5)   
              lWaitCmdTerm(self.term,"er 2",">",5,2)
              USOFDMA=list()
              lWaitCmdTerm(self.term,"exit",">",5)
              lWaitCmdTerm(self.term,"exit",">",5)
              lWaitCmdTerm(self.term,"Test",">",5)
              lWaitCmdTerm(self.term,"freq 0 5.1","est>",5)
              lWaitCmdTerm(self.term,"gain 25","est>",5)
              lWaitCmdTerm(self.term,"symb 0 1","est>",5)
              lWaitCmdTerm(self.term,"mod 0 1","est>",5)
              lWaitCmdTerm(self.term,"sdattn 0 0","est>",5)
              lWaitCmdTerm(self.term,"cont 0 1","est>",5)
              lWaitCmdTerm(self.term,"upstream 0 1","est>",5)
              sc_qam=float('%.3f'%(sdk.ReadPower()+54.35)); print sc_qam
              #sc_qam = gpib.ReadUSQPSKPower(5.1,200,400)+0.1
              lWaitCmdTerm(self.term,"upstream 0 0","est>",5)        
              lWaitCmdTerm(self.term,"gpioSetValue 0 1","est>",5)
              lWaitCmdTerm(self.term,"sdattn 8 15","est>",5)
              lWaitCmdTerm(self.term,"gain %s"%pga_gain,"est>",5)
              lWaitCmdTerm(self.term,"UsOfdma","UsOfdma>",5)
              diff=0
              #gpib.SetUSOFDMACal()
              for index,f in enumerate(freq_range):
                sdk.Freq='%s'%f
                for try_ in range(1):
                  f_=int(f*1000000)
                  lWaitCmdTerm(self.term,"sendTestSine 0 %s 1 0"%f_,">",5)
                  r=float('%.3f'%(sdk.ReadPower()+54.35)); print r
                  #r=gpib.ReadUSOFDMAPower(f,100,150)+0.1
                  if not diff:               
                    diff=abs(sc_qam-r)
                    if diff>7: 
                      pythoncom.CoUninitialize(); time.sleep(2)
                      pid.release()
                      self.running=False
                      self.test_flag=1
                      self.msg='diff:%s over spec(<7)'%diff
                      raise Except('Fail: diff:%s over spec(<7)\n'%diff)
                    self.parent.SendMessage(self.dut_id,'difference of sc_qam and ofdma is %.3f\n'%diff,self.log)
                  r_=r+diff; r_=float('%.3f'%r_)
                  msg = "Freq=%.1f OFDMA_measure=%.3f OFDMAtoSCQAM=%.3f (%.3f ~ %.3f)"%(f,r,r_,self.us_freqs[diplexer][2][index]-self.us_freqs[diplexer][3][index],self.us_freqs[diplexer][2][index]+self.us_freqs[diplexer][3][index])
                  if r_<us_freqs[diplexer][2][index]-us_freqs[diplexer][3][index] or r_>us_freqs[diplexer][2][index]+us_freqs[diplexer][3][index]:
                    msg = "Freq=%.1f OFDMA_measure=%.3f OFDMAtoSCQAM=%.3f (%.3f ~ %.3f) --- fail"%(f,r,r_,self.us_freqs[diplexer][2][index]-self.us_freqs[diplexer][3][index],self.us_freqs[diplexer][2][index]+self.us_freqs[diplexer][3][index])
                    if run_flow:
                       self.parent.SendMessage(self.dut_id,"%s\n"%msg,self.log)
                       self.test_flag=1
                    else:
                      lWaitCmdTerm(self.term,"sendTestSine 0 %s 0 0"%f_,">",5)
                      pythoncom.CoUninitialize(); time.sleep(2)
                      pid.release()
                      self.running=False
                      self.test_flag=1
                      self.msg=msg
                      raise Except('%s\n'%msg)  
                  else:
                    self.parent.SendMessage(self.dut_id,"%s\n"%msg,self.log); break
                USOFDMA.append(r_)
              lWaitCmdTerm(self.term,"sendTestSine 0 %s 0 0"%f_,">",5)
              lWaitCmdTerm(self.term,"exit\n",">",5)
              lWaitCmdTerm(self.term,"exit\n",">",5)
              lWaitCmdTerm(self.term,"Cal\n",">",5)
              lWaitCmdTerm(self.term,"Up\n",">",5)
              lWaitCmdTerm(self.term,"er 0\n",">",5,2)           
              lWaitCmdTerm(self.term,"uf\n",">",5)   
              lWaitCmdTerm(self.term,"er 2\n",">",5,2)
              for index,f in enumerate(freq_range):        
                 lWaitCmdTerm(self.term,"sfreq %.3f %.3f\n"%(f,USOFDMA[index]),">",5,3)       
                 us_table.update([(float(f),USOFDMA[index])])
              lWaitCmdTerm(self.term,"uf\n",">",5)
              USCal_Table_Verify(self.parent,self.dut_id,freq_range,us_table,self.term,self.log)
              lWaitCmdTerm(self.term,"exit\n",">",5)
    
          if pid.locked():
             pid.release()
          self.running=False
          pythoncom.CoUninitialize()

      def join(self):    
          threading.Thread.join(self)
          return self.test_flag,self.msg

pid=thread.allocate_lock()
def USCalibration(parent,dut_id,term,log):  
    test_time = time.time()
    pythoncom.CoInitialize()
    pm=win32com.client.Dispatch("MCL_PM.USB_PM")
    pm_id=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch,pm)
    process=UsCalthread(parent,pm_id,dut_id,term,diplexer_list,us_freqs,log)
    process.start()
    (test_flag,msg)=process.join(); print test_flag    
    pm.Close_Sensor()
    parent.SendMessage(dut_id,'US Calibration Test Done\n',log)
    parent.SendMessage(dut_id,"US Calibration time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
    if test_flag: 
       lWaitCmdTerm(term,"qu","#",3)
       raise Except("FAIL: %s\n"%msg)
       
def USCal_Table_Verify(parent,dut_id,freq,us_table,term,log):
    testfail=0
    data=lWaitCmdTerm(term,'print 1',">",10)
    if print_table: parent.SendMessage(dut_id,"%s\n"%data,log)
    freq_list=list(); power_list=list(); USCal_Table_Board=dict()
    data_list=data.splitlines()
    for i in data_list:
      if 'Freq=' in i: freq_list.append(float(i.split('Freq=')[-1].split('Power')[0]))
      if 'Power=' in i: power_list.append(float(i.split('Power=')[-1].split('Delta')[0]))
    for index in xrange(len(freq_list)): USCal_Table_Board.update([(freq_list[index],power_list[index])])
    print USCal_Table_Board,us_table
    for index in freq:
      if us_table[index]!=USCal_Table_Board[index]:
         testfail=1
         parent.SendMessage(dut_id,"Freq:%s Power:%s(%s) not matched\n"%(index,us_table[index],USCal_Table_Board[index]),log)
    if testfail: lWaitCmdTerm(term,"qu","#",3); raise Except("FAIL: US Table\n")
    
def mxl277_cmoa_csn(parent,dut_id,term,basePower,bandwidth,log):
    '''
    author: YiJie Wang
    date: 2016/12/15
    description: *calibrate 5 diplexer for cmoa-csn
                 *multi-path for multi-dut
    '''
    result=0
    test_time = time.time()
    for diplexer in diplexer_list:
      diplexer_index=ds_freqs[diplexer][0]
      for i in range(5):
        data=lWaitCmdTerm(term,"setDiplexer %s"%diplexer_index,">",5)
        #if diplexer in data: parent.SendMessage(dut_id,"\nswithch to %s\n"%diplexer,log); break
        #elif i == 4: raise Except('Fail: switch to %s'%diplexer) 
        #else: continue 
      lWaitCmdTerm(term,"Down",">",5)
      freq_range=ds_freqs[diplexer][1]
      attn,ds_data=Read_Get_table(dut_id,freq_range,basePower,bandwidth,log)
      pportOut(attn,0x378)
            
      parent.SendMessage(dut_id,"Diplexer %s Frequencies: %s \n"%(diplexer,ds_data[0]),log)
      parent.SendMessage(dut_id,"Noise Power: %s \n"%ds_data[1],log)
      
      lWaitCmdTerm(term,"sfreq %s"%ds_data[0],">",5)
      lWaitCmdTerm(term,"spow %s"%ds_data[1],">",5)
      for t in xrange(3):
        print "Start to run %s Calibration....(%d)"%(diplexer,(t+1))
        parent.SendMessage(dut_id,"Start to run %s Calibration....(%d)\n"%(diplexer,(t+1)),log)
        data=lWaitCmdTerm(term,"runcal","Downstream_Calibration>",20)
        if 'D/S Calibration Finished' not in data:
          parent.SendMessage(dut_id,'Downstream calibration Test...(%d) failed\n'%(t+1),log)
          result=1
          continue
        else:
          for check in xrange(3):
            data=lWaitCmdTerm(term,"printTunerCalInfo","ion>",10); print data
            if 'Index' not in data: time.sleep(1); continue
            else: break
          FreqComp=DS_FreqComp[diplexer]
          result=ConfirmM277CalInfo(parent,dut_id,data,FreqComp[0],FreqComp[1],log)
          if result: raise Except("FAIL: %s Cal"%diplexer)
          else: break
      lWaitCmdTerm(term,"exit",">",5)    
    if not result: 
      lWaitCmdTerm(term,"top",">",5,2)
      lWaitCmdTerm(term,"logger",">",5,2)
      lWaitCmdTerm(term,"AllComponentsConfig 0",">",5,2)
      lWaitCmdTerm(term,"exit",">",5,2)
      lWaitCmdTerm(term,"qu","#",5,2); 
      lWaitCmdTerm(term,"setstartup -e","#",5,2)   
    parent.SendMessage(dut_id,'Downstream calibration Test Done\n',log)
    parent.SendMessage(dut_id,"DS Calibration time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
    
def ConfirmM277CalInfo(parent,dut_id,data,TiltIndex,TiltIndex_offset,log): 
    message = str() 
    test_fail = 0
    Segment = [[0 for j in xrange(13)] for i in xrange(2)]
    for i in range(1):
        split_str = data.split('TiltIndex:%d'%i)[-1].split('TiltIndex:%d'%(i+1))[0].strip()
        for j in split_str.splitlines():
            try:
                s_index = int(j.split('Segment:')[-1].split(' | c2')[0].strip())
                c0 = int(j.split('c0=')[-1].strip())
                Segment[i][s_index] = c0
            except:
                pass
    for i in range(1):
        parent.SendMessage(dut_id,'TiltIndex:%d\n'%i,log) 
        for j in range(13):
          if j < 11:
            msg = 'Segment:%d c0= %d (%d ~ %d)'%(j,Segment[i][j],TiltIndex[i][j]-TiltIndex_offset[i][j],TiltIndex[i][j]+TiltIndex_offset[i][j])
            if abs(TiltIndex[i][j] - Segment[i][j]) > TiltIndex_offset[i][j]:
               msg = 'Segment:%d c0= %d (%d ~ %d) --- fail'%(j,Segment[i][j],TiltIndex[i][j]-TiltIndex_offset[i][j],TiltIndex[i][j]+TiltIndex_offset[i][j])
               test_fail=1
               parent.SendMessage(dut_id,'%s\n'%msg,log,1)
            else:
               parent.SendMessage(dut_id,'%s\n'%msg,log,2)
          else:
            msg = 'Segment:%d c0= %d'%(j,Segment[i][j]); parent.SendMessage(dut_id,'%s\n'%msg,log)
    return test_fail

    
def Read_Get_table(dut_id,freqrange,basePower,bandwidth,log):
    attn = int(GetAttnValue("5-1500_%ddbmv_%sMHz_%s"%(basePower,bandwidth,dut_id),"Station.Cal"))
    if not attn:
      parent.SendMessage(dut_id,"Plz Check The NoiseSource_PowerTable",1)
      result = 1
      return result
    ds_data = GetDsCalTable(dut_id,freqrange,basePower,bandwidth)
    return attn,ds_data

def GetAttnValue(filename,path=""):
    result = []
    flag = 0
    if not path:
        path = "."
    if path[-1] not in ["/","\\"]: path += "/"
    fs = glob.glob(path+filename+".*")
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

def GetDsCalTable(dut_id,ds_freq,basePower,bandwidth):
    freqs = powers =''
    gSA_offset=lReadEquipmentOffsetTable("5-1500_%ddbmv_%sMHz_%s"%(basePower,bandwidth,dut_id),"Station.Cal")
    for freq in ds_freq:
       powers= powers + '%0.2f '%lDownstreamFrequencyPower(gSA_offset,freq)
    powers=powers.strip()
    if len(powers.split())<>len(ds_freq):
       raise Except("Read Ds Table Falied")
    for freq in ds_freq:
       freqs = freqs + '%s '%freq
    freqs=freqs.strip()     
    return (freqs,powers)    

def lReadEquipmentOffsetTable(filename,path=""):
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
    freq=int(freq) 
    for i in freqPwrOffsetTab:
        if int(i[0])== int(freq*1000):
            return i[1]

def tftp_dir(parent,dir_path):
    ConfigFile = ConfigParser.SafeConfigParser()
    if ConfigFile.read('tftp.ini'):
     print dir_path
     ConfigFile.set('TFTPSERVER','tftprootfolder',dir_path)
     fp = open('tftp.ini','w')
     ConfigFile.write(fp)
     fp.close()
     cfgdict = tftpcfg.getconfigstrict(os.getcwd, 'tftp.ini')
     TFTPServer = tftp_engine.ServerState(**cfgdict)
     thread.start_new_thread(tftp_engine.loop_nogui,(TFTPServer,))            
    else: print 'tftp dir error'
  
def log_counter(mac,station,count=0):
    for file in os.listdir(logPath):
      if mac in file: count+=1
    log = open(logPath+mac+"_%s.%s"%(count,station),"w")
    return log

def T1(parent):
    try:
        dut_id = parent.id_
        result = 0
        log = None
        mac = ""
        parent.SendMessage(dut_id,"START",state = "START")
        start_time = end_time = 0
        term =serial.Serial(comport[dut_id-1],b_rate)
        mac = GetMacAddress(parent,dut_id)
        #sn = GetSN(parent,dut_id)        
        log = log_counter(mac,FunctionName)
        start_time=time.time()
        parent.SendMessage(dut_id,"%s test program | %s , Station: %s\n"%(dut_model,function_version,FunctionName),log)
        parent.SendMessage(dut_id,"---------------------------------------\n",log)
        parent.SendMessage(dut_id,"Start Time:"+time.ctime()+"\n",log)
        parent.SendMessage(dut_id,"Scan MAC address:"+mac+"\n",log)
        #parent.SendMessage(dut_id,"Scan SN:"+sn+"\n",log)
        #checktravel(mac,'127.0.0.1',1800,20)        
        parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
        Check_boot_testmode(parent,dut_id,term,log)
        Enter_Testmode(parent,dut_id,term,log)
        ClitoCal(parent,dut_id,term,log)                
        if USCal:USCalibration(parent,dut_id,term,log)
        
    except Except,msg:
        parent.SendMessage(dut_id,"\n%s\n"%msg,log,color=1)
        result = 1
    except: 
        parent.SendMessage(dut_id,"\n%s\n"% traceback.print_exc(),log,color=1)
        result = 1
    end_time = time.time()
    parent.SendMessage(dut_id,'\n'+"End Time:"+time.ctime()+'\n',log)
    parent.SendMessage(dut_id,"total time: %3.2f"%(end_time-start_time)+'\n',log)
    if result:
       parent.SendMessage(dut_id,"Test Result:FAIL"+'\n',log,color=1)
    else:
       parent.SendMessage(dut_id,"Test Result:PASS"+'\n',log,color=2)
    if log:log.close()
    if term: term.close()
    if mac: 
       global mac_list
       mac_list.remove(mac)  
       if result:
          parent.SendMessage(dut_id,'\n',state = "FAIL",color=1)
       else:
          parent.SendMessage(dut_id,"",state = "PASS")   
    else: parent.SendMessage(dut_id,"",state = "FAIL")  


def T2(parent):
    try:
        dut_id = parent.id_
        result = 0
        log = None
        mac = ""
        parent.SendMessage(dut_id,"START",state = "START")
        start_time = end_time = 0
        term =serial.Serial(comport[dut_id-1],b_rate)
        mac = GetMacAddress(parent,dut_id)
        #sn = GetSN(parent,dut_id)        
        log = log_counter(mac,FunctionName)
        start_time=time.time()
        parent.SendMessage(dut_id,"%s test program | %s , Station: %s\n"%(dut_model,function_version,FunctionName),log)
        parent.SendMessage(dut_id,"---------------------------------------\n",log)
        parent.SendMessage(dut_id,"Start Time:"+time.ctime()+"\n",log)
        parent.SendMessage(dut_id,"Scan MAC address:"+mac+"\n",log)
        #parent.SendMessage(dut_id,"Scan SN:"+sn+"\n",log)
        #checktravel(mac,'127.0.0.1',1800,20)        
        parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)  
        Check_boot_testmode(parent,dut_id,term,log)
        Enter_Testmode(parent,dut_id,term,log)
        ClitoCal(parent,dut_id,term,log)                
        if DSCal: mxl277_cmoa_csn(parent,dut_id,term,basePower,bandwidth,log)
        
    except Except,msg:
        parent.SendMessage(dut_id,"\n%s\n"%msg,log,color=1)
        result = 1
    except: 
        parent.SendMessage(dut_id,"\n%s\n"% traceback.print_exc(),log,color=1)
        result = 1
    end_time = time.time()
    parent.SendMessage(dut_id,'\n'+"End Time:"+time.ctime()+'\n',log)
    parent.SendMessage(dut_id,"total time: %3.2f"%(end_time-start_time)+'\n',log)
    if result:
       parent.SendMessage(dut_id,"Test Result:FAIL"+'\n',log,color=1)
    else:
       parent.SendMessage(dut_id,"Test Result:PASS"+'\n',log,color=2)
    if log:log.close()
    if term: term.close()
    if mac: 
       global mac_list
       mac_list.remove(mac) 
       if result:
          parent.SendMessage(dut_id,'\n',state = "FAIL",color=1)
       else:
          parent.SendMessage(dut_id,"",state = "PASS")   
    else: parent.SendMessage(dut_id,"",state = "FAIL") 

    
