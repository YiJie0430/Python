# -*- coding:BIG5-*- 
import wx,cStringIO,os,sys,wx.xrc,thread
from testlibs.model import *

sys.path.append(os.getcwd())
log_lock = thread.allocate_lock() 

execfile("system.ini")

if os.path.isfile('c:\\station.ini'):
   execfile('c:\\station.ini')

FunctionName_path = os.getcwd()+'\\testlibs\\model\\%s\\config.ini'%dut_model
execfile(FunctionName_path)
  
###########################################################################
## Class D70_develop_Frame
###########################################################################
class D70_develop_Frame ( wx.Frame ):
      def __init__( self ):
          wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = '%s  |  %s'%(stationcaption,main_version), pos = wx.DefaultPosition, size = wx.Size( 1077,820 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
          self.SetSizeHintsSz( wx.DefaultSize,wx.DefaultSize )
          self.SetBackgroundColour( wx.Colour( 0xdd,0xdd,0xdd ))
          icon = wx.Icon('Images/D70.ico',wx.BITMAP_TYPE_ICO)
          self.SetIcon(icon)
          self.id_ = None 
          bSizer1 = wx.BoxSizer( wx.VERTICAL )
          bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
          ###########capiton###########
          self.Caption = wx.StaticText( self, wx.ID_ANY, u'   ' , wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
          self.Caption.Wrap( -1 )
          self.Caption.SetFont( wx.Font( 24, 74, 90, 92, False, "Tahoma" ) )
          bSizer2.Add( self.Caption, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          self.m_bitmap3 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
          img=wx.Image('Images/Hitron_logo.bmp')
          self.m_bitmap3.SetBitmap( wx.BitmapFromImage(img))
          bSizer2.Add( self.m_bitmap3, 0, wx.ALL, 5 )
          bSizer1.Add( bSizer2, 0, wx.EXPAND|wx.ALL, 5 )
          ###########################
          self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
          bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
          ############Model/station##############
          bSizer3 = wx.BoxSizer( wx.VERTICAL )
          bSizer4 = wx.BoxSizer( wx.HORIZONTAL )         
          self.m_staticText = wx.StaticText( self, wx.ID_ANY, u"Model:", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText.Wrap( -1 )
          self.m_staticText.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer4.Add( self.m_staticText, 0, wx.ALL, 5 )
          self.Model = wx.StaticText( self, wx.ID_ANY, u"%s"%dut_model, wx.DefaultPosition, wx.Size( 100,-1 ), wx.ALIGN_CENTRE )
          self.Model.Wrap( -1 )
          self.Model.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          self.Model.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )
          bSizer4.Add( self.Model, 0, wx.ALL, 5 )          
          self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Station:", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText4.Wrap( -1 )
          self.m_staticText4.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer4.Add( self.m_staticText4, 0, wx.ALL, 5 )
          self.station = wx.StaticText( self, wx.ID_ANY, u"%s"%FunctionName, wx.DefaultPosition, wx.Size( 100,-1 ), wx.ALIGN_CENTRE )
          self.station.Wrap( -1 )
          self.station.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          self.station.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )
          bSizer4.Add( self.station, 0, wx.ALL, 5 )
          #### Scan DUT ID ####
          self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"DUT ID:", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.m_staticText42.Wrap( -1 )
          self.m_staticText42.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          bSizer4.Add( self.m_staticText42, 0, wx.ALL, 5 )
          bSizer4.AddSpacer( ( 0, 0), 0, 0, 5 )
          self.dut_id = wx.TextCtrl( self, wx.ID_ANY, u'SCAN', wx.DefaultPosition, wx.Size( 100,20 ), wx.TE_PROCESS_ENTER  )
          self.dut_id.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )
          self.dut_id.SetBackgroundColour( wx.Colour( 255, 255, 208 ) )          
          bSizer4.Add( self.dut_id, 0, wx.ALL, 5 )                    
          bSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
          
          self.Btn_Terminal = wx.Button( self, wx.ID_ANY, u"Console", wx.DefaultPosition, wx.DefaultSize, 0 )
          bSizer4.Add( self.Btn_Terminal, 0, wx.ALL, 5 )
          self.Btn_StationCal = wx.Button( self, wx.ID_ANY, u"Cable Loss Calibrate", wx.DefaultPosition, wx.DefaultSize, 0 )
          bSizer4.Add( self.Btn_StationCal, 0, wx.ALL, 5 )
          bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
                              
          bSizer1.Add( bSizer3, 0, wx.EXPAND|wx.ALL, 5 )
          self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
          bSizer1.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )          
          
          if frame/2 >= 2: spliter=2; framlist=[range(1,(frame/2)+1,1), range((frame/2)+1,frame+1,1)]
          else: spliter=1; framelist_=range(1,frame+1,1)

          for x in xrange(spliter):
               if spliter == 1: distance=0.15; pass 
               else:
                    if not x: framelist_=framlist[0]
                    else: framelist_=framlist[1]
                    distance=0.25 
               exec "bSizer5%s = wx.BoxSizer( wx.HORIZONTAL )"%x
               ######  DUT Parameter Setting #########################        
               for n in framelist_:     
                    exec "self.splitterwindow%s = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER|wx.SP_LIVE_UPDATE, size=(-1,1))"%n
                    exec "self.splitterwindow%s.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_SCROLLBAR ) )"%n 
                    
                    exec "self.panel_top%s = wx.Panel(self.splitterwindow%s,wx.ID_ANY,wx.DefaultPosition,wx.DefaultSize,wx.TAB_TRAVERSAL|wx.NO_BORDER)"%(n,n)
                    exec "DUT_area_layer3%s = wx.StaticBoxSizer( wx.StaticBox( self.panel_top%s, wx.ID_ANY, u'DUT%s' ), wx.HORIZONTAL )"%(n,n,n)
                    exec "DUT_area_layer3%s.SetMinSize(wx.Size(-1,-1))"%n
                    
                    exec "self.MAC%s = wx.TextCtrl( self.panel_top%s, wx.ID_ANY, u'MAC', wx.DefaultPosition, wx.Size(-1,-1), wx.TE_PROCESS_ENTER  )"%(n,n)
                    exec "self.MAC%s.SetMinSize( wx.Size( -1,-1 ) )"%n
                    exec "self.MAC%s.SetFont( wx.Font( 16, 74, 90, 92, False, wx.EmptyString ) )"%n
                    exec "self.MAC%s.SetBackgroundColour( wx.Colour( 0, 255, 255 ) )"%n
                    exec "DUT_area_layer3%s.Add( self.MAC%s, 1, wx.ALL, 5 )"%(n,n)
                    
                    if SN:
                      exec "self.SN%s = wx.TextCtrl( self.panel_top%s, wx.ID_ANY, u'SN', wx.DefaultPosition, wx.Size(-1,-1), wx.TE_PROCESS_ENTER  )"%(n,n)
                      exec "self.SN%s.SetMinSize( wx.Size( -1,-1 ) )"%n
                      exec "self.SN%s.SetFont( wx.Font( 16, 74, 90, 92, False, wx.EmptyString ) )"%n
                      exec "self.SN%s.SetBackgroundColour( wx.Colour( 0, 255, 255 ) )"%n
                      exec "DUT_area_layer3%s.Add( self.SN%s, 1, wx.ALL, 5 )"%(n,n)

                    exec "self.Result%s = wx.StaticText( self.panel_top%s, wx.ID_ANY, u'', wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_CENTRE )"%(n,n)
                    exec "self.Result%s.SetMinSize( wx.Size( -1,-1 ) )"%n
                    exec "self.Result%s.Wrap(-1)"%n
                    exec "self.Result%s.SetFont( wx.Font( 16, 74, 90, 92, False, 'Tahoma' ) )"%n
                    exec "DUT_area_layer3%s.Add( self.Result%s, 0, wx.ALL|wx.EXPAND, 5 )"%(n,n)               
                    exec "self.panel_top%s.SetSizer(DUT_area_layer3%s)"%(n,n)

                    exec "self.panel_down%s = wx.Panel(self.splitterwindow%s,wx.ID_ANY,wx.DefaultPosition,wx.DefaultSize,wx.TAB_TRAVERSAL|wx.NO_BORDER)"%(n,n)
                    exec "Result_area_layer3%s = wx.StaticBoxSizer( wx.StaticBox( self.panel_down%s, wx.ID_ANY, u'Log' ), wx.VERTICAL )"%(n,n)
                    exec "Result_area_layer3%s.SetMinSize(wx.Size(-1,150))"%n
                    
                    exec "self.Log%s = wx.TextCtrl( self.panel_down%s, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.HSCROLL|wx.TE_RICH2|wx.TE_READONLY|wx.TE_LINEWRAP|wx.VSCROLL|wx.TE_WORDWRAP )"%(n,n)
                    exec "self.Log%s.SetMinSize( wx.Size(-1,150))"%n
                    exec "Result_area_layer3%s.Add( self.Log%s, 1, wx.ALL|wx.EXPAND, 5 )"%(n,n)

                    exec "self.panel_down%s.SetSizer(Result_area_layer3%s)"%(n,n)
                    exec "self.splitterwindow%s.SetSashGravity(%s)"%(n,distance)
                    exec "self.splitterwindow%s.SplitHorizontally(self.panel_top%s, self.panel_down%s)"%(n,n,n)
                    exec "bSizer5%s.Add(self.splitterwindow%s,1,wx.ALL|wx.EXPAND,5)"%(x,n)
               exec "bSizer1.Add( bSizer5%s, 1, wx.EXPAND, 5 )"%x
                   
          self.SetSizer( bSizer1 )
          self.Layout()          
          self.Centre( wx.BOTH ) 
          self.buf = ''
          self.running = True
          if not gui_debug:
              self.Btn_Terminal.Hide()
              self.Btn_StationCal.Hide()
          
          self.dut_id.SetFocus()
          self.dut_id.SetSelection(-1,-1)
          self.dut_id.Bind( wx.EVT_TEXT_ENTER, self.Scan_DUT )
          
          if SN:
            for index in xrange(1,frame+1,1):
                exec "self.MAC%s.Bind( wx.EVT_TEXT_ENTER, self.scan_sn )"%index
                exec "self.SN%s.Bind( wx.EVT_TEXT_ENTER, self.scan )"%index
          else:
            for index in xrange(1,frame+1,1):
                exec "self.MAC%s.Bind( wx.EVT_TEXT_ENTER, self.scan )"%index
          
          self.Bind( wx.EVT_CLOSE, self.close )
          self.Btn_StationCal.Bind( wx.EVT_BUTTON, self.PathLoss )
          self.Btn_Terminal.Bind( wx.EVT_BUTTON, self.DebugConsole )
          
          ##########inint tcp and tftp service############
          #self.tcps = TCPService(self)
          #self.tcps.start()
          #cfgdict = tftpcfg.getconfigstrict(os.getcwd, 'tftp.ini')
          #self.TFTPServer = tftp_engine.ServerState(**cfgdict)
          #thread.start_new_thread(tftp_engine.loop_nogui, (self.TFTPServer,))
             
      def ShowResult(self,id_,val):
          color = {"PASS":wx.Colour( 0, 255, 0 ),
                   "FAIL":wx.Colour( 255, 0, 0 ),
                   "START":wx.Colour( 255, 255, 0 )} 
          eval('self.splitterwindow%s'%id_).SetBackgroundColour(color[val]) 
          exec "self.splitterwindow%s.Refresh()"%id_
          if val=="START":
             eval('self.Log%d'%id_).SetValue("")
             val="Running" 
             eval('self.MAC%d'%id_).Enable(False)
             if SN: eval('self.SN%d'%id_).Enable(False)
          else:
             eval('self.MAC%d'%id_).Enable(True)
             if SN: eval('self.SN%d'%id_).Enable(True)
          #eval('self.Result%d'%id_).SetLabel("%s"%val)

      def SendMessage(self,id_,val,log=None,state="",color=0):
          colors=[(0,0,0),(255,0,0),(0,0,255)]
          log_lock.acquire()
          beg = eval('self.Log%d'%id_).GetLastPosition()
          end = eval('self.Log%d'%id_).GetLastPosition() + len(val)
          eval('self.Log%d'%id_).SetStyle(beg,end,wx.TextAttr(colors[color],'white'))
          eval('self.Log%d'%id_).AppendText(val)
          eval('self.Log%d'%id_).ShowPosition(end)
          log_lock.release()         
          if log:log.write(val)
          if state in ("PASS","FAIL","START"):
             self.ShowResult(id_,state)     
      
      def Scan_DUT(self,evt):
          self.id_ = int(self.dut_id.GetValue())
          if self.id_ > frame:
             self.MessageBox("Input Error",'Input DUT ID',wx.OK|wx.ICON_ERROR)
          else:
             eval('self.MAC%d'%self.id_).SetFocus()
             eval('self.MAC%d'%self.id_).SetSelection(-1,-1)                                       
          
      def scan_sn(self,evt):
          eval('self.SN%d'%self.id_).SetFocus()
          eval('self.SN%d'%self.id_).SetSelection(-1,-1)
      
      def scan(self,evt):
          thread.start_new_thread(eval('%s.'%dut_model+FunctionName),(self,))
          self.dut_id.SetFocus()
          self.dut_id.SetSelection(-1,-1)
        
      def PathLoss(self,event):
          CalibrateGUI.gui(self) 
    
      def DebugConsole(self,event):
          Terminal.gui(self)  
          
      def close( self,evt ):
          try:
              if self.running:
                 self.running = False                 
          except:
              pass
          sys.exit(1)      
      
      def MessageBox(self,content,title,msg_type):
          dlg = wx.MessageDialog(self,content, title, msg_type)
          result = dlg.ShowModal()
          dlg.Destroy()  
          return result 
      
      def InputBox(self, message='', default_value=''):
          dlg = wx.TextEntryDialog(self, message, defaultValue=default_value)
          dlg.ShowModal()
          result = dlg.GetValue()
          dlg.Destroy()
          return result


################################
#          Main Code           #
################################     
class App(wx.App):
    def OnInit(self):
        try:
            self.main = D70_develop_Frame()
            self.main.Show(True)
            self.SetTopWindow(self.main)
        except Exception,e:
            print e
        return True

if __name__ == '__main__':
   application = App(0)
   application.MainLoop()
