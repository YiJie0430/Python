import decimal
import time,thread,htx,odbc,pyodbc,os
import xurl_core,bz2
#from sajet import *
##############
term_locks={}
#sajet_lock = thread.allocate_lock()  
logserver = '172.28.10.52'
mes_lan_ip = '0.0.0.0'
if '172.28.206' in os.popen('ipconfig').read():
   logserver = '172.28.206.253'
   mes_lan_ip = '172.28.206.' + os.popen('ipconfig').read().split('172.28.206.')[-1].split()[0]
if '172.28.209' in os.popen('ipconfig').read():
   logserver = '172.28.209.253'
   mes_lan_ip = '172.28.209.' + os.popen('ipconfig').read().split('172.28.209.')[-1].split()[0]
Station = 'AFI'
if os.path.isfile('c:\\station.ini'):
   execfile('c:\\station.ini') 
##############

def integer(s):
    return int(s)

def strip(s):
    return s.strip()

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

class SocketTTY(object):
      def __init__(self,buf,pos):
          self.buf = buf[pos[0]][pos[1]]
          self.host = str(pos)
          
      def set(self,val):
          return self.buf.SetIn(val+'\r')
          
      def get(self):
          #data = self.buf.Get()
          #print data
          #self.buf.Clear()
          return self.buf.Get()
      
      def clear(self):
          self.buf.Clear()
          
          
      def wait(self,prompt,timeout):
          prompt = str(prompt)
          timeout += time.time()+0.1
          response = ""
          count = 0 
          while time.time() < timeout:
                count += 1
                if not (count&3):
                   print ".",
                d = self.get()
                response += d
                if not prompt:
                   if not d:
                      return (True,response)
                elif prompt in response:
                   if count >= 3:  print
                   return (True, response)
                time.sleep(0.1)
          if count >= 3: print
          return (False, response)
          
          
      def __repr__(self):
          return self.get()

      def __call__(self):
          return self.get()

      def __str__(self):
          return self.get()

      def __lshift__(self,data):
          return self.set(data) 


def lWaitCmdTerm(term,cmd,waitstr,sec,count=1):
    termport=term.host
    termdata=['']
    if not term_locks.has_key(termport):
       term_locks[termport]=thread.allocate_lock()  
    term_locks[termport].acquire() 
    for i in range(count):
       term.get()
       term << "%s"%cmd
       termdata = term.wait("%s"%waitstr,sec); print termdata
       if waitstr in termdata[-1] and 'ttyS0: 1 input overrun' not in termdata[-1]:
          if term_locks[termport].locked: 
             term_locks[termport].release()
          return termdata[-1]
    if term_locks[termport].locked: 
       term_locks[termport].release()
    #print termdata
    raise Except("%s port : %s  return : %s"%(cmd,termport,termdata[-1]))


def checksn(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return]
    '''
    ServerIP,ServerPort,timeout = map(strip,argv[-3]('Base','MESServer').split('|'))
    mac = argv[2][0]
    sn = argv[2][1]
    MesSocket=htx.UDPService(ServerIP,int(ServerPort),int(timeout))
    MesSocket.set('3,' + mac)  
    Result=MesSocket.get()
    print Result
    Result=Result.strip()
    if Result:
       if Result==sn:
          return 1
       else:
            raise Except("ErrorCode(0005):Check SN Failed:%s"%Result)    
    raise Except("ErrorCode(0005):Connection MES Server Fail ")

def checkcsn(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
    '''
    ServerIP,ServerPort,timeout = map(strip,argv[-3]('Base','MESServer').split('|'))
    mac = argv[2][0]
    sn = argv[2][1]
    MesSocket=htx.UDPService(ServerIP,int(ServerPort),int(timeout))
    MesSocket.set('2,' + mac)  
    Result=MesSocket.get()
    print Result
    Result=Result.strip()
    if Result:
       if Result==sn:
          return 1
       else:
            raise Except("ErrorCode(0005):Check CSN Failed:%s"%Result)    
    raise Except("ErrorCode(0005):Connection MES Server Fail ")


def checktravel(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
    '''
    ServerIP,ServerPort,timeout = map(strip,argv[-3]('Base','MESServer').split('|'))
    mac = argv[2][0]
    MesSocket=htx.UDPService(ServerIP,int(ServerPort),int(timeout))
    MesSocket.set('0,'+ mac)  
    Result=MesSocket.get()
    if Result <> '':
       Result=Result.split('_')
       if Result[0]==mac:
         if Result[1]=='OK':
            return 1
         elif Result[1]=='NG':
            raise Except("ErrorCode(0005):Check MES Failed:%s"%"".join(Result).split(':')[-1])    
    raise Except("ErrorCode(0005):Connection MES Server Fail ")


def passtravel(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
    '''
    ServerIP,ServerPort,timeout = map(strip,argv[-3]('Base','MESServer').split('|'))
    mac = argv[2][0]
    MesSocket=htx.UDPService(ServerIP,int(ServerPort),int(timeout))
    MesSocket.set('1,'+ mac)  
    Result=MesSocket.get()
    if Result <> '':
       Result=Result.split('_')
       if Result[1]==mac:
          if Result[0]=='OK':
             return 1
          elif Result[0]=='NG':
             raise Except("ErrorCode(0005):Pass Travel Failed")    
    raise Except("ErrorCode(0005):Connection MES Server Fail ")

############### connect mes ###############
"""
def checkemp(emp):
    sajet_lock.acquire()
    sajet.StartSajet()
    for try_ in range(3):
        Result = sajet.CheckEmp(emp)
        if Result[0]:break
        time.sleep(1)
    Result=Result[-1].strip()
    sajet.StopSajet()
    sajet_lock.release()
    return  Result   
        
        
        

def checksn(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return]
    '''
    mac = argv[2][0]
    sn = argv[2][1]
    sajet_lock.acquire()
    sajet.StartSajet()
    for try_ in range(3):
        Result = sajet.getsn(mac)
        if Result[0]:break
        time.sleep(1)
    Result=Result[-1].strip()
    sajet.StopSajet()
    sajet_lock.release()
    if Result==sn:
       return 1
    else:
       raise Except("ErrorCode(0005):Check SN Failed:%s"%Result)    
    

def checkcsn(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
    '''
    mac = argv[2][0]
    csn = argv[2][1]
    sajet_lock.acquire()
    sajet.StartSajet()
    for try_ in range(3):
        Result = sajet.getsn(mac)
        if Result[0]:break
        time.sleep(1)
    sn=Result[-1].strip()
    for try_ in range(3):
        Result = sajet.getcsn(sn)
        if Result[0]:break
        time.sleep(1)
    Result=Result[-1].strip()
    sajet.StopSajet()
    sajet_lock.release()
    if Result==csn:
       return 1
    else:
       raise Except("ErrorCode(0005):Check CSN Failed:%s"%Result)    
    

def checktravel(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
    '''
    mac = argv[2][0]
    sajet_lock.acquire()
    sajet.StartSajet()
    for try_ in range(3):
        Result = sajet.getsn(mac)
        if Result[0]:break
        time.sleep(1)
    sn=Result[-1].strip()
    for try_ in range(3):
        Result = sajet.checktravel(sn)
        if Result[0]:break
        time.sleep(1)
    sajet.StopSajet()
    sajet_lock.release()
    if not Result[0]:
       raise Except("ErrorCode(0005):Check MES Failed:%s"%Result[-1])    
    


def passtravel(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
    '''
    mac = argv[2][0]
    emp = argv[-1][0][1]
    model = argv[-3]('Base','ModelName')
    station = argv[-3]('Base','StationName')
    hw,sw = argv[-3]('Base','HSW').split('|')
    logname = "c:\\%s-Log\\"%model+"-".join(map(str,time.gmtime()[:3]))+"\\%s.%s"%(mac,station)
    #upload log
    if not ODBCinsert(mac,station,logname):
       raise Except('ErrorCode(0005):Upload log file failed')
    if argv[-1][0][2]=='FAIL' : return    
    sajet_lock.acquire()
    sajet.StartSajet()
    for try_ in range(3):
        Result = sajet.sethwswtodb(mac,hw,sw)     #insert hw & sw to mesdb
        if Result[0]:break
        time.sleep(1)
    if Result[0]:
       for try_ in range(3):
            Result = sajet.getsn(mac)
            if Result[0]:break
            time.sleep(1)
       sn=Result[-1].strip()
       for try_ in range(3):
           Result = sajet.passtravel(emp,sn)
           if Result[0]:break
           time.sleep(1)
       sajet.StopSajet()
       sajet_lock.release()
       if not Result[0]:
          raise Except("Pass MES Failed:%s"%Result[-1])    
    else:
       sajet.StopSajet()
       sajet_lock.release()
       raise Except("Insert HW & SW Failed:%s"%Result[-1])
"""
def failtravel(emp,mac,errcode):
    sajet_lock.acquire()
    sajet.StartSajet()
    for try_ in range(3):
        Result = sajet.getsn(mac)
        if Result[0]:break
        time.sleep(1)
    sn=Result[-1].strip()
    for try_ in range(3):
        Result = sajet.failtravel(emp,sn,errcode)
        if Result[0]:break
        time.sleep(1)
    sajet.StopSajet()
    sajet_lock.release()
    return Result
    #if not Result[0]:
    #   raise Except("To repair MES Failed:%s"%Result[-1])    

def ReturnDevice_ID_oracle():
    #db = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%('172.28.206.253','test','test','test')) 
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    sql="select * from OPENQUERY(MESDB,'select DRIVER_PARAMETER from tgs_gateway_base where GATEWAY_DESC_E = ''TEST01''')"
    if '172.28.209' in mes_lan_ip:
        sql="select * from OPENQUERY(MESDB,'select DRIVER_PARAMETER from tgs_gateway_base where GATEWAY_DESC_E = ''TEST02''')"
    cursor.execute(sql)
    for i in cursor.fetchone():
        return str(i).split(';')[1].split(',').index(mes_lan_ip)+1

def ReturnPdline_oracle():
    #db = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%('172.28.206.253','test','test','test')) 
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    cursor.execute("select * from OPENQUERY(MESDB,'select pdline_name from sys_pdline where pdline_id = (select pdline_id from sys_terminal where \
     TERMINAL_ID =(select max(TERMINAL_ID) from tgs_terminal_link\
     where DEVICE_ID = %s and SERVER_ID = (select server_ID from tgs_server_base where SERVER_DESC_E = ''TGS_2F_ATE'')))')"\
     %ReturnDevice_ID_oracle())
    for i in cursor.fetchone():
        return str(i)

def ODBCinsert(mac,station,filename,order = '1000'):
       logdata = open(filename,'r').read()
       logfile = bz2.compress(logdata)
       status = 'FAIL'
       for dataline in logdata.split('\n'):
           if 'Test Result' in dataline:
              status = logdata.split(':')[-1].strip().split()[0]
       pdline = ReturnPdline_oracle() 
       db = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(logserver,'test','test','test')) 
       db.autocommit=True
       cursor = db.cursor()
       tmp = time.localtime(time.time())
       #testtime =  "%d/%d/%d %d:%d:%d"%tmp[:6]
       sql = "insert into TESTlog (orderNO,MAC,pdline,station,status,logfile) \
values('%s','%s','%s','%s','%s',?)"%(order,mac,pdline,station,status)
       cursor.execute(sql,(buffer(logfile)))
       time.sleep(2)
       cursor.execute("select status from TESTlog where MAC = '%s'"%mac)
       data = cursor.fetchone()
       if data:
          return data[0]
       else:
          return 0    

def InsertCPK_DB(mac,pn,section,value):
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    pdline = ReturnPdline_oracle()
    keys = ''
    vals = ''
    for key in value:
        print key
        sql = "IF NOT EXISTS (SELECT name FROM syscolumns WHERE (id IN (SELECT id \
FROM sysobjects WHERE name = 'CPKDATA')) AND (name = '%s')) ALTER TABLE CPKDATA ADD %s float"%(key,key)
        cursor.execute(sql)
        keys += key+','
        vals += '%s,'%value[key][2]
        sql = "select limitl,limith from CPKSPEC where (pn='%s') and (testsection='%s') and (item='%s')\
 order by orderid DESC"%(pn,section,key)
        cursor.execute(sql)
        data = cursor.fetchone()
        if not data or data[0] <> value[key][0] or data[1] <> value[key][1]:
           sql = "insert into CPKSPEC (pn,testsection,item,limitl,limith) values ('%s','%s','%s',%s,%s)\
"%(pn,section,key,value[key][0],value[key][1])
           cursor.execute(sql)    
    
    sql = "insert into CPKDATA (%smac,pn,pdline,stationname,testsection) \
values(%s'%s','%s','%s','%s','%s')"%(keys,vals,mac,pn,pdline,Station,section)
    cursor.execute(sql)
    cursor.execute("select * from CPKDATA where mac = '%s'"%mac)
    data = cursor.fetchone()
    if data:
       return data[0]
    else:
       return 0    

def InsertCPK_DB(mac,pn,section,value):
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    pdline = ReturnPdline_oracle()
    keys = ''
    vals = ''
    for key in value:
        print key
        sql = "IF NOT EXISTS (SELECT name FROM syscolumns WHERE (id IN (SELECT id \
FROM sysobjects WHERE name = 'CPKDATA')) AND (name = '%s')) ALTER TABLE CPKDATA ADD %s float"%(key,key)
        cursor.execute(sql)
        keys += key+','
        vals += '%s,'%value[key][2]
        sql = "select limitl,limith from CPKSPEC where (pn='%s') and (testsection='%s') and (item='%s')\
 order by orderid DESC"%(pn,section,key)
        cursor.execute(sql)
        data = cursor.fetchone()
        LSL = '%.2f'%value[key][0]
        USL = '%.2f'%value[key][1]
        if not data or data[0] <> float(LSL) or data[1] <> float(USL):
           sql = "insert into CPKSPEC (pn,testsection,item,limitl,limith) values ('%s','%s','%s',%s,%s)\
"%(pn,section,key,LSL,USL)
           cursor.execute(sql)       
 
    sql = "insert into CPKDATA (%smac,pn,pdline,stationname,testsection) \
values(%s'%s','%s','%s','%s','%s')"%(keys,vals,mac,pn,pdline,Station,section)
    cursor.execute(sql)
    cursor.execute("select * from CPKDATA where mac = '%s'"%mac)
    data = cursor.fetchone()
    if data:
       return data[0]
    else:
       return 0   


    
def CheckHWandSWfromDB(*argv):
    '''
     argv :
         dutid,terms,labels,Panel,Log,Config,flow,[Return])
    '''
    pn = argv[-3]('Base','PN').strip()
    hw,sw = map(strip,argv[-3]('Base','HSW').split('|'))
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    sql="SELECT HW,SW FROM VersionControl WHERE PN='%s' ORDER BY DATATIME DESC"%pn
    cursor.execute(sql)
    data = cursor.fetchone() 
    if not data:raise Except("ErrorCode(0011):get hw and sw failed from db")
    if hw <> data[0] or sw <> data[1]: 
       raise Except("ErrorCode(0010):Check hw and sw failed")
    argv[4]('check hw and sw finish from db',2)

def lDownstreamFrequencyPower(freqPwrOffsetTab,freq): 
    freq=int(freq) 
    for i in freqPwrOffsetTab:
        if int(i[0])== int(freq*1000):
            return i[1] 		    
    #return 5.7

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

def attntrans(attn_value,step):
    value=attn_value/step
    intvalue=int(attn_value/step)
    if (value-intvalue)*step >= step/2-0.05:
       intvalue=intvalue + 1
    return intvalue

def GetAttnValue(filename,path=""):
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
        print "Read Attn value from:",fs[-1]
        for i in open(fs[-1]).readlines():
            if "attn" in i:
                Cattn = int(i.split("Cattn =")[-1].split(",")[0].strip())
                Fattn = int(i.split("Fattn =")[-1].strip())
                print "Cattn = %d,Fattn = %d"%(Cattn,Fattn)
                return (Cattn,Fattn)
            else:
                print "Can't read Attn value"
    raise Except("ErrorCode(0003):Can't read Attn value")

def CheckInputData(data_1,data_2):
    data_1 = data_1.split("<")[-1].split(">")[0].strip()
    a = data_1.split()
    b = data_2.split()
    for i in range(len(b)):
        if not float(a[i])==float(b[i]):
            raise Except("ErrorCode(0004):input value")

def Insert_WiFiKEY(mac,key_dic,log,Trigger=0):#key_dic,mode '0:send keys to each DB(SQL+ORACLE)|1:just send to ORACLE(MES)'
    db = odbc.odbc("TESTlog/TEST/test")
    SQL = db.cursor()
    SQL.execute("DECLARE @Transferor VARCHAR(500) EXEC SSIDSYNC '%s', '%s', '%s', '%s', '%s', %d,\
    @Transferor OUTPUT SELECT @Transferor"%(mac,key_dic['SSID_PASSWORD'],key_dic['NETWORK_KEY'],\
    key_dic['WPS_PIN'],key_dic['FON_KEY'],Trigger))
    data = str(SQL.fetchone()[0]).strip()
    if data != 'ok':raise Except('ErrorCode(0005):'+data)  
    else:log('WiFi keys insert to DB success.',2) 
            

def ConfirmReleaseInformation(data,p_name,p_value,symbol):
    index = data.find(p_name)
    if index == -1:
        return 0
    for i in data.splitlines():
        if not p_name in i:
            continue
        data_p = i.split(symbol)[-1].strip()
        if data_p == p_value:
            return 1
        
    return 0  

def ReleaseInformationCheck(data,dic,symbol):    
    print data
    for i in dic.keys():
        if ConfirmReleaseInformation(data,i,dic[i],symbol)==0:
           return i
    return 0

class Xurl:
    """    snmp://<host>/<community>/<MIB File>/<MIB object>/<type>
    ftp://<user>:<password>@<host>:<port>/<path>
    http://<user>:<password>@<host>:<port>/<url-path>
    udp://<host>:<port>
    htxpy://<host>:<port>
    tcp://<host>:<port>
    term://.:<baud rate>/<com N>
    telnet://<user>:<password>@<host>:<port>
    shell://command string

    example:
       xurl_core.InitXurl("C:/usr")    #if tools path isn't C:/Net-Snmp/bin
       a = Xurl(snmp://192.168.100.1/private/IF-TABLE/ifPhysAddress.2/x")
       a << "0005ca112233"
       value = a.get()
       a.wait(until_string, timeout) """
    def __init__(self,url_str):
        url_list = list(xurl_core.parser(url_str))
        proto = url_list[1]
        del url_list[1]
        exec "self.protocol_obj = apply(xurl_core.HTX_%s,url_list)"%(proto)
    def get(self):
        return self.protocol_obj.get()
    def __repr__(self):
        return self.get()
    def __call__(self):
        return self.get()
    def __str__(self):
        return self.get()
    def set(self,data):
        return self.protocol_obj.set(data)
    def __lshift__(self,data):
        return self.set(data)
    def close(self):
        return self.protocol_obj.close()
    def __del__(self):
        self.protocol_obj.__del__()
    def setWait(self,setData,prompt,timeout):
        self.protocol_obj.set(setData)
        return self.protocol_obj.wait(prompt,timeout)
    def wait(self,data,timeout):
        return self.protocol_obj.wait(data,timeout)
    def getOption(self,optionName):
        return self.protocol_obj.getOption(optionName)
    def setOption(self,**options):
        return self.protocol_obj.setOption(**options)            
