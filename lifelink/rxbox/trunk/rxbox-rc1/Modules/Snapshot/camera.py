#!/usr/bin/env python

import ConfigParser
import os
from subprocess import *
import time
from datetime import datetime

"""
tnow = datetime.now()
tnow = tnow.strftime("%Y_%m_%d_%H_%M_%S")+("_%s"%tnow.microsecond.__str__().replace('.',''))
print tnow

filename = tnow + '.jpg'

pathname = '/home/tim/Desktop/Tim/telehealth/trunk/rxbox-rc1/Modules/Snapshot/webcam.cfg'

config = ConfigParser.ConfigParser()
config.read(pathname)
config.set('grab', 'archive', filename)
config.set('ftp', 'file', filename)
with open('webcam.cfg', 'wb') as configfile:
    config.write(configfile)
"""
print 'webcam %s/Modules/Snapshot/webcam.cfg'%os.getcwd()
p = Popen('webcam %s/Modules/Snapshot/webcam.cfg'%os.getcwd(), shell=True)
time.sleep(2)
os.system('kill -15 %d'%(p.pid + 1))
p.kill()


