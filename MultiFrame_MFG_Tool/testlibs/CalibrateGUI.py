# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 30 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx,time,threading,wx.xrc
import GPIB,htxlib,wxMPL
import inspect
from winioport import *
from toolslib import *
from calibration import *
import wx.richtext as rt
execfile('system.ini')
path = os.getcwd() + "\\Images\\"

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

      def __init__( self, parent ):
          wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"%s"%noise_version, pos = wx.DefaultPosition, size = wx.Size( 966,568 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
          
          self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
          self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
          icon = wx.Icon('Images/D70.ico',wx.BITMAP_TYPE_ICO)
          self.SetIcon(icon)
          
          self.m_menubar1 = wx.MenuBar( 0 )
          self.m_menu1 = wx.Menu()
          self.m_menubar1.Append( self.m_menu1, u"StationCal" )
          self.open = self.m_menu1.Append(-1, "Open a file") 
          
          self.m_menu3 = wx.Menu()
          self.m_menubar1.Append( self.m_menu3, u"About" )
          self.use = self.m_menu3.Append(-1,"User guide")
          
          self.SetMenuBar( self.m_menubar1 )
          
          bSizer1 = wx.BoxSizer( wx.VERTICAL )
          
          bSizer2 = wx.BoxSizer( wx.VERTICAL )
          
          self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"NOISE MEASURE TOOL", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
          self.m_staticText1.Wrap( -1 )
          self.m_staticText1.SetFont( wx.Font( 24, 74, 90, 92, False, "Tahoma" ) )
          self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
          self.m_staticText1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
          
          bSizer2.Add( self.m_staticText1, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
          
          self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
          self.m_staticline1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
          self.m_staticline1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
          
          bSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
          
          bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
          
          bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
          
          bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
          
          bSizer5 = wx.BoxSizer( wx.VERTICAL )
          
          fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
          fgSizer1.SetFlexibleDirection( wx.BOTH )
          fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
          
          self.frequence = wx.StaticText( self, wx.ID_ANY, u"Frequence", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.frequence.Wrap( -1 )
          self.frequence.SetFont( wx.Font( 9, 74, 90, 92, False, "Tahoma" ) )
          self.frequence.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
          
          fgSizer1.Add( self.frequence, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          
          freq_selectChoices = [ u"88~1G" ]
          self.freq_select = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, freq_selectChoices, wx.CB_READONLY )
          fgSizer1.Add( self.freq_select, 1, wx.ALL|wx.EXPAND, 5 )
          
          self.bp = wx.StaticText( self, wx.ID_ANY, u"Band Power", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.bp.Wrap( -1 )
          self.bp.SetFont( wx.Font( 9, 74, 90, 92, False, "Tahoma" ) )
          
          fgSizer1.Add( self.bp, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          
          self.bpvalue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
          fgSizer1.Add( self.bpvalue, 0, wx.ALL|wx.EXPAND, 5 )
          
          self.bw = wx.StaticText( self, wx.ID_ANY, u"Band Width", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.bw.Wrap( -1 )
          self.bw.SetFont( wx.Font( 9, 74, 90, 92, False, "Tahoma" ) )
          
          fgSizer1.Add( self.bw, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          
          self.bwvaule = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
          fgSizer1.Add( self.bwvaule, 0, wx.ALL|wx.EXPAND, 5 )
          
          self.path = wx.StaticText( self, wx.ID_ANY, u"Noise Path", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.path.Wrap( -1 )
          self.path.SetFont( wx.Font( 9, 74, 90, 92, False, "Tahoma" ) )
          
          fgSizer1.Add( self.path, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
          
          self.pathvaule = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
          fgSizer1.Add( self.pathvaule, 0, wx.ALL|wx.EXPAND, 5 )
          

          bSizer5.Add( fgSizer1, 0, 0, 5 )
          
          bSizer6 = wx.BoxSizer( wx.VERTICAL )
          
          self.start = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
          self.start.SetFont( wx.Font( 9, 74, 90, 92, False, "Tahoma" ) )
          self.start.SetMinSize( wx.Size( 170,-1 ) )
          
          bSizer6.Add( self.start, 0, wx.ALL, 5 )
          
          bSizer5.Add( bSizer6, 0, 0, 5 )
          
          sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )
          
          self.message = wx.StaticText( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
          self.message.Wrap( -1 )
          self.message.SetFont( wx.Font( 10, 74, 90, 92, False, "Tahoma" ) )
          
          sbSizer2.Add( self.message, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
          
          bSizer5.Add( sbSizer2, 1, wx.EXPAND, 5 )
          
          bSizer4.Add( bSizer5, 0, wx.EXPAND, 5 )
          
          bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
          
          self.result = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_WORDWRAP )
          bSizer7.Add( self.result, 1, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )
          
          bSizer4.Add( bSizer7, 1, wx.ALIGN_BOTTOM|wx.EXPAND, 5 )
          
          bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
          
          bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
          
          sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Plot Area"), wx.VERTICAL )
          
          self.MPL = wxMPL.MPL_Panel_base(self)
          bSizer8 = wx.BoxSizer( wx.VERTICAL )
          
          bSizer8.Add(self.MPL,proportion = -1, border = 0, flag = wx.ALL | wx.EXPAND)
          sbSizer1.Add( bSizer8, 1, wx.EXPAND, 5 )
          bSizer1.Add( sbSizer1, 1, wx.EXPAND, 5 )
          
          self.SetSizer( bSizer1 )
          self.Layout()
          self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
          
          self.Centre( wx.BOTH )
          self.parent = parent
          
          # Connect Events
          self.Bind( wx.EVT_MENU, self.log, self.open)
          self.Bind( wx.EVT_MENU, self.guide, self.use)
          self.start.Bind( wx.EVT_BUTTON, self.RUNButton )
          
          # init
          self.Cal_init()
      
      def __del__( self ):
          pass
      
      def log(self,event):
          self.dlg = wx.FileDialog(self, "Open a file", style = wx.FD_OPEN)
          self.wildcard = "All files (*.*)|*.*"
          self.dlg.SetWildcard(self.wildcard) 
          dialogResult = self.dlg.ShowModal()
      
      def guide(self,event):
          guideGui(self).Show(True)              
      
      def Cal_init(self):
          self.freq_select.Clear()
          for plan in NS_freq_plan:
             self.freq_select.Append(plan)
          self.start.Enable(True)
          
      def MessageBox(self,msg,title,style):
          MessageBox = windll.user32.MessageBoxA
          return MessageBox(0, msg, title, style)

      def RUNButton( self, event ):         
          if self.freq_select.GetSelection() == -1:
            self.MessageBox('Please Select Freq Range!','Warning',0)
            return
          if self.bpvalue.GetValue() == '':
            self.MessageBox('Please Enter Noise Power','Warning',0)
            return
          if self.bwvaule.GetValue() == '':
            self.MessageBox('Please Enter Noise Width','Warning',0)
            return
          if self.pathvaule.GetValue() == '':
            self.MessageBox('Please Enter Noise Path','Warning',0)
            return
          self.MessageBox('Start on chain %d'%int(self.pathvaule.GetValue()),'Note',0)
          FrameThread(self).start()    
      
      def Funtest(self):
          NSCal_logPath = os.getcwd() + "\\Log\\" + "\\NSCal\\" + "-".join(map(str,time.gmtime()[:3]))+"\\"
          if not os.path.isdir(NSCal_logPath):
              os.system("mkdir %s"%NSCal_logPath)
          self.log = open('%sNoiseSource_%ddbmv_%dMHz_%d.%s'%(NSCal_logPath,float(self.bpvalue.GetValue()),int(self.bwvaule.GetValue()),int(self.pathvaule.GetValue()),"".join(map(str,time.gmtime()[:3]))),'w')
          self.slog = self.result
          self.setlog = SetLog(self.slog,self.log)
          self.setlog << "Noise Measure Tool Version : %s "%noise_version 
          self.setlog << "*****  Noise Power Calibration  *****"
          self.setlog << "------------------------------------------------"
          self.setlog << "Start Time : %s"%time.asctime() 
          self.setlog << "Frequence : %s"%self.freq_select.GetValue()
          self.setlog << "Noise Power : %d"%float(self.bpvalue.GetValue())
          self.setlog << "Baud Width : %d"%int(self.bwvaule.GetValue())
          self.setlog << "Noise Path : %d"%int(self.pathvaule.GetValue())
          self.stime=self.etime=time.time()
          #result=NS2SA(float(self.bpvalue.GetValue()),int(self.bwvaule.GetValue()),ds_freqs[self.freq_select.GetValue()],self.setlog)  #True,range(88,1002,12),range(len(range(88,1002,12))),#
          result=NS2SA(float(self.bpvalue.GetValue()),int(self.bwvaule.GetValue()),str(self.freq_select.GetValue()),NS_freqs[self.freq_select.GetValue()],int(self.pathvaule.GetValue()),self.setlog)  #True,range(88,1002,12),range(len(range(88,1002,12))),#          
          self.setlog << "End Time : %s"%time.asctime()
          self.setlog << "Total Time : %s"%(time.time()-self.stime)
          self.log.close()
          self.start.Enable(True)
          if not result[0]:
             return result[-1]
          else:
             x=result[1]
             y=result[2]
             self.MPL.cla()
             self.MPL.plot(x,y,'--*b')
             #self.MPL.xticker(1.0,0.5)
             #self.MPL.yticker(0.2,0.1)
             self.MPL.xlabel('Freq (MHz)')
             self.MPL.ylabel('Power (dbmv)')
             self.MPL.title_MPL("Noise Power Table ")
             self.MPL.grid()
             self.MPL.UpdatePlot()
             return 0 
class guideGui ( wx.Frame ):
     def __init__( self, parent ):
          wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'User guide ', pos = wx.DefaultPosition, size = wx.Size( 999,666 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
          self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
          layer1 = wx.BoxSizer( wx.HORIZONTAL )
          
          self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )     
          bSizer2 = wx.BoxSizer( wx.VERTICAL )        
          self.about = rt.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.TE_READONLY )
          bSizer2.Add( self.about, 1, wx.EXPAND |wx.ALL, 5 )
          layer1.Add( bSizer2, 1, wx.EXPAND |wx.ALL, 5 )
          
          Cal_layer2 = wx.BoxSizer( wx.VERTICAL )
          Cal_diagram_layer3 = wx.BoxSizer( wx.VERTICAL )
          #self.Cal_diagram = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 290,195 ), wx.DOUBLE_BORDER )
          self.Cal_diagram = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 290,195 ))
          Cal_img=wx.Image('%sCal.bmp'%path)
          Cal_img.Rescale(285,190)
          self.Cal_diagram.SetBitmap( wx.BitmapFromImage(Cal_img))
          Cal_diagram_layer3.Add( self.Cal_diagram, 0, wx.ALL|wx.EXPAND, 5 )
          Cal_layer2.Add( Cal_diagram_layer3, 1, wx.EXPAND, 5 )
          layer1.Add( Cal_layer2, 0, wx.EXPAND |wx.ALL, 5 )
          
          self.SetSizer( layer1 )
          self.Layout()         
          self.Centre( wx.BOTH )
          self.about.LoadFile('How_To_Build_Noise_Table.txt')
     def __del__( self ):
          pass 
                           
class FrameThread(threading.Thread):
      def __init__(self,frame):
          threading.Thread.__init__(self)
          self.Frame=frame
      def run(self):
          self.Frame.start.Enable( False )
          self.Frame.message.SetForegroundColour(wx.Colour(0,0,0))
          self.Frame.message.SetLabel( 'Running.......' ) 
          msg=self.Frame.Funtest()
          result=[wx.BLUE,'Finish']
          if msg:        
             result=[wx.RED,'Failed: %s'%msg] 
          self.Frame.start.Enable( True )
          self.Frame.message.SetForegroundColour(result[0])
          self.Frame.message.SetLabel( result[1] ) 

class App(wx.App):
      def OnInit(self):
          try:
              wx.InitAllImageHandlers()
              self.main = MyFrame1(None)
              self.main.Show(True)
              self.SetTopWindow(self.main)
          except Exception,e:
              print e
          return True
          
def gui(Parent):
    MyFrame1(Parent).Show(True) 
    
def main():
    application = App(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
