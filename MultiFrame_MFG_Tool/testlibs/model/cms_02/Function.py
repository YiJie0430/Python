import os,time,traceback,ConfigParser,thread,threading
from testlibs import *
from testlibs.toolslib import *
from htx import Win32Message
from testlibs.tftp import tftpcfg, tftp_engine
import wx
import random
import serial,glob
execfile("system.ini")
config_path=os.getcwd()+'\\testlibs\\model\\%s\\config.ini'%dut_model
execfile(config_path)
if os.path.isfile('c:\\station.ini'):
    execfile('c:\\station.ini')

gpib = GPIB.SICL_GPIB()
mac_list=list()

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
    lWaitCmdTerm(term,'docsis_init_once',"#",20)
    lWaitCmdTerm(term,'testmode',">",20)
    #lWaitCmdTerm(term,'cli',">",10)
    lWaitCmdTerm(term,'logger',"logger>",15)
    lWaitCmdTerm(term,'AllModulesConfig 1 0',"logger>",3)
    lWaitCmdTerm(term,'ModuleConfig 1 51 1',"logger>",3)
    lWaitCmdTerm(term,'ComponentConfig 1 1',"logger>",3)
    lWaitCmdTerm(term,'exit\n',">",3)

def ClitoCal(parent,dut_id,term,log):
    lWaitCmdTerm(term,"qu","#",3)
    lWaitCmdTerm(term,"cli",">",5)
    lWaitCmdTerm(term,"cable",">",3)
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
    #lWaitCmdTerm(term,"setSN %s"%sn,"Manufacture>",3)
    #parent.SendMessage(dut_id,"Set Serial Number: %s \n"%sn ,log)    
    parent.SendMessage(dut_id,"Set NVM Parameter time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)

def InstallKey(parent,dut_id,term,target,mac,log):
    test_time=time.time();d30_size=list();d31_size=list()
    parent.SendMessage(dut_id,"Hitron dual certificate 3.0 loading start...\n" ,log)
    lWaitCmdTerm(term,"qu","#",5)
    lWaitCmdTerm(term,"cli","mainMenu>",5)
    lWaitCmdTerm(term,"docsis","docsis>",5) 
    lWaitCmdTerm(term,"Manu","Manufacture>",3)
    data=os.popen("C:\\HtSignTools\\HtCmKey.exe DualHitron %s"%mac).read(); print data
    if not os.path.isfile("%s/out/%s.DualHitron"%(openssl_path,mac)): raise Except ("failed:Build BPI key error")
    file_size=os.path.getsize("%s/out/%s.DualHitron"%(openssl_path,mac)); print file_size
    #ca_file = open("%s/out/%s.DualHitron"%(openssl_path,mac),"rb").read(); print ca_file
    tftp_dir(parent,tftp_dir_path)
    data=lWaitCmdTerm(term,"bpiset %s %s.DualHitron"%(tftp_server,mac),"keys saved",10); print data
    parent.SendMessage(dut_id,"Hitron CA(%s.DualHitron,size: %d) loading OK\n"%(mac,file_size),log,color=2)
    parent.SendMessage(dut_id,"\nCertificate loading time: %3.2f (sec)\n"%(time.time()- test_time),log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)

def CA_verify(parent,dut_id,term,mac,log):
    parent.SendMessage(dut_id,'CA content checking...\n',log)
    ca_mac=str();test_time=time.time();mac=mac.upper()
    for index in xrange(0,12,2):
     if index!=10: ca_mac+=mac[index:index+2]+':'
     else: ca_mac+=mac[index:index+2] 
    cmd_list=['top','docsis','Certification'] 
    for cmd in cmd_list:
     term.write(cmd+'\n'); time.sleep(0.3)    
    data=lWaitCmdTerm(term,"cmcert","ion>",10); #print data
    parent.SendMessage(dut_id,data,log);
    if ca_mac in data: 
     parent.SendMessage(dut_id,"\nCA_3.0 content check pass\n",log,color=2)
    else: raise Except ("\nCA_3.0 content check fail\n")
    parent.SendMessage(dut_id,"CA content check time: %3.2f (sec)\n"%(time.time()- test_time),log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)

def ParameterCheck(parent,dut_id,term,mac,log):
    print mac
    scan_mac=''; mac=mac.upper()
    for index in xrange(0,12,2):
     if index!=10: scan_mac+=mac[index:index+2]+'-'
     else: scan_mac+=mac[index:index+2]
    test_time=time.time()
    parent.SendMessage(dut_id,"Check NVM Parameter Start...\n",log)
    cmd_list=['top','docsis','Prod'] 
    for cmd in cmd_list:
     term.write(cmd+'\n'); time.sleep(0.5)    
    data=lWaitCmdTerm(term,"prodsh","Production>",3); #print data
    #data_=data.splitlines(); print data_
    parent.SendMessage(dut_id,data+"\n",log)
    read_mac=data.split('Cable Modem MAC\t\t\t\t- <')[-1].split('>')[0].strip()
    msg="Get RF MAC Address = %s (%s)"%(read_mac,mac)
    if read_mac <> scan_mac: raise Except("FAIL: " + msg)
    parent.SendMessage(dut_id,msg+"\n",log,color=2)
    
    '''
    r_sn=data.split('Cable Modem Serial Number\t\t- <')[-1].split('>')[0].strip()
    msg="Get Serial Number = %s (%s)"%(r_sn,sn)
    if r_sn <> sn: raise Except("FAIL: " + msg)
    parent.SendMessage(msg+"\n",log,color=2)
    '''

    major=data.split('Major HW Revision\t\t\t- <')[-1].split('>')[0].strip()
    minor=data.split('Minor HW Revision\t\t\t- <')[-1].split('>')[0].strip()
    ver=major+minor 
    msg = "Get HW version = %s (%s)"%(ver,hw_ver)
    if ver <> hw_ver: raise Except("FAIL: " + msg)
    parent.SendMessage(dut_id,msg +"\n",log,color=2)
    
    lWaitCmdTerm(term,"top",">",3)
    data=lWaitCmdTerm(term,"ver",">",3)
    parent.SendMessage(dut_id,data+"\n",log)    
    ver = data.split('VERSION=')[-1].split('\r\n')[0].strip()
    msg = "Get SW version = %s (%s)"%(ver,sw_ver)
    if ver <> sw_ver: raise Except("FAIL: " + msg)
    parent.SendMessage(dut_id,msg+"\n",log,color=2)
    
    parent.SendMessage(dut_id,"Check NVM Parameter time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)

def FactoryReset(parent,dut_id,term,log):    
    test_time = time.time()
    parent.SendMessage(dut_id,"Factory Reset Start...\n" ,log)
    lWaitCmdTerm(term,"factoryReset","Uncompressing Kernel Image",40)
    parent.SendMessage(dut_id,"Factory Reset Finished\n",log,color=2)
    parent.SendMessage(dut_id,"Factory Reset Test time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)      

def Check_LED(parent,dut_id,term,log):
    test_time = time.time()
    for index in xrange(3):
     time.sleep(0.5)
     lWaitCmdTerm(term,"ledd -m %d 2"%index,"#",3)
    if parent.MessageBox('LED Twinkle','LED Test (DUT%s)'%dut_id,wx.YES_NO|wx.ICON_QUESTION) == wx.ID_NO:  raise Except("FAIL: LED Test")
    parent.SendMessage(dut_id,"LED Test PASS\n" ,log,color=2)
    parent.SendMessage(dut_id,"LED Test time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)

def USCalibration(parent,dut_id,term,log):  
    test_time = time.time()
    ClitoCal(parent,dut_id,term,log)
    testfail=0
    for diplexer in diplexer_list:
      us_table=dict()
      gpib.SetUSQPSKCal()
      diplexer_index=us_freqs[diplexer][0]
      freq_range=us_freqs[diplexer][1]
      parent.SendMessage(dut_id,"Upstream Frequencies:%s\n"%freq_range,log)
      lWaitCmdTerm(term,"Up",">",5)
      if int(diplexer_index) <= 3:
        for i in range(4):
          lWaitCmdTerm(term,"upstream %s 0"%i,"ion>",5)
        lWaitCmdTerm(term,"scmf 3",">",5)
        lWaitCmdTerm(term,"er 0",">",3)
        lWaitCmdTerm(term,"freq 0 20",">",3)
        lWaitCmdTerm(term,"modulation 0 1",">",3)
        lWaitCmdTerm(term,"symb 0 1",">",3)
        lWaitCmdTerm(term,"sdattn 0 0",">",3)
        lWaitCmdTerm(term,"sapdelta 0",">",5)
        lWaitCmdTerm(term,"uf",">",3)   
        lWaitCmdTerm(term,"er 2",">",3)
        lWaitCmdTerm(term,"cont 0 1",">",3)
        lWaitCmdTerm(term,"upstream 0 1",">",3)        
        for index,f in enumerate(freq_range):          
          for try_ in range(1):
            lWaitCmdTerm(term,"freq 0 %f"%f,">",5)
            lWaitCmdTerm(term,"gain %s"%pga_gain,">",5)
            r = gpib.ReadUSQPSKPower(f,200,400)+0.2; r=float('%.2f'%r)
            msg = "Freq=%.1f measure=%.2f (%.2f ~ %.2f)"%(f,r,us_freqs[diplexer][2][index]-us_freqs[diplexer][3][index],us_freqs[diplexer][2][index]+us_freqs[diplexer][3][index])
            if r<us_freqs[diplexer][2][index]-us_freqs[diplexer][3][index] or r>us_freqs[diplexer][2][index]+us_freqs[diplexer][3][index]:
               msg = "Freq=%.1f measure=%.2f (%.2f ~ %.2f) --- fail"%(f,r,us_freqs[diplexer][2][index]-us_freqs[diplexer][3][index],us_freqs[diplexer][2][index]+us_freqs[diplexer][3][index])
               if run_flow:
                 parent.SendMessage(dut_id,"%s\n"%msg,log)
                 testfail=1
               else: raise Except('%s\n'%msg)                
            else:
               parent.SendMessage(dut_id,"%s\n"%msg,log); break              
          lWaitCmdTerm(term,"sfreq %.1f %.2f"%(f,r),">",5,3)       
          us_table.update([(f,r)])
        lWaitCmdTerm(term,"uf",">",5)
        USCal_Table_Verify(parent,dut_id,freq_range,us_table,term,log)
    parent.SendMessage(dut_id,'US Calibration Test Done\n',log)
    parent.SendMessage(dut_id,"US Calibration time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
    if testfail: 
       lWaitCmdTerm(term,"qu","#",3)
       raise Except("FAIL: PGA Cal")
              
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

def mxl214_ESAM(parent,dut_id,term,basePower,bandwidth,log):
    '''
    author: YiJie Wang
    date: 2017/01/13
    description: *calibrate for MxL214_cms-02
    '''  
    test_time = time.time()
    result=0
    lWaitCmdTerm(term,"D","Downstream_Calibration>",5)
    for diplexer in ds_diplexer_list:
      diplexer_index=ds_freqs[diplexer][0]
      freq_range=ds_freqs[diplexer][1]
      attn,ds_data=Read_Get_table(dut_id,freq_range,basePower,bandwidth,log)
      pportOut(attn,0x378)            
      parent.SendMessage(dut_id,"=============================================\n",log)
      parent.SendMessage(dut_id,"Tuner %s Frequencies: %s \n"%(diplexer_index,ds_data[0]),log)
      parent.SendMessage(dut_id,"Noise Power: %s \n"%ds_data[1],log)
      parent.SendMessage(dut_id,"=============================================\n",log)
      cal_test_time = time.time()
      lWaitCmdTerm(term,"sfreq %s"%ds_data[0],">",5)
      lWaitCmdTerm(term,"spow %s"%ds_data[1],">",5)
      for t in xrange(3):
        parent.SendMessage(dut_id,"Start to run Tuner%s Calibration....(%d)\n"%(diplexer_index,(t+1)),log)
        data=lWaitCmdTerm(term,"runcal %s"%diplexer_index,"Downstream_Calibration>",20)
        if 'D/S Calibration Finished' not in data:
          parent.SendMessage(dut_id,'Downstream calibration Test...(%d) failed\n'%(t+1),log)
          result=1
          continue
        else:
          for check in xrange(3):
            data=lWaitCmdTerm(term,"printTunerCalInfo","ion>",10)
            if 'Index' not in data: time.sleep(1); continue
            else: break
          if int(diplexer_index) == 1:
             result=ConfirmM214CalInfo_Tuner1(parent,dut_id,data,DS_FreqComp,DS_FreqComp_offset,log)
          else: result=ConfirmM214CalInfo(parent,dut_id,data,DS_FreqComp,DS_FreqComp_offset,log)
          if result: 
             if run_flow: pass
             else: raise Except("FAIL: Tuner%s Cal"%diplexer_index)
          else: break
      parent.SendMessage(dut_id,"Tuner%s Calibration time: %3.2f (sec)\n"%(diplexer_index,(time.time()- cal_test_time)),log)          
      result+=result
    lWaitCmdTerm(term,"exit",">",5)    
    if not result: lWaitCmdTerm(term,"qu","#",5,2); lWaitCmdTerm(term,"setstartup -e","#",5,2)  
    else: raise Except("FAIL: DS Cal") 
    parent.SendMessage(dut_id,'Downstream calibration Test Done\n',log)
    parent.SendMessage(dut_id,"DS Calibration time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
    
def ConfirmM214CalInfo_Tuner1(parent,dut_id,data,DS_FreqComp,DS_FreqComp_offset,log): 
    test_fail = 0
    Segment = []
    split_data=[]; split_value=[[0 for j in xrange(8)] for i in xrange(9)]
    for index, string in enumerate(data.splitlines()):
      if 'TiltIndex:0' in string or 'TiltIndex:1' in string or 'TiltIndex:2' in string:
        split_data.append(data.splitlines()[index+1:index+9])
    for index in xrange(9):
      for part in split_data[index]:
        s_index = int(part.split('Segment:')[-1].split('| c2')[0]); #print s_index
        c0=int(part.split('c0=')[-1].strip()); #print c0
        split_value[index][s_index]=c0
    locate=0
    for table in xrange(1):
      parent.SendMessage(dut_id,'\nTable%d\n'%(table+1),log)
      for i in range(3):
        parent.SendMessage(dut_id,'TiltIndex:%d\n'%i,log) 
        message=''
        for j in range(8):
          if (DS_FreqComp[locate+table][j]-DS_FreqComp_offset) < split_value[locate+table][j] < (DS_FreqComp[locate+table][j]+DS_FreqComp_offset):
            msg='Segment:%d c0= %d (%d ~ %d)'%(j,split_value[locate+table][j],DS_FreqComp[locate+table][j]-DS_FreqComp_offset,DS_FreqComp[locate+table][j]+DS_FreqComp_offset)
          else:
            msg='Segment:%d c0= %d (%d ~ %d) -- fail'%(j,split_value[locate+table][j],DS_FreqComp[locate+table][j]-DS_FreqComp_offset,DS_FreqComp[locate+table][j]+DS_FreqComp_offset)  
            test_fail=1
          message+=msg+"\r"
        if i<2:locate+=1
        parent.SendMessage(dut_id,message+'\n',log)
    return test_fail 

def ConfirmM214CalInfo(parent,dut_id,data,DS_FreqComp,DS_FreqComp_offset,log): 
    test_fail = 0
    Segment = []
    split_data=[]; split_value=[[0 for j in xrange(8)] for i in xrange(9)]
    for index, string in enumerate(data.splitlines()):
      if 'TiltIndex:0' in string or 'TiltIndex:1' in string or 'TiltIndex:2' in string:
        split_data.append(data.splitlines()[index+1:index+9])
    for index in xrange(9):
      for part in split_data[index]:
        s_index = int(part.split('Segment:')[-1].split('| c2')[0]); #print s_index
        c0=int(part.split('c0=')[-1].strip()); #print c0
        split_value[index][s_index]=c0
    locate=0
    for table in xrange(3):
      parent.SendMessage(dut_id,'\nTable%d\n'%(table+1),log)
      for i in range(3):
        parent.SendMessage(dut_id,'TiltIndex:%d\n'%i,log) 
        message=''
        for j in range(8):
          if (DS_FreqComp[locate+table][j]-DS_FreqComp_offset) < split_value[locate+table][j] < (DS_FreqComp[locate+table][j]+DS_FreqComp_offset):
            msg='Segment:%d c0= %d (%d ~ %d)'%(j,split_value[locate+table][j],DS_FreqComp[locate+table][j]-DS_FreqComp_offset,DS_FreqComp[locate+table][j]+DS_FreqComp_offset)
          else:
            msg='Segment:%d c0= %d (%d ~ %d) -- fail'%(j,split_value[locate+table][j],DS_FreqComp[locate+table][j]-DS_FreqComp_offset,DS_FreqComp[locate+table][j]+DS_FreqComp_offset)  
            test_fail=1
          message+=msg+"\r"
        if i<2:locate+=1
        parent.SendMessage(dut_id,message+'\n',log)
    return test_fail 

def mxl214_ESAM_Verify(parent,dut_id,term,basePower,bandwidth,log):
    result=0
    #tuner2_range=Tuner2_Verify_Freq; attn,ds_data_tuner2=Read_Get_table_esam(tuner2_range,log)
    #freq_range=ds_freqs['wideband'][1]
    freq_range=Tuner2_Verify_Freq
    attn,ds_data_tuner2=Read_Get_table(dut_id,freq_range,basePower,bandwidth,log)
    pportOut(attn,0x378)
    power=ds_data_tuner2[1].splitlines()
    ns_power=power[0].split(); #print ns_power
    f_msg=str()
    test_time = time.time()
    lWaitCmdTerm(term,"qu","#",5,2)
    lWaitCmdTerm(term,"cli",">",5,2)
    lWaitCmdTerm(term,"cable",">",5,2)
    lWaitCmdTerm(term,"doc",">",5,2)
    lWaitCmdTerm(term,"Esam",">",5,2)
    parent.SendMessage(dut_id,"Tuner2_Verify start...\n",log)       
    for rf_id in RF_Index:
        lWaitCmdTerm(term,"rfSwSet %s"%rf_id,">",5,2)
        for index, freq in enumerate(freq_range):
            freq=freq*1000000
            lWaitCmdTerm(term,"newSpectrumSet %d %d %d %d\n"%(freq,freq,span,bin),"Esam>",5)
            for t in xrange(5):
                data=lWaitCmdTerm(term,"newSpectrumGet %s\n"%Avg,"Esam>",10)
                #rep=float(data.split("Segment0 total power=")[-1].split("\n")[0].strip())
                rep=data.split("Segment0 total power=")[-1].split("\n")[0].strip()
                rep_=float(rep)                                
                if abs(rep_-float(ns_power[index])) > 2.5: 
                   if t==4: pass
                   else: time.sleep(0.5); continue
                else: 
                   msg="RF%d %dMHz Measure=%.2f Report=%.2f Diff=%.2f"%(rf_id,freq,rep_,float(ns_power[index]),(rep_-float(ns_power[index])))
                   parent.SendMessage(dut_id,msg+'\n',log,color=2)
                   break
                msg_fail="RF%d %dMHz Measure=%.2f Report=%.2f Diff=%.2f --- fail"%(rf_id,freq,rep_,float(ns_power[index]),(rep_-float(ns_power[index])))
                f_msg+=msg_fail+'\n'
                parent.SendMessage(dut_id,msg_fail+'\n',log,color=1)
                result=1
                if run_flow: pass
                else: 
                   lWaitCmdTerm(term,"qu","#",5,2);lWaitCmdTerm(term,"setstartup -d","#",5,2)
                   raise Except(msg)
    if result: lWaitCmdTerm(term,"qu","#",5,2);lWaitCmdTerm(term,"setstartup -d","#",5,2); raise Except(f_msg)                
    parent.SendMessage(dut_id,"Tuner2 verify time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
    return result
    
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
        #print "Read Attn value from:",fs[-1]
        for i in open(fs[-1]).readlines():
            if "Attn" in i:
                attn = round(float(i.split("Attn =")[-1].strip()))
                #print "Atenuation = %d"%attn
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
        #print "Read Compensation from:",fs[-1]
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

def testmode(parent,dut_id,term,log):
    lWaitCmdTerm(term,"qu","#",5)
    lWaitCmdTerm(term,"setstartup -d","#",5)
    lWaitCmdTerm(term,"reboot","reboot",5)
    parent.SendMessage(dut_id,"\n---------------------------Startup Disable---------------------------\n",log)

def T0(parent):
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
        
        Check_boot(parent,dut_id,term,log)        
        Cli_Initail(term,30)           
        if Parameter: ParameterSetup(parent,dut_id,term,mac,log)
        if Certificate: InstallKey(parent,dut_id,term,target,mac,log)
        if USCal:USCalibration(parent,dut_id,freqplan,term,log)
        if TestMode: testmode(parent,dut_id,term,log)
        Check_boot_testmode(parent,dut_id,term,log)
        if LED_TEST: Check_LED(parent,dut_id,term,log)
        Enter_Testmode(parent,dut_id,term,log)
        if Parameter_Check: ParameterCheck(parent,dut_id,term,mac,log)
        if CAVerify: CA_verify(parent,dut_id,term,mac,log)
        ClitoCal(parent,dut_id,term,log)
        if DSCal: mxl214_ESAM(parent,dut_id,term,basePower,bandwidth,log)
        if DSVer: result=mxl214_ESAM_Verify(parent,dut_id,term,basePower,bandwidth,log)
        
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
        
        Check_boot(parent,dut_id,term,log)        
        Cli_Initail(term,30)           
        if Parameter: ParameterSetup(parent,dut_id,term,mac,log)
        if Certificate: InstallKey(parent,dut_id,term,target,mac,log)
        if USCal:USCalibration(parent,dut_id,term,log)
        if TestMode: testmode(parent,dut_id,term,log)
        
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
        if LED_TEST: Check_LED(parent,dut_id,term,log)
        Enter_Testmode(parent,dut_id,term,log)
        if Parameter_Check: ParameterCheck(parent,dut_id,term,mac,log)
        if CAVerify: CA_verify(parent,dut_id,term,mac,log)
        ClitoCal(parent,dut_id,term,log)
        if DSCal: mxl214_ESAM(parent,dut_id,term,basePower,bandwidth,log)
        if DSVer: result=mxl214_ESAM_Verify(parent,dut_id,term,basePower,bandwidth,log)
        
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

    
    
