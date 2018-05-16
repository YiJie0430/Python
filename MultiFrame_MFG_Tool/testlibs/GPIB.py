import time
from ctypes import *
execfile("system.ini")
class SICL_GPIB:
    def __init__(self):
        self.sicl = cdll.LoadLibrary("sicl32.dll")
    
    def GenerateSignal(self,frequency,power,compensation):
        self.hpib_out (0, "7,19", "FREQ:CW %.2fMHZ"%frequency)
        #self.hpib_out (0, "7,19", "POW:AMPL %.2fDBUV"%(power+60.0+compensation))
        self.hpib_out (0, "7,19", "POW:AMPL %.2fDBM"%(power - 48.75 + compensation))#
        self.hpib_out (0, "7,19", "OUTP:STAT ON")
        for i in range(1,10000): pass    

    def TurnoffSignal(self):
        self.hpib_out (0, "7,19", "OUTP:STAT OFF")
        
    def hpib_out(self,Timeout,ud,commandstr):
        result = ""
        gpib_ud = self.sicl.iopen("hpib"+ud)
        if Timeout==0:
           Timeout=6
        self.sicl.itimeout(gpib_ud,c_long(Timeout*1000))
        self.sicl.ivprintf(gpib_ud,c_char_p("*CLS\n"))
        self.sicl.ivprintf(gpib_ud, c_char_p(commandstr+"\n"))
        if "?" in commandstr:
            readbuf = create_string_buffer(128)
            self.sicl.iscanf(gpib_ud, c_char_p("%128t"), readbuf)
            result = readbuf.value.strip()
        self.sicl.iclose(gpib_ud)
        return result
        
    def GetE4411BPeakPower(self,freq,dtime,compensation):
        self.hpib_out (0, "7,18", ":FREQ:CENT %dKHz"%freq)
        time.sleep(dtime)  
        self.hpib_out (0, "7,18", "CALC:MARK:MAX")
        pwr = float(self.hpib_out(0, "7,18", "CALC:MARK:Y?"))+compensation
        pfreq = float(self.hpib_out(0, "7,18", "CALC:MARK:X?"))
        return (pwr,pfreq)
    
    def MeasurePower(self,frequency,compensation):
        self.hpib_out (0, "7,18", "INZ 75;")
        self.hpib_out (20,"7,18", "SNGLS;CF%.2fMHZ;SP500KHZ;RB 3KHZ;"%frequency)
        self.hpib_out (0, "7,18", "AUNITS DBMV;")
        self.hpib_out (0, "7,18", "RL 70DB;")
        self.hpib_out (0, "7,18", "SNGLS;TS;MKPK HI;")
        return float(self.hpib_out(0, "7,18", "MKA?;"))+compensation
    
    def MeasureE4405BPeakPwrFreq(self,fa,fb,rl,rb,dtime,compensation):
        self.hpib_out (0, "7,18", "CHP:BAND:INT %dKHz"%(fb-fa))
        self.hpib_out (0, "7,18", ":FREQ:CENT %dKHz"%((fb-fa)/2+fa))
        self.hpib_out (0, "7,18", ":FREQ:STAR %dKHz"%fa)
        self.hpib_out (0, "7,18", ":FREQ:STOP %dKHz"%fb)
        self.hpib_out (0, "7,18", ":BWID %fKHz"%rb) # resolution bandwidth
        self.hpib_out (0, "7,18", "UNIT:POW DBM")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV %d"%rl)
        self.hpib_out (0, "7,18", "INIT:CONT ON")
        time.sleep(dtime)  
        self.hpib_out (0, "7,18", "CALC:MARK:MAX")
        pwr = float(self.hpib_out(0, "7,18", "CALC:MARK:Y?"))+compensation
        pfreq = float(self.hpib_out(0, "7,18", "CALC:MARK:X?"))
        return (pwr,pfreq)
    
    def MeasureFreq(self,frequency):
        self.hpib_out (20,"7,18", "SNGLS;CF%.2fMHZ;SP20KHZ;RB 3KHZ;"%frequency)
        self.hpib_out (0, "7,18", "AUNITS DBMV;")
        self.hpib_out (0, "7,18", "RL 70DB;")
        self.hpib_out (0, "7,18", "SNGLS;TS;MKPK HI;")
        return float(self.hpib_out(0, "7,18", "MKF?;"))
    
    def GetInstrumentType(self,addr):
        return self.hpib_out (0,"7,%d"%addr,"*IDN?").split(",")[1].strip()
    
    def SetMain(self):
        self.hpib_out (0, "7,18", "CHP:BAND:INT 200KHz")
        self.hpib_out (0, "7,18", ":BWID 3KHz") # resolution bandwidth
        self.hpib_out (0, "7,18", ":BWID:VID 3KHz") # video bandwidth
        self.hpib_out (0, "7,18", ":BWID:VID:RAT 1") # video bandwidth ratio
        self.hpib_out (0, "7,18", ":SWE:TIME 167ms") # video bandwidth ratio
        self.hpib_out (0, "7,18", "UNIT:POW DBM")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV 20")
        self.hpib_out (0, "7,18", "INIT:CONT ON")
    ### ecmmv2 uscalibration #####
    
    def MeasureE4405BChPwr(self,freq,sp,bw,rl,rb,compensation):
        self.hpib_out (0, "7,18", ":FREQ:CENT %dKHz"%freq)  
        self.hpib_out (0, "7,18", ":FREQ:SPAN %dKHz"%sp)      
        self.hpib_out (0, "7,18", ":BWID %dKHz"%rb) # resolution bandwidth
        self.hpib_out (0, "7,18", "SENSe:CHPower:AVERage:COUNt 5")
        self.hpib_out (0, "7,18", "SENS:CHP:AVERage ON")
        self.hpib_out (0, "7,18", ":SENS:CHPower:FREQuency:SPAN %dKHz"%sp) 
        self.hpib_out (0, "7,18", "CHP:BAND:INT %dKHz"%bw)
        #self.hpib_out (0, "7,18", ":FREQ:SPAN %dKHz"%sp)
        self.hpib_out (0, "7,18", "UNIT:POW DBM")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV %d"%rl)
        self.hpib_out (0, "7,18", "INIT:CONT OFF")
        pwr = float(self.hpib_out(0, "7,18", ":READ:CHPower?").split(",")[0])+compensation
        #time.sleep(3) 
        self.hpib_out (0, "7,18", "INIT:CONT ON")      
        return pwr
    
    def MeasureSPCHPWR(self,frequency,compensation):
        self.hpib_out (0, "7,18", "INZ 75;")
        self.hpib_out (20,"7,18", "SNGLS;CF%.2fMHZ;SP 1MHZ;"%frequency)
        self.hpib_out (0, "7,18", "RL 55DB;")
        self.hpib_out (0, "7,18", "ACPBW 200KHZ;")
        self.hpib_out (0, "7,18", "AUNITS DBMV;")
        self.hpib_out (0, "7,18", "CHP;")
        #time.sleep(0.5)
        return float(self.hpib_out(0, "7,18", "CHPWR?;"))+compensation
      
    def SetPreset(self):
        self.hpib_out (0, "7,18", "SYST:PRES")
    
    def SetPeakPwr(self):
        self.hpib_out (0, "7,18", "CONF:SAN")
        time.sleep(2)
        self.hpib_out (0, "7,18", "UNIT:POW DBMV")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV 50")
        self.hpib_out (0, "7,18", ":FREQ:SPAN 200KHz")
        self.hpib_out (0, "7,18", ":BWID 1KHz") # resolution bandwidth
        self.hpib_out (0, "7,18", ":BWID:VID 3KHz")
        
    
    def GetPeakPwr(self,freq):
        self.hpib_out (0, "7,18", ":FREQ:CENT %.1fMHz"%freq)
        #time.sleep(0.8)
        for i in range(2):
            time.sleep(0.5)
            self.hpib_out (0, "7,18", "CALC:MARK:MAX")
            pwr = float(self.hpib_out(0, "7,18", "CALC:MARK:Y?"))
            if pwr > 7: break
        return pwr
    
    def SetUSFreqcal(self):
        self.hpib_out (0, "7,18", "CONF:SAN")
        time.sleep(2)
        self.hpib_out (0, "7,18", ":FREQ:CENT 30MHz")
        self.hpib_out (0, "7,18", "UNIT:POW DBMV")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV 65")
        self.hpib_out (0, "7,18", ":FREQ:SPAN 10KHz")
        self.hpib_out (0, "7,18", ":BWID 1KHz") # resolution bandwidth
        self.hpib_out (0, "7,18", ":BWID:VID 300Hz")
        time.sleep(1)  
        self.hpib_out (0, "7,18", "CALC:MARK:MAX")
        pwr = float(self.hpib_out(0, "7,18", "CALC:MARK:Y?"))
        pfreq = float(self.hpib_out(0, "7,18", "CALC:MARK:X?"))
        return (pwr,pfreq)

    def SetUSQPSKCal(self):
        self.hpib_out (0, "7,18", "UNIT:POW DBMV")
        self.hpib_out(0, "7,18", ":READ:CHPower?")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV 30")
        self.hpib_out (0, "7,18", "CHP:BAND:INT 200KHz")
        self.hpib_out (0, "7,18", ":SENS:CHPower:FREQuency:SPAN 400KHz")
        self.hpib_out (0, "7,18", ":BWID 3KHz") # resolution bandwidth
        self.hpib_out (0, "7,18", ":BWID:VID 30KHz")
        self.hpib_out (0, "7,18", "INIT:CONT OFF")
        self.hpib_out (0, "7,18", "CHPower:AVERage:COUNt 5")
        self.hpib_out (0, "7,18", ":SENS:CHP:AVERage ON")
    
    def SetRLEV(self,RLEV):
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV %s"%RLEV)
        
    def ReadUSQPSKPower(self,freq,bw,sp):
        self.hpib_out (0, "7,18", ":FREQ:CENT %.1fMHz"%freq)
        self.hpib_out (0, "7,18", "CHP:BAND:INT %dKHz"%bw)
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV:OFFS %.1f"%Ref_offset)
        self.hpib_out (0, "7,18", ":SENS:CHPower:FREQuency:SPAN %dKHz"%sp)
        self.hpib_out(0, "7,18", "INIT:RESTart")
        pwr = float(self.hpib_out(0, "7,18", ":READ:CHPower?").split(",")[0])     
        return pwr
    
    def SetD3StationCal(self,bw):
        self.hpib_out (0, "7,18", "UNIT:POW DBMV")
        self.hpib_out(0, "7,18", ":READ:CHPower?")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV 30")
        self.hpib_out (0, "7,18", "CHP:BAND:INT %sMHz"%bw)
        self.hpib_out (0, "7,18", ":SENS:CHPower:FREQuency:SPAN %sMHz"%bw)
        self.hpib_out (0, "7,18", ":BWID 100kHz") # resolution bandwidth
        self.hpib_out (0, "7,18", ":BWID:VID 300KHz")
        self.hpib_out (0, "7,18", "INIT:CONT OFF")
        self.hpib_out (0, "7,18", "SENSe:CHPower:AVERage:COUNt 10")
        self.hpib_out (0, "7,18", "SENSe:CHPower:AVERage:TCONtrol Repeat")
        self.hpib_out (0, "7,18", "SENS:CHP:AVERage ON")
    
    def ReadD3StationCalPower(self,freq):
        self.hpib_out (0, "7,18", ":FREQ:CENT %.1fMHz"%freq)
        self.hpib_out(0, "7,18", "INIT:RESTart")
        pwr = float(self.hpib_out(0, "7,18", ":READ:CHPower?").split(",")[0])
        return pwr 
    
    def ReadCounterFreq(self):
        freq = float(self.hpib_out(0, "7,3", ":READ:FREQ?"))
        return freq
    
    def SetphyQPSKCal(self):
        self.hpib_out (0, "7,18", "UNIT:POW DBMV")
        self.hpib_out(0, "7,18", ":READ:CHPower?")
        self.hpib_out (0, "7,18", "DISP:WIND:TRAC:Y:RLEV 20")
        self.hpib_out (0, "7,18", "CHP:BAND:INT 200KHz")
        self.hpib_out (0, "7,18", ":SENS:CHPower:FREQuency:SPAN 400KHz")
        self.hpib_out (0, "7,18", ":BWID 3KHz") # resolution bandwidth
        self.hpib_out (0, "7,18", ":BWID:VID 30KHz")
        self.hpib_out (0, "7,18", "INIT:CONT OFF")
        self.hpib_out (0, "7,18", "CHPower:AVERage:COUNt 5")
        self.hpib_out (0, "7,18", "SENS:CHP:AVERage ON")
    
    def SetphyQPSKCal(self):
        self.hpib_out(0, "7,18", "UNIT:POW DBMV")
        self.hpib_out(0, "7,18", ":READ:CHPower?")
        self.hpib_out(0, "7,18", "DISP:WIND:TRAC:Y:RLEV 20")
        self.hpib_out(0, "7,18", "CHP:BAND:INT 200KHz")
        self.hpib_out(0, "7,18", ":SENS:CHPower:FREQuency:SPAN 400KHz")
        self.hpib_out(0, "7,18", ":BWID 3KHz") # resolution bandwidth
        self.hpib_out(0, "7,18", ":BWID:VID 30KHz")
        self.hpib_out(0, "7,18", "INIT:CONT OFF")
        self.hpib_out(0, "7,18", "CHPower:AVERage:COUNt 5")
        self.hpib_out(0, "7,18", "SENS:CHP:AVERage ON")    
    
    def ReadUSOFDMAPower(self,freq,bw,sp):
        self.hpib_out(0, "7,18", ":FREQ:CENT %.1fMHz"%freq)
        self.hpib_out(0, "7,18", "DISP:WIND:TRAC:Y:RLEV:OFFS %.1f"%Ref_offset)
        self.hpib_out(0, "7,18", "CHP:BAND:INT %dKHz"%bw)
        self.hpib_out(0, "7,18", ":SENS:CHPower:FREQuency:SPAN %dKHz"%sp)
        self.hpib_out(0, "7,18", "INIT:RESTart")
        pwr = float(self.hpib_out(0, "7,18", ":READ:CHPower?").split(",")[0])
        return pwr    
    
    def ReadUSQPSKPower(self,freq,bw,sp):
        self.hpib_out(0, "7,18", ":FREQ:CENT %.1fMHz"%freq)
        self.hpib_out(0, "7,18", "DISP:WIND:TRAC:Y:RLEV:OFFS %.1f"%Ref_offset)
        self.hpib_out(0, "7,18", "CHP:BAND:INT %dKHz"%bw)
        self.hpib_out(0, "7,18", ":SENS:CHPower:FREQuency:SPAN %dKHz"%sp)
        self.hpib_out(0, "7,18", "INIT:RESTart")
        pwr = float(self.hpib_out(0, "7,18", ":READ:CHPower?").split(",")[0])
        return pwr
        
    def SetUSOFDMACal(self):
        self.hpib_out(0, "7,18", "UNIT:POW DBMV")
        self.hpib_out(0, "7,18", ":READ:CHPower?")
        self.hpib_out(0, "7,18", "DISP:WIND:TRAC:Y:RLEV 40")
        #self.hpib_out(0, "7,18", "CHP:BAND:INT 100KHz")
        #self.hpib_out(0, "7,18", ":SENS:CHPower:FREQuency:SPAN 150KHz")        
        #self.hpib_out(0, "7,18", ":BWID 1KHz") # resolution bandwidth
        #self.hpib_out(0, "7,18", ":BWID:VID 10KHz")
        self.hpib_out(0, "7,18", "CHP:BAND:INT 200KHz")
        self.hpib_out(0, "7,18", ":SENS:CHPower:FREQuency:SPAN 400KHz")        
        self.hpib_out(0, "7,18", ":BWID 3KHz") # resolution bandwidth
        self.hpib_out(0, "7,18", ":BWID:VID 30KHz")        
        self.hpib_out(0, "7,18", "INIT:CONT OFF")
        self.hpib_out(0, "7,18", "CHPower:AVERage:COUNt 5")
        self.hpib_out(0, "7,18", "SENS:CHP:AVERage ON")