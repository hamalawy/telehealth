import wx
from wx import xrc
from ecgplotter import Plotter
import ECG
import threading
import time

login = {'Rxbox':'Engine', 'Telehealth':'Telemed', 'Root':'Root', '':''}

class LoginState:
    def __init__(self,engine):
        """State init"""
        self._engine = engine
        self._app = self._engine.app
        
        self.frameOn = False
    
    def start(self):
        """Start state"""
        print 'Login State Starting'
        self._app.frame = self._app.resMain.LoadFrame(None, 'Login')
        self.username = xrc.XRCCTRL(self._app.frame, 'Login_user_text_ctrl')
        self.password = xrc.XRCCTRL(self._app.frame, 'Login_pass_text_ctrl')
        self.status = xrc.XRCCTRL(self._app.frame, 'Login_status')
        self._app.Bind(wx.EVT_BUTTON, self.LoginButtonPressed, id=xrc.XRCID('Login_button'))
        self._app.frame.Show()
        self.frameOn = True
        
    def stop(self):
        """Stop state"""
        if self.frameOn:
            self._app.frame.Destroy()
        print 'Login State Stopped'
        
    def LoginButtonPressed(self, evt):
        """Login Button Event Handler"""
        print 'Login Button Pressed'
        userInput = self.username.GetValue()
        passInput = self.password.GetValue()
        if login.has_key(userInput) and login[userInput] == passInput:
            self._engine.change_state(MainState(self._engine))
        else:
            self.password.SetValue("")
            self.status.SetLabel("Invalid username and password")
            print 'Invalid username and password'

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
        self.plotter = Plotter(self._app.frame, (1120, 380), self.plotgraph_panel)
        
        self.R_bitmap = xrc.XRCCTRL(self._app.frame, 'R_bitmap')
        self.L_bitmap = xrc.XRCCTRL(self._app.frame, 'L_bitmap')
        self.N_bitmap = xrc.XRCCTRL(self._app.frame, 'N_bitmap')
        self.F_bitmap = xrc.XRCCTRL(self._app.frame, 'F_bitmap')
        self.C1_bitmap = xrc.XRCCTRL(self._app.frame, 'C1_bitmap')
        self.C2_bitmap = xrc.XRCCTRL(self._app.frame, 'C2_bitmap')
        self.C3_bitmap = xrc.XRCCTRL(self._app.frame, 'C3_bitmap')
        self.C4_bitmap = xrc.XRCCTRL(self._app.frame, 'C4_bitmap')
        self.C5_bitmap = xrc.XRCCTRL(self._app.frame, 'C5_bitmap')
        self.C6_bitmap = xrc.XRCCTRL(self._app.frame, 'C6_bitmap')
        
        self.frameOn = True
        
        self._app.Bind(wx.EVT_BUTTON, self.PlayButtonPressed, id=xrc.XRCID('play_button'))
        self.play =  False
        #self._app.Bind(wx.EVT_BUTTON, self.lead12_button_clicked, id=xrc.XRCID('lead12_button'))
        
        self._app.frame.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.ECGData = ECG.ECG(daqdur=3)
        self.ECGData.device_ready()
        self.ECGData.stop()
        
        self.timerPlot = wx.Timer(self._app)
        self._app.Bind(wx.EVT_TIMER, self.plotECG, self.timerPlot)
        
    def stop(self):
        if self.frameOn:
            self._app.frame.Destroy()
        print 'stop'

    def onClose(self, evt):
        print 'here'
        self.stop()
        self._engine.change_state(LoginState(self._engine))
        
    def PlayButtonPressed(self, evt):
        if not self.play:
            #if off, turn on
            print 'Play'
            self.play = True
            self.ECGData = ECG.ECG(daqdur=3)
            
            self.alive = True
            self.get_thread = threading.Thread(target=self.Get_ECG)
            self.get_thread.start()
            
            self.timerPlot.Start(250)
        else:
            #if on, turn off
            print 'Stop'
            self.play = False
            self.alive = False
            self.timerPlot.Stop()
            time.sleep(3)
            self.ECGData.stop()
    
    def Get_ECG(self):
        while self.alive:
            self.ECGData.patient_ready()
            time.sleep(0.1)
        
    def plotECG(self, evt):
        try:
            if len(self.ECGData.lead_ecg['II']) > 1500:
                self.statECG()
                self.plotter.plot(self.ECGData.lead_ecg['II'][0:1500])
                self.ECGData.pop(end=125)
        except:
            print 'No New Data'
            
    def statECG(self):
        try:
            if self.ECGData.nodeR:
                self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_connected.png"))
            else:
                self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_unconnected.png"))
            if self.ECGData.nodeL:
                self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_connected.png"))
            else:
                self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_unconnected.png"))
            if self.ECGData.nodeN:
                self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_connected.png"))
            else:
                self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png"))
            if self.ECGData.nodeF:
                self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_connected.png"))
            else:
                self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_unconnected.png"))
            if self.ECGData.nodeC1:
                self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_connected.png"))
            else:
                self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_unconnected.png"))
            if self.ECGData.nodeC2:
                self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_connected.png"))
            else:
                self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_unconnected.png"))
            if self.ECGData.nodeC3:
                self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_connected.png"))
            else:
                self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png"))
            if self.ECGData.nodeC4:
                self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_connected.png"))
            else:
                self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_unconnected.png"))
            if self.ECGData.nodeC5:
                self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_connected.png"))
            else:
                self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png"))
            if self.ECGData.nodeC6:
                self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_connected.png"))
            else:
                self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_unconnected.png"))
        except Exception,e:
            print e
        
class RxboxEngine:
    """Engine/Controller class for Rxbox"""
    def run(self):
        """Run engine and start up GUI"""
        self.app = RxboxApp(False)
        self.state = LoginState(self)
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