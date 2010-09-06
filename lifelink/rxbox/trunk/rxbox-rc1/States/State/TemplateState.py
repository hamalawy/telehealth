from States.State import *

class TemplateState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        
        self.dbuuid = self._engine.dbuuid
        self.rxboxDB = self._engine.rxboxDB
        
    def __name__(self):
        return 'TemplateState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())

    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
