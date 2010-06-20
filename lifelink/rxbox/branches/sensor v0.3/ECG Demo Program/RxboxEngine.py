import wx
from wx import xrc
import ECG
import threading
import time
import copy
import math
import random
from lead12dialog import Lead12Dialog
from CPlotter import *
import subprocess,os
DURATION = 1

class MainState:
    def __init__(self,engine):
        self._engine = engine
        self._app = self._engine.app
        self.frameOn = False
    
    def start(self):
        """Start state"""
        self._app.frame = self._app.resMain.LoadFrame(None, 'ECGFrame')
        self._app.frame.Show()
        
        self.plotgraph_panel = xrc.XRCCTRL(self._app.frame, 'plotgraph_panel')
        self.plotter = CPlotter(self,panel=self.plotgraph_panel,mode='normal',cont=True,time=1)
        self.frameOn = True
        
        self._app.Bind(wx.EVT_BUTTON, self.PlayButtonPressed, id=xrc.XRCID('play_button'))
        self._app.Bind(wx.EVT_BUTTON, self.Lead12ButtonPressed, id=xrc.XRCID('lead12_button'))
        
        self.play =  False

        self.ind = 0
        self.ECGData = ECG.ECG(panel=self,port='/dev/ttyUSB0',daqdur=DURATION,ecmcheck=0,debug=True)
        self.ECGData.device_ready()
        self.ECGData.stop()
        self._app.frame.Bind(wx.EVT_CLOSE, self.onClose)
        
    def stop(self):
        if self.frameOn:
            self._app.frame.Destroy()
        print 'stop'

    def onClose(self, evt):
        self.plotter.Close()
        self.ECGData.stop()
        self.stop()
        
    def PlayButtonPressed(self, evt):
        if not self.play:
            #if off, turn on
            print 'Play'
            self.play = True
            self.alive = True
            self.ECGData = ECG.ECG(panel=self,port='/dev/ttyUSB0',daqdur=DURATION,ecmcheck=0,debug=True)
            self.ind=0
            self.plotter.Open()
#            self.plotter.Calibrate()
            self.get_thread = threading.Thread(target=self.Get_ECG)
            self.get_thread.start()
        else:
            #if on, turn off
            print 'Stop'
            self.alive = False
            self.play = False
            time.sleep(1)
            self.plotter.Close()
            self.ECGData.stop()
            self.ind = 0;

    def Get_ECG(self):
        self.ind = 0
        past = 0
        while self.alive:
            past = len(self.ECGData.lead_ecg['II'])
            self.ECGData.patient_ready()
            print len(self.ECGData.lead_ecg['II'])-past
            self.ind = self.plotter.Plot(self.ECGData.lead_ecg['II'][past:],xs=self.ind)
            if len(self.ECGData.lead_ecg['II']) > 7500:
                minus = len(self.ECGData.lead_ecg['II']) - 7500
                self.ECGData.pop(end=len(self.ECGData.lead_ecg['II'][0:minus]))
        print 'Stop'
        
    def Lead12ButtonPressed(self,evt):
        CreateDialog2 = Lead12Dialog2(self._app.frame, False, False, self._app.frame)
        CreateDialog2.Show()
        self.plotter.Close()
#        self.ECGData.stop()
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_I,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['I'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_II,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['II'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_III,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['III'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_aVR,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['VR'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_aVL,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['VL'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_aVF,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['VF'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V1,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['V1'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V2,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['V2'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V3,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['V3'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V4,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['V4'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V5,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['V5'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V6,mode='small',time=3,tlen=3,cont=False,data=self.ECGData.lead_ecg['V6'][-1500:])
        plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_bigII,mode='extend',time=15,tlen=15,cont=False,data=self.ECGData.lead_ecg['II'][-7500:])
        
        self.plotter = CPlotter(self,panel=self.plotgraph_panel,mode='normal',cont=True,time=3)
        self.plotter.Open()
        """
        self.ECGData = ECG.ECG(panel=self,port='/dev/ttyUSB0',daqdur=DURATION,ecmcheck=0,debug=True)
        self.alive = True
        self.get_thread = threading.Thread(target=self.Get_ECG)
        self.get_thread.start()
        """

class Lead12Dialog2(Lead12Dialog):
    """ Class that creates the 12 Lead Dialog Window where the 12 leads will be plotted
    
    Methods:
        __init__(Lead12Dialog)         
         
    """   
    def __init__(self, parent, ECGSimulated, ECGData, *args, **kwds):
        """ initializes the placement of the plotter to the 12 lead dialog window

        Parameters
        ----------
        parent  :  the main window which calls the creation of the dialog window

        """
        Lead12Dialog.__init__(self, *args, **kwds)
        self.parent = parent
        parent = self
        sizersize = self.leadI_sizer.GetSize()
        bigsizer = self.leadII_sizer.GetSize()
        
        self.plotter_I = wx.Panel(parent)
        self.plotter_II = wx.Panel(parent)
        self.plotter_III = wx.Panel(parent)
        self.plotter_aVR = wx.Panel(parent)
        self.plotter_aVL = wx.Panel(parent)
        self.plotter_aVF = wx.Panel(parent)
        self.plotter_V1 = wx.Panel(parent)
        self.plotter_V2 = wx.Panel(parent)
        self.plotter_V3 = wx.Panel(parent)
        self.plotter_V4 = wx.Panel(parent)
        self.plotter_V5 = wx.Panel(parent)
        self.plotter_V6 = wx.Panel(parent)
        self.plotter_bigII = wx.Panel(parent)
        
        self.leadI_sizer.Add(self.plotter_I, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.small_leadII_sizer.Add(self.plotter_II, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.leadIII_sizer.Add(self.plotter_III, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.aVR_sizer.Add(self.plotter_aVR, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.aVL_sizer.Add(self.plotter_aVL, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.aVF_sizer.Add(self.plotter_aVF, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V1_sizer.Add(self.plotter_V1, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V2_sizer.Add(self.plotter_V2, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V3_sizer.Add(self.plotter_V3, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V4_sizer.Add(self.plotter_V4, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V5_sizer.Add(self.plotter_V5, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V6_sizer.Add(self.plotter_V6, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        
        self.leadII_sizer.Add(self.plotter_bigII, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
                
class RxboxEngine:
    """Engine/Controller class for Rxbox"""
    def run(self):
        """Run engine and start up GUI"""
        self.app = RxboxApp(False)
        self.state = MainState(self)
        self.change_state(self.state)
        self.app.MainLoop()
        
    def change_state(self, state):
        """Change state to state"""
        if self.state is not None:
            self.state.stop()
        self.state = state
        if self.state is None:
            self.app.Exit()
        else:
            self.state.start()
            
class RxboxApp(wx.App):
    """wxPython app for Rxbox"""
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        self.resMain = xrc.XmlResource('RxboxECG.xrc')
        
if __name__ == '__main__':
    engine = RxboxEngine()
    engine.run()
