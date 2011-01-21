import ConfigParser
import threading
import re

from Modules.Module import *
from ECGPanel import *
from CPlotter import *
from Lead12Panel import *
import  wx.lib.newevent

config = ConfigParser.ConfigParser()
config.read('rxbox.cfg')
if config.getboolean('ECG', 'simulated'):
    from ECGDAQSim import *
else:
    from ECGDAQLive import *

(ECGEvent, EVT_ECG) = wx.lib.newevent.NewEvent()
    
ECGLEADKEY = ['L', 'R', 'N', 'F', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6']

class Lead12Panel2(Lead12Panel):
    def __init__(self, *args, **kwds):
        Lead12Panel.__init__(self, *args, **kwds)
        self._frame = args[0]
        self._engine = self._frame._engine
        self._panel = self._frame._panel
        
        self.filter = True
    
    def Plot(self):
        self.data = self._frame._panel['ecg'].ECGData.ecg_lead
        plot1 = CPlotter(panel=self.plotter_I, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['I'][-1500:])
        plot1 = CPlotter(panel=self.plotter_II, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['II'][-1500:])
        plot1 = CPlotter(panel=self.plotter_III, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['III'][-1500:])
        plot1 = CPlotter(panel=self.plotter_aVR, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['VR'][-1500:])
        plot1 = CPlotter(panel=self.plotter_aVL, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['VL'][-1500:])
        plot1 = CPlotter(panel=self.plotter_aVF, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['VF'][-1500:])
        plot1 = CPlotter(panel=self.plotter_V1, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['V1'][-1500:])
        plot1 = CPlotter(panel=self.plotter_V2, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['V2'][-1500:])
        plot1 = CPlotter(panel=self.plotter_V3, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['V3'][-1500:])
        plot1 = CPlotter(panel=self.plotter_V4, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['V4'][-1500:])
        plot1 = CPlotter(panel=self.plotter_V5, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['V5'][-1500:])
        plot1 = CPlotter(panel=self.plotter_V6, mode='small', sample_time=3, plot_timelength=3, cont=False, filterOn=self.filter, data=self.data['V6'][-1500:])
        plot1 = CPlotter(panel=self.plotter_bigII, mode='extend', sample_time=15, plot_timelength=15, cont=False, filterOn=self.filter, data=self.data['II'][-7500:])
        
    def OnPaneClose(self):
        del self._panel['lead12']
        self._frame.setGui('unlock')
        

class ECG(Module, ECGPanel):
    def __init__(self, *args, **kwds):
        Module.__init__(self, *args, **kwds)
        ECGPanel.__init__(self, *args, **kwds)
        self.load_config()
            
        self.plotter = False
        self.alive = False
    
    def __name__(self):
        return 'ECG'

    def load_config(self):
        self.simulated = self._config.getboolean('ECG', 'simulated')
        self.ecmcheck = self._config.getint('ECG', 'ecmcheck')
        #self.ecmchecktimeout = self._config.getint('ECG', 'ecmchecktimeout')
        self.ecmchecktimeout = 15
        self.filter = self._config.getboolean('ECG', 'filter')
        
        self.port = self._config.get('ECG', 'port')
        if self.simulated:
            self.port = self._config.get('ECG', 'simfile')
        self.baud = self._config.getint('ECG', 'baud')
        self.timeout = self._config.getint('ECG', 'timeout')
        self.mode = self._config.get('ECG', 'mode')
        self.freq = self._config.getint('ECG', 'freq')
        self.daqdur = self._config.getfloat('ECG', 'daqdur')
        self.debug = self._config.getboolean('ECG', 'debug')

        self.ECGData = ECGDAQ(port=self.port, baud=self.baud, mode=self.mode, freq=self.freq, timeout=self.timeout, daqdur=self.daqdur, debug=self.debug, logger=self._logger)
        
    def lead12_button_clicked(self, event): # wxGlade: ECGPanel.<event_handler>
        self._logger.info('Lead 12 Button Clicked')
        self._frame.setGui('lock')
        self._panel['lead12'] = Lead12Panel2(self._frame, -1)
        self._frame._mgr.AddPane(self._panel['lead12'], wx.aui.AuiPaneInfo().
                          Caption("12 Lead ECG").Dockable(False).Name("lead12").
                          Float().FloatingPosition(wx.Point(25, 25)).DestroyOnClose(True).
                          FloatingSize(wx.Size(916, 710)).CloseButton(True).MaximizeButton(True))
        self._frame._mgr.Update()
        self._panel['lead12'].Plot()
        
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
        if self.status == 'start':
            [getattr(self, ('%s_bitmap') % i).SetBitmap(wx.Bitmap(("Icons/%s_%s.png") % (i, 'connected' if self.ECGData.ecm_stat[i] else 'unconnected'), wx.BITMAP_TYPE_ANY)) for i in ECGLEADKEY]

    def ecm_fail(self):
        dlg = wx.MessageDialog(self, 'ECM Failed! Would you life to proceed?', 'ECM Check', \
                            wx.YES_NO | wx.ICON_ERROR)
        responce = dlg.ShowModal()
        if responce == wx.ID_YES:
            self.alive = True
            self.getecgthread = threading.Thread(target=self.get_ecg_thread)
            self.getecgthread.start()
        
    def get_ecg_thread(self):
        self.plotter.Open()
        self.ECGData.config_analog()
        self.ECGData.start_ecg()
        ind = 0
        interval = int(-500*self.daqdur)
        get_ecg = self.ECGData.get_ecg
        leadII = self.ECGData.ecg_lead['II']
        pop = self.ECGData.Pop
        while self.alive:
            try:
                get_ecg()
                ind = self.plotter.Plot(leadII[interval:], xs=ind)
                minus = len(leadII) - 7500
                if minus > 0: pop(end=minus)
            except Exception, e:
                self._logger.error(ERROR('DAQ Error'))
                self.status = 'error'
                self.alive = False
                self.status = 'restart'

        self.plotter.Close()        
        self.ECGData.stop_ecg()
        self.ECGData.stop_ecg()
        self.ECGData.Close()

        if self.status == 'restart':
            self.status = 'start'
            self.alive = True
            self.plotter = CPlotter(panel=self.plot_panel, mode='normal', sample_time=self.daqdur, plot_timelength=3, cont=True, filterOn=self.filter, data=False)
            self.ECGData.Open()
            self.getecgthread = threading.Thread(target=self.get_ecg_thread)
            self.getecgthread.start()
            

    def get_ecm_thread(self):
        self._logger.info('ECM Start')
        self.ECGData.set_ecm_threshold()
        self.ECGData.start_ecm()
        count = 0
        Basetime = time.time() + self.ecmchecktimeout
        while self.alive and time.time() < Basetime and count < self.ecmcheck:
            if self.ECGData.get_ecm(): count += 1
            wx.CallAfter(self.ecm_update)
        self.ECGData.stop_ecm()
        if self.status != 'start':
            return False
        if count >= self.ecmcheck:
            self._logger.info('ECM Success!!!')
            self.getecgthread = threading.Thread(target=self.get_ecg_thread)
            self.getecgthread.start()
        else:
            self._logger.info('ECM Failed!!!')
            self.alive = False
            self.status = 'stop'
            wx.CallAfter(self.ecm_fail)
        
    def Start(self):
        try:
            self.ECGData.Open()
            self.plotter = CPlotter(panel=self.plot_panel, mode='normal', sample_time=self.daqdur, plot_timelength=3, cont=True, filterOn=self.filter, data=False)
            if self.ECGData.status:
                self.alive = True
                self.getecmthread = threading.Thread(target=self.get_ecm_thread)
                self.getecmthread.start()
                self._logger.info('DAQ Start')
                self.status = 'start'
                return True
        except Exception, e:
            self.status = 'error'
            self._logger.error(ERROR('DAQ Start Failed'))
            wx.PostEvent(self._frame, ECGEvent())
        return False
        
    def Stop(self):
        try:
            self.alive = False
            self.getecmthread.join(8)
            self.getecgthread.join(8)
            self.ECGData.flushout()
            self._logger.info('DAQ Stop')
            self.status = 'stop'
            return True
        except Exception, e:
            self.status = 'error'
            self._logger.error(ERROR('DAQ Stop Failed'))
            wx.PostEvent(self._frame, ECGEvent())
        return False

    def get_port(self):
        comm = subprocess.Popen("dmesg | grep ttyUSB", shell=True, stdout=subprocess.PIPE)
        port_list = ['/dev/ttyUSB'+i.split('ttyUSB')[-1].strip() for i in comm.stdout.read().strip().split('\n')]
        port_list_p = [100]*len(port_list)

        comm = subprocess.Popen("dmesg | grep ttyUSB %s"%self._config.get('ECG', 'dynamic'), shell=True, stdout=subprocess.PIPE)
        ecgport='/dev/ttyUSB'+comm.stdout.read().split('ttyUSB')[-1].strip()

        try:    
            port_list_p[port_list.index(ecgport)] += 100
            port_list_p[port_list.index(self._config.get('ECG', 'port'))] += 50
        except:
            pass
        port_list = zip(port_list_p,port_list)
        port_list.sort()
        port_list.reverse()
        for port in port_list:
            print port
            if self.ECGData.Check(port[1]):
                return port[1]
        return ''

    def setGui(self, mode='unlock'):
        if mode not in ['lock','unlock']:
            self._logger.info('setGui mode unsupported')
            return
            
        modeb = (mode == 'unlock')
        self.lead12_button.Enable(modeb)

    def OnPaneClose(self):
        pass
