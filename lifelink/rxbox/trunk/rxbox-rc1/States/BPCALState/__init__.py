from States.State import *
import os

class BPCALState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        
        self.dbuuid = self._engine.dbuuid
        self.rxboxDB = self._engine.rxboxDB
        
    def __name__(self):
        return 'BPCALState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        print os.getcwd()
        path=os.getcwd()
        os.system('python '+path+'/Modules/BP/BP_Calibration/bp_cal.py')
        self._engine.change_state('StandbyState')
        self._logger.info('State Machine: %s Stop'%self.__name__())

    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
