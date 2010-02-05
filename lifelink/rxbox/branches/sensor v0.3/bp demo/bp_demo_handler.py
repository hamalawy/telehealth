"""
Project LifeLink: RxBox Stand-Alone Blood Pressure Sensor

Authors:    Bangoy, Mark Jan
            Sy, Luke Wicent
            Luis Sison, PhD
            ------------------------------------------------
            Instrumentation, Robotics and Control Laboratory
            University of the Philippines - Diliman
            ------------------------------------------------
            February 2010
"""
from bpmvc import MyFrame
import wx
from BP import BP

class bpdemo(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_BUTTON, self.onBPNow, self.bpNow_Button)
        self.timer1 = wx.Timer(self)
        self.pressure_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.get_bp, self.timer1)
        self.Bind(wx.EVT_TIMER, self.pressure_update, self.pressure_timer)
        self.bp = BP(self,'/dev/ttyUSB1')
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 250, size=(50, 100),style=wx.GA_VERTICAL)
        self.bp_pressure_indicator.Enable(False)
        self.bp_status_check()
    def onBPNow(self, event): # wxGlade: MyFrame.<event_handler>
        self.get_bp()
        
    def get_bp(self):
        self.bp_pressure_indicator.Enable(True)#enable the vertical bar pressurte reading
        self.bpNow_Button.Enable(False)#disable the bp acquire button until the bp reaidng is finished
        self.bp.send_request()
        self.pressure_timer.Start(200)#updates the readings every 200ms
        self.count=1
        
    def pressure_update(self,event):
        #print "timer for pressure"
        press = self.bp.get_reply()
        self.bp.nibp.read(1)
        #print "pressure: ", press, " mmHg"
        press = int(press[1:4])
        print self.count
        print press
        if press != 999:
            self.bpNow_Button.Enable(False)
            self.bp_pressure_indicator.SetValue(press)
            self.bp_infolabel.SetLabel(str(press)+' mmHg')
            self.count=0
            #self.bp_pressure_indicator.SetValue(press)
        else:
            self.bp_pressure_indicator.SetValue(0)
            self.bp_infolabel.SetLabel('BP Acquired')
            self.bp_pressure_indicator.Enable(False)
            self.bpNow_Button.Enable(True)
            self.bp.get()
            self.pressure_timer.Stop()
            
    def bp_status_check(self):
        self.bp.POST()
        self.bp.device_ready()
        self.bp_infolabel.SetLabel(self.bp.device_message)
        
    def updateBPDisplay(self, data):
        self.bpvalue_label.SetLabel(data) 





if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = bpdemo(None, -1, "")
    app.SetTopWindow(rx_frame)
    #rx_frame.Maximize(True)
    rx_frame.Show()
    app.MainLoop()
