# -*- coding:BIG5-*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 30 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx,cStringIO,os,sys,odbc
import wx.xrc,thread
from TCPService import TCPService
from tftp import tftpcfg, tftp_engine
import htx_local
sys.path.append(os.getcwd())
from MFT512 import *
log_lock = thread.allocate_lock()  
###########################################################################
## Class MyFrame1
###########################################################################
execfile("config.ini")
if os.path.isfile('c:\\station.ini'):
   execfile('c:\\station.ini')


def GetTargetPower():
    f = open(TargetPowerFilePath,'r')
    value = f.read()
    f.close()
    value = value.split("),f.0;")[0].split(',')[-1]
    return value
    
def GetCableLoss():
    import glob   
    global CableLossPath   
    if CableLossPath[-1] not in ["/","\\"]: CableLossPath += "/"
    fs = glob.glob(CableLossPath+'Pathloss_*.csv')
    if not fs:
       htx_local.Win32Message("Warning!","No such cable loss file.")
       sys.exit(1)
    """ 
    loss = open(fs[-1],'r').read()
    f = open("bin/start_default.art",'r')
    val = '''#----------------------------------------------------------------
#Pathlosses 
#----------------------------------------------------------------\n'''+loss+f.read()+"\nequipment model=litepoint; arg=%s	# Litepoint"%IQip
    f.close
    f = open("bin/start.art",'w') 
    f.write(val)
    f.close()  
    f = open("bin/litepoint_setup_default.txt",'r')
    val ="RFPORT=%s;			# 0: left RFport(default), 1: right RFport"%IQPort+f.read()  
    f.close()
    f = open("bin/litepoint_setup.txt",'w') 
    f.write(val)
    f.close()   
    """ 
    return os.path.abspath(fs[-1])

class AtherosFrame ( wx.Frame ):
      def __init__( self ):
          wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = '%s  |  Version: %s'%(StationCaption,version), pos = wx.DefaultPosition, size = wx.Size( 620,650 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
          self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
          self.SetBackgroundColour( wx.Colour( 0xcc,0xee,0xdd ))
          IconStream='\x00\x00\x01\x00\x01\x00  \x10\x00\x00\x00\x00\x00\xe8\x02\x00\x00\x16\x00\x00\x00(\x00\x00\x00 \x00\x00\x00@\x00\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x80\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x80\x00\x00\x00\x80\x80\x00\x80\x00\x00\x00\x80\x00\x80\x00\x80\x80\x00\x00\x80\x80\x80\x00\xc0\xc0\xc0\x00\x00\x00\xff\x00\x00\xff\x00\x00\x00\xff\xff\x00\xff\x00\x00\x00\xff\x00\xff\x00\xff\xff\x00\x00\xff\xff\xff\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\xaa\xa0\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xe1\x86\x18a\xff\x86\x18a\xff\x86\x18a\xff\x86\x18a\xff\x86\x18a\xff\x86\x18a\xff\xfe\x18a\xff\xfe\x18a\xff\xfe\x18a\xff\xfe\x18a\xff\xff\xf8a\xff\xff\xf8a\xff\xff\xf8a\xff\xff\xf8a\xff\xff\xf8a\xff\xff\xff\xe1\xff\xff\xff\xe1\xff\xff\xff\xe1\xff\xff\xff\xe1'
          stream = cStringIO.StringIO(IconStream)
          icon = wx.EmptyIcon()
          icon.CopyFromBitmap(wx.BitmapFromImage(wx.ImageFromStream(stream)))
          self.SetIcon(icon) 
          bSizer1 = wx.BoxSizer( wx.VERTICAL )
          bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
          self.m_bitmap3 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 60,55 ), 0 )
          img=wx.Image('images/atheros.JPG')
          img.Rescale(60,55)
          self.m_bitmap3.SetBitmap( wx.BitmapFromImage(img))
          bSizer2.Add( self.m_bitmap3, 0, wx.ALL, 5 )
          ###########capiton###########
          self.Caption = wx.StaticText( self, wx.ID_ANY, StationCaption , wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
          self.Caption.Wrap( -1 )
          self.Caption.SetFont( wx.Font( 18, 74, 90, 92, False, "Tahoma" ) )
          bSizer2.Add( self.Caption, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          bSizer1.Add( bSizer2, 0, wx.EXPAND|wx.ALL, 5 )
          ###########################
          self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
          bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
          bSizer3 = wx.BoxSizer( wx.VERTICAL )
          bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
          ############station##############
          self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Station:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText4.Wrap( -1 )
          self.m_staticText4.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer4.Add( self.m_staticText4, 0, wx.ALL, 5 )
          self.station = wx.StaticText( self, wx.ID_ANY, u"%s"%Test_station, wx.DefaultPosition, wx.Size( 100,-1 ), wx.ALIGN_CENTRE )
          self.station.Wrap( -1 )
          self.station.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          self.station.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )
          bSizer4.Add( self.station, 0, wx.ALL, 5 )
          bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
          bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
          ###############IC Type###############
          self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"IC Type: ", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText41.Wrap( -1 )
          self.m_staticText41.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer41.Add( self.m_staticText41, 0, wx.ALL, 5 )
          self.ICType = wx.StaticText( self, wx.ID_ANY, u"%s"%ICType, wx.DefaultPosition, wx.Size( 100,-1 ), wx.ALIGN_CENTRE )
          self.ICType.Wrap( -1 )
          self.ICType.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          self.ICType.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )
          bSizer41.Add( self.ICType, 0, wx.ALL, 5 )
          bSizer3.Add( bSizer41, 0, wx.EXPAND, 5 )
          bSizer411 = wx.BoxSizer( wx.HORIZONTAL )
          ###############IQ Port###############
          self.m_staticText411 = wx.StaticText( self, wx.ID_ANY, u"NI Port:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText411.Wrap( -1 )
          self.m_staticText411.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer411.Add( self.m_staticText411, 0, wx.ALL, 5 )
          self.IQPort = wx.StaticText( self, wx.ID_ANY, u"%s"%ni_port, wx.DefaultPosition, wx.Size( 100,-1 ), wx.ALIGN_CENTRE )
          self.IQPort.Wrap( -1 )
          self.IQPort.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          self.IQPort.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )
          bSizer411.Add( self.IQPort, 0, wx.ALL, 5 )
          bSizer3.Add( bSizer411, 0, wx.EXPAND, 5 )
          bSizer4111 = wx.BoxSizer( wx.HORIZONTAL )
          ###############Target Power###############
          self.m_staticText4111 = wx.StaticText( self, wx.ID_ANY, u"Target Power: ", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText4111.Wrap( -1 )
          self.m_staticText4111.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer4111.Add( self.m_staticText4111, 0, wx.ALL, 5 )
          self.TargetPower = wx.StaticText( self, wx.ID_ANY, u"%s "%TargetPowerType, wx.DefaultPosition, wx.Size( 65,-1 ), wx.ALIGN_CENTRE )
          self.TargetPower.Wrap( -1 )
          self.TargetPower.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          self.TargetPower.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )
          bSizer4111.Add( self.TargetPower, 0, wx.ALL, 5 )
          bSizer3.Add( bSizer4111, 0, wx.EXPAND, 5 )
          bSizer41111 = wx.BoxSizer( wx.HORIZONTAL )
          ###############Cable loss file###############
          self.m_staticText41111 = wx.StaticText( self, wx.ID_ANY, u"Cable Loss File:", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText41111.Wrap( -1 )
          self.m_staticText41111.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer41111.Add( self.m_staticText41111, 0, wx.ALL, 5 )
          #self.CableLossFile = wx.StaticText( self, wx.ID_ANY, u"    %s    "%GetCableLoss(), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
          #self.CableLossFile.Wrap( -1 )
          #self.CableLossFile.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          #self.CableLossFile.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )
          #bSizer41111.Add( self.CableLossFile, 0, wx.ALL, 5 )
          bSizer3.Add( bSizer41111, 0, wx.EXPAND, 5 )
          self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
          bSizer3.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
          bSizer1.Add( bSizer3, 0, wx.EXPAND|wx.ALL, 5 )
          bSizer20 = wx.BoxSizer( wx.VERTICAL )
          bSizer41112 = wx.BoxSizer( wx.HORIZONTAL )
          ############### Input Mac ###############
          self.m_staticText41112 = wx.StaticText( self, wx.ID_ANY, u"MAC:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText41112.Wrap( -1 )
          self.m_staticText41112.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer41112.Add( self.m_staticText41112, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          self.MAC = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.TE_PROCESS_ENTER  )
          self.MAC.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
          self.MAC.SetBackgroundColour( wx.Colour( 255, 255, 0 ) )   
          bSizer41112.Add( self.MAC, 0, wx.ALL, 5 )
          ############### Input SN ###############
          self.m_staticText41113 = wx.StaticText( self, wx.ID_ANY, u"SN:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText41113.Wrap( -1 )
          self.m_staticText41113.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer41112.Add( self.m_staticText41113, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          self.SN = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.TE_PROCESS_ENTER  )
          self.SN.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
          self.SN.SetBackgroundColour( wx.Colour( 255, 255, 0 ) )   
          bSizer41112.Add( self.SN, 0, wx.ALL, 5 )
          ############### Start Button ###############
          self.StartBtn = wx.Button(self, wx.ID_OK, "START")
          bSizer41112.Add( self.StartBtn, 0,wx.EXPAND|wx.ALL,5 ) 
          bSizer41112.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 ) 
          


          ############### Result ###############         
          self.Result = wx.StaticText( self, wx.ID_ANY, u"     PASS     ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
          self.Result.Wrap( -1 )
          self.Result.SetFont( wx.Font( 16, 74, 90, 92, False, "Tahoma" ) )
          self.Result.SetBackgroundColour( wx.Colour( 0, 255, 0 ) )          
          bSizer41112.Add( self.Result, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )          
          bSizer41112.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )        
          bSizer20.Add( bSizer41112, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )  
          self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
          bSizer20.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )     
          bSizer1.Add( bSizer20, 0, wx.EXPAND, 5 )      
          ############### Log ###############   
          self.Log = wx.TextCtrl( self, wx.ID_ANY, u"NA", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_TAB|wx.TE_MULTILINE
                                                                                              |wx.HSCROLL|wx.TE_RICH2|wx.TE_READONLY
                                                                                              |wx.TE_LINEWRAP|wx.HSCROLL|wx.VSCROLL )
          self.Log.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
          self.Log.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
          self.Log.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )          
          bSizer1.Add( self.Log, 1, wx.ALL|wx.EXPAND, 5 )          
          self.SetSizer( bSizer1 )
          self.Layout()          
          self.Centre( wx.BOTH ) 
          self.buf = ''
          self.run_cart=False
          self.running = True
          self.timer_ = wx.Timer(self)
          self.Bind(wx.EVT_TIMER, self.MACSetFocus, self.timer_)
          self.timer_.Start(1000)
          #self.MAC.Bind( wx.EVT_TEXT_ENTER, self.OnFocusStart )
          self.MAC.Bind( wx.EVT_TEXT_ENTER, self.ScanSN )
          self.SN.Bind( wx.EVT_TEXT_ENTER, self.OnFocusStart )
          self.Bind( wx.EVT_CLOSE, self.close )
          self.Bind(wx.EVT_BUTTON, self.scan, self.StartBtn)
          self.en_ = 0
          self.MAC.SetValue("688F2E470700")
          self.SN.SetValue("123456789012")
          ##########inint tcp and tftp service############
          #os.popen("TASKKILL /F /IM cart.exe /T")
          #self.tcps = TCPService(self)
          #self.tcps.start()
          
          self.tcps = TCPService(self)
          self.tcps.start()
          f = open("tftp.ini",'r') 
          tftp_cfg = f.read() 
          f.close()
          f=open("tftp.ini",'w')
          for i in tftp_cfg.splitlines(): 
              if 'tftprootfolder' in i: i = "tftprootfolder = %s"%tftp_path
              f.write(i + '\n')    
          f.close()
          cfgdict = tftpcfg.getconfigstrict(os.getcwd, 'tftp.ini')
          self.TFTPServer = tftp_engine.ServerState(**cfgdict)
          thread.start_new_thread(tftp_engine.loop_nogui, (self.TFTPServer,))    
      
      def OnFocusStart(self,event):
          self.StartBtn.SetFocus()
    
      def ShowResult(self,val):
          color = {"PASS":wx.Colour( 0, 255, 0 ),
                   "FAIL":wx.Colour( 255, 0, 0 ),
                   "START":wx.Colour( 255, 255, 0 )
                  }
          self.Result.SetBackgroundColour(color[val])  
          if val=="START":
             self.Log.SetValue("")
             val="Running" 
             self.MAC.Enable(False)
             self.SN.Enable(False) 
          else:
             self.MAC.Enable(True)
             self.SN.Enable(True)
             time.sleep(0.1)
             self.en_ = 1
             self.StartBtn.Enable(True) 
          self.Result.SetLabel("     %s     "%val)
          
      def SendMessage(self,val,log=None,state="",color=0):
          colors=[(255,255,255),(255,0,0),(0,255,0)]
          
          log_lock.acquire()
          beg = self.Log.GetLastPosition()
          end = self.Log.GetLastPosition() + len(val)
          self.Log.SetStyle(beg,end,wx.TextAttr(colors[color],'black'))
          self.Log.AppendText(val)
          self.Log.ShowPosition(end)
          log_lock.release()
          
          if log:log.write(val)
          if state in ("PASS","FAIL","START"):
             self.ShowResult(state)
      
      def MACSetFocus(self,evt):
          if self.MAC.Enabled and self.en_:
             self.MAC.SetFocus()
             self.MAC.SetSelection(-1,-1)
             self.en_ = 0

      def ScanSN(self,evt):
          self.SN.Enable(True)
          time.sleep(0.1)
          self.SN.SetFocus()
          self.SN.SetSelection(-1,-1)
          
      def scan(self,evt):
          self.StartBtn.Enable(False) 
          #if not self.run_cart:
          #   os.startfile('ni.bat')
          #   #self.run_cart = True
          thread.start_new_thread(eval(FunctionName),(self,))
          
      def close( self,evt ):
          try:
              self.TFTPServer.shutdown()
              if self.running:
                 self.running = False
                 #self.tcps.close()
          except:
              pass
          sys.exit(1)

class App(wx.App):
    def OnInit(self):
        try:
            self.main = AtherosFrame()
            self.main.Show(True)
            self.SetTopWindow(self.main)
        except Exception,e:
            print e
        return True

if __name__ == '__main__':
   application = App(0)
   application.MainLoop()

