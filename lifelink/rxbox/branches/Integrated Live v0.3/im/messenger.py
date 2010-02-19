import sys, os, time
import xmpp
import signal
import wx
import threading

class Messenger(threading.Thread):
    def __init__(self, jid, password, resource=None):
        threading.Thread.__init__(self)
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
	self.recipient = ''
	
	self.password = password
       	self.jid=xmpp.protocol.JID(jid)
#      	self.client = xmpp.Client(self.jid.getDomain(), debug=['always'])
	self.client = xmpp.Client(self.jid.getDomain(), debug=[])
                             			       
    def connect(self):
	print "Connecting to Messenger server..."
        if self.client.connect() == "":
                print "Warning: Messenger not connected"
                return False

        if self.client.auth(self.jid.getNode(),self.password) == None:
               print "Warning: Messenger authentication failed"
               return False
	
	return True
	       
    def stop(self):
        self.stopEvent.set()
        
    def run(self):
	self.client.sendInitPresence()
       	self.client.RegisterHandler('message', self.handler_new_message)
        
	while True:
		# Keep alive
		if int(time.time()) % 150 == 0:
			self.client.sendPresence()

		if self.stopEvent.isSet():
			self.client.disconnect()
			break
		self.client.Process(1)


    def send_message(self, msg, typ='chat'):
	if self.recipient is not '':
		self.client.send(xmpp.protocol.Message(self.recipient,msg,typ))
	else:
		print 'Unable to send. Set recipient first'
		
	if typ is 'chat':
		self.handler_sent_message(msg)
	else:
		pass
	
    def set_recipient(self, rec_jid):
	self.recipient = rec_jid
		

    # Public Virtual functions
    def handler_new_message(self, conn, msg):
	pass
	#print "-------\n" + str(msg) + "\n\n"
        #print "Sender: " + str(msg.getFrom())
        #print "Content: " + str(msg.getBody())

    def handler_sent_message(self, msg):
	pass
