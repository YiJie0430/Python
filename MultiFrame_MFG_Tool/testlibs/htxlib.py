import serial,time,os

def IsConnect(ip,timeout):
    ip = ip.strip()
    current = time.time()
    timeout += current
    os.popen("arp -d")
    while current < timeout:
        try:
            ping_data = os.popen("ping -n 1 %s"%ip).read()
            data=int(ping_data.split('(')[-1].split('% loss')[0])
            print ping_data
            if 'expired in transit' in ping_data: 
                data =100 
            print "Ping Loss: %d"%data  
            if data < 1: return 1                         
        except:
            data=100       
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

################################################################################
#    Class
################################################################################
DEFAULT_LOG=0
class Controller(object):
    def get(self):
        return ""
    def set(self, value):
        pass
    def wait(self,timeout):
        return (False,"")
    def setWait(self,value,timeout):
        return (False,"")
    def isConnect(self):
        return True

class Terminal(Controller):
    LOST_CONNECT = "** Fail Connection **"
    def __init__(self,host,port):
        self.log = DEFAULT_LOG
        self.host = host
        self.cr = "\r"   # default Carriage Return
        self.buffer_size = 32768   # default waiting buffer size
        self.port = port
        self.tn = None

    def _init(self):
        pass
    
    def _get(self):
        pass
    
    def _set(self,value):
        pass

    def _close(self):
        self.tn.close()

    def init(self):
        self.close(0)
        try:
           self._init()
        except:
           self.tn = 0

    def isConnect(self):
        return self.tn

    def get(self):
        if self.tn == None:
            self.init()
        if self.tn == 0:
            print self.LOST_CONNECT
            return ""
        #time.sleep(0.01)
        try:
            r = self._get()
        except:
            self.tn = 0
            print self.LOST_CONNECT
            return ""
        if self.log&2:
            print "[GET]:",r
        return r

    def set(self,value):
        if self.tn == None:
            self.init()
        if self.tn == 0:
            print self.LOST_CONNECT
            return 0
        if self.log&1:
            print "[SET]:",value
        try:
            r = self._set(value+self.cr)
        except:
            self.tn = 0
            print self.LOST_CONNECT
            return 0
        return r

    def close(self,force=1):
        if self.tn:
            self._close()
            self.tn = None
            time.sleep(0.1)
        elif force:
            self.tn = None

    def wait(self,prompt,timeout):
        if self.tn == None:
            self.init()
        if self.tn == 0:
            print self.LOST_CONNECT
            return (False, "")
        prompt = str(prompt)
        timeout += time.time()+0.01
        response = ""
        count = 0 
        while time.time() < timeout and self.tn:
            count += 1
            if not (count&3):
                pass
                #print ".",
            if len(response)>self.buffer_size:
                response = response[-len(prompt):]
            d = self.get()
            response += d
            if not prompt:
                if not d:
                    return (False, response)
            else:
                if prompt in response:
                    if count >= 3:  pass#print
                    return (False, response)
            time.sleep(0.1)
        if count >= 3: pass#print
        if self.log&1:
            print "Terminal: Timeout"
        return (True, response)

    def __del__(self):
        self.close()

    def getOption(self,optionName):
        return self.__dict__[optionName]

    def setOption(self,**options):
        for k in options.keys():
            self.__dict__[k] = options[k]

    def setWait(self,setData,prompt,timeout):
        if self.tn == 0:
            print self.LOST_CONNECT
            return (False,"")
        self.set(setData)
        return self.wait(prompt,timeout)

    def __repr__(self):
        return self.get()

    def __call__(self):
        return self.get()

    def __str__(self):
        return self.get()

    def __lshift__(self,data):
        return self.set(data)
        
class SerialTTY(Terminal):
    def __init__(self,host,port=115200):
        Terminal.__init__(self,host,port)

    def _init(self):
        try:
            self.tn = serial.Serial(self.host, self.port, timeout=3)
            self.tn.writeTimeout=3
        except:
            self.tn = 0

    def _get(self):
        buf = ""
        while 1:
            count = self.tn.inWaiting()
            #print count
            if (not count) or (len(buf) > 200):
                break
            buf += self.tn.read(count)
        return buf

    def _set(self,value):
        self.tn.write(value)
        return len(value)
 

    
    
    
