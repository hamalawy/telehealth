class StandbyState:
    def __init__(self, engine, *args):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        
        self._frame = self._engine._frame
        self._panel = self._frame._panel
    
    def __name__(self):
        return 'StandbyState'
        
    def start(self):
        print 'State Machine: StandbyState Start'
        self._panel['comm'].setGui('standby')
        [self._panel[i].setGui('unlock') for i in ['patientinfo','bp']]
        [self._panel[i].setGui('lock') for i in ['ecg','spo2']]
        
    def stop(self):
        print 'State Machine: StandbyState Stop'
        pane = self._frame._mgr.GetPane("snapshot2")
        self._frame._mgr.ClosePane(pane)
        self._frame._mgr.Update()
