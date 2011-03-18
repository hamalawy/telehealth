import wx
import time
import threading
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('rxbox.cfg')
if config.getboolean('BP', 'simulated'):
    from BPDAQSim import *
else:
    from BPDAQLive import BPDAQ

from BPPanel import *
from Modules.Module import *
import bp_portcheck


class BP (Module, BPPanel):
    def __init__(self, *args, **kwds):
        config.read('rxbox.cfg')
        BPPanel.__init__(self, *args, **kwds)
        Module.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_BUTTON, self.onBPNow, self.bpNow_Button)
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 250, size=(50, 100),style=wx.GA_VERTICAL)
        self.bp_pressure_indicator.Enable(False)
#coeff=(1.593,-1.148,17.98,0.107,0.227,39.25),coeff=(0.981,0,-6.59,0,0.38741,38.45)
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(1,0,0,0,1,0))
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 250, size=(50, 100),style=wx.GA_VERTICAL)
        self.bp_pressure_indicator.Enable(False)
        self.alive=False       
        self.updatealive=False
        self.bp_infolabel.SetLabel('Restart Software')
        self.bpNow_Button.Enable(False)
    
    def __name__(self):
        return 'BP'

    def onBPNow(self, event):
        self.Start()

    def Start(self):
        config.read('rxbox.cfg')
        port2check=[config.get('BP','port')]
        c=bp_portcheck.Bp_check(port2check)
        port=c.check()
        if port == None:
            self.bp_infolabel.SetLabel('Cannot Proceed:BP Unavailable')
            return
        #(config.get('BP','sys_coeff_a'),0,config.get('BP','sys_coeff_b'),0,config.get('BP','dias_coeff_a'),config.get('BP','dias_coeff_b'))
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(float(config.get('BP','sys_coeff_a')),0,float(config.get('BP','sys_coeff_b')),0,float(config.get('BP','dias_coeff_a')),float(config.get('BP','dias_coeff_b'))),debug=True,logger=self._logger)
        #self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(0.74212,0,19.00353,0,0.36265,45.688))
        #(0.981,0,-6.59,0,0.38741,38.45)

        #self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(1,0,0,0,1,0))

        self.bp.OpenSerial()
        self._logger.info('BP: '+str(self.setBPmaxpressure_combobox.GetValue()[:3])) 
        self.bp.send_request(self.setBPmaxpressure_combobox.GetValue()[:3])
        self.setBPmaxpressure_combobox.Enable(False)
        self.bpNow_Button.SetToolTipString("Acquiring BP")
        self.bpdaq_thread = threading.Thread(target=self.Get_bp)
        self.bpdaq_thread.start()
        self._logger.info('DAQ Start')
        return True
        
    def Stop(self):
        if self.bp==True:
            if self.bp.nibp.isOpen()== True:
                self.bp.stop()
                self._logger.debug('BP serial deactivated')
            self._logger.info('DAQ Stop')
        return True
        
    def setGui(self, mode='unlock'):
        if mode not in ['lock','unlock']:
            self._logger.info('setGui mode unsupported')
            return
            
        if mode == 'lock':
            self.bpNow_Button.Enable(False)
            self.setBPmaxpressure_combobox.Enable(False)
        elif mode == 'unlock':
            self.bpNow_Button.Enable(True)
            self.setBPmaxpressure_combobox.Enable(True)

    def find_port(self,port_list):
        port2check=port_list
        c=bp_portcheck.Bp_check(port2check)
        port=c.check()
        self._logger.info('BP Port is '+str(port))
        return port

    def minor_check(self):
        config.read('rxbox.cfg')
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(1,0,0,0,1,0),debug=True,logger=self._logger)
        status=self.bp.init_status_check()
        if status== False:
            self._logger.debug('BP: Initialization Failed') 
            self.bp_infolabel.SetLabel('BP Unavailable:Restart Software')
            return
        self._logger.debug('BP init part 1 done')

        status=self.bp.init_firmware_version()
        if status== False:
            print 'initialization failed'
            self._logger.debug('BP: Initialization Failed') 
            self.bp_infolabel.SetLabel('BP Unavailable:Restart Software')
            return
        
        self._logger.debug('BP: init part 2 done')        

        self.bpNow_Button.Enable(True)
        self.bp_infolabel.SetLabel('BP Ready')

    def Get_bp(self):
        self.alive=True 
        none_count=0
        while self.alive:
            time.sleep(0.1)
            press = self.bp.get_reply()
            if press == 'S5':
                press =''
                continue
            if press == None or press == '':
                self._logger.debug('BP: none type returned')
                none_count+=1
                if none_count<1:
                    continue
                else:
                    press='09990'
            try:
                self.press = int(press[1:4])
            except:
                self._logger.debug('BP: BP packet mismatch, fixing')   
                self.press=999
            if self.press== 999:
                self.alive=False
                self.bp.get()
                self.updatealive=False
                self.bp.stop()
                self.bp.CloseSerial()
            wx.CallAfter(self.pressure_update)
        self.bp.CloseSerial()
                
    def pressure_update(self):
        if self.press != 999:
            self.bpNow_Button.Enable(False)
            self.bp_pressure_indicator.SetValue(self.press)
            self.bp_infolabel.SetLabel(str(self.press)+' mmHg')
        else:
            self.updatealive=False
            self.alive=False
            self.bp_pressure_indicator.SetValue(0)
            self.bp_infolabel.SetLabel(self.bp.bpstatus)
            self.bp_pressure_indicator.Enable(False)
            self.bpNow_Button.Enable(True)
            self.setBPmaxpressure_combobox.Enable(True)
            self.bpNow_Button.SetToolTipString("Acquire BP Reading")
            self.bpvalue_label.SetLabel(str(self.bp.bp_systolic)+'/'+str(self.bp.bp_diastolic))
        
