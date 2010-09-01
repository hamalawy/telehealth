"""
Project LifeLink: edfviewer Module
Contains classes and methods used in viewing an EDF file. It displays
the header record and plots the signals in the data record using
matplotlib.

Authors: Julius Miguel J. Broma
         Arlan Roie A. Santos
         Luis G. Sison, PhD
         ------------------------------------------------
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         ------------------------------------------------
         January 2008
"""

import matplotlib.pyplot as plt
import copy

class BioSignal:
    """ contains the technical characteristics of a biosignal """

    def __init__(self):
        
        # Technical information fields specific for a signal (Header Record)
        self.Label          = ''                           
        self.TransducerType = ''
        self.PhyDimension   = ''
        self.PhyMin         = 0   
        self.PhyMax         = 0
        self.DigMin         = 0                       
        self.DigMax         = 0                       
        self.Prefiltering   = ''
        self.NRsamples      = 0
        self.Reserved       = ''
        self.RawBioSignal   = []

        self.TechInfolist = [self.Label, self.TransducerType, self.PhyDimension,\
                             self.PhyMin, self.PhyMax, self.DigMin, self.DigMax,\
                             self.Prefiltering, self.NRsamples, self.Reserved]
        
class EDF_File:
    """ manipulates an EDF file """

    def __init__(self, filename):
        """ opens the desired EDF file with the given filename and sets the attributes of the class """

        self.filename      = filename
        self.HeaderRecord  = ''
        self.TechnicalInfo = ''
        self.DataRecord    = ''
        self.BioSignals    = []
        # list of integers version of self.DataRecord
        self.DataRecord_int = []
        # parsed DataRecord per signal
        self.RawBioSignal = []

        # Header Record fields
        self.Version            = 0
        self.LocalPatientID     = ''
        self.LocalRecordingID   = ''
        self.StartDate          = ''
        self.StartTime          = ''
        self.nBytesHeader       = 0
        self.EDFPlus            = ''
        self.nDataRecord        = 0
        self.DurationDataRecord = 0
        self.nSignals           = 0
        
        # open the EDF file with the given filename
        try:
            self.file     = open(self.filename, 'rb')
            self.values   = self.file.read()
            self.file.close()
        except TypeError:
            self.values   = self.filename

        self.getPatientInfo()
        self.getTechnicalInfo()


    def getPatientInfo(self):
        """ gets the Patient's information and the recording details of the EDF file """

        self.nBytesHeader = int(self.values[184:192])
        self.HeaderRecord = self.values[:self.nBytesHeader]

        self.Version            = self.HeaderRecord[0:8]
        self.LocalPatientID     = self.HeaderRecord[8:88]
        self.LocalRecordingID   = self.HeaderRecord[88:168]
        self.StartDate          = self.HeaderRecord[168:176]
        self.StartTime          = self.HeaderRecord[176:184]
        self.EDFPlus            = self.HeaderRecord[192:236]
        self.nDataRecord        = self.HeaderRecord[236:244]
        self.DurationDataRecord = self.HeaderRecord[244:252]
        self.nSignals           = int(self.HeaderRecord[252:256])
        
    def getTechnicalInfo(self):
        """ gets the technical information of each signal """

        self.TechnicalInfo = self.values[256:self.nBytesHeader]
        self.TechInfotext  = ['Signal Label       :',\
                              'Transducer Type    :',\
                              'Physical Dimension :',\
                              'Physical Minimum   :',\
                              'Physical Maximum   :',\
                              'Digital Minimum    :',\
                              'Digital Maximum    :',\
                              'PreFiltering       :',\
                              'Number of Samples  :',\
                              'Reserved           :']    
        Lengthlist = [16, 80, 8, 8, 8, 8, 8, 80, 8, 32]
        Fieldstart = 0
        
        # create a BioSignal object for every biomedical signal
        for i in range(self.nSignals):
            self.BioSignals.append(BioSignal())

        for i in range(len(Lengthlist)):
            FieldLength = self.nSignals * Lengthlist[i]
            Fieldend = Fieldstart + FieldLength
            persignalfield = self.TechnicalInfo[Fieldstart:Fieldend]
            persignalstart = 0
            
            for x in range(len(self.BioSignals)):
                persignalend = persignalstart + Lengthlist[i]
                self.BioSignals[x].TechInfolist[i] = persignalfield[persignalstart:persignalend]
                persignalstart = persignalend

            Fieldstart = Fieldend
        
    def parseDataRecords(self):
        """ plots each signal in the data record """

        counter = 0
        end = []
        offset = []
        start = 0
        temp = []
        
        
        self.DataRecord = self.values[self.nBytesHeader:]
        tempDataRecord = list(self.DataRecord)

        def DecToBin(num):
            BinStr = ''
            if num == 0: return '0'*8
            while num > 0:
                BinStr = str(num % 2) + BinStr
                num = num >> 1
            BinStr = BinStr.zfill(8)
            return BinStr
        temp=[]

        for i in range(len(self.DataRecord)):
            intvalue = ord(tempDataRecord[i])
            binvalue = DecToBin(intvalue)
            temp.append(binvalue)
#            tempDataRecord.remove(tempDataRecord[i])
#            tempDataRecord.insert(i,binvalue)
        tempDataRecord=copy.copy(temp)

        for i in range(0,len(tempDataRecord),2):
            LSByte = tempDataRecord[i]
            MSByte = tempDataRecord[i+1]
            int_2bytedata = int(MSByte + LSByte,2)

            if int_2bytedata <= 32767:
                self.DataRecord_int.append(int_2bytedata)

            else:
                negative_num = int_2bytedata - (2**16-1)
                self.DataRecord_int.append(negative_num)

        for i in range(len(self.BioSignals)):
            offset.append(int(self.BioSignals[i].TechInfolist[8]))
            end.append(0)
            self.RawBioSignal.append([])

        while (counter < int(self.nDataRecord)):
            
            for i in range(len(self.BioSignals)):

                end[i] = start + offset[i]
                temp = self.DataRecord_int[start:end[i]]
                self.RawBioSignal[i].extend(temp)
                start = end[i]
                
            counter += 1
                
        return (self.RawBioSignal)

    def plotDataRecords(self):
        """ plot the signals """

        for i in range(len(self.RawBioSignal)):

            plt.subplot(len(self.RawBioSignal),1,i + 1)
            plt.plot(self.RawBioSignal[i])

        plt.show()    


            
                
        
            

        
            
