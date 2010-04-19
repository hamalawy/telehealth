import wx
from wx import xrc
from ecgplotter import Plotter

login = {'Rxbox':'Engine', 'Telehealth':'Telemed', 'Root':'Root'}

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
        
    def LoginButtonPressed(self,evt):
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
        
        self.frameOn = True
        
    def stop(self):
        if self.frameOn:
            self._app.frame.Destroy()
        print 'stop'

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