import os,time,traceback,threading
from toolslib import *
import socket,re
import bz2
#import odbc
import glob #,thread


execfile("config.ini")
if os.path.isfile('c:\\station.ini'):
    execfile('c:\\station.ini')
    

#os.system("taskkill /F /IM Connectivity_Client.exe /T") 
time.sleep(1)



###############################################################################################################
def find(pattern, string):
    match = re.search(pattern,string)
    if match: return match.group()
    else: raise Except("re string not find:%s"%pattern)
    
def IsConnect(ip,timeout):
    ip = ip.strip()
    current = time.time()
    timeout += current
    os.popen("arp -d")
    while current < timeout:
        try:
            data=int(os.popen("ping -w 1000 -n 3 %s"%ip).read().split('(')[-1].split('%')[0])
        except:
            data=100
        if not data:return 1
        current = time.time()
    return 0

def IsDisconnect(ip,timeout):
    ip = ip.strip()
    current = time.time()
    timeout += current
    os.popen("arp -d")
    while current < timeout:
        if os.popen("ping -w 500 -n 1 %s"%ip).read().find(r"100%")>=0 and \
           os.popen("ping -w 500 -n 2 %s"%ip).read().find(r"100%")>=0:
            return 1
        time.sleep(1)
        current = time.time()
    return 0

          
def GetMacAddress(parent):
    val = parent.MAC.GetValue()
    try:
        if len(val) == 12 and int(val,16):
           return val
    except ValueError:
           pass
    raise Except("Input Label Error %s !"%val)

def GetSN(parent):
    val = parent.SN.GetValue()
    try:
        if len(val) == 12 and int(val,16):
           return val
    except ValueError:
           pass
    raise Except("Input Label Error %s !"%val)


def Check_MAC(parent,mac,targetIP,log):
    target=targetIP       
    lan_mac = "%012X"%(int(mac,16))                
    lan_mac = lan_mac[0:2]+"-"+lan_mac[2:4]+"-"+lan_mac[4:6]+"-"+lan_mac[6:8]+"-"+lan_mac[8:10]+"-"+lan_mac[10:12]
    parent.SendMessage('\n Scan MAC : %s \n'%lan_mac,log)
    for z in range(2):
        os.popen('arp -d').read()       
    
    for try_ in range(15):
        os.popen('arp -d').read()
        os.popen('ping %s -w 1000 -n 2'%target).read()
        phy_add =''
        time.sleep(2)
        for x in range(5):    
            info =  os.popen('arp -a').read()

        #print info
        print '%s------------------------------------------------'%try_    
        if '192.168.0.10' in info:      
            #os.popen('ping %s -w 1000 -n 2'%target)  
            data = info.split('\n')

            for k in data:
                if ('%s'%target in k) and ('dynamic' in k):
                   #print info
                   phy_add=k.split(target)[-1].split('dynamic')[0].strip()
                if k==data[-1]:continue 
            if phy_add:
               phy_add = phy_add.upper()
            else:continue     
            parent.SendMessage('\n Network Show DUT MAC : %s \n'%phy_add,log)     
            
            if not phy_add == lan_mac:
               #parent.SendMessage('Check DUT inner MAC:  %s !\n'%phy_add,log,color=1)
               raise Except("Scan MAC Error\n")
            else:
               parent.SendMessage('Check MAC OK !\n',log,color=2)
               break

        else:
            if try_==14:
               raise Except("Pls add LAN IP 192.168.0.10 \n")
                                              
        if try_==14:
           raise Except("detect %s Fail \n"%target)       




def lWaitCmdTcp(parent,cmd,waitstr,timeout=10):
    s = time.time()
    while time.time() - s < timeout:
          if waitstr in parent.tcps.buf:
             if cmd:parent.tcps.set(cmd)
             return 0
    raise Except("failed :%s\n,\n%s"%(cmd,parent.tcps.buf))         

def lWaitTcpBuf(parent,term_TCP,log,waitstr,timeout=10):
    s = time.time()
    test_fail = 0
    while time.time() - s < timeout:
          data=term_TCP.get()
          parent.SendMessage('%s'%data,log) 
          if waitstr in data: return [1,data]
          #if "Error message: Error" in data: return [1,data]
          if 'Test Done' in data: return [1,data]
    return 0


    
def lShowTcpBuf(parent,cmd,waitstr,timeout=10):
    s = time.time()
    parent.tcps.buf = ''
    content = ''
    pstr = "" 
    if cmd:parent.tcps.set(cmd)
    while time.time() - s < timeout:
          if pstr <> parent.tcps.buf:
             content=content+parent.tcps.buf
             pstr = parent.tcps.buf
          if waitstr in content:
             return content
    return 'Err'


def lSetWaitTcpBuf(parent,cmd,waitstr,timeout=10,count=1):
    for i in range(count):
        s = time.time()
        parent.tcps.buf = ''
        content = ''
        pstr = "" 
        if cmd:parent.tcps.set(cmd)
        while time.time() - s < timeout:
              if pstr <> parent.tcps.buf:
                 content=content+parent.tcps.buf
                 pstr = parent.tcps.buf
              if 'ERROR' in content:
                  parent.tcps.buf = ''
                  content = ''
                  pstr = ""
                  time.sleep(0.5)  
                  parent.tcps.set(cmd)
                  if pstr <> parent.tcps.buf:
                      content=content+parent.tcps.buf
                      pstr = parent.tcps.buf
              if waitstr in content:
                 return content
    raise Except('Err: %s'%content)
    #return 'Err: %s'%content


def USBTest(parent,term,log):
    parent.SendMessage('\n'+"USB Test...............\n",log)
    for i in range(3):
        data = lWaitCmdTerm(term,"mount","#",5,3)
        if not '/dev/sda1' in data or not "/dev/sdb1" in data:
           time.sleep(1)
           if i ==2:raise Except("USB Mount FAIL.")
        else:
           addr1 = data.split("/dev/sda1 on")[1].strip().split()[0].strip()
           addr2 = data.split("/dev/sdb1 on")[1].strip().split()[0].strip()  
           break     
       #parent.SendMessage("%s"%addr,log,color=2)
    term.get()
    data1 = lWaitCmdTerm(term,"ls %s"%addr1,"#",5,3)
    data2 = lWaitCmdTerm(term,"ls %s"%addr2,"#",5,3)
    
    if not 'test.txt' in data1 or not 'test.txt' in data2:
        parent.SendMessage('\n'+"check content FAIL\n",log,color=1)
        raise Except("Check USB Content FAIL.")
    else:
        parent.SendMessage('\n'+"check content PASS\n",log,color=2)


def getSelfAddr():
    ip = socket.gethostbyname_ex(socket.gethostname())
    for i in ip[-1]:
       if '172.28.' in i:
          return i
    return 0

''' 
def Get_PowChkResult(ip):
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    cursor.execute("select station_ip from wifiPowerCheck_FailStation where station_ip = '%s'"%ip)
    data = cursor.fetchone()
    if data:
       return 0
    else:
       return 1
'''

def StartCmd(term,cmd,waitstr,wait_time):
    a = 0
    while 1:
        term << "%s"%cmd
        data = term.wait("%s"%waitstr,3)
        a = a+1
        if not data:
            if a < wait_time:
                continue
            raise Except("failed: %s"%cmd)
        else:
            return data[-1]


def start_hostapd(parent,term,log):
    ################### for W21 WDS mode test
    for i in range(3):
        lWaitCmdTerm(term,"cd /nvram",'#',10,3)    
        data= lWaitCmdTerm(term,"tftp -g 192.168.0.10 -r start_hostapd.sh",'#',30,1) 
        time.sleep(5)
        parent.SendMessage("sync",log,color=2)
        lWaitCmdTerm(term,"sync",'#',10,2)
        time.sleep(3)
        data = lWaitCmdTerm(term,"ls",'#',10,2) 
        parent.SendMessage("\n%s\n"%data,log,color=2)
        if 'start_hostapd.sh' not in data:
           if i ==2:raise Except("failed: %s"%data)
        else:break
    ################### for W21 WDS mode test

def Chec_ver(parent,term,log):
    for i in range(3):
        data = lWaitCmdTerm(term,"cat /proc/athversion",'#',10,2) 
        parent.SendMessage("\n%s\n"%data,log,color=2)
        if '10.2-00082-4' not in data:
           if i ==2:raise Except("failed: %s"%data)
        else:break

def PCI_ID_check(parent,term,log):
    parent.SendMessage("\nPCI ID check\n",log,color=2)
    lWaitCmdTerm(term,"cd /tmp/",'#',10,3) 
    lWaitCmdTerm(term,"tftp 192.168.0.10 -g -r checkpci",'#',10,3)
    lWaitCmdTerm(term,"chmod 755 checkpci",'#',10,3)
    data = lWaitCmdTerm(term,"./checkpci",'#',50,2)
    
    #data = lWaitCmdTerm(term,"cat /proc/bus/pci/devices|grep ath",'#',10,2)
    #data = lWaitCmdTerm(term,"lspci",'#',10,2)
    parent.SendMessage("\n%s\n"%data,log)
    if 'AR9381 PCI ID check PASS' not in data: 
       raise Except("failed: 2G value write Fail!")  
    '''
    if '0030' not in data:
       if '003c' not in data:
          raise Except("failed: 2G & 5G value write Fail!")
       else:
          raise Except("failed: 2G value write Fail!")
    else:
      if '003c' not in data:
          raise Except("failed:5G value write Fail!")
    '''
    parent.SendMessage("\n2G value write PASS!\n",log,color=2)


def partition_miss(parent,term,log):
    lWaitCmdTerm(term,"cd /tmp/",'#',10,3) 
    lWaitCmdTerm(term,"tftp 192.168.0.10 -g -r sfdisk.tgz",'#',10,3)
    lWaitCmdTerm(term,"tar -xzf sfdisk.tgz",'#',10,3)
    lWaitCmdTerm(term,"cd sfdisk",'#',10,3)
    data = lWaitCmdTerm(term,"./run.sh",'#',50,2)
    
    parent.SendMessage("\n%s\n"%data,log,color=2)
    if 'Partition Fix Pass' not in data: 
       if 'Unit is ok, exiting' not in data:
          raise Except("failed: Partition Fix Fail!")  


'''
def Get_PowerCheck(ip):
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    cursor.execute("SELECT state FROM wifiPowerCheck where station_ip= '%s' and state = 'lock'"%ip)
    data = cursor.fetchall()
    print data
    if data:
       return 'lock'
    return 'unlock'
    
def Get_DUTState(mac,ip):
    db = odbc.odbc("TESTlog/TEST/test")
    cursor = db.cursor()
    cursor.execute("select fail_mac from wifiPowerCheck  where state = 'lock' and fail_mac='%s' and station_ip='%s'"%(mac,ip))
    data=cursor.fetchone()
    print data
    if data:
       return 1
    return 0    
'''    
    
################### add  in 20160121  by TDL #######################################    
def read_Cableloss(fs):
    execfile(fs[-1])
    return eval("cableloss")
def Trans_Cableloss(parent,term_TCP,log):  
    import glob   
    global CableLossPath 
    Cal_loss = ""  
    print '\nChain,Freq,Loss'
    if CableLossPath[-1] not in ["/","\\"]: CableLossPath += "/"
    for f in ['2G','5G']:
        fs = glob.glob(CableLossPath+'Pathloss_%s*.csv'%f)
        if not fs:
           htx_local.Win32Message("Warning!","No such cable loss file.")
           sys.exit(1)
           
        for i in open(fs[-1]).readlines():
                if not i.strip(): continue
                if f == '2G':
                    if int(i.split(',')[1]) >3000: continue
                else:
                    if int(i.split(',')[1]) < 5000: continue 
                ant,ch,offset = i.split(',')
                for j in range(4):
                    if ch < 5000:
                        if int(ant) == j: offset = float(offset) + connector_2G[j]
                    else:
                        if int(ant) == j: offset = float(offset) + connector_5G[j]
                Cal_loss = Cal_loss + "%s,%s,%.2f\n"%(ant,ch,offset)         
                        
    print Cal_loss
    term_TCP << Cal_loss
    data = term_TCP.wait("OK",10)[-1]
    #data = term_TCP.get()
    print 'Cableloss transmit :%s'%data
    if not data == 'OK':
       raise Except("Cableloss transmit Fail!")

################### plume script @ y.j. wang 20180912 ##############################    

def CheckNrm(func):
    def checkdata(*args):
        result = 1
        rep = str()
        data = func(args[0],args[1],args[2],args[3],args[4])
        parsing = re.findall(r'(?<=:\s\s)(.*)(?=.*)', data)
        if str(args[3]) != str(parsing[0].split('\r')[0]): 
            print args[3], parsing[0].split('\r')[0]
            result = 0
            rep = 'SN Failed'
        if '0xfe71' != str(parsing[5].split('\r')[0]):
            result = 0
            rep = 'BT UUID Failed'
        return (result, rep)
    return checkdata
    
def CheckBootUp(func):
    def checkstatus(*args):
        test_time = time.time()
        for count in range(2):
            if IsConnect(dut_ip,timeout=40):
               #term = htx_local.SerialTTY(comport,115200)
               term = htx_local.Telnet(dut_ip)
            else: raise Except("Ping DUT Failed") 
            term.wait('#',3)
            term << 'pmf -e'
            time.sleep(0.1)
            data = term.get()
            args[0].SendMessage(data,args[4])
            if 'already in factory mode' in data:
                lWaitCmdTerm(term,'pmf -i','Erasing /dev/mtd7',5)
                time.sleep(2)
                lWaitCmdTerm(term,'mtd erase /dev/mtd14','Erasing /dev/mtd14',5)
                time.sleep(1)
                break
            if count == 1:
                raise Except("Check Mode Failed")
        data = func(args[0], term, args[2], args[3], args[4])
        if data[0]:
            args[0].SendMessage( "NrmSetup Test time: %3.2f (sec)\n"%((time.time() - test_time)),args[4])
            args[0].SendMessage( "---------------------------------------------------------------------------\n",args[4])
            return term
        else:
            raise Except('NrmSetup Failed : {}'.format(data[1]))

    return checkstatus


@CheckBootUp
@CheckNrm
def NrmSetup(parent,term,mac,sn,log):
    mac1 = "%012X"%(int(mac,16))
    ethmac = mac1[0:2]+":"+mac1[2:4]+":"+mac1[4:6]+":"+mac1[6:8]+":"+mac1[8:10]+":"+mac1[10:12]
    mac2 = "%012X"%(int(mac,16) + 3)
    btmac = mac2[0:2]+":"+mac2[2:4]+":"+mac2[4:6]+":"+mac2[6:8]+":"+mac2[8:10]+":"+mac2[10:12]
    setupitem = {'SN' : 'pmf -s -w {}'.format(sn),
                 'Eth.MAC' : 'pmf -m -w {}'.format(ethmac),
                 'BT.MAC' : 'pmf -b -w {}'.format(btmac),
                 'BT.UUID' : 'pmf -u -w 0xfe71',
                 'Dload ca.pem.' : 'cd /var && tftp -g {} -r ca.pem'.format(tftp_server),
                 'Dload client.pem.' : 'cd /var && tftp -g {} -r client.pem'.format(tftp_server),
                 'Dload client_dec.key.' : 'cd /var && tftp -g {} -r client_dec.key'.format(tftp_server)
                }
    parent.SendMessage("\nNrmSetup Start...\n" ,log)
    lWaitCmdTerm(term,"\n",'#',3)
    for item in list(setupitem.keys()):
        data = lWaitCmdTerm(term,setupitem[item],'#',10)
        parent.SendMessage('{}:\n{}\n'.format(item,data))
        data += term.get()
        if 'error' in data or 'timeout'in data: 
            raise Except("{} setup failed".format(item))
    data = lWaitCmdTerm(term,"pmf -f -a",'#',10)
    data += lWaitCmdTerm(term,"pmf -f -r",'#',10)
    if 'Error' in data or 'timeout'in data:
        if 'exists in flash' in data:
            pass #raise Except("please reboot DUT")
        else: 
            raise Except("Nrm setup failed:\n{}".format(data))    
    report = lWaitCmdTerm(term,"pmf --report",'#',10)
    return report
    #parent.SendMessage( "NrmSetup Test time: %3.2f (sec)\n"%((time.time()- test_time)) ,log)
    #parent.SendMessage( "---------------------------------------------------------------------------\n",log)
    


################### add  in 20160121  by TDL #######################################    

def CheckNartReady(parent,interface,pwr_check,log):
    test_time = time.time()
    wait_str = {'2G':['nart.out -console -port 2390',"manufacture_ath_up",'2G_Calibration mode'],
                '5G':['Qcmbr -instance 1 -pcie 1 -console',"manufacture_ath_up_10x",'5G_Calibration mode']
               }
    rm_file = {'2G':"rm /tmp/calData_11n.bin",'5G':"rm /nvram/wifi1.caldata.bin"}
    parent.SendMessage("\nCheck %s nart ready Start...\n"%interface ,log)
    #term =htx_local.SerialTTY(comport,115200)
    #term=htx_local.Telnet(target)
    lWaitCmdTerm(term,"\n",'#',3) 
    if not pwr_check: lWaitCmdTerm(term,"%s"%rm_file[interface],'#',3)
    data = lWaitCmdTerm(term,"ps",'#',3)
    if wait_str[interface][0] not in data:
        parent.SendMessage("Start up %s by %s\n"%(interface,wait_str[interface][1]),log)
        lWaitCmdTerm(term,"%s"%wait_str[interface][1],'%s'%wait_str[interface][2],60,1) 
    time.sleep(4)
    lWaitCmdTerm(term,"\n",'#',3,1)
    #term.close()
    parent.SendMessage( "Check %s initial ready Test time: %3.2f (sec)\n"%(interface,(time.time()- test_time)) ,log)
    parent.SendMessage( "---------------------------------------------------------------------------\n",log)
    
def PwrCheckInitReady(parent,log):
    test_time = time.time()
    term =htx_local.SerialTTY(comport,115200)
    #term=htx_local.Telnet(target) 
    lWaitCmdTerm(term,"\n",'#',3)
    if 'wifi0.caldata.bin' in lWaitCmdTerm(term,"ls /nvram/","#",5):
        data = lWaitCmdTerm(term,"cp /nvram/wifi0.caldata.bin /tmp/%s"%cal_fname_2g,"#",5)                 
    else: raise Except("failed: No 2g calibration file") 
    parent.SendMessage(data + "\n" + "copy /tmp/%s OK"%cal_fname_2g+'\n',log)
    lWaitCmdTerm(term,"\n",'#',3)
    if test_5g:    ## None calibrate 5G
        bin_path = os.getcwd() + "\\NI_CART\\PlugIn\\DUT_Control_QCA9381_9986\\boardData\\"
        for i in range(3):
            data = os.popen("dir %s"%bin_path).read()
            if 'wifi1.caldata.bin' in data:
                if i ==2: raise Except("failed: delete 5g calibration file")
                data = os.popen("del %s\wifi1.caldata.bin"%bin_path).read()
            else: 
                break                     
        parent.SendMessage('Delete %s\\wifi1.caldata.bin OK...\n'%bin_path,log)
        if not PingLinux(term,tftp_server,10): raise Except("failed: tftp server %s ping error"%tftp_server) 
        lWaitCmdTerm(term,"\n",'#',3) 
        lWaitCmdTerm(term,"cd /nvram/",'#',3)
        lWaitCmdTerm(term,"tftp -p %s -l %s"%(tftp_server,cal_fname_5g),"#",5)           
    term.close()
    parent.SendMessage( "2G_5G power check initial ready Test time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage( "---------------------------------------------------------------------------\n",log)         

def CheckTxVerify():
    cfg_file = os.getcwd() + "\\NI_CART\\PlugIn\\DUT_Control_QCA9381_9986\\DUT_Control_QCA9381_9986.ini"
    f = open(cfg_file,'r') 
    content = f.read() 
    f.close()
    pat = r"\Verify Test =.+"
    return int(find(pat,content)[-2])

def lLogin(term,username,password,prompt):
    print "Telnet Login...."
    data = term.wait(":",15)
    if ":" not in data[-1]: term << "\n"
    lWaitCmdTerm(term,username,":",10)
    lWaitCmdTerm(term,password,prompt,10)
    
def PingLinux(term,ip,timeout):
    s = time.time()
    while time.time() - s < timeout:
        print ip
        data = lWaitCmdTerm(term,"ping %s -c 2"%ip,'packet loss',10)
        pat=r'\d+%'
        if int(find(pat,data)[:-1]) == 0: 
        #if "0% packet loss" in data:
            print "%s Connected OK ...."%ip 
            return 1
        else: time.sleep(1) 
    print "%s Connected FAIL ...."%ip
    return 0    
            

###########   Main script    ###########     
def W11(parent):
    try:
        result = 0
        log = None
        term = None
        mac = str()
        sn = str()
        parent.SendMessage("START",state = "START")
        start_time = end_time = 0
        #term =htx_local.SerialTTY(comport,115200)
        #term=htx_local.Telnet(target)
        mac = GetMacAddress(parent)
        mac = str(mac).upper()
        sn = GetSN(parent)
        pwr_check = CheckTxVerify()
        if pwr_check: log = open(logPath+mac+".pck","w")
        else:log = open(logPath+mac+".w11","w")        
 
 
        #MES inspection 
        #checktravel(mac,'127.0.0.1',1800,20)

        start_time=time.time()
        parent.SendMessage("WIFI Calibration test program version: %s , Station: %s\n"%(version,Test_station),log)
        parent.SendMessage( "---------------------------------------\n",log)
        parent.SendMessage( "Start Time:"+time.ctime()+"\n",log)
        parent.SendMessage( "Scan MAC address:"+mac+"\n",log)
      
        '''
        #########################   NI  Test by TDL  in 20160121  ##################### 
        parent.SendMessage( "Try to connect NI tester at %s\n"%NIip,log)
        if not IsConnect(NIip,5):
            raise Except("%s never connect\n"%NIip)
        else:
            parent.SendMessage("                             Success!\n",log)  
        if not htx_local.IsConnect(dut_ip,60): raise Except("DUT IP %s never connect\n"%dut_ip)   
        term_TCP = htx_local.TCPClient("127.0.0.1",6432)  
        if not parent.run_cart:  
           #os.system("taskkill /F /IM Connectivity_Client.exe")  
           os.system("NI.bat")
           time.sleep(3)        
           term_TCP << "File"
           #time.sleep(3)
           data = term_TCP.wait("OK",10)[-1]
           #data = term_TCP.get()
           print 'command.rar transmit :%s'%data
           if not data == 'OK':
              raise Except("Pls Check command.rar is alive")
           else:
              Trans_Cableloss(parent,term_TCP,log)  
           term_TCP << "Port%s"%ni_port   # Set DUT port in C:station.ini
           data = term_TCP.wait("Port=%s"%ni_port,15)[-1]
           print 'set %s'%data
           parent.SendMessage('\nset %s\n'%data,log,color=2)
           if not data == "Port=%s"%ni_port:
              raise Except("Set NI Port Fail")

           parent.run_cart = True
        #########################   NI  Test by TDL  in 20160121  ##################### 
        '''
        parent.SendMessage('wait dut boot...........\n',log)
        term = NrmSetup(parent,term,mac,sn,log)
        if pwr_check: PwrCheckInitReady(parent,log)     
        CheckNartReady(parent,term,'2G',pwr_check,log)
        term_TCP << '%s'%mac
        parent.SendMessage( '\n'+"Waitting NI Running TEST...... "+'\n',log,color=2)
        if (test_2g & test_5g):
            NI_result = lWaitTcpBuf(parent,term_TCP,log,"Finish",80)
            #if "Error message: Error" in NI_result[1]: raise Except("ERROR :2G None test done!Pls reload test program")
            if "FAIL" in NI_result[1]: raise Except("ERROR :2G None test done!Pls reload test program")
            if "Finish" in NI_result[1]:              
                result_ = int(NI_result[1].split("Finish,")[1].strip())
                if not result_: 
                    term_TCP << 'Stop'
                    data = term_TCP.wait("OK",10)[-1]
                    raise Except("FAIL: 2G Tx Rx Verify Fail")
                else:
                    CheckNartReady(parent,'5G',pwr_check,log)
                    term_TCP << 'Run'
                    data = term_TCP.wait("OK",10)[-1]
                    parent.SendMessage("Start 5G Calibration testing\n",log)
            else: raise Except("FAIL: Not recieve Labview 2G test finished")
                          
        NI_result = lWaitTcpBuf(parent,term_TCP,log,"Test Done",250)
        if not NI_result[0]:
           raise Except("ERROR :No test done!Pls reload test program")
        parent.SendMessage( '\n'+"NI Running TEST Done...... "+'\n',log,color=2)
        data = NI_result[1].split('Test Done:')[-1].split('\n')[0].strip()
        if 'PASS' not in data:
           result = 1
           parent.SendMessage( '\n'+"NI Running TEST FAIL...... "+'\n',log,color=1)
        else:
           if not  pwr_check:
                term =htx_local.SerialTTY(comport,115200)
                #term=htx_local.Telnet(target)
                lWaitCmdTerm(term,"\n",'#',3)
                if cal_fname_2g in lWaitCmdTerm(term,"ls /tmp/","#",5):
                    data = lWaitCmdTerm(term,"cp /tmp/%s /nvram/wifi0.caldata.bin"%cal_fname_2g,"#",5)
                else: raise Except("failed: No 2g calibration file")
                parent.SendMessage( data + "\n" + "Write /nvram/wifi0.caldata.bin OK"+'\n',log)
                lWaitCmdTerm(term,"\n",'#',3)
                if test_5g:  # None calibrate 5G
                    data = lWaitCmdTerm(term,"ls /nvram/","#",5)
                    if not cal_fname_5g in data:
                        raise Except("failed: No 5g calibration file %s"%cal_fname_5g)
                    parent.SendMessage( data + "\n" + "Check /nvram/wifi1.caldata.bin OK"+'\n',log)                
                term.close()  
           parent.SendMessage( '\n'+"NI Running TEST PASS...... "+'\n',log,color=2)

        #USBTest(parent,term,log)        

        




    except Except,msg:
        parent.SendMessage("\n%s\n"%msg,log,color=1)
        result = 1
    except: 
        parent.SendMessage("\n%s\n"% traceback.print_exc(),log,color=1)
        result = 1
    

    #parent.tcps.set('unload')
    end_time = time.time()
    parent.SendMessage('\n'+"End Time:"+time.ctime()+'\n',log)
    parent.SendMessage("total time: %3.2f"%(end_time-start_time)+'\n',log)
    os.popen("taskkill /F /IM nart.exe")  # MUST kill nart when re-test  
    time.sleep(1)
    if result:
       parent.SendMessage( "Test Result:FAIL"+'\n',log,color=1)
       parent.SendMessage("",state = "FAIL")       
    else:
       parent.SendMessage( "Test Result:PASS"+'\n',log,color=2)
       parent.SendMessage("",state = "PASS")
    if log:log.close()
    '''
    if mac:                   
        travel = passtravel(mac,'127.0.0.1',1800,30)
        if travel or result:
          parent.SendMessage('\n'+"%s\n"%travel,state = "FAIL",color=1)
        else:
        parent.SendMessage("",state = "PASS")
         
    else: parent.SendMessage("",state = "FAIL") 
    '''   
    

    
def W21(parent):
    pass
