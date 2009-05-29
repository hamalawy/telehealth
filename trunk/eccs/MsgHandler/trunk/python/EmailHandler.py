#!/usr/bin/python

import getopt
import sys, os
import time
import tempfile
import ConfigParser

from MHTools import stopd, startd
from MHTools import get_logger
from MHTools import ConfigError
from MHLink import DbLink

import re
import datetime
import poplib
import smtplib

import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

class EmailReader:
    def __init__(self, config_file):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(config_file)
        
        try:
            self.email_params = {'server': self.cfg.get('email', 'popserver'),
                                'user': self.cfg.get('email', 'popuser'),
                                'passwd': self.cfg.get('email', 'poppasswd')}
            self.sleep = int(self.cfg.get('email', 'sleep'))
            self.mode = self.cfg.get('email', 'mode')
            
            if not self.cfg.has_section('headers'):
                raise ConfigParser.NoSectionError
            
            self.login()
        except ConfigParser.NoSectionError, e:
            raise ConfigError(str(e))
        except ConfigParser.NoOptionError, e:
            raise ConfigError(str(e))
    
    def login(self):
        self.serv = poplib.POP3_SSL(self.email_params['server'])
        self.serv.user(self.email_params['user'])
        self.serv.pass_(self.email_params['passwd'])
    
    def logout(self):
        self.serv.quit()
    
    def get_unread(self):
        CNT, SIZE = self.serv.stat()
        log.info("%d message(s) unread" % CNT)
        return CNT
    
    def get_message(self, emailnum):
        RESP, TEXT, OCTETS = self.serv.retr(emailnum)
        return email.message_from_string('\n'.join(TEXT))
    
    def test_mode(self):
        while True:
            for i in range(1, self.get_unread()+1):
                msg = self.get_message(i)
                outp = self._parse(msg)
                
                (contact, headers, text_content, attachments) = outp
                if 'caseid' not in headers:
                    headers['caseid'] = '100'
                self.respond_to_msg(contact, headers, 'reply', attachments)
            time.sleep(self.sleep)
    
    def run(self):
        while True:
            for i in range(1, self.get_unread()+1):
                msg = self.get_message(i)
                outp = self._parse(msg)
                self.insert_msg_to_db(outp)
                self.respond_to_msg(*outp)
            time.sleep(self.sleep)
    
    def _parse(self, msg):
        headers = self.get_headers(msg)
        contact = self.get_contact(headers)
        text_content = self.get_text_content(msg.get_payload())
        attachments = self.get_attachments(msg.get_payload())
        
        return (contact, headers, text_content, attachments)
    
    def get_headers(self, msg):
        headers = self.get_headers_orig(msg)
        headers = self.get_headers_spl(msg)
        headers['keyword'] = self.get_keyword(headers)
        headers['date'] = self.get_date(headers)
        headers['mode'] = self.mode
        
        return headers
    
    def get_headers_orig(self, msg):
        headers = [(elem.lower(), item) for (elem, item) in msg.items()]
        #log.info(headers)
        return dict(headers)
    
    def get_headers_spl(self, headers):
        res = dict()
        vals = self.cfg.items('headers')
        for (item, elem) in vals:
            for obj in elem.split(','):
                obj = obj.lower().strip()
                if obj in headers:
                    res[item] = headers[obj]
                    break
        return res
    
    def get_contact(self, headers):
        if 'from' in headers:
            return email.utils.parseaddr(headers['from'])[1]
        return ''
    
    def get_keyword(self, headers):
        if 'caseid' in headers:
            return 'followup'
        else:
            return 'refer'
    
    def get_date(self, headers, date_fmt="%m-%d-%Y %H:%M:%S"):
        if 'date' in headers:
            val = email.utils.parsedate(headers['date'])
            # unpack tuple and get year, month, day, hr, min, sec
            #return datetime.datetime(*val[:6])
            val = datetime.datetime(*val[:6])
        else:
            val = datetime.datetime.now()
        
        return val.strftime(date_fmt)
    
    def get_text_content(self, content):
        try:
            return self.get_text_content(content[0].get_payload())
        except AttributeError:
            return content
    
    def get_attachments(self, content):
        if not isinstance(content, list):
            return dict()
        res = dict()
        for elem in content[1:]:
            fname = elem.get_filename()
            if fname:
                res[fname] = elem.get_payload(decode=True)
        return res
    
    def respond_to_msg(self, contact, headers, text_content, attachments):
        email_send = EmailSender(self.cfg)
        email_send.send_message(contact, headers, text_content, attachments)
    
    def insert_msg_to_db(self, outp):
        cfg = dict(self.cfg.items('database'))
        db = DbLink(**cfg)
        uuid = db.insert_msg(*outp)
        db.close()

class EmailSender:
    def __init__(self, config):
        self.cfg = config
        
        try:
            self.email_params = {'server': self.cfg.get('email', 'smtpserver'),
                                'user': self.cfg.get('email', 'smtpuser'),
                                'passwd': self.cfg.get('email', 'smtppasswd')}
        except ConfigParser.NoSectionError, e:
            raise ConfigError(str(e))
        except ConfigParser.NoOptionError, e:
            raise ConfigError(str(e))
    
    def send_message(self, contact, headers, text_content, attachments):
        # http://snippets.dzone.com/posts/show/757
        msg = MIMEMultipart()
        
        msg.add_header('To', contact)
        for (elem, item) in headers.items():
            msg.add_header(elem.capitalize(), item)
        
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
        serv = smtplib.SMTP(self.email_params['server'])
        serv.ehlo()
        serv.starttls()
        serv.ehlo()
        serv.login(self.email_params['user'], self.email_params['passwd'])
        
        serv.sendmail('', contact, msg)
        serv.quit()

def main():
    opts, args = getopt.getopt(sys.argv[1:], 'hdtc:', ['help', 'debug', 'config-file=', 'test'])
    
    action = args[0]
    #debug_level = logging.INFO
    config_file = '-'
    test_mode = False
    
    for o, a in opts:
        if o in ('-h', '--help'):
            print 'hello'
            sys.exit(0)
        elif o in ('-d', '--debug'):
            pass#debug_level = logging.DEBUG
        elif o in ('-c', '--config-file'):
            config_file = a
        elif o in ('-t', '--test'):
            test_mode = True
    
    if not os.path.exists(config_file):
        raise ConfigError("%s not found" % config_file)
    
    pidfile = 'email.pid'
    if not cmp(action, 'stop') or not cmp(action, 'restart'):
        for elem in stopd(pidfile):
            log.error(elem)
        if not cmp(action, 'restart'):
            action = 'start'
    if not cmp(action, 'start'):
        x = EmailReader(config_file)
        log.info("Daemon PID %d" % startd(pidfile))
        if test_mode:
            x.test_mode()
        else:
            x.run()

if __name__ == '__main__':
    smsfile = '-'
    log = get_logger("emailhandler")
    try:
        main()
    except Exception, e:
        log.error('Exception processing "%s": %s' % (smsfile, e))
        raise
else:
    log = get_logger("emailhandler")