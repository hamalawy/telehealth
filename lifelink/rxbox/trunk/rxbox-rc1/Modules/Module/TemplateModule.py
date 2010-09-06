#from TemplatePanel import *
#from TemplateDAQ import *

"""
This is the template module
A module is the class which combines the GUI and the DAQ

basic functions include:
    Start
    Stop
    setGui
"""
class Template (TemplatePanel):
    def __init__(self, *args, **kwds):
        TemplatePanel.__init__(self, *args, **kwds)
        
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        
        self.rxboxDB = self._engine.rxboxDB
        self.dbuuid = self._engine.dbuuid
        self._panel = self._frame._panel
        self.status = 'stop'
        self.error = ''
        
    def Start(self):
        """
        Starts the function of the module
        Includes DAQ and GUI
        """
        self.status = 'start'
        pass
        
    def Stop(self):
        """
        Stops the function of the module
        Includes DAQ and GUI
        """
        self.status = 'stop'
        pass
        
    def setGui(self, mode='unlock'):
        """
        This locks or unlocks the gui elements.
        String is used as an indicator to be more readable.
        Boolean may also be used but who knows, there might be the need of another mode other than lock and unlock.
        """
        if mode not in ['unlock', 'lock']:
            print 'mode unsupported'
            return
            
    def OnPaneClose(self):
        pass
