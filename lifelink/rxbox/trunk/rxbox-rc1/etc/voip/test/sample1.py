import sys
sys.path.append('../')
import time

import linphone

class LinphoneHandle(linphone.Linphone):
    def __init__(self):
	linphone.Linphone.__init__(self)

    def handle_incoming(self):
	print self.caller , " is calling."
	#you may put GUI codes here (callafter function maybe?)

    def handle_terminated(self):
	print "Call ended."
	#you may put GUI codes here (callafter function maybe?)

    def handle_answered(self):
	print "Call answered"
	#you may put GUI codes here (callafter function maybe?)

    def handle_failed(self):
	print "Call failed"
	#you may put GUI codes here (callafter function maybe?)


l = LinphoneHandle()

l.spawn()
l.start()
time.sleep(60)
l.stop()

