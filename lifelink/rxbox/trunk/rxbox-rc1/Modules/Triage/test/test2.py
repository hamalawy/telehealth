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

  headers = {'Subject': 'refer rxbox test 1', 'X-Eccs-Priority': 'emergency', 
	      'X-Eccs-Rxboxextension': '2001', 'X-Eccs-Test': '1'}
  body='Patient not breathing.'
  afilename=['Ebido_113056.edf']
  attach={}

  for i in afilename:
	f = open(i, 'r')
	attach[i] = f.read()
	f.close()
	
  print "sending..\n";
  triage.request(headers, body, attach)
  print "sent";

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        raise

