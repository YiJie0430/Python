import htx,time,Snmp,os,wx
from ColorConsole import *
import socket
import sys


#import xurl_core

class SetLog:
    '''
       color : 0  --  black
               1  --  red
               2  --  blue
               3  --  lime
    '''
    def __init__(self,slog,log):
        self.slog = slog
        self.log = log
        
    def set(self,s,color=0):
        #colors=[(255,255,255),(255,0,0),(0,255,0)]
        colors=[(0,0,0),(255,0,0),(0,0,255),(0,255,0)]
        s += '\n'
        self.log.write(s) 
        beg = self.slog.GetLastPosition()
        end = self.slog.GetLastPosition() + len(s)
        #self.slog.SetStyle(beg,end,wx.TextAttr(colors[color],'black'))
        self.slog.SetStyle(beg,end,wx.TextAttr(colors[color],'white'))
        self.slog.AppendText(s)
        self.slog.ShowPosition(end)
    
    def __lshift__(self,data):
        self.set(data)
        
class SendMessage:
      '''
         color : 0  --  white
                 1  --  red
                 2  --  lime
      '''
      def __init__(self,slog,log):
          self.slog = slog
          self.log = log
          
      def set(self,s,color=0):
          colors=[(255,255,255),(255,0,0),(0,255,0)]
          s += '\n'
          self.log.write(s) 
          beg = self.slog.GetLastPosition()
          end = self.slog.GetLastPosition() + len(s)
          self.slog.SetStyle(beg,end,wx.TextAttr(colors[color],'black'))
          self.slog.AppendText(s)
          self.slog.ShowPosition(end)
      
      def __lshift__(self,data):
          self.set(data) 

#        MessageBox Color
msgcolor_std = "<fg_color=CYAN,bg_color=GREY>"
msgcolor_pass = "<fg_color=BLUE,bg_color=WHITE>"
msgcolor_fail = "<fg_color=BLACK,bg_color=RED>"

##### Color Settings
#default_colors = getTextAttr()
#default_fg = default_colors & 0x0007
#default_bg = default_colors & 0x0070
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_RED = 0x0004
FOREGROUND_YELLOW = 0x0006
FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

default_fg = 0x7
default_bg = 0x0000

#SERVICE_PORT = 514
SERVICE_PORT = 19831120
Receive_PORT = 19831121
##### SNMP OIDs
ifPhysAddress2_OID = ".1.3.6.1.2.1.2.2.1.6.2"
docsDevServerBootState_OID = ".1.3.6.1.2.1.69.1.4.1"
modemProdResetAccessStart_OID = ".1.3.6.1.4.1.8595.1.400.2.1.1.8.0"
modemCmTelnetAccessEnable_OID = ".1.3.6.1.4.1.8595.1.400.3.1.9.0"
modemProdCommandLine_OID = ".1.3.6.1.4.1.8595.1.400.4.1.9.0"
modemProdSwBank_OID = "1.3.6.1.4.1.8595.1.400.2.1.2.40.5.1.1.0"
docsIfCmStatusValue_OID = ".1.3.6.1.2.1.10.127.1.2.2.1.1.2"
docsIfSigQSignalNoise_OID = ".1.3.6.1.2.1.10.127.1.1.4.1.5.3"
docsIfDownChannelPower_OID = ".1.3.6.1.2.1.10.127.1.1.1.1.6.3"
docsIfCmStatusTxPower_OID = ".1.3.6.1.2.1.10.127.1.2.2.1.3.2"

##### paths
tool_dir = "C:/Net-SNMP/bin"


def checktravel(mac,ServerIP,ServerPort,timeout):
    MesSocket=htx.UDPService(ServerIP,ServerPort,timeout)
    MesSocket.set('0,'+ mac)  
    Result=MesSocket.get()
    print Result
    if Result <> '':
       Result=Result.split('_')
       if Result[0]==mac:
         if Result[1]=='OK':
            return 1
         elif Result[1]=='NG':
            raise Except("Check MES Failed:%s"%"".join(Result).split(':')[-1])    
    raise Except("failed: Connection MES Server Fail ")

def passtravel(mac,ServerIP,ServerPort,timeout):
    MesSocket=htx.UDPService(ServerIP,ServerPort,timeout)
    MesSocket.set('1,'+ mac)  
    Result=MesSocket.get()
    if Result <> '':
       Result=Result.split('_')
       if Result[1]==mac:
          if Result[0]=='OK':
             return ""
          elif Result[0]=='NG':
             return "failed: Pass Travel Failed"    
    return "failed: Connection MES Server Fail "


def isPortConnect(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(3)
    result =1 
    try:
       s.connect((ip,int(port)))
    except Exception:
       result = 0
    s.close()
    return result

def SendMessage(s,ip="127.0.0.1"):
    index = s.find(">")
    htx.UDPService("127.0.0.1",SERVICE_PORT).set(s)
    print s[index+1:]
    

def IsLinkup(nic,timeout):
    """    IsLinkup(nic, timeout), return 1 if link-up, 0 if timeout
        where nic is network card name, timeout for waiting"""
    nic = nic.strip()
    current = time.time()
    timeout += current
    while current < timeout:
        data = os.popen("ipconfig").read().split("Ethernet adapter")
        for item in data:
            if item.count(nic) and item.count("isconnected") == 0:  #Connected
                return 1
        time.sleep(0.5)
        current = time.time()
    return 0



def IsLinkdown(nic,timeout):
    """    IsLinkdown(nic, timeout), return 1 if link-down, 0 if timeout
        where nic is network card name, timeout for waiting"""
    nic = nic.strip()
    current = time.time()
    timeout += current
    while current < timeout:
        data = os.popen("ipconfig").read().split("Ethernet adapter")
        for item in data:
            if item.count(nic) and item.count("isconnected"):  #Disconnected
                return 1
        time.sleep(0.5)
        current = time.time()
    return 0

def SetPatternColor(color=None):
#3 : setTextAttr(FOREGROUND_BLUE | default_bg | FOREGROUND_INTENSITY)
#2 : setTextAttr(FOREGROUND_YELLOW | default_bg | FOREGROUND_INTENSITY)
#1 : setTextAttr(FOREGROUND_GREEN | default_bg | FOREGROUND_INTENSITY)
#0 : setTextAttr(FOREGROUND_RED | default_bg | FOREGROUND_INTENSITY)
    if color==None:
        #setTextAttr(default_colors)
        setTextAttr(default_fg | default_bg)         
    else:
        color_dic = {0:FOREGROUND_RED,1:FOREGROUND_GREEN,2:FOREGROUND_YELLOW,3:FOREGROUND_BLUE}
        setTextAttr(color_dic[color] | default_bg | FOREGROUND_INTENSITY) 
        #setTextAttr(default_fg)  
    return ""

def WaitOperational(ip,oid,timeout):
    time_out = 0
    while 1:
        if time_out < timeout:
            if Snmp.SnmpGet(ip,oid,community="private").values()[0] == 12:
                break
        else:
            return 0
        time_out += 1
        time.sleep(1)
    return 1

def Ping(ip,length,count,interval):
    """    Ping(ip,length,count,interval), return the loss rate (float)
        where ip is target ip address, length is IP packet length
              count is packet number, interval is ms unit"""
    result = os.popen(tool_dir+"/hrping -f -l %d -s %d -n %d %s"%(length-14,interval,count,ip)).read()
    return float(result[result.rfind("(")+1:result.rfind("%")])

def RemoveWhiteSpace(value):
    """   RemoveWhiteSpace(value), return string without space like 'AABBCCDDEEFFKK'
       where value is a string like '11 22 33 44...' """
    return "".join(value.split())

def TransferHexToBinary(value):
    """    TransferHexToBinary(hex_string), return binary string like '\x00\x11\x22'
        where hex_string is a string data like '0123456789ABCDEF' """
    value = RemoveWhiteSpace(value)
    return "".join(map(chr,[int(h+l,16) for h,l in zip(value[::2],value[1::2])]))

def TransferBinaryToHex(binary):
    """    TransferBinaryToHex(binary), return heximal string like '001122AAFF'
        where binary is a string data like '\x00\x11\x22...' """
    return "".join(["%02X"%ord(x) for x in binary])
    
def InputMacAddress(prompt):
    """    InputMacAddress(prompt), return MAC address like "112233445566"
        it also check the input string is really MAC address"""
    while 1:
        SetPatternColor()
        print prompt,
        SetPatternColor(1)
        val = raw_input().strip()
        SetPatternColor()
        try:
            #if len(val) == 12 and int(val,16):
            if (len(val) == 12 or len(val) == 10): 
                return val.upper()
        except ValueError:
            pass
        #SetPattern(0)
        SetPatternColor(0)
        print "ERROR %s!!"%prompt

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

    
def lWaitCmdTerm(term,cmd,waitstr,sec,count=1):
    time.sleep(0.1)
    cmd_sec=time.time()
    while 1:
        term << "%s"%cmd
        data = term.wait("%s"%waitstr,sec)
        
        print data[-1]
        if waitstr in data[-1]:
            return data[-1]
        if time.time()-cmd_sec < sec: continue
        else: raise Except("failed: %s,%s"%(cmd,data))
        
def lWaitCmdTerm(term,cmd,waitstr,sec,retry=1):
    for loop in xrange(retry):        
        data_=str()
        cmd_sec=time.time()+0.5
        term.write(cmd+'\n')
        flag=0
        wait=0    
        while 1:
            new_data=list()            
            while 1:
                time.sleep(0.3)
                count=term.inWaiting()
                if count:
                   flag=0
                   new_data.append(term.read(count)); print 'command',new_data                        
                else: flag+=1
                if flag>2: break
            if not wait:
               data=''.join(new_data); #print data; 
               data=''.join(data.split('\r')[1:]); print 'wait0',data
            else: data=''.join(new_data); print 'wait1',data
            if waitstr in data: return data
            if time.time()-cmd_sec < sec: wait+=1; continue
            else: break
    raise Except("failed: %s,%s"%(cmd,data))
    
def StartCmd(term,cmd,waitstr,wait_time):
    a = 0
    while 1:
        term.get()
        term << "%s"%cmd
        data = term.wait("%s"%waitstr,1)
        a = a+1
        if not waitstr in data[-1]:
            if a < wait_time:
                continue
            raise Except("failed: %s"%cmd)
        else:
            return data

def Cli_Initail__(term,wait_time):
    a = 0
    while 1:
        flag = 0
        for i in ['/#','r>','r#',')#']:
            term.get()
            term << chr(0x04)
            data = term.wait("%s"%i,0.5)
            #print data[-1]
            a = a+1  
            if not i in data[-1]:
                #print '---%s---'%i
                flag+=1
            else:
                if i == '/#': 
                    term<<"exit"
                    data = term.wait("'r>'",1)
                    if not ">" in data[-1]:
                        flag+=1 
                        break
                elif i == 'r>': pass
                elif i == 'r#':
                    term<<"exit"
                    data = term.wait("'r>'",1)
                    if not "r>" in data[-1]:
                        flag+=1 
                        break
                elif i == ')#':
                    term<<"exit"
                    data = term.wait("r#",1)
                    term<<"exit"
                    data = term.wait("'r>'",1)
                    if not "r>" in data[-1]:
                        flag+=1 
                        break 
                return data
        if a < wait_time and flag >0:
            a+=1
            continue
        
        raise Except("Failed: Initial CLI command")
    

def Cli_Initail(term,wait_time):
    term.write("qu"+"\n")
    #term.write(chr(0x03)+'\n')
    time.sleep(0.5)
    data=term.read(term.inWaiting())  
    if '#' not in data: raise Except("Failed: Initial CLI command")
    else:
     lWaitCmdTerm(term,"cli" ,">",5)
     lWaitCmdTerm(term,"cable" ,">",5)
     lWaitCmdTerm(term,"logger","logger>",3) 
     lWaitCmdTerm(term,"AllComponentsConfig 0","logger>",3)
     lWaitCmdTerm(term,"exit",">",3)                        

def FPing(ip,length,count,interval):
    print ip
    """    Ping(ip,length,count,interval), return the loss rate (float)
        where ip is target ip address, length is IP packet length
              count is packet number, interval is ms unit"""
    #result = os.popen("Fping %s -s %d -t %d -n %d"%(ip,length,interval,count)).read()
    result = os.popen("Fping %s -s %d -t %d -n %d"%(ip,length,interval,count)).read()
    return float(result[result.rfind("(")+1:result.rfind("%")])

 

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
    
def IsConnect(ip,timeout):
    ip = ip.strip()
    current = time.time()
    timeout += current
    os.popen("arp -d")
    while current < timeout:
        rate = FPing(ip,64,5,1)
        if rate == 0: return 1 
        time.sleep(1)                             
        current = time.time()
    return 0

def IsConnect(ip,timeout):
    ip = ip.strip()
    current = time.time()
    timeout += current
    os.system("arp -d")
    while current < timeout:
        #data = os.popen("ipconfig").read()
        #if data.find("IP Address")>=0 and data.find(ip[:ip.rfind(".")+1])>=0 and \
        #   os.popen("ping -w 1000 -n 1 %s"%ip).read().find("Reply")>=0:
        #    return 1
        if os.popen("ping -w 1000 -n 1 %s"%ip).read().find(r"100%")<0:
            return 1
        current = time.time()
    return 0


def IsDisconnect(ip,timeout):
    ip = ip.strip()
    current = time.time()
    timeout += current
    os.popen("arp -d")
    while current < timeout:
        rate = FPing(ip,64,5,1)
        if rate == 100: return 1  
        time.sleep(1)
        current = time.time()
    return 0

def MSPing(ip1,ip2):
    print ip1,ip2
    """    Ping(ip,length,count,interval), return the loss rate (float)
        where ip is target ip address, length is IP packet length
              count is packet number, interval is ms unit"""
    result = os.popen("ping -S %s %s"%(ip1,ip2)).read()
    return float(result[result.rfind("(")+1:result.rfind("%")])