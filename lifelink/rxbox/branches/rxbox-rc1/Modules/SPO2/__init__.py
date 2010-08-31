
from SPO2Panel import *
import wx
import time
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('rxbox.cfg')
if config.getboolean('SPO2', 'simulated'):
    from SPO2DAQSim import *
else:
    from SPO2DAQLive import *

import threading

class SPO2 (SPO2Panel):
    def __init__(self, *args, **kwds):
        SPO2Panel.__init__(self, *args, **kwds)
        
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        
    def Start(self):
        print 'SPO2Panel START'
        self.spo2data=SPO2DAQ(self, port =config.get('SPO2','port'))
        self.spo2_get_thread = threading.Thread(target=self.get_spo2)
        self.spo2_thread_alive=True
        self.spo2_get_thread.start()
        return True
 
            

    def Stop(self):
        print 'SPO2Panel STOP'
        self.spo2_thread_alive=False
        return True

    def get_spo2(self):
        while self.spo2_thread_alive:
            self.spo2data.get()
            self.blood_oxy=self.spo2data.current_spo2
            self.heart_rate=self.spo2data.current_bpm
            wx.CallAfter(self.update_label)
            time.sleep(0.1)

    def update_label(self):
        self.spo2value_label.SetLabel(str(self.blood_oxy))
        self.bpmvalue_label.SetLabel(str(self.heart_rate))
        
    def setGui(self, mode='unlock'):
        if mode == 'lock':
            print 'SPO2 Panel lock'
        elif mode == 'unlock':
            print 'SPO2 Panel unlock'
        else:
            print 'mode unsupported'
