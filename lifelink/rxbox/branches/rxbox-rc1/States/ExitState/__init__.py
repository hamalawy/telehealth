import wx

class ExitState:
    def __init__(self, engine, *args, **kwds):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        
        self._frame = self._engine._frame
        self._panel = self._frame._panel
        
    def __name__(self):
        return 'ExitState'
    
    def start(self):
        print 'State Machine: ExitState Start'
        current_perspective = self._frame._mgr.SavePerspective()
        self._config.set('Perspective', 'onoff', current_perspective)
        self._config.write(open('rxbox.cfg', 'w'))
        print 'Configuration Saved'
        self._frame.Destroy()
        self._engine.change_state(None)
        
    def stop(self):
        print 'State Machine: ExitState Stop'
