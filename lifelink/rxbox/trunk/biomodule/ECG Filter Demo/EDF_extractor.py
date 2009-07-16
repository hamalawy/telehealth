#import matplotlib.pyplot

def DecToBin(num):
    """ DecToBin(num) -> binary string of num """
    BinStr = ''
    if num == 0: return '0'*8
    while num > 0:
        BinStr = str(num % 2) + BinStr
        num = num >> 1                  # right-shift the num by 1 bit
    BinStr = BinStr.zfill(8)            # make BinStr an 8-bit string
    return BinStr

def ExtractLabels(HeaderFile,Signal_count):
        """ ExtractLabels(HeaderFile,n) -> ECG Lead types, Lead Sampling Rates

            Extracts the 12 lead ECG labels as well as the sampling rate of
            each lead. Valid lead types are:
            I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6            
        """
        ECGlabel = {}
        ECGsampling = [i*0 for i in range(Signal_count)]
        for i in range(Signal_count):
                label = HeaderFile[256+(16*i):272+(16*i)] # extract the lead type i's label
                sampling = int(HeaderFile[2848+(8*i):2854+(8*i)]) # extract lead type i's sampling rate
                ECGlabel[i] = RemoveSpace(label)
                ECGsampling[i] = sampling
        return ECGlabel, ECGsampling

def ExtractLead(tempDataRecord,index,start,duration,fs,n):
        """ Extracts a duration of data starting from 'start' from raw data """
        lead = []
        for i in range(duration):
                lead[(i*1000):(i*1000)+1000] = tempDataRecord[((i+start)*2*fs*n)\
                                    +((index+1)*1000):((i+start)*2*fs*n)+((index+2)*1000)]
        return lead

def RawToBinary(leadII):
        """ Converts the list of integer data to binary strings """
        for i in range(len(leadII)):
                intvalue = ord(leadII[i])
                binvalue = DecToBin(intvalue)
                leadII.remove(leadII[i])
                leadII.insert(i,binvalue)
        return leadII

def BinaryTomV(leadII):
        """ Convert the binary string representation of data to mV """
        DataRecord_Int = []
        for i in range(0,len(leadII),2):
                LSByte = leadII[i]
                MSByte = leadII[i+1]
                int_2bytedata = int(MSByte + LSByte,2)
                if int_2bytedata <= 32767:
                        DataRecord_Int.append(int_2bytedata)
                else:
                        negative_num = int_2bytedata - (2**16-1)
                        DataRecord_Int.append(negative_num)
        for i in range(len(DataRecord_Int)):
            DataRecord_Int[i] = DataRecord_Int[i]*0.00263
        return DataRecord_Int

def writeFile(File,Data):
        """ writeFile(File,Data) -> writes the contents of list Data to File """
        leadII_file = open(File,'w')
        for i in range(len(Data)):
                leadII_file.write(str(Data[i]))
                leadII_file.write(',\n')
        leadII_file.close()

def RemoveSpace(string):
        """ remove spaces to the string """
        for i in range(len(string)):
            if string[i] == ' ':
                string = string[:i]
                break;
        return string

def CheckLabel(lead, ECGlabel):
    """ (lead, ECGlabel) -> determine if lead is in tuple ECGlabel """
    for i in range(len(ECGlabel)):
        if ECGlabel[i] == lead:
            return True
    return False

def getEDFparameters(ECGlabel,ECGSampling,lead_type):
    """ Extracts the index and sampling rate of specified lead_type from ECGlabel """
    for i in range(len(ECGlabel)):
        if ECGlabel[i] == lead_type:
            index = i
            sampling_rate = ECGSampling[i]
    return index, sampling_rate

def ExtractECG(InputFile, OutputFile, lead_type, duration, start):
        """ ExtractECG(InputFile, OutputFile, lead_type, duration, start)

            This Method extracts a specified ECG signal from InputFile.
            Parameters:
                Lead -> a list of Lead II ECG Signal values
                InputFile -> edf file containing 12-lead ECG signals
                OutputFile -> File where the values are to be printed
                lead_type -> determines which ECG signal to be extracted (ex. "II")
                duration -> number of seconds to be extraced
                start -> determines where to start extracting data

            Duration should be in seconds and should not exceed the total duration
            the ECG signal. start should be an integer greater than zero but less
            than or equal to the total duration minus the desired duration to be
            extracted from the ECG signal.

            Ex.
                ExtractECG('Sison,Luis.edf','leadII.csv','II',15,30)

                The output file 'leadII.csv' will contain values (in mV) of
                the lead 'II' signal of 'Sison,Luis.edf'. The output file will
                contain 15 seconds worth of data starting from the 30th second
                after the telemetry was started.
        """
        # Read and store the data contained in the input File
        myEDFFile = open(InputFile,'rb')
        EDFValues = myEDFFile.read()
        myEDFFile.close()

        # Extract the Header File that contains info about the record
        HeaderSize = int(EDFValues[184:192])
        HeaderFile = EDFValues[:HeaderSize]
        # Extract the actual data in the input file
        rawDataRecord = EDFValues[HeaderSize:]
        tempDataRecord = list(rawDataRecord)

        # Extract information from the EDF Header File
        duration_per_sample = int(HeaderFile[236:244]) # duration per sample (in seconds)
        total_duration = int(HeaderFile[236:244]) # total duration of the signal (in seconds)
        n = int(HeaderFile[252:256]) # number of signals in edf file

        # Determine the signal to be extracted by using the lead_type
        # provided before calling the function
        [ECGlabel, ECGSampling] = ExtractLabels(HeaderFile,n) # extract signals from edf file
        [index, fs] = getEDFparameters(ECGlabel,ECGSampling,lead_type) # determine the signal and sampling rate

        # Check for possible errors in function call
        # 1. Determine the validity of lead type
        if not CheckLabel(lead_type, ECGlabel):
            print "ERROR: ECG Label not found."
            return None
        # 2. Determine if the desired duration to be extracted
        #    is less than the total duration
        elif duration > total_duration:
            print "ERROR: Duration to be extracted is longer than the signal duration."
            return None
        # 3. Determine if the desired duration to be extracted
        #    is within the signal in the EDF file
        elif start > total_duration - duration:
            print "ERROR: start time will not accomodate specified duration"
            return None

        # Extract the desired portion of signal and store it to output file
        lead = ExtractLead(tempDataRecord,index,start,duration,fs,n) # Extract the desired duration of the signal
        lead = RawToBinary(lead) # Convert data readings to 2 Byte, Binary Form
        DataRecord_Int = BinaryTomV(lead) # Convert the 2 Byte binary data to mV
        writeFile(OutputFile,DataRecord_Int) # Write the extracted data to Output File
        return DataRecord_Int
        #matplotlib.pyplot.plot(DataRecord_Int)
        #matplotlib.pyplot.show()
