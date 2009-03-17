import sys, os, time
import xmpp
import signal
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
       	self.client.RegisterHandler('message', self.messageCB, typ='chat')
	self.client.RegisterHandler('message', self.rxbstatCB, typ='rbxstat')
       	self.client.sendInitPresence()
        
	while True:
		# Keep alive
		if int(time.time()) % 150 == 0:
			self.client.sendPresence()

		if self.stopEvent.isSet():
			self.client.disconnect()
			break
		self.client.Process(1)


    def messageCB(self, conn, msg):
	#print "Sender: " + str(msg.getFrom())
       	#print "Content: " + str(msg.getBody())
	wx.CallAfter(self.wxParent.UpdateIMRcvText, msg.getBody())
	
    def rxbstatCB(self, conn, msg):
	#rxbox status messages
	#print "Sender: " + str(msg.getFrom())
       	#print "Content: " + str(msg.getBody())
	status = msg.getBody().split(',')
	if status[0] is 'PatientSaved' and hasattr(self.wxParent, 'onPatientSaved'):
		wx.CallAfter(self.wxParent.onPatientSaved, status)
	elif status[0] is 'PatientOpened' and hasattr(self.wxParent, 'onPatientOpened'):
		wx.CallAfter(self.wxParent.onPatientOpened, status)
	elif status[0] is 'CaseSaved' and hasattr(self.wxParent, 'onCaseSaved'):
		wx.CallAfter(self.wxParent.onCaseSaved, status)
	elif status[0] is 'CaseOpened' and hasattr(self.wxParent, 'onCaseOpened'):
		wx.CallAfter(self.wxParent.onCaseOpened, status)
	elif status[0] is 'DataSaved' and hasattr(self.wxParent, 'onDataSaved'):
		wx.CallAfter(self.wxParent.onDataSaved, status)
	elif status[0] is 'DataOpened' and hasattr(self.wxParent, 'onDataOpened'):
		wx.CallAfter(self.wxParent.onDataOpened, status)
	else:
		print 'Ignoring RxBox Status. Unknown status or callback not defined.'
	
    def sendMessage(self, msg, recipient = None, typ='chat'):
	if recipient is None:
		self.client.send(xmpp.protocol.Message(self.recipient,msg,typ))
	else:
		self.client.send(xmpp.protocol.Message(recipient,msg,typ))
	
	if typ is 'chat':
		wx.CallAfter(self.wxParent.UpdateIMText, msg)	
	else:
		pass
	#print "sendM mesg: ", msg
	#print "sendM recpient self: ", recipient, self.recipient
	
    def setRecipient(self, rec_jid):
	self.recipient = rec_jid
		
