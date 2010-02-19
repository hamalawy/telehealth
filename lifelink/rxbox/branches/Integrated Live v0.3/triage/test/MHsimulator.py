#!/usr/bin/python
from mailer import EmailSender

import time
def main():
  sender = EmailSender('MHsimulator.cfg')

  headers = {'Subject': 'cobra bite', 'X-Eccs-priority': 'emergency', 
	      'X-Eccs-Caseid': '8888', 'X-Eccs-Uploadurl': 'http://localhost/upload.cgi',
	      'X-Eccs-Rxboxticket': '9999'}
  body='Patient not breathing.'
  sendto = 'dttb.rxbox@gmail.com'
  
  sender.send_message(sendto, headers, body, {})

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        raise

