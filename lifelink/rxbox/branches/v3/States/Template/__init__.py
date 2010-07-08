from TemplateFrame import *
from TemplateLibraries import *

class TemplateFrame2(TemplateFrame):
    def __init__(self, engine, *args, **kwds):
        TemplateFrame.__init__(self, *args, **kwds)
        self._engine = engine
        
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
    def OnExit(self, event):
        self._engine.change_state()
                                  
class TemplateState:
    def __init__(self, engine):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        
        self._frame = TemplateFrame(engine, None, -1, "")
        self._panel = self._engine.mainstate._panel
        
        self.frameOn = False
        
    def start(self):
        print 'State Machine: TemplateState Start'
        self._frame.Maximize(True)
        self._frame.Show()
        self._frameOn = True
        
    def stop(self):
        print 'State Machine: TemplateState Stop'
        self._frame.Destroy()
        self.frameOn = False