"""
TriageClient module for Triage Server Communication.
"""
import SOAPpy

WS_PROXY	=	"http://10.36.2.112:8080/Triage/"
WS_NAMESPACE	=	"http://ws/"
USERKEY		=	"DUmmy"
SOAP_DEBUG	=	1


class Patient:
	"""
	A class for manipulating patient records, such as saving,
	retrieving, updating and searching.
	"""
	__userkey = None
	__patientid = None
	__firstname = None
	__middlename = None
	__lastname = None
	__maidenname = None
	__sex = None
	__birthdate = None
	__agevalidity = None
	__location = None

	def __init__(self):
		self.__userkey = SOAPpy.stringType(USERKEY)
		SOAPpy.Config.debug = SOAP_DEBUG

		#Assume first that a person has a single case
		#TODO: self.cases should be an array of cases
		self.cases = Case()

		

	def setAll(self, patient_id, firstname, middlename, lastname, \
			maidenname, sex, birthdate, age, agevalidity, location):
		self.__patientid = SOAPpy.stringType(patient_id)
		self.__firstname = SOAPpy.stringType(firstname)
		self.__middlename = SOAPpy.stringType(middlename)
		self.__lastname = SOAPpy.stringType(lastname)
		self.__maidenname = SOAPpy.stringType(maidenname)
		self.__sex = SOAPpy.stringType(sex)
		self.__birthdate = SOAPpy.stringType(birthdate)
		self.__age = SOAPpy.intType(age)
		self.__agevalidity = SOAPpy.stringType(agevalidity)
		self.__location = SOAPpy.stringType(location)
		
	def setPatientId(self, id):
		self.__patientid = SOAPpy.stringType(id)



	def save(self, patient_id, firstname, middlename, lastname, \
			maidenname, sex, birthdate, age, agevalidity, location):
	        """
		Sends the patient information to the server. All parameters
		are of string type except for the age. Birthdate is of the format
		'dd-mm-yyyy'
		Note that the current Triage Server does not support error
		checking yet.
		Note also that this function is not yet European Data Format - Compliant.
		Future versions will be EDF compliant.
		"""
		self.setAll(patient_id, firstname, middlename, lastname, maidenname, \
			sex, birthdate, age, agevalidity, location)
		proxy = SOAPpy.SOAPProxy(WS_PROXY + "CreatePatientService")
		proxy._ns(WS_NAMESPACE).createPatient(userkey=self.__userkey, patientid=self.__patientid, \
				firstname=self.__firstname, middlename = self.__middlename, lastname=self.__lastname, \
				maidenname=self.__maidenname, sex=self.__sex, birthdate=self.__birthdate, \
				agevalidity=self.__agevalidity, age=self.__age, location=self.__location)

	def searchPatients(self, last_name, first_name):
		"""
		Returns an array of patient ids in the database with a 
		last name last_name OR with a first name first_name.
		All arguments are of string type.
		"""
		proxy = SOAPpy.SOAPProxy(WS_PROXY + "ViewPatientService")
		first_name = SOAPpy.stringType(first_name)
		last_name = SOAPpy.stringType(last_name)
		return proxy._ns(WS_NAMESPACE).searchPatients(lastname=last_name, firstname=first_name)

	def getCases(self, id=None):
		"""
		Returns the an array of case ids of the patient with ID id.
		The 'id' argument could be of string or int type.
		"""
		#replace with view
		proxy = SOAPpy.SOAPProxy(WS_PROXY + "ViewCaseService")
		id = SOAPpy.stringType(id)
		return proxy._ns(WS_NAMESPACE).getCases(patientid=id)
	
	def getPatientInfo(self, id):
		"""
		Returns an array of information related to the patient with ID id.
		The 'id' argument could be of string or int type.
		"""
		#replace with view
		proxy = SOAPpy.SOAPProxy(WS_PROXY + "ViewPatientService")
		id = SOAPpy.stringType(id)
		return proxy._ns(WS_NAMESPACE).viewPatient(patientid=id)


		

class Case:
	"""
	A class for manipulating cases or referrals, such as saving, updating
	and retrieving.
	"""
	__userkey__ = None
	__referralid__ = None
	__description__ = None
	__reason__ = None
	__patientid__ = None
	__institutionid__ = None
	__docname__ = None
	__docnum__ = None
	__status__ = None


	def __init__(self):
		self.__userkey = SOAPpy.stringType(USERKEY)
		SOAPpy.Config.debug = SOAP_DEBUG
	
	def setAll(self, referral_id, description, reason, patient_id, institution_id, \
				doctor_name, doctor_num, status):

		#TODO: Make sure that any fields with the same value will still be stored
		self.__referralid=SOAPpy.stringType(referral_id)
		self.__description=SOAPpy.stringType(description)
		self.__reason=SOAPpy.stringType(reason)
		self.__patientid=SOAPpy.stringType(patient_id)
		self.__institutionid=SOAPpy.stringType(institution_id)
		self.__docname=SOAPpy.stringType(doctor_name)
		self.__docnum=SOAPpy.stringType(doctor_num)
		self.__status=SOAPpy.stringType(status)


	def saveCase(self, description, reason, patient_id, institution_id, \
				doctor_name, doctor_num, status):
		"""
		Sends the referral or case information to the Triage Server for
		saving. All arguments are of string type.
		Note that the current Triage Server does not support error
		checking yet.
		Note also that this function is not yet European Data Format - Compliant.
		Future versions will be EDF compliant.		
		"""

		proxy = SOAPpy.SOAPProxy(WS_PROXY + "CreateCaseService")

		#self.__referralid=SOAPpy.stringType(referral_id)
		self.__description=SOAPpy.stringType(description)
		self.__reason=SOAPpy.stringType(reason)
		self.__patientid=SOAPpy.stringType(patient_id)
		self.__institutionid=SOAPpy.stringType(institution_id)
		self.__docname=SOAPpy.stringType(doctor_name)
		self.__docnum=SOAPpy.stringType(doctor_num)
		self.__status=SOAPpy.stringType(status)


		proxy._ns(WS_NAMESPACE).createCase(userkey=self.__userkey, \
				description=self.__description, reason=self.__reason, patientid=self.__patientid, \
				institutionid=self.__institutionid, docname=self.__docname, docnum=self.__docnum, \
				status=self.__status)

	def getCaseInfo(self, case_id = None):
		"""
		Returns an array of strings containing the information about the
		case with id 'case_id'
		Returns an array of NULL if a case could not be found.
		"""
		case_id = SOAPpy.stringType(case_id)
		
		proxy = SOAPpy.SOAPProxy(WS_PROXY + "ViewCaseService")
		return proxy._ns(WS_NAMESPACE).ViewCase(caseid=case_id)


class RxData:
	"""
	A class for manipulating rxdata, such as sending and retrieving
	medical data from Triage Server.
	Note that this is not yet European Data Format - Compliant.
	"""
	__userkey__ = None
	__referralid = None


	def __init__(self):
		self.__userkey = SOAPpy.stringType(USERKEY)
		SOAPpy.Config.debug = SOAP_DEBUG
	

	def sendRxData(self, referral_id, ecgtime, bloodox, bpressureu, bpressured, heartrate, ecgsize, timestamp):
		"""
		Sends medical data to the Triage Server. All arguments
		are of double type except for referral_id which is an int type
		and timestamp which is a string with format dd-mm-yyy
		Future versions will be an EDF - Compliant function.
		"""
		py_referral_id=4
		soap_referralid=SOAPpy.integerType(py_referral_id)

		py_ecgtime=['2008-09-08', '2008-09-07', '2008-09-06']
		soap_ecgtime = SOAPpy.arrayType(py_ecgtime)

		py_ecgy=['20', '7', '12']
		soap_ecgy=SOAPpy.arrayType(py_ecgtime)

		py_bloodox=4
		soap_bloodox=SOAPpy.doubleType(py_bloodox)

		py_bpressureu=3.3
		soap_bpressureu=SOAPpy.doubleType(py_bloodox)

		py_bpressured=3.3
		soap_bpressured=SOAPpy.doubleType(py_bloodox)

		py_heartrate=3.3
		soap_heartrate=SOAPpy.doubleType(py_bloodox)

		py_ecgsize= len(py_ecgtime)
		soap_ecgsize =SOAPpy.doubleType(py_ecgsize) 

		py_timestamp='2008-09-06'
		soap_timestamp=SOAPpy.stringType(py_timestamp)
		
		proxy = SOAPpy.SOAPProxy(WS_PROXY + "SendRxDataService")
		return proxy._ns(WS_NAMESPACE).sendRxData(userkey=self.__userkey, referralid=soap_referralid, ecgtime=soap_ecgtime, ecgy=soap_ecgy, bloodox=soap_bloodox, bpressureu=soap_bpressureu, bpressured=soap_bpressured, heartrate=soap_heartrate, ecgsize=soap_ecgsize, timestamp=soap_timestamp)



