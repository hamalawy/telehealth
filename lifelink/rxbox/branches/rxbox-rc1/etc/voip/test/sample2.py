import sys
sys.path.append('../')
import time

import linphone

import wx
from wx import xrc


# This class will implement the callback functions
# for Linphone events
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




class RxBoxApp(wx.App):
   
    def OnInit(self):
        self.res = xrc.XmlResource('resources/rxbox.xrc')
        self.init_frame()
        return True

    def init_frame(self):
	# Get the gui objects from xrc
        self.rxbox_frame = self.res.LoadFrame(None, 'RxboxFrame')
        self.video_panel = xrc.XRCCTRL(self.rxbox_frame, 'video_panel')

	# Bind frame close event
	self.rxbox_frame.Bind(wx.EVT_CLOSE, self.OnClose)
	
	# Show frame first before initializing the phone
        self.rxbox_frame.Show()

	# Initialize the ohone
	self.init_phone()

    def init_phone(self):
	# Create a LinphoneHandle object which is a subclass of
	# the linphone object
	self.l = LinphoneHandle()

	wid = self.video_panel.GetHandle()
	self.l.set_window(wid)

	
	# Call the program. A separate process for the linphone  will be started.
	self.l.spawn()

	# Start the linphone loop. This is non-blocking because
	# linphone object is implemented in a separate thread
	self.l.start()

    def OnClose(self, event):
	# Stop before destroying the frame.
	self.l.stop()

	# Make sure that the linphone thread has been stopped.
	# This will block 
	self.l.join()

	# Ready to destroy
	self.rxbox_frame.Destroy()


if __name__ == '__main__':
    app = RxBoxApp(False)
    app.MainLoop()



