# -*- coding: utf-8 -*-

import wx

import numpy as np

import matplotlib

# matplotlib采用WXAgg?后台,?matplotlib嵌入wxPython中
matplotlib.use("WXAgg")

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter

import pylab
from matplotlib import pyplot




######################################################################################
class MPL_Panel_base(wx.Panel):
    ''' #MPL_Panel_base面板,可以?承或者?建?例'''
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

        ###方便?用
        self.pylab=pylab
        self.pl=pylab
        self.pyplot=pyplot
        self.numpy=np
        self.np=np
        self.plt=pyplot

    def UpdatePlot(self):
        '''#修改?形的任何?性后都必?使用self.UpdatePlot()更新GUI界面 '''
        self.FigureCanvas.draw()


    def plot(self,*args,**kwargs):
        '''#最常用的??命令plot '''
        self.axes.plot(*args,**kwargs)
        self.UpdatePlot()


    def semilogx(self,*args,**kwargs):
        ''' #??坐???命令 '''
        self.axes.semilogx(*args,**kwargs)
        self.UpdatePlot()

    def semilogy(self,*args,**kwargs):
        ''' #??坐???命令 '''
        self.axes.semilogy(*args,**kwargs)
        self.UpdatePlot()

    def loglog(self,*args,**kwargs):
        ''' #??坐???命令 '''
        self.axes.loglog(*args,**kwargs)
        self.UpdatePlot()


    def grid(self,flag=True):
        ''' ##?示网格  '''
        if flag:
            self.axes.grid()
        else:
            self.axes.grid(False)


    def title_MPL(self,TitleString="wxMatPlotLib Example In wxPython"):
        ''' # ??像添加一???   '''
        self.axes.set_title(TitleString)


    def xlabel(self,XabelString="X"):
        ''' # Add xlabel to the plotting    '''
        self.axes.set_xlabel(XabelString)


    def ylabel(self,YabelString="Y"):
        ''' # Add ylabel to the plotting '''
        self.axes.set_ylabel(YabelString)


    def xticker(self,major_ticker=1.0,minor_ticker=0.1):
        ''' # ?置X?的刻度大小 '''
        self.axes.xaxis.set_major_locator( MultipleLocator(major_ticker) )
        self.axes.xaxis.set_minor_locator( MultipleLocator(minor_ticker) )


    def yticker(self,major_ticker=1.0,minor_ticker=0.1):
        ''' # ?置Y?的刻度大小 '''
        self.axes.yaxis.set_major_locator( MultipleLocator(major_ticker) )
        self.axes.yaxis.set_minor_locator( MultipleLocator(minor_ticker) )


    def legend(self,*args,**kwargs):
        ''' #?例legend for the plotting  '''
        self.axes.legend(*args,**kwargs)


    def xlim(self,x_min,x_max):
        ''' # ?置x?的?示范?  '''
        self.axes.set_xlim(x_min,x_max)


    def ylim(self,y_min,y_max):
        ''' # ?置y?的?示范?   '''
        self.axes.set_ylim(y_min,y_max)


    def savefig(self,*args,**kwargs):
        ''' #保存?形到文件 '''
        self.Figure.savefig(*args,**kwargs)


    def cla(self):
        ''' # 再次??前,必??用?命令清空原?的?形  '''
        self.axes.clear()
        self.Figure.set_canvas(self.FigureCanvas)
        self.UpdatePlot()
        
    def ShowHelpString(self,HelpString="Show Help String"):
        ''' #可以用它??示一些?助信息,如鼠?位置等 '''
        self.StaticText.SetLabel(HelpString)

################################################################

class MPL_Panel(MPL_Panel_base):
    ''' #MPL_Panel重要面板,可以?承或者?建?例 '''
    def __init__(self,parent):
        MPL_Panel_base.__init__(self,parent=parent)

        #??一下
        self.FirstPlot()


    #??用于??和初始化,意?不大
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
#  MPL_Frame添加了MPL_Panel的1??例
###############################################################################
class MPL_Frame(wx.Frame):
    """MPL_Frame可以?承,并可修改,或者直接使用"""
    def __init__(self,title="MPL_Frame Example In wxPython",size=(-1,-1)):
        wx.Frame.__init__(self,parent=None,title = title,size=size)

        self.MPL = MPL_Panel_base(self)

        #?建FlexGridSizer
        self.FlexGridSizer=wx.FlexGridSizer( rows=9, cols=1, vgap=5,hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)

        self.RightPanel = wx.Panel(self,-1)

        #??按?1
        self.Button1 = wx.Button(self.RightPanel,-1,"TestButton",size=(100,40),pos=(10,10))
        self.Button1.Bind(wx.EVT_BUTTON,self.Button1Event)

        #??按?2
        self.Button2 = wx.Button(self.RightPanel,-1,"AboutButton",size=(100,40),pos=(10,10))
        self.Button2.Bind(wx.EVT_BUTTON,self.Button2Event)

        #加入Sizer中
        self.FlexGridSizer.Add(self.Button1,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button2,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)

        self.RightPanel.SetSizer(self.FlexGridSizer)
        
        self.BoxSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.BoxSizer.Add(self.MPL,proportion =-10, border = 0,flag = wx.ALL | wx.EXPAND)
        self.BoxSizer.Add(self.RightPanel,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)
        
        self.SetSizer(self.BoxSizer)	

        #???
        self.StatusBar()

        #MPL_Frame界面居中?示
        self.Centre(wx.BOTH)



    #按?事件,用于??
    def Button1Event(self,event):
        self.MPL.cla()#必?清理?形,才能?示下一幅?
        x=np.arange(-10,10,0.25)
        y=np.cos(x)
        self.MPL.plot(x,y,'--*g')
        self.MPL.xticker(2.0,0.5)
        self.MPL.yticker(0.5,0.1)
        self.MPL.title_MPL("MPL1")
        self.MPL.ShowHelpString("You Can Show MPL Helpful String Here !")
        self.MPL.grid() 
        self.MPL.UpdatePlot()#必?刷新才能?示

    def Button2Event(self,event):
        self.AboutDialog()


    #打?文件,用于??
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



    #自??建???
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -2, -1])


    #About??框
    def AboutDialog(self):
        dlg = wx.MessageDialog(self, '\twxMatPlotLib\t\nMPL_Panel_base,MPL_Panel,MPL_Frame and MPL2_Frame \n Created by Wu Xuping\n Version 1.0.0 \n 2012-02-01',
                                'About MPL_Frame and MPL_Panel', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

###############################################################################
###  MPL2_Frame添加了MPL_Panel的???例
###############################################################################
class MPL2_Frame(wx.Frame):
    """MPL2_Frame可以?承,并可修改,或者直接使用"""
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

        #?建FlexGridSizer
        self.FlexGridSizer=wx.FlexGridSizer( rows=9, cols=1, vgap=5,hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)

        #??按?1
        self.Button1 = wx.Button(self.RightPanel,-1,"TestButton",size=(100,40),pos=(10,10))
        self.Button1.Bind(wx.EVT_BUTTON,self.Button1Event)

        #??按?2
        self.Button2 = wx.Button(self.RightPanel,-1,"AboutButton",size=(100,40),pos=(10,10))
        self.Button2.Bind(wx.EVT_BUTTON,self.Button2Event)

        #加入Sizer中
        self.FlexGridSizer.Add(self.Button1,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button2,proportion =0, border = 0,flag = wx.ALL | wx.EXPAND)

        self.RightPanel.SetSizer(self.FlexGridSizer)

        #???
        self.StatusBar()


        #MPL2_Frame界面居中?示
        self.Centre(wx.BOTH)



    #按?事件,用于??
    def Button1Event(self,event):
        self.MPL1.cla()#必?清理?形,才能?示下一幅?
        x=np.arange(-5,5,0.2)
        y=np.cos(x)
        self.MPL1.plot(x,y,'--*g')
        self.MPL1.xticker(2.0,1.0)
        self.MPL1.yticker(0.5,0.1)
        self.MPL1.title_MPL("MPL1")
        self.MPL1.ShowHelpString("You Can Show MPL1 Helpful String Here !")
        self.MPL1.grid()
        self.MPL1.UpdatePlot()#必?刷新才能?示

        self.MPL2.cla()
        self.MPL2.plot(x,np.sin(x),':^b')
        self.MPL2.xticker(1.0,0.5)
        self.MPL2.yticker(0.2,0.1)
        self.MPL2.title_MPL("MPL2")
        self.MPL2.grid()
        self.MPL2.UpdatePlot()

    def Button2Event(self,event):
        self.AboutDialog()



    #自??建???
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -2, -1])


    #About??框
    def AboutDialog(self):
        dlg = wx.MessageDialog(self, '\twxMatPlotLib\t\nMPL_Panel_base,MPL_Panel,MPL_Frame and MPL2_Frame \n Created by Wu Xuping\n Version 1.0.0 \n 2012-02-01',
                                'About MPL_Frame and MPL_Panel', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()




########################################################################

#主程序??
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MPL2_Frame()
    #frame =MPL_Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()
