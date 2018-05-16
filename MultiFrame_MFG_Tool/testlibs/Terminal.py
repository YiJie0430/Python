# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 30 2011)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import serial,time,threading
###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Terminal Tools", pos = wx.DefaultPosition, size = wx.Size( 785,589 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( 10, 74, 90, 90, False, "Arial" ) )
        self.SetBackgroundColour( wx.Colour( 189, 206, 213 ) )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Debug Terminal", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.m_staticText5.Wrap( -1 )
        self.m_staticText5.SetFont( wx.Font( 20, 74, 90, 92, False, "Arial" ) )
        self.m_staticText5.SetForegroundColour( wx.Colour( 204, 102, 0 ) )
        self.m_staticText5.SetBackgroundColour( wx.Colour( 151, 242, 238 ) )
        bSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
        sbSizer61 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Config" ), wx.VERTICAL )
        bSizer112 = wx.BoxSizer( wx.HORIZONTAL )
        self.com_lbl1 = wx.StaticText( self, wx.ID_ANY, u"COM Port", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.com_lbl1.Wrap( -1 )
        bSizer112.Add( self.com_lbl1, 0, wx.ALL, 5 )
        bSizer112.AddSpacer( ( 50, 0), 0, wx.EXPAND, 5 )
        self.com_txt = wx.TextCtrl( self, wx.ID_ANY, u"COM1", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer112.Add( self.com_txt, 0, wx.ALL, 5 )
        bSizer112.AddSpacer( ( 100, 0), 0, wx.EXPAND, 5 )
        self.connect_btn = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer112.Add( self.connect_btn, 0, wx.ALL, 5 )
        bSizer112.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        sbSizer61.Add( bSizer112, 1, wx.EXPAND, 5 )
        bSizer1111 = wx.BoxSizer( wx.HORIZONTAL )
        self.bound_lbl1 = wx.StaticText( self, wx.ID_ANY, u"Boud Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.bound_lbl1.Wrap( -1 )
        bSizer1111.Add( self.bound_lbl1, 0, wx.ALL, 5 )
        bSizer1111.AddSpacer( ( 45, 0), 0, 0, 5 )
        self.bound_txt = wx.TextCtrl( self, wx.ID_ANY, u"115200", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1111.Add( self.bound_txt, 0, wx.ALL, 5 )
        bSizer1111.AddSpacer( ( 100, 0), 0, wx.EXPAND, 5 )
        self.disconnect_btn = wx.Button( self, wx.ID_ANY, u"Disconnect", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1111.Add( self.disconnect_btn, 0, wx.ALL, 5 )
        sbSizer61.Add( bSizer1111, 1, wx.EXPAND, 5 )
        bSizer15.Add( sbSizer61, 1, 0, 5 )
        bSizer1.Add( bSizer15, 0, wx.EXPAND, 5 )
        bSizer27 = wx.BoxSizer( wx.VERTICAL )
        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer27.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
        #self.Buffer = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Buffer = wx.TextCtrl(self, -1, "",
                                            style=wx.TE_PROCESS_TAB|wx.TE_MULTILINE
                                            |wx.TE_READONLY|wx.HSCROLL|wx.TE_RICH2
                                            |wx.TE_LINEWRAP)
        self.Buffer.SetForegroundColour( wx.Colour( 255,255,255 ) )
        self.Buffer.SetBackgroundColour( wx.Colour( 0,0,0 ) )
        bSizer27.Add( self.Buffer, 1, wx.ALL|wx.EXPAND, 5 )
        bSizer1.Add( bSizer27, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
    
    
        # Connect Events
        self.connect_btn.Bind( wx.EVT_BUTTON, self.Connect )
        self.Buffer.Bind( wx.EVT_CHAR, self.onChar )
        self.disconnect_btn.Bind( wx.EVT_BUTTON, self.DisConnect )
        # Initial
        self.buffer_=[]
   
    
    def onChar(self, event):
        char = event.GetKeyCode()
        #if char == 8 or char == 127:return
        if char < 256:
            if chr(char) == '\b':
               beg = self.Buffer.GetLastPosition()
               end = beg - 1
               self.Buffer.Remove(beg, end)
               if self.buffer_:self.buffer_.pop()
            else:
               self.buffer_.append(char)
               self.Buffer.AppendText(chr(char))
    
    def Connect(self,event):
        self.connect_btn.Enable(False)
        self.tn = serial.Serial(str(self.com_txt.GetValue()),  int(self.bound_txt.GetValue()), timeout=3)
        self.connect = 1
        self.Buffer.SetFocus()
        Console(self).start()
        self.disconnect_btn.Enable(True)
       
            
        
            
    def DisConnect(self,event):
        self.disconnect_btn.Enable(False)
        self.connect = 0
        self.tn.close()
        self.connect_btn.Enable(True)
        
        
        
    def __del__( self ):
        pass


class Console(threading.Thread):
      def __init__(self,parent):
          threading.Thread.__init__(self)
          self.parent = parent
          self.tn = self.parent.tn
      def run(self):
          #self.tn = serial.Serial(str(self.parent.com_txt.GetValue()),  int(self.parent.bound_txt.GetValue()), timeout=3)
          self.tn.writeTimeout=3
          while 1:
                if not self.parent.connect: break
                if 0x0A in self.parent.buffer_ or 0x0D in  self.parent.buffer_:
                   cmd = ''
                   for c in self.parent.buffer_: 
                       cmd += chr(c)                   
                   self.tn.write(cmd) 
                   self.parent.buffer_ = []
                data = ''
                while 1:
                    count = self.tn.inWaiting()
                    if (not count) or (len(data) > 200):
                        break
                    data += self.tn.read(count)
                if data: self.parent.Buffer.AppendText(data)                                 

def gui(Parent):
    MyFrame1(Parent).Show(True)
    
class App(wx.App):
    def OnInit(self):
        try:
            self.main = MyFrame1(None)
            self.main.Show(True)
            self.SetTopWindow(self.main)
        except Exception,e:
            print e
        return True

def main():
    application = App(0)
    application.MainLoop()

if __name__ == '__main__':
   main()

