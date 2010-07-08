import wx
import ConfigParser
import States
from Modules import rxboxdb

class RxboxEngine:
    """Engine/Controller class for Rxbox"""
    def run(self):
        """Run engine and start up GUI"""
        self._app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        self._config = ConfigParser.ConfigParser()
        self._config.read('rxbox.cfg')
        
        self.dbuuid = ''
        self.rxboxDB = rxboxdb.rxboxDB()
        self.rxboxDB.dbconnect()
        self.rxboxDB.dbcreatetables()
        
        self.mainstate = States.MainState(self)
        self.state = self.mainstate
        self.state.start()
        self._app.MainLoop()
        
    def change_state(self, state=''):
        """Change state to state"""
        self.state.stop()
        if state == 'MainState':
            self.state = self.mainstate
        else: self.state = getattr(States,state)(self)
        self.state.start()
            
    def restart(self):
        self.mainstate = States.MainState(self)
        self.mainstate.show()
        self.change_state()
        
    def exit(self):
        self._app.Exit()
        self.mainstate.exit()
            
if __name__ == '__main__':
    engine = RxboxEngine()
    engine.run()
