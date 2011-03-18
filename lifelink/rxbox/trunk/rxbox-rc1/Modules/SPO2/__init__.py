import wx
import time
import threading
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('rxbox.cfg')
if config.getboolean('SPO2', 'simulated'):
    from SPO2DAQSim import *
else:
    from SPO2DAQLive import *

from SPO2Panel import *
from Modules.Module import *
import spo2_portcheck

class SPO2 (Module, SPO2Panel):
    def __init__(self, *args, **kwds):
        Module.__init__(self, *args, **kwds)
        SPO2Panel.__init__(self, *args, **kwds)
        config.read('rxbox.cfg')

    def __name__(self):
        return 'SPO2'
                
    def Start(self):
        port2check=[config.get('SPO2','port')]
        c=spo2_portcheck.Spo2_check(port2check)
        port=c.check()
        if port == None:
            self.heartrate_infolabel.SetLabel('HeartRate Unavailable:Check Connections')
            self.spo2_infolabel.SetLabel(' % Oxygen Unavailable:Check Connections')
            return
        self.heartrate_infolabel.SetLabel('Ready')
        self.spo2_infolabel.SetLabel('      Ready')
        config.read('rxbox.cfg')
        self.spo2data=SPO2DAQ(self, port =config.get('SPO2','port'),debug=True,logger=self._logger)
        self.spo2_get_thread = threading.Thread(target=self.get_spo2)
        self.spo2_thread_alive=True
        self.spo2_get_thread.start()
        self._logger.info('DAQ Start')
        return True
 
    def Stop(self):
        self.spo2_thread_alive=False
        self._logger.info('DAQ Stop')
        return True

    def get_spo2(self):
        while self.spo2_thread_alive:
            self.spo2data.get()
            self.blood_oxy=self.spo2data.current_spo2
            self.heart_rate=self.spo2data.current_bpm
            wx.CallAfter(self.update_label)
            time.sleep(0.1)

    def find_port(self,port_list):
        port2check=port_list
        c=spo2_portcheck.Spo2_check(port2check)
        port=c.check()
        self._logger.info('SPO2 Port is '+str(port))
        return port

    def minor_check(self):
        config.read('rxbox.cfg')
        self.heartrate_infolabel.SetLabel('Ready')
        self.spo2_infolabel.SetLabel('            Ready')
        
        #self.spo2data=SPO2DAQ(self, port =config.get('SPO2','port'))
        #self.spo2data.POST()

    def update_label(self):
        self.spo2value_label.SetLabel(str(self.blood_oxy))
        self.bpmvalue_label.SetLabel(str(self.heart_rate))
        
    def setGui(self, mode='unlock'):
        if mode not in ['lock','unlock']:
            self._logger.info('setGui mode unsupported')
            return
            
        if mode == 'lock':
            print 'SPO2 Panel lock'
        elif mode == 'unlock':
            print 'SPO2 Panel unlock'
