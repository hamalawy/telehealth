import datetime

class Patient:

    def __init__(self,ID = 0,firstname = 'First Name',\
                middlename = 'Middle Name',lastname = 'Last Name',\
                maidenname = 'Maiden Name', gender = 'Gender',\
                birthday = '01.01.01',age = 0):
        
        self.ID = str(ID)
        self.FirstName = firstname
        self.MiddleName = middlename
        self.LastName = lastname
        self.MaidenName = maidenname
        self.Gender = gender
        self.Birthday = birthday
        self.Age = str(age)
        self.LocalPatientID = ''
        self.createLocalID()
        
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

        LocalPatientIDlist = [self.ID, self.FirstName, self.MiddleName,\
                            self.LastName, self.MaidenName, self.Gender,\
                            self.Birthday, self.Age]
        lenLocalPatientID = [lenID, lenFirstName, lenMiddleName,\
                            lenLastName, lenMaidenName, lenGender,\
                            lenBirthday, lenAge]
        
        for i in range(len(LocalPatientIDlist)):
            maxlen = lenLocalPatientID[i]
            if len(LocalPatientIDlist[i]) > maxlen:
                # truncates the string if length is greater than limit
                LocalPatientIDlist[i] = LocalPatientIDlist[i][:maxlen]      
            else:                
                LocalPatientIDlist[i] = LocalPatientIDlist[i].ljust(maxlen)
                
        # converts the list to a string with no separator in between elements
        self.LocalPatientID = ''.join(LocalPatientIDlist)

    def get(self):
        """ returns the LocalPatientID attribute """

        return self.LocalPatientID
        
class BioSignal:
    """contains the biomedical signals of the patient as well as their technical information"""

    def __init__(self, Label = 'Label', TransducerType = '', PhyDimension = 'Dimension',\
                 PhyMin = -32767, PhyMax = 32767, DigMin = -32767, DigMax = 32767, Prefiltering = '',\
                 NRsamples = 1, RawBioSignal = []):
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
        
        self.TechInfo = []                     # list containing 256 bytes of characters describing the technical characteristics of each signal
        self.RawBioSignal = RawBioSignal                # the biomedical signal itself

        self.createTechInfo()
        
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

        self.TechInfo = [self.Label, self.TransducerType, self.PhyDimension, self.PhyMin, self.PhyMax, self.DigMin, self.DigMax, self.Prefiltering,\
                             self.NRsamples, self.Reserved]
        lenTechInfo = [lenLabel, lenTransducerType, lenPhyDimension, lenPhyMin, lenPhyMax, lenDigMin, lenDigMax, lenPrefiltering, lenNRsamples, lenReserved]

        for i in range(len(self.TechInfo)):
            maxlen = lenTechInfo[i]
            if len(self.TechInfo[i]) > maxlen:
                # truncates the string if length is greater than limit
                self.TechInfo[i] = self.TechInfo[i][:maxlen]      
            else:
                
                self.TechInfo[i] = self.TechInfo[i].ljust(maxlen)
                
class EDF:
    """manipulates the Patient and BioSignal objects to create an EDF file"""

    def __init__(self,  Patient, BioSignals, StartDate = '01.01.01', StartTime = '01.59.59', Location = '',\
                 nDataRecord = -1, DurationDataRecord = 1, ):
        # StartDate = dd.mm.yy
        # StartTime = hh.mm.ss
        
        Reserved = ' '*44

        # fields defined in the EDF format
        self.Version = '0'                                   # 0 is the only version number allowed
        self.LocalPatientID = Patient.get()  
        self.LocalRecordingID = 'Startdate ' + Location      # Location should contain a date (DD-MMM-YYYY) and the location of the patient
        self.StartDate = StartDate
        self.StartTime = StartTime
        self.nSignals = str(len(BioSignals))
        self.nBytesHeader = str(256 + 256*int(self.nSignals))
        self.EDFPlus = Reserved
        self.nDataRecord = str(nDataRecord)                  # if unknown, default value is -1 (prior or during recording)
        self.DurationDataRecord = str(DurationDataRecord)

        self.BioSignals = BioSignals
        self.HeaderRecord = ''                               # contains the header record information of the EDF data
        self.DataRecord = ''                                 # contains the 2-byte ASCII encided data record values of the BioSignals
        self.EDFFile = ''                                    # contains the EDF file of a patient and will be saved as .edf
        
        self.Starttime = datetime.datetime.today() + datetime.timedelta(seconds = -15)
        self.timestamp = self.Starttime.strftime("%H%M%S")
        
        self.createHeaderRecord()
        self.createDataRecord()

        
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

        # concatenates each BioSignal TechInfo to the Header Record string
        for i in range(len(self.BioSignals[0].TechInfo)):
            for x in range(len(self.BioSignals)):
                self.HeaderRecord = self.HeaderRecord + self.BioSignals[x].TechInfo[i]


    def createDataRecord(self):
        """creates the data record fields of the EDF file"""

        counter = 0
        DataRecordlist = []
        end = []
        offset = []
        start = []
        temp = []

        for i in range(len(self.BioSignals)):
            offset.append(int(self.BioSignals[i].NRsamples))
            start.append(0)
            end.append(0)
        print "edf loop"
        while (counter < int(self.nDataRecord)):
            
            for x in range(len(self.BioSignals)):

                end[x] = start[x] + offset[x]
                temp =  self.BioSignals[x].RawBioSignal[start[x]:end[x]]

                for i in range(len(temp)):
                    intRawValue = temp[i]

                    if intRawValue >= 0:
                        # if positive-valued, convert to binary
                        binRawValue = bin(intRawValue)[2:].zfill(16)
                    else:
                        # if negative, get the positive representation by adding (2**16-1)
                        # these are the numbers from 32768-65535
                        negRawValue = intRawValue + (2**16-1)
                        # then convert to binary
                        binRawValue = bin(negRawValue)[2:].zfill(16)

                    # divide the 16-bit binary number to two 8-bit binary numbers (MSByte and LSByte)
                    MSByte = binRawValue[:8]
                    LSByte = binRawValue[8:]

                    # convert each byte to decimal then get its ASCII representation 
                    chrMSByte = chr(int(MSByte,2))
                    chrLSByte = chr(int(LSByte,2))

                    # each value in the data record is a 2-byte 2's complement integer represented by its ASCII character
                    # it is arranged as: Value = LSB,MSB
                    DataRecordlist.extend([chrLSByte, chrMSByte])

                # update the pointer for the next set of data records
                start[x] = end[x]

            counter += 1

        # when all BioSignal objects are accessed and encoded, converts the list to a string
        print "end loop"
        self.DataRecord = ''.join(DataRecordlist)
            
    def get(self,myPatient):

        self.EDFFile = ''.join([self.HeaderRecord,self.DataRecord])
        self.edfilename = 'EDF/' + myPatient.LastName + '_' + self.timestamp + '.edf'
        edffile   = open(self.edfilename, 'wb+')
        edffile.write(self.EDFFile)
        edffile.close()
