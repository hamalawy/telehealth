from BPPanel import *

class BP (BPPanel):
    def __init__(self, *args, **kwds):
        BPPanel.__init__(self, *args, **kwds)
        
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        
    def Start(self):
        pass
        
    def Stop(self):
        pass
        
    def setGui(self, mode='unlock'):
        if mode == 'lock':
            print 'BP Panel lock'
        elif mode == 'unlock':
            print 'BP Panel unlock'
        else:
            print 'mode unsupported'
        
