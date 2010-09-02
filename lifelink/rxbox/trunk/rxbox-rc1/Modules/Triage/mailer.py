# Receiver
import imaplib
import os

# Sender
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

import ConfigParser
imaplib.debug = 10

class EmailReader:
    def __init__(self, config_file, starget = 'msghandler'):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(config_file)
        
        try:
            self.email_params = {'server': self.cfg.get('email', 'imapserver'),
                                'user': self.cfg.get('email', 'imapuser'),
                                'passwd': self.cfg.get('email', 'imappasswd')}
            self.sleep = int(self.cfg.get('email', 'sleep'))
            self.msghandler = self.cfg.get('email', starget)
        except ConfigParser.NoSectionError, e:
            pass
        except ConfigParser.NoOptionError, e:
            pass

    
    def login(self):
        self.serv = imaplib.IMAP4_SSL(self.email_params['server'])
        self.serv.login(self.email_params['user'], self.email_params['passwd'])

    
    def logout(self):
	self.serv.close()
        self.serv.logout()
    
    def get_unread(self):
	self.serv.select()
	criteria = '(FROM "' + self.msghandler + '" UNSEEN)'
	typ, data = self.serv.search(None, criteria)

	return data
    
    def get_headers(self, emailnum):
	return self.serv.fetch(emailnum, '(BODY.PEEK[HEADER] FLAGS)') 

    def setunread(self, msgnum):
	self.serv.store(msgnum, '+FLAGS', '\\Seen')


class EmailSender:
    def __init__(self, config_file):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(config_file)
        
        try:
            self.email_params = {'server': self.cfg.get('email', 'smtpserver'),
                                'user': self.cfg.get('email', 'smtpuser'),
                                'passwd': self.cfg.get('email', 'smtppasswd')}
        except ConfigParser.NoSectionError, e:
	    pass
            #raise ConfigError(str(e))
        except ConfigParser.NoOptionError, e:
	    pass
            #raise ConfigError(str(e))
    
    def send_message(self, contact, headers, text_content, attachments):
        # http://snippets.dzone.com/posts/show/757
        msg = MIMEMultipart()
        
        msg.add_header('To', contact)
        for (elem, item) in headers.items():
            msg.add_header(elem, item)
        
        msg.attach(MIMEText(text_content))
        for (elem, item) in attachments.items():
            part = MIMEBase('application', "octet-stream")
            part.set_payload(item)
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % elem)
            msg.attach(part)
        
        self.send(contact, msg.as_string())
        return True
    
    def send(self, contact, msg):
        serv = smtplib.SMTP(self.email_params['server'], 587)
        serv.ehlo()
        serv.starttls()
        serv.ehlo()
        serv.login(self.email_params['user'], self.email_params['passwd'])
        
        serv.sendmail('', contact, msg)
        serv.quit()

