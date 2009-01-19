"""
LifeLink edf Module
Contains classes and methods used in encapsulating acquired raw biomedical signals
into European Data Format (EDF) - a standard used for the exchange and storage of
medical time-series recordings. It produces a .edf file which can be tested using
available edf viewer software.

Authors: Julius Miguel J. Broma
         Arlan Roie A. Santos
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         
"""

class Patient:
    """contains information about the patient"""

    def __init__(self, ID, firstname, middlename, lastname, maidenname, gender, birthday, age):
        # gender = 'Male' or 'Female'
        # birthday = mm.dd.yy
        
        self.ID = str(ID)
        self.FirstName = firstname
        self.MiddleName = middlename
        self.LastName = lastname
        self.MaidenName = maidenname
        self.Gender = gender
        self.Birthday = birthday
        self.Age = str(age)
        self.LocalPatientID = ''
       
        

    def createLocalID(self):
        """encodes the patient information to the LocalPatientID in the EDF header record field"""

        # ascii-character limit for every patient information (in bytes)
        lenID = 5
        lenFirstName = 20
        lenMiddleName = 12
        lenLastName = 12
        lenMaidenName  = 12
        lenGender = 6
        lenBirthday = 10
        lenAge = 3

        LocalPatientIDlist = [self.ID, self.FirstName, self.MiddleName, self.LastName, self.MaidenName, self.Gender, self.Birthday, self.Age]
        lenLocalPatientID = [lenID, lenFirstName, lenMiddleName, lenLastName, lenMaidenName, lenGender, lenBirthday, lenAge]
        
        for i in range(len(LocalPatientIDlist)):
            maxlen = lenLocalPatientID[i]
            if len(LocalPatientIDlist[i]) > maxlen:
                # truncates the string if length is greater than limit
                LocalPatientIDlist[i] = LocalPatientIDlist[i][:maxlen]      
            else:
                
                LocalPatientIDlist[i] = LocalPatientIDlist[i].ljust(maxlen)
                
        # converts the list to a string with no separator in between elements
        self.LocalPatientID = ''.join(LocalPatientIDlist)                   
        
class BioSignal:
    """contains the biomedical signals of the patient as well as their technical information"""

    def __init__(self, Label, TransducerType, PhyDimension, PhyMin, PhyMax, DigMin, DigMax, Prefiltering,NRsamples, RawBioSignal):
        # Label = Standard: 'TypeOfSignal Sensor'
        # DigMin > -32767
        # DigMax <  32767
        
        Reserved = ' '*32

        # fields defined in the EDF format
        self.Label = Label                           
        self.TransducerType = TransducerType
        self.PhyDimension = PhyDimension
        self.PhyMin = str(PhyMin)   
        self.PhyMax = str(PhyMax)
        self.DigMin = str(DigMin)                       
        self.DigMax = str(DigMax)                       
        self.Prefiltering = Prefiltering
        self.NRsamples = str(NRsamples)
        self.Reserved = Reserved
        
        self.TechnicalInfolist = []                     # list containing 256 bytes of characters describing the technical characteristics of each signal
        self.RawBioSignal = RawBioSignal                # the biomedical signal itself
        
    def createTechInfo(self):
        """encodes the biomedical signal technical information to the EDF header record"""

        # ascii-character limit for every biosignal information (in bytes)
        lenLabel = 16
        lenTransducerType = 80
        lenPhyDimension = 8
        lenPhyMin = 8
        lenPhyMax = 8
        lenDigMin = 8
        lenDigMax = 8
        lenPrefiltering = 80
        lenNRsamples = 8
        lenReserved = 32

        self.TechnicalInfolist = [self.Label, self.TransducerType, self.PhyDimension, self.PhyMin, self.PhyMax, self.DigMin, self.DigMax, self.Prefiltering,\
                             self.NRsamples, self.Reserved]
        lenTechnicalInfo = [lenLabel, lenTransducerType, lenPhyDimension, lenPhyMin, lenPhyMax, lenDigMin, lenDigMax, lenPrefiltering, lenNRsamples, lenReserved]

        for i in range(len(self.TechnicalInfolist)):
            maxlen = lenTechnicalInfo[i]
            if len(self.TechnicalInfolist[i]) > maxlen:
                # truncates the string if length is greater than limit
                self.TechnicalInfolist[i] = self.TechnicalInfolist[i][:maxlen]      
            else:
                
                self.TechnicalInfolist[i] = self.TechnicalInfolist[i].ljust(maxlen)


class EDF:
    """manipulates the Patient and BioSignal objects to create an EDF file"""

    def __init__(self, StartDate, StartTime, Location, nDataRecord, DurationDataRecord, Patient, BioSignals, EDFfileCount):
        # StartDate = dd.mm.yy
        # StartTime = hh.mm.ss
        
        Reserved = ' '*44

        # fields defined in the EDF format
        self.Version = '0'                                   # 0 is the only version number allowed
        self.LocalPatientID = Patient.LocalPatientID    
        self.LocalRecordingID = 'Startdate ' + Location      # Location should contain a date (DD-MMM-YYYY) and the location of the patient
        self.StartDate = StartDate
        self.StartTime = StartTime
        self.nSignals = str(len(BioSignals))
        self.nBytesHeader = str(256 + 256*int(self.nSignals))
        self.EDFPlus = Reserved
        self.nDataRecord = str(nDataRecord)                  # if unknown, default value is -1 (prior or during recording)
        self.DurationDataRecord = str(DurationDataRecord)
        self.EDFfileCount = str(EDFfileCount)  # counts the number of edf files produced

        self.Patient = Patient
        self.BioSignals = BioSignals
        self.HeaderRecord = ''                               # contains the header record information of the EDF data
        self.DataRecord = ''                                 # contains the 2-byte ASCII encided data record values of the BioSignals
        self.EDFFile = ''                                    # contains the EDF file of a patient and will be saved as .EDF
        
        
    def createHeaderRecord(self):
        """creates the header record fields of the EDF file"""

        # ascii-character limit for every header record information (in bytes)
        lenVersion = 8
        lenLocalPatientID = 80
        lenLocalRecordingID = 80
        lenStartDate = 8
        lenStartTime = 8
        lennBytesHeader = 8
        lenEDFPlus = 44
        lennDataRecord = 8
        lenDurationDataRecord = 8
        lennSignals = 4
    
        HeaderInfolist = [self.Version, self.LocalPatientID, self.LocalRecordingID, self.StartDate, self.StartTime, self.nBytesHeader, self.EDFPlus,\
                          self.nDataRecord, self.DurationDataRecord, self.nSignals]
        lenHeaderInfo = [lenVersion, lenLocalPatientID, lenLocalRecordingID, lenStartDate, lenStartTime, lennBytesHeader, lenEDFPlus, lennDataRecord,\
                         lenDurationDataRecord, lennSignals]

        for i in range(len(HeaderInfolist)):
            maxlen = lenHeaderInfo[i]
            if len(HeaderInfolist[i]) > maxlen:
                # truncates the string if length is greater than limit
                HeaderInfolist[i] = HeaderInfolist[i][:maxlen]      
                
            else:
                HeaderInfolist[i] = HeaderInfolist[i].ljust(maxlen)
                
        # converts the list to a string with no separator in between elements
        self.HeaderRecord = ''.join(HeaderInfolist)                 

        # concatenates each BioSignal TechnicalInfo to the Header Record string
        for i in range(len(self.BioSignals[0].TechnicalInfolist)):
            for x in range(len(self.BioSignals)):
                self.HeaderRecord = self.HeaderRecord + self.BioSignals[x].TechnicalInfolist[i]


    def createDataRecord(self):
        """creates the data record fields of the EDF file"""

        DataRecordlist = []

        def DecToBin(num):
            # converts a decimal number to its 16-bit binary representation
            
            BinStr = ''
            if num == 0: return '0'*16
            while num > 0:
                BinStr = str(num % 2) + BinStr
                num = num >> 1                   # right-shift the num by 1 bit
            BinStr = BinStr.zfill(16)            # make BinStr a 16-bit string
            return BinStr

        for i in range(len(self.BioSignals)):
            for x in range(len(self.BioSignals[i].RawBioSignal)):       
                intRawValue = self.BioSignals[i].RawBioSignal[x]

                if intRawValue >= 0:
                    # if positive-valued, convert to binary
                    binRawValue = DecToBin(intRawValue)
                else:
                    # if negative, get the positive representation by adding (2**16-1)
                    # these are the numbers from 32768-65535
                    negRawValue = intRawValue + (2**16-1)
                    # then convert to binary
                    binRawValue = DecToBin(negRawValue)

                # divide the 16-bit binary number to two 8-bit binary numbers (MSByte and LSByte)
                MSByte = binRawValue[:8]
                LSByte = binRawValue[8:]

                # convert each byte to decimal then get its ASCII representation 
                chrMSByte = chr(int(MSByte,2))
                chrLSByte = chr(int(LSByte,2))

                # each value in the data record is a 2-byte 2's complement integer represented by its ASCII character
                # it is arranged as: Value = LSB,MSB
                DataRecordlist.extend([chrLSByte, chrMSByte])

        # when all BioSignal objects are accessed and encoded, converts the list to a string
        self.DataRecord = ''.join(DataRecordlist)

      
    def createEDF(self):
        """integrates the created Header Record field with the Data Record field to create a complete EDF file"""
        
        self.EDFFile = self.HeaderRecord + self.DataRecord

#        filename = raw_input('Enter filename to save the file: ')

        edffile = open('C:/Users/ARLAN ROIE SANTOS/Desktop/' + 'testfile' + self.EDFfileCount + '.edf', 'wb+')    # temporarily stores to Desktop (in Windows)
        edffile.write(self.EDFFile)
        edffile.close()


        


        
            

