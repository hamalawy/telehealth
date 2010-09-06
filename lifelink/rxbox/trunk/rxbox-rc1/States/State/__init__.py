#from TemplateFrame import *
#from TemplateLibraries import *

from Modules.Util import *

class State:
    def __init__(self, engine, *args, **kwds):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        self._logger = logging.getLogger(self.__name__())
                
        self._frame = self._engine._frame
        self._panel = self._frame._panel

    
    def __name__(self):
        return 'State'
        
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        
    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
