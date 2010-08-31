from Linphone import *
from VoIPPanel import *

class LinphoneHandle(Linphone):
    def __init__(self):
        Linphone.__init__(self)

    def handle_incoming(self):
        print self.caller , " is calling."
        self.answer()

    def handle_terminated(self):
        print "Call ended."
        #you may put GUI codes here (callafter function maybe?)

    def handle_answered(self):
        print "Call answered"
        #you may put GUI codes here (callafter function maybe?)

    def handle_failed(self):
        print "Call failed"
        #you may put GUI codes here (callafter function maybe?)
        
class VoIP (VoIPPanel):
    def __init__(self, *args, **kwds):
        VoIPPanel.__init__(self, *args, **kwds)
        
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
        self.linphone = LinphoneHandle()
        wid = self.video_panel.GetHandle()
        self.linphone.set_window(wid)
        self.linphone.spawn()
        self.linphone.start()
        
    def Stop(self):
        """
        Stops the function of the module
        Includes DAQ and GUI
        """
        self.status = 'stop'
        self.linphone.stop()
        self.linphone.join()
        
    def setGui(self, mode='unlock'):
        """
        This locks or unlocks the gui elements.
        String is used as an indicator to be more readable.
        Boolean may also be used but who knows, there might be the need of another mode other than lock and unlock.
        """
        if mode not in ['unlock', 'lock']:
            print 'mode unsupported'
            return
