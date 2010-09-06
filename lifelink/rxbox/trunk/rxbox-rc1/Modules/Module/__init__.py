#from TemplatePanel import *
#from TemplateDAQ import *

from Modules.Util import *

"""
This is the template module
A module is the class which combines the GUI and the DAQ

basic functions include:
    Start
    Stop
    setGui
"""
class Module:
    def __init__(self, *args, **kwds):
        self._frame = args[0]
        self._panel = self._frame._panel
        self._engine = self._frame._engine
        self._config = self._engine._config
        self.SetStatusText = self._frame.RxFrame_StatusBar.SetStatusText
        
        self._logger = logging.getLogger(self.__name__())
        self._logger.info('%s Module Initialized'%self.__name__())
        
        self.rxboxDB = self._engine.rxboxDB
        self.dbuuid = self._engine.dbuuid
        
        self.status = 'stop'
        
    def __name__(self):
        return 'Module'
        
    def Start(self):
        """
        Starts the function of the module
        Includes DAQ and GUI
        """
        self._logger.info('DAQ Start')
        self.status = 'start'
        
    def Stop(self):
        """
        Stops the function of the module
        Includes DAQ and GUI
        """
        self._logger.info('DAQ Stop')
        self.status = 'stop'
        
    def setGui(self, mode='unlock'):
        """
        This locks or unlocks the gui elements.
        String is used as an indicator to be more readable.
        Boolean may also be used but who knows, there might be the need of another mode other than lock and unlock.
        """
        if mode not in ['lock','unlock']:
            self._logger.info('setGui mode unsupported')
            return
            
    def OnPaneClose(self):
        pass
