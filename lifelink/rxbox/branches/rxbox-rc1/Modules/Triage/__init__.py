import threading, mailer
import re
import pycurl

#temporary modules
import time, random

class Triage(mailer.EmailReader, mailer.EmailSender):
    def __init__(self, config_file):
    	mailer.EmailReader.__init__(self, config_file)
    	mailer.EmailSender.__init__(self, config_file)
    
        self.stop_event = threading.Event()
    
    	#Generated during call to request
    	self.localticketid = -1 
    
    	#Generated by the Triage
    	self.eccscaseid = -1
    
    	self.response = {}

        
    def stop(self):
        self.stop_event.set()
  
    def request(self, headers, body, attachments={}):
    	sendto= self.msghandler
     
    	#self.localticketid  = random.randrange(0, 9999)
    	self.localticketid = 9999
    	headers['X-Eccs-Rxboxticket'] = str(self.localticketid)
        self.send_message(sendto, headers, body, attachments)
    
        return self.localticketid

    def wait(self, localticketid = None):
    	print 'Waiting for MsgHandler Response'
    	response = {'ticketid': -1, 'case_id': '', 'uploadurl': '', 'piority': ''}
    	headers = ''
    	typ = ''
    
        while not self.stop_event.isSet() and response['case_id'] == "" and response['ticketid'] != self.localticketid:
    	    mailnum = self.get_unread()
    	    num = 0;
    	    for num in mailnum[0].split():
    	      typ, msginfo = self.get_headers(num)
    	      headers = msginfo[0][1]
    	      #print headers
    
    	      res1 = re.findall(r"X-Eccs-Rxboxticket: ([\w]+)", headers,re.M | re.I)
    	      res2 = re.findall(r"X-Eccs-Caseid: ([\w]+)", headers,re.M | re.I)
    	      res3 = re.findall(r"X-Eccs-Uploadurl: ([\w\d\./:]+)", headers,re.M | re.I)
    	      res4 = re.findall(r"X-Eccs-Priority: ([\w\d]+)", headers,re.M | re.I)
    
    	      # Check if the header contains case id
    	      if (len(res2) == 0):
    		continue
    	      else:
    		response['ticketid'] = res1[0]
    		response['case_id'] = res2[0]
    		response['uploadurl'] = res3[0]
    		response['piority'] = res4[0]
    		break
        
    	    time.sleep(1)
    
    	if (num != 0):
    	    self.setunread(num)
    
    
    	self.response = response
    	return response

    def upload(self, data):
    	if (data['uploadurl'] == ""):
    	    return False
    
    	pf = [ ('file', (pycurl.FORM_FILE, data['filename'])),
    	      ('sequence_id', '9999'),
    	      ('case_id', '100')
    	]
    
    	c = pycurl.Curl()
    	c.setopt(c.URL, data['uploadurl'])
    	c.setopt(c.HTTPPOST, pf)
    	c.setopt(c.VERBOSE, 1)
    	c.perform()
    	c.close()
    
    	return True
    	
