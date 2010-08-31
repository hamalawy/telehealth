#!/usr/bin/python

import time, signal, sys
sys.path.append("../")

from triage import Triage


def signal_handler(signal, frame):
        print 'Stopped.'
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def main():
  triage = Triage('/home/jerome/Desktop/WORKAREA/v2/Gui/triage/email.cfg')

  triage.login()

  headers = {'Subject': 'cobra bite', 'X-Eccs-Priority': 'emergency', 
	      'X-Eccs-Rxboxextension': '2001'}
  body='Patient not breathing.'

  triage.request(headers, body)
  response = triage.wait()


  print response

  while True:
    for i in range(1,5):
	response['filename'] = "file%s.jpg" % (i,)
	response['sequence_id'] = i
    	triage.upload(response)
	time.sleep(15)

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        raise

