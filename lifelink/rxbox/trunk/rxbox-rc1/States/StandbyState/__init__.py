from States.State import *

class StandbyState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
    
    def __name__(self):
        return 'StandbyState'
        
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        self._panel['comm'].setGui('standby')
        [self._panel[i].setGui('unlock') for i in ['patientinfo','bp','snapshot']]
        [self._panel[i].setGui('lock') for i in ['ecg','spo2']]
        
    def stop(self):
        pane = self._frame._mgr.GetPane("snapshot2")
        self._frame._mgr.ClosePane(pane)
        self._frame._mgr.Update()
        [self._panel[i].setGui('lock') for i in ['snapshot']]
        self._logger.info('State Machine: %s Stop'%self.__name__())
