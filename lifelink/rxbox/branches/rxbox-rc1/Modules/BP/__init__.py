from BPPanel import *
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

class BP (BPPanel):
    def __init__(self, *args, **kwds):
        BPPanel.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_BUTTON, self.onBPNow, self.bpNow_Button)
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 250, size=(50, 100),style=wx.GA_VERTICAL)
        self.bp_pressure_indicator.Enable(False)
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
#coeff=(1.593,-1.148,17.98,0.107,0.227,39.25)
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(0.981,0,-6.59,0,0.38741,38.45))
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 250, size=(50, 100),style=wx.GA_VERTICAL)
        self.bp_pressure_indicator.Enable(False)
        self.alive=False       
        self.updatealive=False
        self.bp_infolabel.SetLabel('Not Ready')
        self.bpNow_Button.Enable(False)
        

    def onBPNow(self, event):
        self.Start()

    def Start(self):
        print 'BP START'
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(0.981,0,-6.59,0,0.38741,38.45))
        self.bp.OpenSerial()
        self.bp.send_request(self.setBPmaxpressure_combobox.GetValue()[:3])
        self.setBPmaxpressure_combobox.Enable(False)
        self.bpNow_Button.SetToolTipString("Acquiring BP")
        self.bpdaq_thread = threading.Thread(target=self.Get_bp)
        self.bpdaq_thread.start()
        return True
        
    def Stop(self):
        print 'BP STOP'
        self.bp.OpenSerial()
        self.bp.stop()
        self.bp.CloseSerial()
        return True
        
    def setGui(self, mode='unlock'):
        if mode == 'lock':
            print 'BP Panel lock'
            self.bpNow_Button.Enable(False)
            self.setBPmaxpressure_combobox.Enable(False)
        elif mode == 'unlock':
            print 'BP Panel unlock'
            self.bpNow_Button.Enable(True)
            self.setBPmaxpressure_combobox.Enable(True)
        else:
            print 'mode unsupported'

    def minor_check(self):
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(0.981,0,-6.59,0,0.38741,38.45))

        status=self.bp.init_status_check()
        if status== False:
            print 'initialization failed'
            self.bp_infolabel.SetLabel('Not Ready')
            return
        print 'bp init part 1 done'

        status=self.bp.init_firmware_version()
        if status== False:
            print 'initialization failed'
            self.bp_infolabel.SetLabel('Not Ready')
            return
        print 'bp init part 2 done'

        self.bpNow_Button.Enable(True)
        self.bp_infolabel.SetLabel('BP Ready')

    def Get_bp(self):
        self.alive=True 
        while self.alive:
            time.sleep(0.1)
            press = self.bp.get_reply()
            if press == 'S5':
                press =''
                continue
            if press == None:
                print 'none type returned'
                continue
            self.press = int(press[1:4])
            if self.press== 999:
                self.alive=False
                self.bp.get()
                self.updatealive=False
                self.bp.stop()
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
        
