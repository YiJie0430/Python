# -*- coding: utf-8 -*-

import wx

import numpy as np

import matplotlib

# matplotlibノWXAgg?,?matplotlib碠wxPythonい
matplotlib.use("WXAgg")

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter

import pylab
from matplotlib import pyplot




######################################################################################
class MPL_Panel_base(wx.Panel):
    ''' #MPL_Panel_base狾,?┯┪??ㄒ'''
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent, id=-1)

        self.Figure = matplotlib.figure.Figure(figsize=(-1,-1))        
        self.axes = self.Figure.add_axes([0.1,0.1,0.8,0.8])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        
        #self.NavigationToolbar = NavigationToolbar(self.FigureCanvas)

        #self.StaticText = wx.StaticText(self,-1,label='Show Help String')

        #self.SubBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.SubBoxSizer.Add(self.NavigationToolbar,proportion = 0, border = 0,flag = wx.ALL | wx.EXPAND)
        #self.SubBoxSizer.Add(self.StaticText,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)

        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        #self.TopBoxSizer.Add(self.SubBoxSizer,proportion = 0, border = 0,flag = wx.ALL | wx.EXPAND)
        self.TopBoxSizer.Add(self.FigureCanvas,proportion = 100, border = 0,flag = wx.ALL | wx.EXPAND)

        self.SetSizer(self.TopBoxSizer)

        ###よ獽?ノ
        self.pylab=pylab
        self.pl=pylab
        self.pyplot=pyplot
        self.numpy=np
        self.np=np
        self.plt=pyplot

    def UpdatePlot(self):
        '''#э?ヴ?┦常ゲ?ㄏノself.UpdatePlot()穝GUI '''
        self.FigureCanvas.draw()


    def plot(self,*args,**kwargs):
        '''#程盽ノ??㏑plot '''
        self.axes.plot(*args,**kwargs)
        self.UpdatePlot()


    def semilogx(self,*args,**kwargs):
        ''' #??Г???㏑ '''
        self.axes.semilogx(*args,**kwargs)
        self.UpdatePlot()

    def semilogy(self,*args,**kwargs):
        ''' #??Г???㏑ '''
        self.axes.semilogy(*args,**kwargs)
        self.UpdatePlot()

    def loglog(self,*args,**kwargs):
        ''' #??Г???㏑ '''
        self.axes.loglog(*args,**kwargs)
        self.UpdatePlot()


    def grid(self,flag=True):
        ''' ##?ボ蔍  '''
        if flag:
            self.axes.grid()
        else:
            self.axes.grid(False)


    def title_MPL(self,TitleString="wxMatPlotLib Example In wxPython"):
        ''' # ??钩睰???   '''
        self.axes.set_title(TitleString)


    def xlabel(self,XabelString="X"):
        ''' # Add xlabel to the plotting    '''
        self.axes.set_xlabel(XabelString)


    def ylabel(self,YabelString="Y"):
        ''' # Add ylabel to the plotting '''
        self.axes.set_ylabel(YabelString)


    def xticker(self,major_ticker=1.0,minor_ticker=0.1):
        ''' # ?竚X?ㄨ '''
        self.axes.xaxis.set_major_locator( MultipleLocator(major_ticker) )
        self.axes.xaxis.set_minor_locator( MultipleLocator(minor_ticker) )


    def yticker(self,major_ticker=1.0,minor_ticker=0.1):
        ''' # ?竚Y?ㄨ '''
        self.axes.yaxis.set_major_locator( MultipleLocator(major_ticker) )
        self.axes.yaxis.set_minor_locator( MultipleLocator(minor_ticker) )


    def legend(self,*args,**kwargs):
        ''' #?ㄒlegend for the plotting  '''
        self.axes.legend(*args,**kwargs)


    def xlim(self,x_min,x_max):
        ''' # ?竚x??ボ璖?  '''
        self.axes.set_xlim(x_min,x_max)


    def ylim(self,y_min,y_max):
        ''' # ?竚y??ボ璖?   '''
        self.axes.set_ylim(y_min,y_max)


    def savefig(self,*args,**kwargs):
        ''' #玂?ゅン '''
        self.Figure.savefig(*args,**kwargs)


    def cla(self):
        ''' # Ω??玡,ゲ??ノ?㏑睲??  '''
        self.axes.clear()
        self.Figure.set_canvas(self.FigureCanvas)
        self.UpdatePlot()
        
    def ShowHelpString(self,HelpString="Show Help String"):
        ''' #ノウ??ボㄇ?獺,公?竚单 '''
        self.StaticText.SetLabel(HelpString)

################################################################

class MPL_Panel(MPL_Panel_base):
    ''' #MPL_Panel璶狾,?┯┪??ㄒ '''
    def __init__(self,parent):
        MPL_Panel_base.__init__(self,parent=parent)

        #??
        self.FirstPlot()


    #??ノ??㎝﹍て,種?ぃ
    def FirstPlot(self):
        #self.rc('lines',lw=5,c='r')
        self.cla()
        x = np.arange(-5,5,0.25)
        y = np.sin(x)
        self.yticker(1.0,0.1)
        self.xticker(1.0,0.1)
        self.xlabel('X')
        self.ylabel('Y')
        self.title_MPL("wxMatPlotLib Example In wxPython")
        self.grid()
        self.plot(x,y,'--^g')


###############################################################################
#  MPL_Frame睰MPL_Panel1??ㄒ
###############################################################################
class MPL_Frame(wx.Frame):
    """MPL_Frame?┯,э,┪钡ㄏノ"""
    def __init__(self,title="MPL_Frame Example In wxPython",size=(-1,-1)):
        wx.Frame.__init__(self,parent=None,title = title,size=size)

        self.MPL = MPL_Panel_base(self)

        #?FlexGridSizer
        self.FlexGridSizer=wx.FlexGridSizer( rows=9, cols=1, vgap=5,hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)

        self.RightPanel = wx.Panel(self,-1)

        #???1
        self.Button1 = wx.Button(self.RightPanel,-1,"TestButton",size=(100,40),pos=(10,10))
        self.Button1.Bind(wx.EVT_BUTTON,self.Button1Event)

        #???2
        self.Button2 = wx.Button(self.RightPanel,-1,"AboutButton",size=(100,40),pos=(10,10))
        self.Button2.Bind(wx.EVT_BUTTON,self.Button2Event)

        #Sizerい
        self.FlexGridSizer.Add(self.Button1,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button2,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)

        self.RightPanel.SetSizer(self.FlexGridSizer)
        
        self.BoxSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.BoxSizer.Add(self.MPL,proportion =-10, border = 0,flag = wx.ALL | wx.EXPAND)
        self.BoxSizer.Add(self.RightPanel,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)
        
        self.SetSizer(self.BoxSizer)	

        #???
        self.StatusBar()

        #MPL_Frame﹡い?ボ
        self.Centre(wx.BOTH)



    #?ㄆン,ノ??
    def Button1Event(self,event):
        self.MPL.cla()#ゲ?睲瞶?,?ボ碩?
        x=np.arange(-10,10,0.25)
        y=np.cos(x)
        self.MPL.plot(x,y,'--*g')
        self.MPL.xticker(2.0,0.5)
        self.MPL.yticker(0.5,0.1)
        self.MPL.title_MPL("MPL1")
        self.MPL.ShowHelpString("You Can Show MPL Helpful String Here !")
        self.MPL.grid() 
        self.MPL.UpdatePlot()#ゲ?穝?ボ

    def Button2Event(self,event):
        self.AboutDialog()


    #ゴ?ゅン,ノ??
    def DoOpenFile(self):
        wildcard = r"Data files (*.dat)|*.dat|Text files (*.txt)|*.txt|ALL Files (*.*)|*.*"
        open_dlg = wx.FileDialog(self,message='Choose a file',wildcard = wildcard, style=wx.OPEN|wx.CHANGE_DIR)
        if open_dlg.ShowModal() == wx.ID_OK:
            path=open_dlg.GetPath()
            try:
                file = open(path, 'r')
                text = file.read()
                file.close()
            except IOError, error:
                dlg = wx.MessageDialog(self, 'Error opening file\n' + str(error))
                dlg.ShowModal()

        open_dlg.Destroy()



    #?????
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -2, -1])


    #About??
    def AboutDialog(self):
        dlg = wx.MessageDialog(self, '\twxMatPlotLib\t\nMPL_Panel_base,MPL_Panel,MPL_Frame and MPL2_Frame \n Created by Wu Xuping\n Version 1.0.0 \n 2012-02-01',
                                'About MPL_Frame and MPL_Panel', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

###############################################################################
###  MPL2_Frame睰MPL_Panel???ㄒ
###############################################################################
class MPL2_Frame(wx.Frame):
    """MPL2_Frame?┯,э,┪钡ㄏノ"""
    def __init__(self,title="MPL2_Frame Example In wxPython",size=(-1,-1)):
        wx.Frame.__init__(self,parent=None,title = title,size=size)

        self.BoxSizer=wx.BoxSizer(wx.HORIZONTAL)

        self.MPL1 = MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL1,proportion =-1, border = 0,flag = wx.ALL | wx.EXPAND)

        self.MPL2 = MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL2,proportion =-1, border = 0,flag = wx.ALL | wx.EXPAND)

        self.RightPanel = wx.Panel(self,-1)
        self.BoxSizer.Add(self.RightPanel,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)

        self.SetSizer(self.BoxSizer)

        #?FlexGridSizer
        self.FlexGridSizer=wx.FlexGridSizer( rows=9, cols=1, vgap=5,hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)

        #???1
        self.Button1 = wx.Button(self.RightPanel,-1,"TestButton",size=(100,40),pos=(10,10))
        self.Button1.Bind(wx.EVT_BUTTON,self.Button1Event)

        #???2
        self.Button2 = wx.Button(self.RightPanel,-1,"AboutButton",size=(100,40),pos=(10,10))
        self.Button2.Bind(wx.EVT_BUTTON,self.Button2Event)

        #Sizerい
        self.FlexGridSizer.Add(self.Button1,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button2,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)

        self.RightPanel.SetSizer(self.FlexGridSizer)

        #???
        self.StatusBar()


        #MPL2_Frame﹡い?ボ
        self.Centre(wx.BOTH)



    #?ㄆン,ノ??
    def Button1Event(self,event):
        self.MPL1.cla()#ゲ?睲瞶?,?ボ碩?
        x=np.arange(-5,5,0.2)
        y=np.cos(x)
        self.MPL1.plot(x,y,'--*g')
        self.MPL1.xticker(2.0,1.0)
        self.MPL1.yticker(0.5,0.1)
        self.MPL1.title_MPL("MPL1")
        self.MPL1.ShowHelpString("You Can Show MPL1 Helpful String Here !")
        self.MPL1.grid()
        self.MPL1.UpdatePlot()#ゲ?穝?ボ

        self.MPL2.cla()
        self.MPL2.plot(x,np.sin(x),':^b')
        self.MPL2.xticker(1.0,0.5)
        self.MPL2.yticker(0.2,0.1)
        self.MPL2.title_MPL("MPL2")
        self.MPL2.grid()
        self.MPL2.UpdatePlot()

    def Button2Event(self,event):
        self.AboutDialog()



    #?????
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -2, -1])


    #About??
    def AboutDialog(self):
        dlg = wx.MessageDialog(self, '\twxMatPlotLib\t\nMPL_Panel_base,MPL_Panel,MPL_Frame and MPL2_Frame \n Created by Wu Xuping\n Version 1.0.0 \n 2012-02-01',
                                'About MPL_Frame and MPL_Panel', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()




########################################################################

#祘??
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MPL2_Frame()
    #frame =MPL_Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()
