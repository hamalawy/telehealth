from SPO2Panel import *

class SPO2 (SPO2Panel):
    def __init__(self, *args, **kwds):
        SPO2Panel.__init__(self, *args, **kwds)
        
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        
    def Start(self):
        pass
        
    def Stop(self):
        pass
        
    def setGui(self, mode='unlock'):
        if mode == 'lock':
            print 'SPO2 Panel lock'
        elif mode == 'unlock':
            print 'SPO2 Panel unlock'
        else:
            print 'mode unsupported'
