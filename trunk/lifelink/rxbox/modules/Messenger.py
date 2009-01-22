import sys
import xmpp
import os
import signal
import time
import wx
import threading

class Messenger(threading.Thread):
    def __init__(self, wxParent, jid, password, resource=None):
        threading.Thread.__init__(self)
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.wxParent = wxParent
	self.recipient = ''
	
	self.password = password
       	self.jid=xmpp.protocol.JID(jid)
       	self.client = xmpp.Client(self.jid.getDomain(), debug=[])

	print "Connecting to Messenger server..."
        if self.client.connect() == "":
                print "not connected"
                sys.exit(0)

        if self.client.auth(self.jid.getNode(),self.password) == None:
               print "authentication failed"
               sys.exit(0)
                               
    def stop(self):
        self.stopEvent.set()
        
    def run(self):
       	self.client.RegisterHandler('message', self.messageCB)
       	self.client.sendInitPresence()
        
	while True:
		if self.stopEvent.isSet():
			self.client.disconnect()
			break
		self.client.Process(1)


    def messageCB(self, conn, msg):
	#print "Sender: " + str(msg.getFrom())
       	#print "Content: " + str(msg.getBody())
	wx.CallAfter(self.wxParent.UpdateIMRcvText, msg.getBody())
	
    def sendMessage(self, msg, recipient = None):
	if recipient is None:
		self.client.send(xmpp.protocol.Message(self.recipient,msg))
	else:
		self.client.send(xmpp.protocol.Message(recipient,msg))
	wx.CallAfter(self.wxParent.UpdateIMText, msg)	
	#print "sendM mesg: ", msg
	#print "sendM recpient self: ", recipient, self.recipient
	
    def setRecipient(self, rec_jid):
	self.recipient = rec_jid
		
