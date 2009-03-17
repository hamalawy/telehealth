import wx, time
import threading
#import serial
import socket
import TriageClient as tc
import edfviewer as edf

RQT_MSSG        = 'TELEMED'
PKY_MSSG        = '1234'
WEL_MSSG        = RQT_MSSG + ' ' + PKY_MSSG
VFY_MSSG        = 'READY TO RECEIVE'
REF_MSSG        = 'CONNECTION REFUSED'
FIN_MSSG        = 'FINISHED TRANSMISSION'

BUFSIZ 			= 1024
BUF_SAMPLES     = 30            


#INPUT_FILE      = open('testfile0.edf', 'rb')
#INPUT_FILE      = INPUT_FILE.read()
#print type(INPUT_FILE)
#INPUT_FILE      = 'x'

class AcquireDataThr(threading.Thread):
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.stopAcquireThr = threading.Event()
        self.stopAcquireThr.clear()
        
        self.window = window
        
    def stop(self):
        self.stopAcquireThr.set()
       
    def run(self):
	self.window.onStartAcquire_MenuClick(None)

        #wx.CallAfter(self.window.onClickStop)
       # self.sent -= 1
