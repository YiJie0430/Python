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
    val = eval('parent.SN%d'%dut_id).GetValue()
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
    mac2="%012X"%(int(mac,16)+2)
    ecm=mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
    cmdiag=mac2[0:2]+":"+mac2[2:4]+":"+mac2[4:6]+":"+mac2[6:8]+":"+mac2[8:10]+":"+mac2[10:12]
    cmd_list=["qu",\
              "echo '[macAddr]' > /var/tmp/temp.ini",\
              "echo 'ecm=%s' >> /var/tmp/temp.ini"%ecm,\
              "echo 'cmdiag=%s' >> /var/tmp/temp.ini"%cmdiag,\
              "cli","docsis","Prod","prodset","createAsset /var/tmp/temp.ini production.ini 1"]
    parent.SendMessage(dut_id,"Set NVM Parameter Start...\n" ,log)
    for cmd in cmd_list:
      term.write(cmd+'\n'); time.sleep(0.5)
      if cmd is "prodset":
         while 1:
           time.sleep(0.5)
           data=lWaitCmdTerm(term,"\n",">",5,2)
           if 'Cable Modem Serial Num' in data:
              lWaitCmdTerm(term,"%s"%sn,">",5,2)
           if '[w]-Save and quit' in data:
              lWaitCmdTerm(term,"w\n",">",5,2)   
              break
    parent.SendMessage(dut_id,"Set MAC Address: %s \n"%mac ,log)    
    parent.SendMessage(dut_id,"Set Serial Number: %s \n"%sn ,log)    
    parent.SendMessage(dut_id,"Set NVM Parameter time: %3.2f (sec)\n"%(time.time()- test_time) ,log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)

def InstallKey(parent,dut_id,term,mac,log):
    test_time=time.time();d30_size=list();d31_size=list()
    a = "%012X"%(int(mac,16))
    ca_mac = a[0:2]+"-"+a[2:4]+"-"+a[4:6]+"-"+a[6:8]+"-"+a[8:10]+"-"+a[10:12]
    
    for format in ["cer","prv"]:
        if not os.path.isfile("%s/%s.%s"%(tftp_dir_path[0],ca_mac,format)):
            raise Except ("failed:No such file %s.%s"%(ca_mac,format))
        file_size=os.path.getsize("%s/%s.%s"%(tftp_dir_path[0],ca_mac,format)); print file_size
        if file_size>1000: raise Except ("failed:file size %s.%s"%(ca_mac,format)) ##check size
        else: d30_size.append(file_size)

        if not os.path.isfile("%s/%s.%s"%(tftp_dir_path[1],ca_mac,format)):
            raise Except ("failed:No such file %s.%s"%(ca_mac,format))
        file_size=os.path.getsize("%s/%s.%s"%(tftp_dir_path[1],ca_mac,format)); print file_size
        if file_size<1000: raise Except ("failed:file size %s.%s"%(ca_mac,format)) ##check size 
        else: d31_size.append(file_size)

    cmd_list=["qu","cd /var/tmp && mkdir d30", "cd d30",\
              "tftp -g %s -r %s.cer"%(tftp_server,ca_mac),\
              "tftp -g %s -r %s.prv"%(tftp_server,ca_mac),\
              "tftp -g %s -r mfg_cert.cer"%(tftp_server),\
              "tftp -g %s -r root_pub_key.bin"%(tftp_server),\
              "cli","docsis","Prod",\
              "createAsset /var/tmp/d30/%s.cer cm_cert.cer 1"%ca_mac,\
              "certNameSet 0 0 cm_cert.cer",\
              "createAsset /var/tmp/d30/%s.prv cm_key_prv.bin 1"%ca_mac,\
              "certNameSet 0 1 cm_key_prv.bin",\
              "createAsset /var/tmp/d30/mfg_cert.cer mfg_cert.cer 1",\
              "createAsset /var/tmp/d30/root_pub_key.bin root_pub_key.bin 1"]
    
    parent.SendMessage(dut_id,"Cable lab. Certificate 3.0 loading start...\n" ,log)
    tftp_dir(parent,tftp_dir_path[0]); time.sleep(1)
    flag=0
    for retry in xrange(10):
      if flag: break
      for index,cmd in enumerate(cmd_list):
        #term.write(cmd+'\n'); time.sleep(2);print cmd
        if index<=6: 
          data=lWaitCmdTerm(term,"%s"%cmd,"#",20)
          if 'tftp' in data: time.sleep(8); tftp_dir(parent,tftp_dir_path[0]); break
          if retry==9: raise Except ("TFTP Server Error")
          if index==6: 
            data=lWaitCmdTerm(term,"ls | grep -e '.cer' -e '.prv' -e '.bin'","#",10); #print data; 
            parent.SendMessage(dut_id,"%s\n"%data ,log)
            for file in ["%s.cer"%ca_mac,"%s.prv"%ca_mac,"mfg_cert.cer","root_pub_key.bin"]:
              if file not in data: raise Except ("failed:No such file - %s"%file)
              else: flag=1
        else:
          print index 
          data=lWaitCmdTerm(term,"%s"%cmd,">",20)
          parent.SendMessage(dut_id,"%s\n"%data ,log)
          if 'not' in data: raise Except ("failed:command - %s"%cmd)


    parent.SendMessage(dut_id,"CA_3.0(%s.cer,size:%d | %s.prv,size:%d) loading OK\n"%(ca_mac,d30_size[0],ca_mac,d30_size[1]),log,color=2)
    
    time.sleep(5)
    
    cmd_list=["qu","cd /var/tmp",\
              "tftp -g %s -r %s.cer"%(tftp_server,ca_mac),\
              "tftp -g %s -r %s.prv"%(tftp_server,ca_mac),\
              "tftp -g %s -r CableLabs_Device_CA_01.cer"%tftp_server,\
              "tftp -g %s -r CableLabs_Root_CA_01.cer"%tftp_server,\
              "cli","docsis","Prod",\
              "createAsset /var/tmp/%s.cer D3_1_cm_device_cert.cer 1"%ca_mac,\
              "createAsset /var/tmp/%s.prv D3_1_cm_device_prv_key.bin 1"%ca_mac,\
              "createAsset /var/tmp/CableLabs_Device_CA_01.cer D3_1_device_ca_cert.cer 1",\
              "createAsset /var/tmp/CableLabs_Root_CA_01.cer D3_1_root_ca_cert.cer 1"]

    parent.SendMessage(dut_id,"Cable lab. Certificate 3.1 loading Start...\n" ,log)
    tftp_dir(parent,tftp_dir_path[1]); time.sleep(1)
    flag=0
    for retry in xrange(10):
      if flag: break
      for index,cmd in enumerate(cmd_list):
        #term.write(cmd+'\n'); time.sleep(1)
        if index<6: 
          data=lWaitCmdTerm(term,"%s"%cmd,"#",20)
          if 'tftp' in data: time.sleep(8); tftp_dir(parent,tftp_dir_path[0]); break
          if retry==9: raise Except("TFTP Server Error")
          if index==5:
            data=lWaitCmdTerm(term,"ls | grep -e '.cer' -e '.prv'","#",10); print data; 
            parent.SendMessage(dut_id,"%s\n"%data ,log)
            for file in ["%s.cer"%ca_mac,"%s.prv"%ca_mac,"CableLabs_Device_CA_03_Cert.cer","CableLabs_Root_CA_01.cer"]:
              if file not in data: raise Except ("failed:No such file - %s"%file)
              else: flag=1
        else: 
          data=lWaitCmdTerm(term,"%s"%cmd,">",10)
          parent.SendMessage(dut_id,"%s\n"%data ,log)
          if 'not' in data: raise Except ("failed:command - %s"%cmd)

    parent.SendMessage(dut_id,"CA_3.1(%s.cer,size:%d | %s.prv,size:%d) loading OK\n"%(ca_mac,d31_size[0],ca_mac,d31_size[1]),log,color=2)
    
    '''
    parent.SendMessage("Setup symbolic link...",log)
    cmd_list=['qu',
              'cd /nvram/1/security',
              'ln -s /etc/docsis/security/CableLabs_Root_CA_01.cer D3_1_root_ca_cert.cer',
              'ln -s /etc/docsis/security/CableLabs_Device_CA_03_Cert.cer D3_1_device_ca_cert.cer']
    for cmd in cmd_list:
     term << cmd; time.sleep(0.5)
    term.get()
    #data=lWaitCmdTerm(term,"ls -n","#",10) 
    #parent.SendMessage(data,log)
    parent.SendMessage("Symbolic link created pass\n%s\n%s"%(cmd_list[2],cmd_list[3]),log,color=2)
    '''
    parent.SendMessage(dut_id,"\nCertificate loading time: %3.2f (sec)\n"%(time.time()- test_time),log)
    parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
def USCalibration(parent,dut_id,term,log):  
    test_time = time.time()
    testfail=0
    for index,diplexer in enumerate(diplexer_list):
      us_table=dict()
      gpib.SetUSQPSKCal()
      diplexer_index=us_freqs[diplexer][0]
      freq_range=us_freqs[diplexer][1]
      parent.SendMessage(dut_id,"Upstream Frequencies:%s\n"%freq_range,log)
      lWaitCmdTerm(term,"Up",">",5)
      lWaitCmdTerm(term,"setSwitchBand %s"%index,">",5)
      lWaitCmdTerm(term,"uf",">",5)                   
      if int(diplexer_index) <= 3:
        for i in range(8):
          lWaitCmdTerm(term,"upstream %s 0"%i,"ion>",5)
        lWaitCmdTerm(term,"er 0",">",5,2)
        lWaitCmdTerm(term,"freq 0 20",">",5)
        lWaitCmdTerm(term,"modulation 0 1",">",5)
        lWaitCmdTerm(term,"symb 0 1",">",10)
        lWaitCmdTerm(term,"cont 0 1",">",5)
        lWaitCmdTerm(term,"sdattn 0 0",">",5)
        lWaitCmdTerm(term,"uf",">",5)           
        lWaitCmdTerm(term,"er 2",">",5,2)
        lWaitCmdTerm(term,"upstream 0 1",">",5)
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
        lWaitCmdTerm(term,"exit",">",5)
      else:
        #lWaitCmdTerm(term,"uf",">",5)   
        #lWaitCmdTerm(term,"er 2",">",5,2)
        USOFDMA=list()
        lWaitCmdTerm(term,"exit",">",5)
        lWaitCmdTerm(term,"exit",">",5)
        lWaitCmdTerm(term,"Test",">",5)
        lWaitCmdTerm(term,"freq 0 5.1","est>",5)
        lWaitCmdTerm(term,"gain 25","est>",5)
        lWaitCmdTerm(term,"symb 0 1","est>",5)
        lWaitCmdTerm(term,"mod 0 1","est>",5)
        lWaitCmdTerm(term,"sdattn 0 0","est>",5)
        lWaitCmdTerm(term,"cont 0 1","est>",5)
        lWaitCmdTerm(term,"upstream 0 1","est>",5)
        sc_qam = gpib.ReadUSQPSKPower(5.1,200,400)+0.1
        lWaitCmdTerm(term,"upstream 0 0","est>",5)        
        lWaitCmdTerm(term,"gpioSetValue 0 1","est>",5)
        lWaitCmdTerm(term,"sdattn 8 15","est>",5)
        lWaitCmdTerm(term,"gain %s"%pga_gain,"est>",5)
        lWaitCmdTerm(term,"UsOfdma","UsOfdma>",5)
        diff=0
        gpib.SetUSOFDMACal()
        for index,f in enumerate(freq_range):
          for try_ in range(1):
            f_=int(f*1000000)
            lWaitCmdTerm(term,"sendTestSine 0 %s 1 0"%f_,">",5)
            r=gpib.ReadUSOFDMAPower(f,100,150)+0.1
            if not diff:               
              diff=abs(sc_qam-r)
              if diff>7: raise Except('Fail: diff:%s over spec(7)\n'%diff)
              parent.SendMessage(dut_id,'difference of sc_qam and ofdma is %.2f\n'%diff,log)
            r_=r+diff; r_=float('%.2f'%r_)
            msg = "Freq=%.1f OFDMA_measure=%.2f OFDMAtoSCQAM=%.2f (%.2f ~ %.2f)"%(f,r,r_,us_freqs[diplexer][2][index]-us_freqs[diplexer][3][index],us_freqs[diplexer][2][index]+us_freqs[diplexer][3][index])
            if r_<us_freqs[diplexer][2][index]-us_freqs[diplexer][3][index] or r_>us_freqs[diplexer][2][index]+us_freqs[diplexer][3][index]:
              msg = "Freq=%.1f OFDMA_measure=%.2f OFDMAtoSCQAM=%.2f (%.2f ~ %.2f) --- fail"%(f,r,r_,us_freqs[diplexer][2][index]-us_freqs[diplexer][3][index],us_freqs[diplexer][2][index]+us_freqs[diplexer][3][index])
              if run_flow:
                 parent.SendMessage(dut_id,"%s\n"%msg,log)
                 testfail=1
              else: raise Except('%s\n'%msg)  
            else:
              parent.SendMessage(dut_id,"%s\n"%msg,log); break
          USOFDMA.append(r_)
        lWaitCmdTerm(term,"exit\n",">",5)
        lWaitCmdTerm(term,"exit\n",">",5)
        lWaitCmdTerm(term,"Cal\n",">",5)
        lWaitCmdTerm(term,"Up\n",">",5)
        lWaitCmdTerm(term,"er 0\n",">",5,2)           
        lWaitCmdTerm(term,"uf\n",">",5)   
        #lWaitCmdTerm(term,"er 2\n",">",5,2)
        for index,f in enumerate(freq_range):        
           lWaitCmdTerm(term,"sfreq %.1f %.2f\n"%(f,USOFDMA[index]),">",5,3)       
           us_table.update([(f,USOFDMA[index])])
        lWaitCmdTerm(term,"uf\n",">",5)
        USCal_Table_Verify(parent,dut_id,freq_range,us_table,term,log)
        lWaitCmdTerm(term,"exit\n",">",5)
                   
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
    
def mxl277_cmoa_al(parent,dut_id,term,basePower,bandwidth,log):
    '''
    author: YiJie Wang
    date: 2017/6/15
    description: *submission/pure Intel API
    '''
    result=0
    test_time = time.time()
    for index,diplexer in enumerate(diplexer_list): 
      lWaitCmdTerm(term,"Down",">",5)
      lWaitCmdTerm(term,"setSwitchBand %s"%index,">",5)
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
       print len(powers.split()), len(ds_freq)
       print powers, ds_freq
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
        sn = GetSN(parent,dut_id)        
        log = log_counter(mac,FunctionName)
        start_time=time.time()
        parent.SendMessage(dut_id,"%s test program | %s , Station: %s\n"%(dut_model,function_version,FunctionName),log)
        parent.SendMessage(dut_id,"---------------------------------------\n",log)
        parent.SendMessage(dut_id,"Start Time:"+time.ctime()+"\n",log)
        parent.SendMessage(dut_id,"Scan MAC address:"+mac+"\n",log)
        parent.SendMessage(dut_id,"Scan SN:"+sn+"\n",log)
        #checktravel(mac,'127.0.0.1',1800,20)        
        parent.SendMessage(dut_id,"---------------------------------------------------------------------------\n",log)
        Check_boot_testmode(parent,dut_id,term,log)
        Enter_Testmode(parent,dut_id,term,log)
        if Parameter: ParameterSetup(parent,dut_id,term,mac,sn,log)
        if Certificate: InstallKey(parent,dut_id,term,mac,log)
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
        if DSCal: mxl277_cmoa_al(parent,dut_id,term,basePower,bandwidth,log)
        
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

    
