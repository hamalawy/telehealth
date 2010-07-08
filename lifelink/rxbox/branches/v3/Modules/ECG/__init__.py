import ConfigParser
import threading

from ECGPanel import *
from CPlotter import *

config = ConfigParser.ConfigParser()
config.read('rxbox.cfg')
if config.getboolean('ECG', 'simulated'):
    from ECGDAQSim import *
else:
    from ECGDAQLive import *
    
ECGLEADKEY = ['L', 'R', 'N', 'F', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']

class ECG(ECGPanel):
    def __init__(self, *args, **kwds):
        ECGPanel.__init__(self, *args, **kwds)
        
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        self.rxboxDB = self._engine.rxboxDB
        self.dbuuid = self._engine.dbuuid
        
        self.simulated = self._config.getboolean('ECG', 'simulated')
        self.ecmcheck = self._config.getint('ECG', 'ecmcheck')
        self.filter = self._config.getboolean('ECG', 'filter')
        
        self.port = self._config.get('ECG', 'port')
        if self.simulated:
            self.port = self._config.get('ECG', 'simfile')
        self.baud = self._config.getint('ECG', 'baud')
        self.timeout = self._config.getint('ECG', 'timeout')
        self.mode = self._config.get('ECG', 'mode')
        self.freq = self._config.getint('ECG', 'freq')
        self.daqdur = self._config.getint('ECG', 'daqdur')
        self.debug = self._config.getboolean('ECG', 'debug')
            
        self.ECGData = False
        self.plotter = False
        self.alive = False
        
        self.SetStatusText = self._frame.RxboxFrame_statusbar.SetStatusText
    
    def lead12_button_clicked(self, event): # wxGlade: ECGPanel.<event_handler>
        self._engine.change_state('Lead12State')
        
    def ecm_statreset(self):
        [getattr(self, ('%s_bitmap') % i).SetBitmap(wx.Bitmap(("Icons/%s_initial.png") % i, wx.BITMAP_TYPE_ANY)) for i in ECGLEADKEY]
        """
        self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_initial.png", wx.BITMAP_TYPE_ANY))
        self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_initial.png", wx.BITMAP_TYPE_ANY))
        self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_initial.png", wx.BITMAP_TYPE_ANY))
        self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_initial.png", wx.BITMAP_TYPE_ANY))
        self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
        self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_initial.png", wx.BITMAP_TYPE_ANY))
        self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
        self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_initial.png", wx.BITMAP_TYPE_ANY))
        self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_initial.png", wx.BITMAP_TYPE_ANY))
        """
    
    def ecm_update(self):
        [getattr(self, ('%s_bitmap') % i).SetBitmap(wx.Bitmap(("Icons/%s_%s.png") % (i, 'connected' if self.ECGData.ecm_stat[i] else 'unconnected'), wx.BITMAP_TYPE_ANY)) for i in ECGLEADKEY]
        
    def get_ecg_thread(self):
        self.plotter.Open()
        self.ECGData.config_analog()
        self.ECGData.start_ecg()
        ind = 0
        get_ecg = self.ECGData.get_ecg
        leadII = self.ECGData.ecg_lead['II']
        pop = self.ECGData.Pop
        while self.alive:
            try:
                get_ecg()
                ind = self.plotter.Plot(leadII[-500:], xs=ind)
                minus = len(leadII) - 7500
                if minus > 0: pop(end=minus)
            except Exception, e:
                print 'ECG Error: ', e
                self.ECGData.Close()
                self.ECGData = ECGDAQ(port=self.port, baud=self.baud, mode=self.mode, freq=self.freq, timeout=self.timeout, daqdur=self.daqdur, debug=self.debug)
                
        self.plotter.Close()
        self.ECGData.stop_ecg()
        self.ECGData.Close()

    def get_ecm_thread(self):
        self.ECGData.set_ecm_threshold()
        self.ECGData.start_ecm()
        count = 0
        Basetime = time.time() + 15
        while time.time() < Basetime and count < self.ecmcheck:
            if self.ECGData.get_ecm(): count += 1
            wx.CallAfter(self.ecm_update)
        self.ECGData.stop_ecm()
        if count >= self.ecmcheck:
            print 'ECG Count', count, self.ecmcheck
            self.alive = True
            self.getecgthread = threading.Thread(target=self.get_ecg_thread)
            self.getecgthread.start()
        
    def Start(self):
        self.ECGData = ECGDAQ(port=self.port, baud=self.baud, mode=self.mode, freq=self.freq, timeout=self.timeout, daqdur=self.daqdur, debug=self.debug)
        self.plotter = CPlotter(panel=self.plot_panel, mode='normal', sample_time=self.daqdur, plot_timelength=3, cont=True, filterOn=self.filter, data=False)
        if self.ECGData.status:
            self.getecmthread = threading.Thread(target=self.get_ecm_thread)
            self.getecmthread.start()
            return True
        return False
        
    def Stop(self):
        self.alive = False
        self.ECGData.abort_ecg()
        
    def setGui(self, mode='unlock'):
        if mode == 'lock':
            pass
        elif mode == 'unlock':
            pass
        else:
            print 'mode unsupported'
        modeb = mode == 'unlock'
        self.lead12_button.Enable(modeb)
