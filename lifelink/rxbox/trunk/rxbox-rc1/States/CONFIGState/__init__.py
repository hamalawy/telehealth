from States.State import *
import os

class CONFIGState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        
        self.dbuuid = self._engine.dbuuid
        self.rxboxDB = self._engine.rxboxDB
        
    def __name__(self):
        return 'CONFIGState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        print os.getcwd()
        path=os.getcwd()
        os.system('python '+path+'/Configuration/Configuration.py')
        self._engine.change_state('StanbyState')
        self._logger.info('State Machine: %s Stop'%self.__name__())

    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
