
from Linphone import *
from VoIPPanel import *
from Modules.Module import *

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
        
class VoIP (Module, VoIPPanel):
    def __init__(self, *args, **kwds):
        Module.__init__(self, *args, **kwds)
        VoIPPanel.__init__(self, *args, **kwds)
        
    def __name__(self):
        return 'VoIP'
        
    def Start(self):
        """
        Starts the function of the module
        Includes DAQ and GUI
        """
        self.linphone = LinphoneHandle()
        wid = self.video_panel.GetHandle()
        self.linphone.set_window(wid)
        self.linphone.spawn()
        self.linphone.start()
        self.status = 'start'
        self._logger.info('Start')
        
    def Stop(self):
        """
        Stops the function of the module
        Includes DAQ and GUI
        """

        self.linphone.stop()
        self.linphone.join()
        self.status = 'stop'
        self._logger.info('Stop')
        
    def setGui(self, mode='unlock'):
        """
        This locks or unlocks the gui elements.
        String is used as an indicator to be more readable.
        Boolean may also be used but who knows, there might be the need of another mode other than lock and unlock.
        """
        if mode not in ['unlock', 'lock']:
            print 'mode unsupported'
            return
