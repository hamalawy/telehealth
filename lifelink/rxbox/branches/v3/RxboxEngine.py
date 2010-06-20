import wx
import ConfigParser
from States import *

class RxboxEngine:
    """Engine/Controller class for Rxbox"""
    def run(self):
        """Run engine and start up GUI"""
        self.app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        self.state = None
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg') 
        self.change_state(MainState(self))
        self.app.MainLoop()
        
    def change_state(self, state):
        """Change state to state"""
        #if self.state is main, don't close
        if self.state is not None:
            self.state.stop()
        #if self.state is main, and state is main, restart
        if isinstance(self.state,MainState) and isinstance(state,MainState):
            self.state.restart()
            
        self.state = state
        if self.state is None:
            self.app.Exit()
        else:
            self.state.start()
            
if __name__ == '__main__':
    engine = RxboxEngine()
    engine.run()