import scipy
import time
import leadcalc
import string
from string import atoi
from filters import besselfilter
from filters import besselfilter
from matplotlib import pyplot

class ECG:
    """manages data request and processes reply packets to/from ECG module"""

    def __init__(self):
        """initializes port settings and request data sequence according to specified setting for EMI12"""
        
        self.logfile = '12lead40lines.txt'
        self.data_sequence = []             # initialize data_sequence as a list -> to hold old data_sequence and (new)data_sequence_w/checksum
        self.packet_num = 0                 # intitialize packet number = 0
        self.checksum_list = []             # initialize checksum data as a list(tuple) 
        self.Request = ''                   # initialize request as a string
        self.old_dataset_counter = 0        # initialize old value for counter for datasets
        self.prev_dataset_counter = 0       # initialize previous dataset counter

        self.start_flag = 0                 # if start_flag is 1, don't send start_ecg request anymore
        self.required_nr_samples = 1500     # required number of samples for a 15sec DAQ with sampling rate of 100Hz
        self.resolution = 0.00263           # resolution of ecg reading in mV/bit
        self.ecg_leadI = []
        self.ecg_leadII = []                # "dynamic" list that continuously accommodates lead II readings
        self.ecg_leadIII = []               # "dynamic" list that continuously accommodates lead III readings
        self.ecg_leadaVR = []
        self.ecg_leadaVL = []
        self.ecg_leadaVF = []
        self.ecg_leadV1 = []
        self.ecg_leadV2 = []
        self.ecg_leadV3 = []
        self.ecg_leadV4 = []
        self.ecg_leadV5 = []
        self.ecg_leadV6 = []
        
        self.daqduration = 15               # DAQ duration in seconds
        self.firmware_string = ''           # initialize the string which will contain the firmware version
        self.device_ready_counter = 0       # initialize the counter for device ready checking
        self.ecmbyte1 = []                  # initialize the offline ecm status byte1 for electrode contact checking
        self.ecmbyte2 = []                  # initialize the offlinie ecm status byte2 for electrode contact checking
        self.packet_index = 0               # initialize the packet index of the of lead values

    def get(self,rawfile):
        """acquire pseudo ECG reading from text file"""

        myFile = open(rawfile, 'r')
        ecg=[]
        done=0
        while not done:
            value = myFile.readline()
            if value != '':      
                sample=value.split()
                sample=[chr(atoi(x,16)) for x in sample]
                ecg.append(sample)
            else:
                done = 1
        myFile.close()
        return ecg   
    
    def byte_destuff(self, reply_packet):
        """
        Detect and decode byte-stuffed data in reply packet; return a list of char strings called destuff
        Accept a string called reply_packet"""
        
        #---------------------------------------------------------------------------
        # If reserved character 0xfe is found in a reply packet it is to be ignored
        # and the following character is XOR linked with 0x20 and saved
        #---------------------------------------------------------------------------

        destuff = [chr(0xfc)]                                   # initialize list for 'destuffed' reply packet; list already contains start flag
        skip_counter = 0                                        # initialize skip for going to next char
        
        for index in range(1, (len(reply_packet)-1)):           # end flag excluded (next last character is the last candidate for destuffing)
            if skip_counter == 1:                               # re-initialize skip_counter
                skip_counter = 0                                # reset skip_counter to 0                                 
                continue                                        # another skip
            elif skip_counter == 0:
                if reply_packet[index] == chr(0xfe):
                    destuff.append(chr( ord(reply_packet[index+1])^int(0x20) ))         # append next char(XOR-linked with 0x20) to 'destuffed' data_stream list
                    skip_counter+= 1                                                    # move to next next char
                    continue                                                            # skip
                else:
                    destuff.append(chr( ord(reply_packet[index]) ))                     # char is not 0xfe, simply append it to 'destuffed' data_stream list        
                    continue
        destuff.append(chr(0xfd))                               # append end flag
        return destuff                                          # return the 'destuffed' reply packet as a list of char strings
    
    def byte_decoder(self, byte):
        """
        Differentiate between 8- and 16-bit data; return a tuple containing the byte count and mask byte of the ecg data field
        Accept a char string called byte"""
        
        #------------------------------------------------------------------------------------------------------------
        # Data value is 15 bits(signed) long; if only 7 bits within a data value are used, ECG transmits only 1 byte.
        # Hence, missing bits need to be filled up by the software monitor(python code).
        # To differentiate between 1- and 2-byte values, a mask Bit(LSB) within first byte is used:
        # if LSB=1, data value is 2 bytes long; if LSB=0, data value is 1 byte long 
        #------------------------------------------------------------------------------------------------------------

        num = ord(byte)
        if (num%2)==1:                              # a byte with LSB=1 is 'odd'
            val = ((num >> 1)&int(0x7f))<<8         # 2-byte value, return 'num' as the high byte (B8-B13, Bsign)
            byte_count = 2
        elif (num%2)==0:                            # a byte with LSB=0 is 'even'
            val = (num >> 1)&int(0x7f)              # 1-byte value, return 'num' as the single byte (B0-B5, Bsign)
            byte_count = 1
        ecg_data = byte_count, val
        return ecg_data                             # ecg_data is a tuple containing the byte count and the decoded mask byte

    def sign_checker(self, byte):
        """
        Check whether the sign of the reading is (+) of (-); return the sign of the ecg reading
        Accept a char string called byte"""
        
        num = ord(byte)
        if (num <= int(0x7f)):                      # if sign bit is 0
            sign = 1                                # sign is (+)
        elif (num > int(0x7f)):                     # if sign bit is 1
            sign = -1                               # sign is (-)
        return sign

    def payload_parser(self,packet,ecg_data):
        """
        Extract the reading for each ecg channel
        Usage: ECG_channels = ECG().payload_parser()"""

        sign = self.sign_checker(packet[self.packet_index])
        if ecg_data[0] == 1:
             if sign > 0:
                 ecg_reading = (ecg_data[1])
             elif sign < 0:
                 ecg_reading = (ecg_data[1]&int(0x7f)) - (2**7-1)                       # reading derived from 15-bit 2's complement format
             payload_index = 1
        elif ecg_data[0] == 2:
             if sign > 0:
                 ecg_reading = sign * (ecg_data[1]+ord(packet[self.packet_index+1]))
             elif sign < 0:
                 ecg_reading = (ecg_data[1]+ord(packet[self.packet_index+1])) - (2**15-1)     # reading derived from 7-bit 2's complement format
             payload_index = 2

        lead_value = payload_index, ecg_reading
        return lead_value

    def ecg_lead(self):
        
        destuffed=[]

        ecg_reply = self.get(self.logfile)
        for i in range(len(ecg_reply)):
            destuffed.append(self.byte_destuff(ecg_reply[i]))
        
        for i in range(0,30):
            ecg_data=self.reply_parser(destuffed[i])

        self.ecg_leadI = leadcalc.calcLI(self.ecg_leadII,self.ecg_leadIII)
        self.ecg_leadaVR = leadcalc.calcLVR(self.ecg_leadII,self.ecg_leadIII)
        self.ecg_leadaVL = leadcalc.calcLVL(self.ecg_leadII,self.ecg_leadIII)
        self.ecg_leadaVF = leadcalc.calcLVF(self.ecg_leadII,self.ecg_leadIII)

        #return self.ecg_leadII
        #return self.ecg_leadI, self.ecg_leadII, self.ecg_leadIII, \
         #      self.ecg_leadaVR, self.ecg_leadaVL, self.ecg_leadaVF,\
          #     self.ecg_leadV1, self.ecg_leadV2, self.ecg_leadV3,\
           #    self.ecg_leadV4, self.ecg_leadV5, self.ecg_leadV6
        
        pyplot.plot(besselfilter(self.ecg_leadII))
        pyplot.show()
        
        return besselfilter(self.ecg_leadI), besselfilter(self.ecg_leadII), besselfilter(self.ecg_leadIII), \
               besselfilter(self.ecg_leadaVR), besselfilter(self.ecg_leadaVL), besselfilter(self.ecg_leadaVF),\
               besselfilter(self.ecg_leadV1), besselfilter(self.ecg_leadV2), besselfilter(self.ecg_leadV3),\
               besselfilter(self.ecg_leadV4), besselfilter(self.ecg_leadV5), besselfilter(self.ecg_leadV6)
                                                        
    def reply_parser(self, packet):
        """
        Extract the reading for each ecg channel and update the lists ecg_leadII and ecg_leadIII for plotting.
        Usage: ECG_channels = ECG().reply_parser()"""
        
        new_dataset_counter = ((ord(packet[len(packet)-4]) & int(0x7f))<<14) + \
                              ((ord(packet[len(packet)-5]) & int(0x7f))<<7) + \
                              (ord(packet[len(packet)-6]) & int(0x7f))
        frames = new_dataset_counter - self.old_dataset_counter
        print frames
        self.prev_dataset_counter = self.old_dataset_counter
        
        
        payload_index = 0
        self.packet_index = 9
        for frame in range(0,frames):
##            if (len(self.ecg_leadII)!=frames) and (len(self.ecg_leadIII)!=frames) and\
##               (len(self.ecg_leadV1)!=frames) and (len(self.ecg_leadV2)!=frames) and\
##               (len(self.ecg_leadV5)!=frames) and (len(self.ecg_leadV6)!=frames):

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)

            #get the value for lead II
            #self.leadII_values.append(ecg_reading[1])
            self.ecg_leadII.append(lead_value[1]*0.00263)
            self.packet_index = self.packet_index + lead_value[0]

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)
                
            #get the value for lead III
            #self.leadIII_values.append(lead_value[1])
            self.ecg_leadIII.append(lead_value[1]*0.00263)

            self.packet_index = self.packet_index + lead_value[0]

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)

            #get the value for lead V1
            #self.leadV1_values.append(lead_value[1])
            self.ecg_leadV1.append(lead_value[1]*0.00263)

            self.packet_index = self.packet_index + lead_value[0]

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)
            
            #get the value for lead V2
            #self.leadV2_values.append(lead_value[1])
            self.ecg_leadV2.append(lead_value[1]*0.00263)

            self.packet_index = self.packet_index + lead_value[0]

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)
            
            #get the value for lead V3
            #self.leadV3_values.append(lead_value[1])
            self.ecg_leadV3.append(lead_value[1]*0.00263)

            self.packet_index = self.packet_index + lead_value[0]

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)

            #get the value for lead V4
            #self.leadV4_values.append(lead_value[1])
            self.ecg_leadV4.append(lead_value[1]*0.00263)

            self.packet_index = self.packet_index + lead_value[0]

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)
            
            #get the value for lead V5
            #self.leadV5_values.append(lead_value[1])
            self.ecg_leadV5.append(lead_value[1]*0.00263)

            self.packet_index = self.packet_index + lead_value[0]

            ecg_data = self.byte_decoder(packet[self.packet_index])
            lead_value = self.payload_parser(packet,ecg_data)

            #get the value for lead V6
            #self.leadV5_values.append(lead_value[1])
            self.ecg_leadV6.append(lead_value[1]*0.00263)
            
            self.packet_index = self.packet_index + lead_value[0]
             
        self.old_dataset_counter = new_dataset_counter
        #print self.ecg_leadII, self.ecg_leadIII, self.ecg_leadV1, self.ecg_leadV2, self.ecg_leadV3, self.ecg_leadV4, self.ecg_leadV5, self.ecg_leadV6
        
        return self.ecg_leadII, self.ecg_leadIII, self.ecg_leadV1, self.ecg_leadV2, self.ecg_leadV3, self.ecg_leadV4, self.ecg_leadV5, self.ecg_leadV6
        #return self.ecg_leaIII
        #return self.ecg_leadV1
        #return self.


    

    
                
   
