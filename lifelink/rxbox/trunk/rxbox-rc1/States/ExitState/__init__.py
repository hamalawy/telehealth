import wx

from States.State import *

class ExitState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        
    def __name__(self):
        return 'ExitState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        current_perspective = self._frame._mgr.SavePerspective()
        self._config.read('rxbox.cfg')
        self._config.set('Perspective', 'onoff', current_perspective)
        self._config.write(open('rxbox.cfg', 'w'))
        self._logger.info('Configurations Saved')
        
        self._frame.Destroy()
        self._engine.change_state(None)
        
    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
