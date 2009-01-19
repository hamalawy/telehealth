import sys
import xmpp
import os
import signal
import time
import wx
import threading

class Messenger(threading.Thread):
    def __init__(self, wxParent, password, resource=None):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.wxParent = wxParent
	
	self.jid="1011@192.168.0.3"
       	self.password="cuv4xlifelink"
	
       	self.jid=xmpp.protocol.JID(jid)
       	self.client = xmpp.Client(jid.getDomain(), debug=[])
                               
    def stop(self):
        self.stopEvent.set()
        
    def run(self):
       	if self.client.connect() == "":
        	print "not connected"
               	sys.exit(0)

       	if self.client.auth(jid.getNode(),pwd) == None:
               print "authentication failed"
               sys.exit(0)
       
       	self.client.RegisterHandler('message', messageCB)
       	self.client.sendInitPresence()
        
	while True:
		if self.stopEvent.isSet():
			self.client.disconnect()
			break
		self.client.Process(1)


    def messageCB(self, conn, msg):
	print "Sender: " + str(msg.getFrom())
       	print "Content: " + str(msg.getBody())
	wx.CallAfter(self.wxParent.UpdateIMRcvText, msg)
		
		
