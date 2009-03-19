import sys, binascii
from Messenger import Messenger
from CreateCaseService_client import *
from CreatePatientService_client import *
from ViewCaseService_client import *
from ViewPatientService_client import *
from SendRxDataService_client import *
from ViewRxDataService_client import *

USERKEY = "DUmmy"

class Triage:
    def __init__(self, messenger=None):
	if (messenger is None):
		self.messenger = None
		print 'Warning: No messenger initialized. Signaling is disabled.'
	else:
		self.messenger = messenger

    def savePatient(self, *args, **kwds):
        loc = CreatePatientServiceLocator()
        port = loc.getCreatePatientPort()
        req = createPatient()

        req.Age=int(kwds['Age'])
        req.Agevalidity=kwds['Agevalidity']
        req.Birthdate=kwds['Birthdate']
        req.Firstname=kwds['Firstname']
        req.Lastname=kwds['Lastname']
        req.Location=kwds['Location']
        req.Middlename=kwds['Middlename']
        req.Patientid=kwds['Patientid']
        req.Sex=kwds['Gender']
        req.Userkey=USERKEY

        resp = port.createPatient(req)
	if (self.messenger is not None):
		stat = 'PatientSaved,'+ req.Patientid
		self.messenger.sendMessage(stat, None, 'rxbstat')
        return resp.Result


    def getPatient(self, patientid):
        loc = ViewPatientServiceLocator()
        port = loc.getViewPatientPort()
        req = viewPatient()

        req.Patientid = patientid

        resp = port.viewPatient(req)
	
	if (self.messenger is not None):
		stat = 'PatientOpened,'+ req.Patientid
		self.messenger.sendMessage(stat, None, 'rxbstat')
        return resp.Result

    def searchPatient(self, lastname, firstname):
        loc = ViewPatientServiceLocator()
        port = loc.getViewPatientPort()
        req = searchPatients()
        req.Firstname = firstname
        req.Lastname = lastname

        resp = port.searchPatients(req)
        return resp.Result

    def saveCase(self, *args, **kwds):
        loc = CreateCaseServiceLocator()
        port = loc.getCreateCasePort()
        req = createCase()

        req.Patientid = kwds['Patientid']
        req.Description = kwds['Description']
        req.Reason = kwds['Reason']
        req.Institutionid = kwds['Institutionid']
        req.Docname = kwds['Doctor']
        req.Docnum = kwds['Docnumber']
        req.Userkey = USERKEY

        resp = port.createCase(req)
	
	if (self.messenger is not None and resp.Result is not -1):
		stat = 'CaseSaved,' + resp.Result + ',' + req.Patientid
		self.messenger.sendMessage(stat, None, 'rxbstat')
        return resp.Result

    def searchCase(self, patientid):
        loc = ViewCaseServiceLocator()
        port = loc.getViewCasePort()
        req = getCases()
        req.Patientid = patientid

        resp = port.getCases(req)
        return resp.Result


    def getCase(self, caseid):
        loc = ViewCaseServiceLocator()
        port = loc.getViewCasePort()
        req = viewCase()
        req.Caseid = caseid

        resp = port.viewCase(req)
	if (self.messenger is not None):
		stat = 'CaseOpened,'+ req.Caseid
		self.messenger.sendMessage(stat, None, 'rxbstat')
        return resp.Result


    def sendEDF(self, caseid, edfbin):
        loc = SendRxDataServiceLocator()
        port = loc.getSendRxDataPort()
        req = fileUpload()

        data = binascii.b2a_base64(edfbin)

	#print dir(req)
        req.Data = data
        req.Caseid = caseid
        resp = port.fileUpload(req)
	if (self.messenger is not None and resp.Result is not -1):
		stat = 'DataSaved,' + resp.Result + ',' + req.Caseid
		self.messenger.sendMessage(stat, None, 'rxbstat')
	return resp.Result

    def getB64EDF(self, caseid, dataid):
        loc = ViewRxDataServiceLocator()
        port = loc.getViewRxDataPort()
        req = fileDownload()

        req.Dataid = dataid
        req.Caseid = caseid
        resp = port.fileDownload(req)
	
	if (self.messenger is not None):
		stat = 'DataOpened,'+ req.Dataid
		self.messenger.sendMessage(stat, None, 'rxbstat')
        return resp.Result

    def getBinEDF(self, caseid, dataid):
	return binascii.a2b_base64(self.getB64EDF(caseid, dataid))
    
    
    ### START: Temporary Methods###
    def getLatestPatient(self):
        loc = ViewPatientServiceLocator()
        port = loc.getViewPatientPort()
        req = getLatestPatient()

        resp = port.getLatestPatient(req)
        return resp.Result

    def getLatestCase(self):
        loc = ViewCaseServiceLocator()
        port = loc.getViewCasePort()
        req = getLatestCase()

        resp = port.getLatestCase(req)
        return resp.Result
    
    def getLatestEDF(self):
        loc = ViewRxDataServiceLocator()
        port = loc.getViewRxDataPort()
        req = getLatestEDF()
        resp = port.getLatestEDF(req)

	return binascii.a2b_base64(resp.Result)
    ### END: Temporary Methods ###
