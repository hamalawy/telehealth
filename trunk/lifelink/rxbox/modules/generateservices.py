#!/usr/bin/python

import os

URL 		= "http://10.32.148.253:81/Triage/"
services	= ["CreatePatient", "CreateCase", "SendRxData", \
			"ViewPatient", "ViewCase", "ViewRxData"]

for service in services:
	print "Generating python code for %s%sService?wsdl" % (URL, service)
	os.system("wsdl2py --complexType %s%sService?wsdl" % (URL, service))
