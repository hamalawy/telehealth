#! /usr/bin/env python
# rcx web service client with ZSI

import sys

from ZSI import TC
from ZSI.client import Binding

serverPath = 'http://perfumesorry:8080/Triage/CreateCaseService'
myns = 'http://ws/'

mybind = Binding(url=serverPath, nsdict={'ns1':myns, 'ns2':myns}, tracefile=sys.stdout)

# we define a class mapping 
# the parameter for the function readLS
class CreateCaseRequest:
  def __init__(self, userkey, description, reason, patientid, institutionid, docname, docnum):
    self.userkey = userkey
    self.description = description
    self.reason = reason
    self.patientid = patientid
    self.institutionid = institutionid
    self.docname = docname
    self.docnum = docnum

CreateCaseRequest.typecode = TC.Struct(CreateCaseRequest,
[TC.String('userkey'),
TC.String('description'),
TC.String('reason'),
TC.String('patientid'),
TC.String('institutionid'),
TC.String('docname'),
TC.String('docnum')],
pname="ns1:createCase",
inline=1)


class CreateCaseResponse:
  def __init__(self, result='false'):
    self.result = result

  def __str__(self):
    return self.result

CreateCaseResponse.typecode = TC.Struct(CreateCaseResponse,
[TC.String('result')], 'createCaseResponse')


try:

  # call readLS
  mybind.Send(serverPath, 'ns1:createCase',  CreateCaseRequest('y', '2', '2' ,'3', '4','5', '5'),  nsdict={'ns1':myns})
  result = mybind.Receive(CreateCaseResponse.typecode)

  # print the results
  print 'Light sensor simulation: %s' % result

except:
  raise
  print 'reply=', mybind.reply_code
  print 'reply_msg=', mybind.reply_msg
  print 'headers=', mybind.reply_headers
  print 'data=', mybind.data

