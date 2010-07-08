from Lead12Frame import *
from Modules.ECG import CPlotter

class Lead12Frame2(Lead12Frame):
    def __init__(self, engine, *args, **kwds):
        Lead12Frame.__init__(self, *args, **kwds)
        self._engine = engine
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
    def OnExit(self, event):
        self._engine.change_state('MainState')
        
class Lead12State:
    def __init__(self, engine):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        
        self.filter = self._config.getboolean('ECG','filter')
        
        self._frame = Lead12Frame2(engine, None, -1, "")
        self._panel = self._engine.mainstate._panel
        self.data = self._panel['ecg'].ECGData.ecg_lead
        self.frameOn = False
        
    def start(self):
        print 'State Machine: Lead12State Start'
        self._frame.Maximize(True)
        self._frame.Show()
        self._frameOn = True
        
        plot1 = CPlotter(panel=self._frame.plotter_I,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['I'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_II,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['II'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_III,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['III'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_aVR,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['VR'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_aVL,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['VL'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_aVF,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['VF'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_V1,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['V1'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_V2,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['V2'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_V3,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['V3'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_V4,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['V4'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_V5,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['V5'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_V6,mode='small',sample_time=3,plot_timelength=3,cont=False,filterOn=self.filter,data=self.data['V6'][-1500:])
        plot1 = CPlotter(panel=self._frame.plotter_bigII,mode='extend',sample_time=15,plot_timelength=15,cont=False,filterOn=self.filter,data=self.data['II'][-7500:])
        
    def stop(self):
        print 'State Machine: Lead12State Stop'
        self._frame.Destroy()
        self.frameOn = False