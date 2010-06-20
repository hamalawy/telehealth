"""Project LifeLink: API for EMI12 ECG Module
Facilitates Data Acquisition (DAQ) from ECG module

Authors:    Julius Miguel J. Broma
            Luis Sison, PhD
Editted by: Sy, Luke Wicent
            ------------------------------------------------
            Instrumentation, Robotics and Control Laboratory
            University of the Philippines - Diliman
            ------------------------------------------------
            February 2008
"""

#python library import
import serial
import time
import wx
import copy

import leadcalc

#checksum parameters (for updating CRC)
CRC = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,\
        0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,\
        0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,\
        0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,\
        0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,\
        0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,\
        0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,\
        0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,\
        0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,\
        0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,\
        0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,\
        0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,\
        0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,\
        0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,\
        0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,\
        0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,\
        0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,\
        0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,\
        0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,\
        0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,\
        0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,\
        0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,\
        0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,\
        0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,\
        0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,\
        0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,\
        0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,\
        0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,\
        0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,\
        0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,\
        0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,\
        0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0]
CONFIG_ANALOG_REQ = [0x01, 0x09, 0x01, 0x0A]                   # 0x01 = 3-lead; 0x0A = 1kHz sampling rate
CONFIG_ANALOG_REQ_100 = [0x01, 0x09, 0x01, 0x01]               # 0x01 = 3=lead; 0x01 = 100Hz sampling rate
CONFIG_ANALOG_REQ_500_12L = [0x01, 0x09, 0x02, 0x05]           # 0x02 = 12 lead; 0x05 = 500Hz sampling rate
SET_ECM_THRESHOLD_REQ = [0x18, 0x09, 0x00, 0x9F, 0x24]
START_OFFLINE_ECM = [0x26, 0x09, 0x01]
STOP_OFFLINE_ECM = [0x26, 0x09, 0x00]
PROTOCOL_VERSION_INQUIRY = [0x00, 0x08, 0x00, 0x01]
FIRMWARE_VERSION_INQUIRY = [0x00, 0x08, 0x50, 0x01]
IDENTIFICATION_INQUIRY = [0x00, 0x08, 0x00, 0x05]
SELFTEST_INQUIRY = [0x00, 0x08, 0x00, 0x06]
START_ECG_TRANSMISSION = [0x05, 0x09, 0x01]
STOP_ECG_TRANSMISSION = [0x05, 0x09, 0x00]

class ECG:
    """manages data request and processes reply packets to/from ECG module"""
    def __init__(self, panel=False, port='/dev/ttyUSB0', baud=230400, timeout=0.01, daqdur=15, ecmcheck=3, debug=True):
        """initializes port settings and request data sequence according to specified setting for EMI12"""

        self.parentPanel = panel
        self.port = port                
        self.baudrate = baud            
        self.timeout = timeout
        self.daqdur = daqdur           # DAQ duration in seconds
        self.ecmcheck = ecmcheck
        self.debug = debug
        
        self.ecm_threshold = 2400000
        self.ecm_status = 0
        self.device_status = 0
        self.patient_status = 0
        self.data_sequence = []             # initialize data_sequence as a list -> to hold old data_sequence and (new)data_sequence_w/checksum ??
        self.packet_num = 0                 # intitialize packet number = 0
        self.checksum_list = []             # initialize checksum data as a list(tuple) 
        self.Request = ''                   # initialize request as a string
        self.old_dataset_counter = 0        # initialize old value for counter for datasets
        self.prev_dataset_counter = 0       # initialize previous dataset counter

        self.start_flag = 0                 # if start_flag is 1, don't send start_ecg request anymore
        self.required_nr_samples = daqdur*500     # required number of samples for a 15sec DAQ with sampling rate of 100Hz
        self.resolution = 0.00263           # resolution of ecg reading in mV/bit
        
        self.lead_temp = {'II':[],'III':[],'V1':[],'V2':[],'V3':[],'V4':[],'V5':[],'V6':[]}
        self.lead_ecg = {'I':[],'II':[],'III':[],'V1':[],'V2':[],'V3':[],'V4':[],'V5':[],'V6':[],'VR':[],'VL':[],'VF':[]}
        self.firmware_string = ''           # initialize the string which will contain the firmware version
        self.device_ready_counter = 0       # initialize the counter for device ready checking
        self.ecmbyte1 = []                  # initialize the offline ecm status byte1 for electrode contact checking
        self.ecmbyte2 = []                  # initialize the offlinie ecm status byte2 for electrode contact checking
        
        # open port 'self.port w/ baudrate=self.baud & timeout=self.timeout:
        try:
            self.ecg = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=0)
            self.serialstatus = True
        except serial.SerialException:
            self.Print("Unable to open COM port %d\nPlease check serial port settings and ECG connection."%self.port)
            self.serialstatus = False
            
        self.stop_ecm()     #in case the program is hang in ecm mode or ecg mode, we can close it properly
        self.stop_ecg()
 
    def Print(self, msg=""):
        """self.Print only if in debug mode"""
        if self.debug:
            print msg
            
    def firmware(self):
        """
        get firmware version of ecg module

        Usage: ECG().firmware()

        Returns
        -------
        True    :  Firmware Version identified
        False   :  Firmware Version unidentified 
        """

        self.Print()
        self.Print("***Firmware Version Inquiry***")
        self.request(FIRMWARE_VERSION_INQUIRY)             # Inquire about Firmware Version
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # Get reply from ECG module: GET Firmware Version
        packet = self.byte_destuff(packet)

        if (packet[2]== chr(0x50)) and (packet[3]== chr(0x1)):
            self.firmware_string = ''.join(packet[4:15])
            self.Print("REPLY: Firmware Version: %s"%(self.firmware_string))
            self.device_ready_counter+=1
            self.device_status = True
            return self.device_status
        else:
            self.Print("Error: Firmware Unidentified")
            self.device_status = False
            return self.device_status

    def protocol(self):
        """
        get protocol version of ecg module

        Usage: ECG().protocol()

        Returns
        -------
        True   :  Protocol Version Identified
        False  :  Protocol Version Unidentified
        """

        self.Print() 
        self.Print("***Protocol Version Inquiry***")
        self.request(PROTOCOL_VERSION_INQUIRY)             # 9. Inquire about Protocol version
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 10. Get reply from ECG module: GET Protocol Version
        packet = self.byte_destuff(packet)

        if (packet[2]== chr(0x0)) and (packet[3]== chr(0x1)):
            self.Print("REPLY: Protocol Version: %d" % (ord(packet[4])))
            self.device_status = True
        else:
            self.Print("Unknown Protocol Version")
            self.device_status = False
        return self.device_status
            
    def device_id(self):
        """
        get identification of ecg module

        Usage: ECG().device_id()

        Returns
        -------
        True  : identified Manufacturer and Device ID
        False : unidentified Manufacturer and Device ID       
        """

        self.Print()
        self.Print("***Device Identification Inquiry***")
        self.request(IDENTIFICATION_INQUIRY)             # Inquire about Device Identification
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # Get reply from ECG module: GET Device Identification
        packet = self.byte_destuff(packet)

        if (packet[2]== chr(0x0)) and (packet[3]== chr(0x5)) and \
            (packet[4]== chr(0x1)) and (packet[5]== chr(0x1e)):
            self.Print("REPLY: Manufacturer ID: Corscience")
            self.Print("REPLY: Device ID: OEM Board")
            self.device_ready_counter+=1
            self.device_status = True
        else:
            self.Print("Error: Unknown Device")
            self.device_status = False
        return self.device_status
            
    def selftest(self):
        """
        get integrated self test result

        Usage: ECG().selftest()

        Returns
        -------
        True   :  Succesfully Passed Integrated Self Test
        False  :  Failed to pass the Integrated Self Test
        """

        self.Print()
        self.Print("***Integrated Self Test Inquiry***")
        self.request(SELFTEST_INQUIRY)             # Inquire about Integrated Self Test Result
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # Get reply from ECG module: Self Test Result
        packet = self.byte_destuff(packet)

        if (packet[2]== chr(0x0)) and (packet[3]== chr(0x6)) and\
           (packet[4]== chr(0xe4)) and (packet[5]== chr(0x20)):
            self.Print("REPLY: Device Successfully Passed!")
            self.device_ready_counter+=1
            self.device_status = True
        elif (packet[2]== chr(0x0)) and (packet[3]== chr(0x6)) and\
           (ord(packet[4]) & 128 !=128):
            self.Print("Erro: RAM Test Failed!")
            self.device_status = False
        elif (packet[2]== chr(0x0)) and (packet[3]== chr(0x6)) and\
           (ord(packet[4]) & 64 !=64):
            self.Print("Error: int_FLASH Test Failed!")
            self.device_status = False
        elif (packet[2]== chr(0x0)) and (packet[3]== chr(0x6)) and\
           (ord(packet[4]) & 32 !=32):
            self.Print("Error: PLD/ADC Test Failed!")
            self.device_status = False
        else:
            self.Print("Error: Self Test Error!")
            self.device_status = False
        return self.device_status
            
    def device_ready(self):
        """
        identifies the status of the ECG. It checks the serial port setting
        and runs the four methods: device_id(), protocol(), selftest(); to get
        the status of the ECG device.

        Usage: ECG().device_ready()

        Returns
        -------
        True    :   Device is Ready = passed all the four tests: device_id(),
                    firmware(), protocol(),selftest()
        False   :   Device Not Ready = failed to pass the series of tests
        """
     
        if self.serialstatus == True:
            ID_status = self.device_id()
            firm_status = self.firmware()
            prot_status = self.protocol()
            test_status = self.selftest()
            #print ID_status,firm_status,prot_status,test_status
            if ID_status==True and firm_status==True and prot_status==True\
               and test_status==True:
                self.device_status = "\nDevice Ready"
            else:
                self.device_status = "\nDevice Not Ready"
                self.ecg.close()
        elif self.serialstatus == False:
            self.device_status = "\nDevice Not Ready"
        return self.device_status
           
    def reset(self):
        """reset serial port input buffer"""
        self.ecg.flushInput()
        
    def packet_number(self, data_sequence):
        """
        Update self.packet_num for monitor side; Return data_sequence (list of char strings) with updated packet number
        Accept a list of hex numbers called data_sequence
        """
        numbered_data_seq = [chr(elem) for elem in data_sequence]
        PacketNum = chr(self.packet_num)
        numbered_data_seq.insert(0, PacketNum)
        self.packet_num = (self.packet_num+1)%256
        return numbered_data_seq
    
    def checksum(self, data_sequence2):
        """
        Calculate the checksum(BASED ON CRC16 CCITT) from the ECG request/repy data sequence, append checksum at the end of the sequence
        Return a tuple: crc_LoByte, crc_HiByte, data_sequence_w/checksum_list
        """
        data_seq_cs = [(elem) for elem in data_sequence2]
        crc_startval = 0xFFFF
        crc = int(crc_startval)
        for char in data_seq_cs:
            tmp = (crc>>8)^(ord(char))                          # calculate index called tmp for corresponding crc_polynomial in crctttab
            crc = ((crc<<8)&int(0xFFFF))^(int(CRC[tmp]))        # Or-link shifted version of crc(get 16bits only) with the crc_polynomial referenced by the index
        crc_HiByte = crc>>8                                     # get high-byte of checksum
        crc_LoByte = crc&int(0xFF)                              # get low-byte of checksum
        
        # append the checksum, lower byte goes first:
        data_seq_cs.append(chr(crc_LoByte)) 
        data_seq_cs.append(chr(crc_HiByte))
        self.checksum_list = chr(crc_LoByte), chr(crc_HiByte), data_seq_cs      
        return self.checksum_list                                               
        
    def byte_stuff(self, data_stream):
        """filter the data stream for reserved flags; return a list (of char strings) for byte-stuffed data sequence"""

        #------------------------------------------------------------------------------------------------
        # Rid packets of reserved flags like 0xFC, 0xFD, 0xFE. Special flags are XOR-linked with '0x20':
	    # 0xFC replaced with 0xFE 0xDC
        # 0xFD replaced with 0xFE 0xDD
	    # 0xFE replaced with 0xFE 0xDE
        #------------------------------------------------------------------------------------------------    
        encoded_sequence = []                                   # initialize a list for the byte-stuffed data sequence  
        for char in data_stream:
            if char == chr(0xfc):                                  
                encoded_sequence.append(chr(0xfe))
                encoded_sequence.append(chr(0xdc))
            elif char == chr(0xfd):
                encoded_sequence.append(chr(0xfe))
                encoded_sequence.append(chr(0xdd))
            elif char == chr(0xfe):
                encoded_sequence.append(chr(0xfe))
                encoded_sequence.append(chr(0xde))
            else:
                encoded_sequence.append(char)
        return encoded_sequence                                 # return a list containing the byte-stuffed data sequence
    
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
      
    def request(self, data_sequence3):
        """
        Arrange the request packet for sending to EMI12 ECG module
        Accept a list of char strings called data_sequence3
        """
        data_wpacket_num = self.packet_number(data_sequence3)       # append packet number at the start of data sequence
        data_wchecksum = self.checksum(data_wpacket_num)            # get checksum and append it to the data sequence list
        data_wbyte_stuff = self.byte_stuff(data_wchecksum[2])       # data sequence w/ checksum undergoes byte stuffing
        request = [elem for elem in data_wbyte_stuff]               # move byte-stuffed data sequence to request list
        request.insert(0,chr(0xfc))                                 # insert start flag at the begining of request sequence  
        request.append(chr(0xfd))                                   # append end flag at the end of request
        self.Request = ''.join(request)                             # convert request into string

    def ecgreply(self):
        """
        Wait for complete reply packet from ECG module; return a string called packet
        Usage: packet = ECG().ecgreply()
        """
        reply = ''
        byte = chr(0x00)
        basetime = time.time()
        while (byte[-1] != chr(0xfd)) and (time.time()<(basetime+3)):
            byte = self.ecg.readline(size=None,eol=0xfd)
            reply = reply + byte
            if(len(byte)==0):
                byte=chr(0x00)
        if time.time()>(basetime+3):
            self.Print("timeout! Reply packet incomplete: %s"%(list(reply)))
        return reply

    def payload_parser(self,packet,ecg_data):
        """
        Extract the reading for each ecg channel
        Usage: ECG_channels = ECG().payload_parser()
        """
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

    def reply_parser(self, packet):
        """
        Extract the reading for each ecg channel and update the lists ecg_leadII and ecg_leadIII for plotting.
        Usage: ECG_channels = ECG().reply_parser()
        """
        new_dataset_counter = ((ord(packet[len(packet)-4]) & int(0x7f))<<14) + \
                              ((ord(packet[len(packet)-5]) & int(0x7f))<<7) + \
                              (ord(packet[len(packet)-6]) & int(0x7f))
        frames = new_dataset_counter - self.old_dataset_counter
        #print frames
        self.prev_dataset_counter = self.old_dataset_counter
        
        payload_index = 0
        self.packet_index = 9
        for frame in range(0,frames):
            for keys in self.lead_temp:
                ecg_data = self.byte_decoder(packet[self.packet_index])
                lead_value = self.payload_parser(packet,ecg_data)
                self.lead_temp[keys].append(lead_value[1])
                self.packet_index = self.packet_index + lead_value[0]
             
        self.old_dataset_counter = new_dataset_counter
        
                
    def config_analog(self):
        """set ecg-type and sampling rate"""

        self.Print()
        self.Print("***Configure Analog Request***")

        self.request(CONFIG_ANALOG_REQ_500_12L)            # 1. Configure sampling rate and active ECG channels
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 2. Get reply from ECG module: To CONFIRM Configure Analog Setting
        if (packet[2]== chr(0x1)) and (packet[3]== chr(0x7)) and \
            (packet[4]== chr(0x2)) and (packet[5]== chr(0x5)):
            self.Print("REPLY: Configure Analog Request Confirmed")
            self.Print("ECG Type: 12-lead Sampling Rate: 500Hz")

    def ecg_lead(self):
        filtered = {}
        if len(self.lead_temp['II'])>1:
            self.lead_ecg['I'].extend(leadcalc.LI(self.lead_temp['II'],self.lead_temp['III']))    
            self.lead_ecg['VR'].extend(leadcalc.LVR(self.lead_temp['II'],self.lead_temp['III']))
            self.lead_ecg['VL'].extend(leadcalc.LVL(self.lead_temp['II'],self.lead_temp['III']))
            self.lead_ecg['VF'].extend(leadcalc.LVF(self.lead_temp['II'],self.lead_temp['III']))
            
            for keys in self.lead_temp:
                self.lead_ecg[keys].extend(self.lead_temp[keys])
                del self.lead_temp[keys][:]
        
    def set_ecm_threshold(self):
        """set electrode contact measurement (ecm) threshold for the ecg module"""

        self.Print()
        self.Print("***Set ECM Threshold Request***")
        self.request(SET_ECM_THRESHOLD_REQ)                     # 3. Set ECM Threshold
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 4. Get reply from ECG module: To CONFIRM ECM Threshold
        if (packet[2]== chr(0x18)) and (packet[3]== chr(0x7)) and \
            (packet[4]== chr(0x0)) and (packet[5]== chr(0x9f))and \
            (packet[6]== chr(0x24)):                          
            self.Print("REPLY: Set ECM Threshold Request Confirmed")

    def start_ecm(self):
        """start offline electrode contact measurement (ecm)"""

        self.Print()
        self.Print("***Start Offline ECM***")
        self.request(START_OFFLINE_ECM)                    # 5. Start Offline ECM
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 6. Get reply from ECG module: To ACKNOWLEDGE last received packet
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        if (packet[2]== chr(0x0)) and (packet[3]== chr(0x2)) and \
            (packet[4]==chr(last_received_packet)):                          
            self.Print("REPLY: Start_Offline_ECM ACK")

    def get_ecm(self):
        """get ecm readings; stop only after 'self.ecmcheck' consecutive successful ecm"""

        contact_counter = 0                                     # initialize counter for determining ECG electrodes contact (contact is "OK" when counter reaches self.ecmcheck)
        basetime = time.time()
        while (contact_counter < self.ecmcheck) and (time.time()<(basetime+15)):
            raw_packet = self.ecgreply()                        # get reply from ECG module: To determine if ECM is ok (if so, plus 1 to contact_counter)
            packet = self.byte_destuff(raw_packet)              # decodes reply packet for byte-stuffed data; packet here is a list
             
            if (packet[2] == chr(0x26)) and (packet[3] == chr(0x7)):             # 0x0726 - offline ecm
                ecm_N = (ord(packet[8])<<16)+(ord(packet[7])<<8)+(ord(packet[6]))
                ecm_F = (ord(packet[11])<<16)+(ord(packet[10])<<8)+(ord(packet[9]))
                ecm_L = (ord(packet[14])<<16)+(ord(packet[13])<<8)+(ord(packet[12]))
                ecm_R = (ord(packet[17])<<16)+(ord(packet[16])<<8)+(ord(packet[15]))
                ecm_V6 = (ord(packet[20])<<16)+(ord(packet[19])<<8)+(ord(packet[18]))
                ecm_V5 = (ord(packet[23])<<16)+(ord(packet[22])<<8)+(ord(packet[21]))
                ecm_V4 = (ord(packet[26])<<16)+(ord(packet[25])<<8)+(ord(packet[24]))
                ecm_V3 = (ord(packet[29])<<16)+(ord(packet[28])<<8)+(ord(packet[27]))
                ecm_V2 = (ord(packet[32])<<16)+(ord(packet[31])<<8)+(ord(packet[30]))
                ecm_V1 = (ord(packet[35])<<16)+(ord(packet[34])<<8)+(ord(packet[33]))
                self.Print("\t------------------------")
                self.Print("\tECM for lead N: %d"%(ecm_N))
                self.Print("\tECM for lead F: %d"%(ecm_F))
                self.Print("\tECM for lead L: %d"%(ecm_L))
                self.Print("\tECM for lead R: %d"%(ecm_R))
                self.Print("\tECM for lead C6: %d"%(ecm_V6))
                self.Print("\tECM for lead C5: %d"%(ecm_V5))
                self.Print("\tECM for lead C4: %d"%(ecm_V4))
                self.Print("\tECM for lead C3: %d"%(ecm_V3))
                self.Print("\tECM for lead C2: %d"%(ecm_V2))
                self.Print("\tECM for lead C1: %d"%(ecm_V1))
                self.Print("\t------------------------")
                self.ecmbyte1 = packet[4:5]              # get the offline ecm byte1 and ecm byte2 data to check which electrodes are in contact
                self.ecmbyte2 = packet[5:6]              
                contact_counter += self.electrode_check()
                self.Print()
                self.Print("--->> ECM PASS COUNT: %d"%(contact_counter))
        ecm_endtime = time.time()
        if ecm_endtime >(basetime+15):
            self.ecm_status = 0
        else:
            self.ecm_status = 1
        return self.ecm_status

    def electrode_check(self):
        """ checks the whether the electrodes L, R, F, and N has contact
        
        Checks the ECM Status Byte 1 and ECM Status Byte 2 of the reply packet
        transmitted by the electrode contact measurement and prints the electrodes
        that has contact.
        
        Usage: ECG().electrode_check()
        """
        
        self.nodeR = self.electrode_R()
        self.nodeL = self.electrode_L()
        self.nodeN = self.electrode_N()
        self.nodeF = self.electrode_F()
        self.nodeC1 = self.electrode_C1()
        self.nodeC2 = self.electrode_C2()
        self.nodeC3 = self.electrode_C3()
        self.nodeC4 = self.electrode_C4()
        self.nodeC5 = self.electrode_C5()
        self.nodeC6 = self.electrode_C6()

        if self.nodeR == True and self.nodeL==True and self.nodeN == True and self.nodeF == True and \
           self.nodeC1 == True and self.nodeC2 == True and self.nodeC3 == True and self.nodeC4 == True and\
           self.nodeC5 == True and self.nodeC6 == True:
            contact_counter = 1
            self.Print("All electrodes has contact")
            return contact_counter
        elif self.nodeR == True and self.nodeL==True and self.nodeN == True and self.nodeF == True:
            contact_counter = 1
            self.Print("R,L,N,F has contact")
            return contact_counter
        else:
            contact_counter = 0
            self.Print("Check electrodes")
            return contact_counter

    def electrode_R(self):

        if (ord(self.ecmbyte1[0]) & 2 == 2):
            self.Print("--->>electrode R has contact")
#            self.parentPanel.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_connected.png"))
            return True               
        else:
            self.Print("--->>electrode R has no contact")
#            self.parentPanel.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_unconnected.png"))
            return False
        
    def electrode_L(self):
        
        if (ord(self.ecmbyte1[0]) & 4 == 4):
            self.Print("--->>electrode L has contact")
#            self.parentPanel.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_connected.png"))
            return True
        else:
            self.Print("--->>electrode L has no contact")
#            self.parentPanel.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_unconnected.png"))
            return False

    def electrode_N(self):

        if (ord(self.ecmbyte2[0]) & 64 == 64):
            self.Print("--->>electrode N has contact")
#            self.parentPanel.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_connected.png"))
            return True
        else:
            self.Print("--->>electrode N has no contact")
#            self.parentPanel.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png"))
            return False

    def electrode_F(self):    

        if (ord(self.ecmbyte1[0]) & 1 == 1):
            self.Print("--->>electrode F has contact")
#            self.parentPanel.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_connected.png"))
            return True
        else:
            self.Print("--->>electrode F has no contact")
#            self.parentPanel.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_unconnected.png"))
            return False

    def electrode_C1(self):

        if (ord(self.ecmbyte2[0]) & 1 == 1):
            self.Print("--->>electrode C1 has contact")
#            self.parentPanel.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_connected.png"))
            return True
        else:
            self.Print("--->>electrode C1 has no contact")
#            self.parentPanel.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_unconnected.png"))
            return False

    def electrode_C2(self):

        if (ord(self.ecmbyte2[0]) & 2 == 2):
            self.Print("--->>electrode C2 has contact")
#            self.parentPanel.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_connected.png"))

            return True
        else:
            self.Print("--->>electrode C2 has no contact")
#            self.parentPanel.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_unconnected.png"))
            return False

    def electrode_C3(self):

        if (ord(self.ecmbyte2[0]) & 4 == 4):
            self.Print("--->>electrode C3 has contact")
#            self.parentPanel.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_connected.png"))

            return True
        else:
            self.Print("--->>electrode C3 has no contact")
#            self.parentPanel.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png"))
            return False

    def electrode_C4(self):

        if (ord(self.ecmbyte2[0]) & 8 == 8):
            self.Print("--->>electrode C4 has contact")
#            self.parentPanel.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_connected.png"))
            return True
        else:
            self.Print("--->>electrode C4 has no contact")
#            self.parentPanel.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_unconnected.png"))
            return False

    def electrode_C5(self):

        if (ord(self.ecmbyte2[0]) & 16 == 16):
            self.Print("--->>electrode C5 has contact")
#            self.parentPanel.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_connected.png"))
            return True
        else:
            self.Print("--->>electrode C5 has no contact")
#            self.parentPanel.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png"))
            return False

    def electrode_C6(self):
        if (ord(self.ecmbyte2[0]) & 32 == 32):
            self.Print("--->>electrode C6 has contact")
#            self.parentPanel.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_connected.png"))
            return True
        else:
            self.Print("--->>electrode C6 has no contact")
#            self.parentPanel.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_unconnected.png"))
            return False  

    def stop_ecm(self):
        """stop offline electrode contact measurement (ecm)"""

        self.Print()
        self.Print("***Stop Offline ECM***")
        self.request(STOP_OFFLINE_ECM)                          # 7. Stop Offline ECM
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 8. Get reply from ECG module: To ACKNOWLEDGE last received packet
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        if (packet[2]==chr(0x0)) and (packet[3]==chr(0x2)) and \
            (packet[4]==chr(last_received_packet)):                          
            self.Print("REPLY: Stop_Offline_ECM ACK")

    def start_ecg(self):
        """start ecg transmission"""
        self.Print()
        self.Print("***Start ECG Transmission***")
        self.request(START_ECG_TRANSMISSION)               # 13. Start ECG transmission
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 14. Get reply from ECG module: To ACKNOWLEDGE last received packet
        destuffed_reply = self.byte_destuff(packet)
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        if (packet[2]== chr(0x0)) and (packet[3]==chr(0x2)) and \
           (packet[4]==chr(last_received_packet)):                          
            self.Print("REPLY: Start_ECG_TRANSMISSION ACK")

    def get_ecg(self):
        """get ecg readings"""
        self.getecg = True
        BaseTime = time.time()                                   # get reference time
        self.Print()
        self.Print("Acquiring ECG readings...")
        self.Print("DAQ started at: %s"%time.ctime())                 # get start time
        while (time.time()-BaseTime <= self.daqdur and self.getecg):
            raw_packet = self.ecgreply()                         # get reply packet; raw_packet is a string
            packet = self.byte_destuff(raw_packet)
            self.reply_parser(packet)
        self.Print("DAQ ended at: %s"%time.ctime())                   # get end time

    def real_val(self, digital_readings):
        """convert digital readings into the actual readings using resolution"""
        actual_readings = [ (digiVal*self.resolution) for digiVal in digital_readings ]
        return actual_readings
    
    def stop_ecg(self):
        """stop ecg transmission"""

        self.Print()
        self.Print("***Stop ECG Transmission***")
        self.request(STOP_ECG_TRANSMISSION)                # 15. Stop ECG transmission
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 16. Get reply from ECG module: To ACKNOWLEDGE last received packet
        destuffed_reply = self.byte_destuff(packet)
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        
        if (packet[2]== chr(0x0)) and (packet[3]==chr(0x2)) and \
           (packet[4]==chr(last_received_packet)):                          
            self.Print("REPLY: Stop_ECG_TRANSMISSION ACK")
    
    def patient_ready(self):
        """checks whether the patient is ready for ECG by electrode contact measurement"""
        if self.start_flag == 0:
            self.set_ecm_threshold()
            self.start_ecm()
            self.ecm_status = self.get_ecm()
            self.Print("ECM STATUS: %d"%self.ecm_status)
            self.Print()
            self.stop_ecm()
            if self.ecm_status == 0:
                self.Print("\n--->>PATIENT IS NOT READY")
                self.Print("\nTimeout: Cannot get correct ECM. Please attach the electrodes properly.")
                self.ecg.close()
                self.Print("\nSerial port closed.")
            elif self.ecm_status == 1:
                self.Print("\n--->>PATIENT IS NOW READY")
                self.config_analog()
                self.start_ecg()
                self.start_flag = 1

        if self.ecm_status == 1:
            self.get_ecg()
            self.ecg_lead()
    
    def stop(self):
        """stop acquisition of ecg readings and close the serial port"""
        if self.start_flag == 1:
            self.getecg = False
            time.sleep(0.1)
            self.stop_ecm()     #in case the program is hang in ecm mode or ecg mode, we can close it properly
            self.stop_ecg()
            self.start_flag = 0
        if self.serialstatus:
            self.ecg.close()
            print "Serial port for EMI12 ECG closed."
            
    def pop(self,start=0,end=0):
        """Delete ECG main lead data from 'start' to 'end'"""
        temp = {}
        for keys in self.lead_ecg:
            temp[keys] = self.lead_ecg[keys][start:end]
            del self.lead_ecg[keys][start:end]
        return temp
