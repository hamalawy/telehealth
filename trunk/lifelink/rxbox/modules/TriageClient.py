import sys, binascii
sys.path.append('webservices/')
from CreateCaseService_client import *
from CreatePatientService_client import *
from ViewCaseService_client import *
from ViewPatientService_client import *
from SendRxDataService_client import *
from ViewRxDataService_client import *

USERKEY = "DUmmy"

class Triage:
    def __init__(self):
	pass

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
        return resp.Result


    def getPatient(self, patientid):
        loc = ViewPatientServiceLocator()
        port = loc.getViewPatientPort()
        req = viewPatient()

        req.Patientid = patientid

        resp = port.viewPatient(req)
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
        return resp.Result


    def sendEDF(self, caseid, edfbin):
        #If filename is not given, send  parsed version of biomedical data
        #else, send edf file given
        if (parsed == False):
            pass
        else:
            loc = SendRxDataServiceLocator()
            port = loc.getSendRxDataPort()
            req = fileUpload()

            data = binascii.b2a_base64(edfbin)

            #TODO: req.Name should be req.caseid. Coordinate with Pepz
            req.Data = data
            req.Name = "temporary"
            resp = port.fileUpload(req)

    def getB64EDF(self, caseid, timestamp):
            loc = ViewRxDataServiceLocator()
            port = loc.getViewRxDataPort()
            req = fileDownload()

            req.Timestamp = timestamp
            req.Caseid = caseid
            resp = port.fileDownload(req)

            return resp.Result

    def getBinEDF(self, caseid, timestamp):
	return binascii.a2b_base64(getB64EDF(caseid, timestamp))
