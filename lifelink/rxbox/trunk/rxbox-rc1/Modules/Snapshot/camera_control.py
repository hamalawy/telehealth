import sys
sys.path.append('../')

import linphone

class LinphoneHandle(linphone.Linphone):
    def __init__(self):
        linphone.Linphone.__init__(self)

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
    
class WebcamControl():
    
    def __init__(self, parent, video_display):
        
        self.parent = parent
        self.video_display = video_display
        self.init_phone()
        
        
    def init_phone(self):
        
        self.l = LinphoneHandle()
        wid = self.parent.video_panel.GetHandle()
        self.l.set_window(wid)
        self.l.spawn()
        self.l.start()
        self.l.execute('webcam use ' + self.video_display)
        self.l.execute('unregister')
        
    def close_phone(self):
        self.l.stop()
        
        
