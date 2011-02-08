from States.State import *
import os
from startup import *

class TestState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        
        self.dbuuid = self._engine.dbuuid
        self.rxboxDB = self._engine.rxboxDB
        self._frame2 = ShowMain(self._engine, None, -1, "")
        
        
    def __name__(self):
        return 'TestState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        self._frame2.Maximize(True)
        self._frame2.Show()

    def stop(self):
        #self._frame2.Destroy()
        self._logger.info('State Machine: %s Stop'%self.__name__())
