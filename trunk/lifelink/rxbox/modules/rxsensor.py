
"""Project LifeLink: API for EMI12 ECG Module
Facilitates Data Acquisition (DAQ) from ECG module

Authors:    Julius Miguel J. Broma
            Luis Sison, PhD
            ------------------------------------------------
            Instrumentation, Robotics and Control Laboratory
            University of the Philippines - Diliman
            ------------------------------------------------
            February 2008
"""
import serial
import time
from edf import BioSignal
from wx import CallAfter

class ECG:
    """manages data request and processes reply packets to/from ECG module"""

    def __init__(self, parent, port=2, baud=230400, timeout=None):
        """initializes port settings and request data sequence according to specified setting for EMI12"""
        
        self.port = port                
        self.baudrate = baud            
        self.timeout = timeout
        self.ecm_threshold = 2400000
        self.ecm_status = 0
        self.data_sequence = []             # initialize data_sequence as a list -> to hold old data_sequence and (new)data_sequence_w/checksum
        self.packet_num = 0                 # intitialize packet number = 0
        self.checksum_list = []             # initialize checksum data as a list(tuple) 
        self.Request = ''                   # initialize request as a string
        self.old_dataset_counter = 0        # initialize old value for counter for datasets
        self.prev_dataset_counter = 0       # initialize previous dataset counter

        self.start_flag = 0                 # if start_flag is 1, don't send start_ecg request anymore
        self.required_nr_samples = 1500     # required number of samples for a 15sec DAQ with sampling rate of 100Hz
        self.resolution = 0.00263           # resolution of ecg reading in mV/bit
        self.ecg_leadII = []                # "dynamic" list that continuously accommodates lead II readings
        self.ecg_leadIII = []               # "dynamic" list that continuously accommodates lead III readings
        self.daqduration = 15               # DAQ duration in seconds
        self.actual_readings = []           # 1500 samples for plotting
     
        #checksum parameters (for updating CRC)
        self.CRC = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,\
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
                
        self.CONFIG_ANALOG_REQ = [0x01, 0x09, 0x01, 0x0A]                   # 0x01 = 3-lead; 0x0A = 1kHz sampling rate
        self.CONFIG_ANALOG_REQ_100 = [0x01, 0x09, 0x01, 0x01]               # 0x01 = 3=lead; 0x01 = 100Hz sampling rate
        self.SET_ECM_THRESHOLD_REQ = [0x18, 0x09, 0x00, 0x9F, 0x24]
        self.START_OFFLINE_ECM = [0x26, 0x09, 0x01]
        self.STOP_OFFLINE_ECM = [0x26, 0x09, 0x00]
        self.PROTOCOL_VERSION_INQUIRY = [0x00, 0x08, 0x00, 0x01]
        self.FIRMWARE_VERSION_INQUIRY = [0x00, 0x08, 0x50, 0x01] 
        self.START_ECG_TRANSMISSION = [0x05, 0x09, 0x01]
        self.STOP_ECG_TRANSMISSION = [0x05, 0x09, 0x00]
        
        self.parentPanel = parent

        # open port 'self.port w/ baudrate=self.baud & timeout=self.timeout:
        try:
            self.ecg = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=0)      
        except serial.SerialException:
            print "Unable to open COM port", 3, "\nPlease check serial port settings."
        
    def status(self):
        """check connectivity; confirm if device is ready"""
        pass

    def reset(self):
        """reset serial port input buffer"""
        self.ecg.flushInput()
        
    def packet_number(self, data_sequence):
        """
        Update self.packet_num for monitor side; Return data_sequence (list of char strings) with updated packet number
        Accept a list of hex numbers called data_sequence"""

        numbered_data_seq = [chr(elem) for elem in data_sequence]
        PacketNum = chr(self.packet_num)
        numbered_data_seq.insert(0, PacketNum)
        if self.packet_num < 255:
            self.packet_num = self.packet_num + 1
        elif self.packet_num == 255:
            self.packet_num = 0
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
            crc = ((crc<<8)&int(0xFFFF))^(int(self.CRC[tmp]))   # Or-link shifted version of crc(get 16bits only) with the crc_polynomial referenced by the index
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
        Accept a list of char strings called data_sequence3"""
        
        data_wpacket_num = self.packet_number(data_sequence3)       # append packet number at the start of data sequence
        data_wchecksum = self.checksum(data_wpacket_num)            # get checksum and append it to the data sequence list
        data_wbyte_stuff = self.byte_stuff(data_wchecksum[2])       # data sequence w/ checksum undergoes byte stuffing
        request = [elem for elem in data_wbyte_stuff]               # move byte-stuffed data sequence to request list
        request.insert(0,chr(0xfc))                                 # insert start flag at the begining of request sequence  
        request.append(chr(0xfd))                                   # append end flag at the end of request
        self.Request = ''.join(request)                             # convert request into string
        #print "Request:", request

    def ecgreply(self):
        """
        Wait for complete reply packet from ECG module; return a string called packet
        Usage: packet = ECG().ecgreply()"""
        
        reply = ''
        byte = chr(0x00)
        basetime = time.time()
        while (byte != chr(0xfd)) and (time.time()<(basetime+3)):
            byte = self.ecg.read(1)
            reply = reply + byte
        if time.time()>(basetime+3):
            print "timeout! Reply packet incomplete:",reply
        return reply

    def reply_parser(self, packet):
        """
        Extract the reading for each ecg channel and update the lists ecg_leadII and ecg_leadIII for plotting.
        Usage: ECG_channels = ECG().reply_parser()"""
        """
        # For 12-lead ecg: 
        II = 0
        III = 0
        V1 = 0
        V2 = 0
        V3 = 0
        V4 = 0
        V5 = 0
        V6 = 0
        ecg_leads = {'II':II, 'III':III, 'V1':V1, 'V2':V2, 'V3':V3, 'V4':V4, 'V5':V5, 'V6':V6}
        """
        new_dataset_counter = ((ord(packet[len(packet)-4]) & int(0x7f))<<14) + \
                              ((ord(packet[len(packet)-5]) & int(0x7f))<<7) + \
                              (ord(packet[len(packet)-6]) & int(0x7f))
        frames = new_dataset_counter - self.old_dataset_counter
        self.prev_dataset_counter = self.old_dataset_counter
        II = 0
        III = 0
        ecg_leads = {'II':II, 'III':III}
        payload_index = 0
        packet_index = 9
        for frame in range(0, frames):
            for lead in ecg_leads:
                ecg_data = self.byte_decoder(packet[packet_index])
                sign = self.sign_checker(packet[packet_index])
                if ecg_data[0] == 1:
                    if sign > 0:
                        ecg_reading = (ecg_data[1])
                    elif sign < 0:
                        ecg_reading = (ecg_data[1]&int(0x7f)) - (2**7-1)                       # reading derived from 15-bit 2's complement format
                    payload_index = 1
                elif ecg_data[0] == 2:
                    if sign > 0:
                        ecg_reading = sign * (ecg_data[1]+ord(packet[packet_index+1]))
                    elif sign < 0:
                        ecg_reading = (ecg_data[1]+ord(packet[packet_index+1])) - (2**15-1)     # reading derived from 7-bit 2's complement format
                    payload_index = 2
                if lead == 'II':
                    self.leadII_values.append(ecg_reading)
                    self.ecg_leadII.append(ecg_reading * 0.00263)                               # add ecg lead II reading immediately to "dynamic list"    
                #elif lead =='III':
                    #self.leadIII_values.append(ecg_reading)
                    #self.ecg_leadIII.append(ecg_reading * 0.00263)                             # add ecg lead III reading immediately to "dynamic list" 
                packet_index = packet_index + payload_index
        self.old_dataset_counter = new_dataset_counter
                
    def config_analog(self):
        """set ecg-type and sampling rate"""

        print
        print "***Configure Analog Request***"
        self.request(self.CONFIG_ANALOG_REQ_100)                # 1. Configure sampling rate and active ECG channels
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 2. Get reply from ECG module: To CONFIRM Configure Analog Setting
        if (packet[2]== chr(0x1)) and (packet[3]== chr(0x7)) and \
            (packet[4]== chr(0x1)) and (packet[5]== chr(0x1)):
            print "REPLY: Configure Analog Request Confirmed"
            print "ECG Type: 3-lead", "Sampling Rate: 100Hz"
        
    def set_ecm_threshold(self):
        """set electrode contact measurement (ecm) threshold for the ecg module"""

        print          
        print "***Set ECM Threshold Request***"
        self.request(self.SET_ECM_THRESHOLD_REQ)                # 3. Set ECM Threshold
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 4. Get reply from ECG module: To CONFIRM ECM Threshold
        if (packet[2]== chr(0x18)) and (packet[3]== chr(0x7)) and \
            (packet[4]== chr(0x0)) and (packet[5]== chr(0x9f))and \
            (packet[6]== chr(0x24)):                          
            print "REPLY: Set ECM Threshold Request Confirmed"

    def start_ecm(self):
        """start offline electrode contact measurement (ecm)"""

        print
        print "***Start Offline ECM***"
        self.request(self.START_OFFLINE_ECM)                    # 5. Start Offline ECM
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 6. Get reply from ECG module: To ACKNOWLEDGE last received packet
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        if (packet[2]== chr(0x0)) and (packet[3]== chr(0x2)) and \
            (packet[4]==chr(last_received_packet)):                          
            print "REPLY: Start_Offline_ECM ACK"

    def get_ecm(self):
        """get ecm readings; stop only after three consecutive successful ecm"""

        contact_counter = 0                                     # initialize counter for determining ECG electrodes contact (contact is "OK" when counter reaches 3)
        basetime = time.time()
        while (contact_counter < 3) and (time.time()<(basetime+15)):
            raw_packet = self.ecgreply()                        # get reply from ECG module: To determine if ECM is ok (if so, plus 1 to contact_counter)
            packet = self.byte_destuff(raw_packet)              # decodes reply packet for byte-stuffed data; packet here is a list
            if (packet[2] == chr(0x26)) and (packet[3] == chr(0x7)):             # 0x0726 - offline ecm
                ecm_N = (ord(packet[8])<<16)+(ord(packet[7])<<8)+(ord(packet[6]))
                ecm_F = (ord(packet[11])<<16)+(ord(packet[10])<<8)+(ord(packet[9]))
                ecm_L = (ord(packet[14])<<16)+(ord(packet[13])<<8)+(ord(packet[12]))
                ecm_R = (ord(packet[17])<<16)+(ord(packet[16])<<8)+(ord(packet[15]))
                print "\t------------------------"
                print "\tECM for lead N:", ecm_N
                print "\tECM for lead F:", ecm_F
                print "\tECM for lead L:", ecm_L
                print "\tECM for lead R:", ecm_R
                print "\t------------------------"
                print
                if (packet[4] == chr(0x07)) and (packet[5] == chr(0xc0)):         # 0x07 = 0 0 0 0  0 1 1 1 and 0xc0 = 1  1           0  0  0  0  0  0
                    ###############################################                            ^ ^ ^                   ^  ^           ^  ^  ^  ^  ^  ^
                    ###############################################                            L R F                   N type:3-lead  V6 V5 V4 V3 V2 V1
                    ###############################################
                    if (ecm_N <= self.ecm_threshold) and (ecm_F <= self.ecm_threshold) and \
                       (ecm_L <= self.ecm_threshold) and (ecm_R <= self.ecm_threshold):
                        print "---> ECM is ok."
                        print
                        contact_counter+= 1
                    else:
                        print "---> ECM NOT ok."
                        print
                        contact_counter = 0
                else:
                    contact_counter = 0
                print "--->> ECM PASS COUNT:", contact_counter
        ecm_endtime = time.time()
        #print "ecm check duration:", (ecm_endtime - basetime)
        if ecm_endtime >(basetime+15):
            self.ecm_status = 0
        else:
            self.ecm_status = 1
            
        return self.ecm_status

    def stop_ecm(self):
        """stop offline electrode contact measurement (ecm)"""

        print
        print "***Stop Offline ECM***"
        self.request(self.STOP_OFFLINE_ECM)                     # 7. Stop Offline ECM
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 8. Get reply from ECG module: To ACKNOWLEDGE last received packet
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        if (packet[2]==chr(0x0)) and (packet[3]==chr(0x2)) and \
            (packet[4]==chr(last_received_packet)):                          
            print "REPLY: Stop_Offline_ECM ACK"

    def inquiry(self):
        """get protocol version of ecg module"""

        print 
        print "***Protocol Version Inquiry***"
        self.request(self.PROTOCOL_VERSION_INQUIRY)             # 9. Inquire about Protocol version
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 10. Get reply from ECG module: GET Protocol Version
        packet = self.byte_destuff(packet)

        if (packet[2]== chr(0x0)) and (packet[3]== chr(0x1)):
            print "REPLY: Protocol Version:", ord(packet[4])

    def start_ecg(self):
        """start ecg transmission"""

        print
        print "***Start ECG Transmission***"
        self.request(self.START_ECG_TRANSMISSION)               # 13. Start ECG transmission
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 14. Get reply from ECG module: To ACKNOWLEDGE last received packet
        destuffed_reply = self.byte_destuff(packet)
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        if (packet[2]== chr(0x0)) and (packet[3]==chr(0x2)) and \
           (packet[4]==chr(last_received_packet)):                          
            print "REPLY: Start_ECG_TRANSMISSION ACK"

    def get_ecg(self):
        """get ecg readings"""

        BaseTime = time.time()                                  # get reference time
        print
        print "Acquiring ECG readings..."
        print "DAQ started at:", time.ctime()                   # get start time
        count = 0
        self.leadII_values = []
        self.leadIII_values = []
        while (time.time() - BaseTime <= self.daqduration):
            raw_packet = self.ecgreply()                        # get reply packet; raw_packet is a string
            packet = self.byte_destuff(raw_packet)  
            self.reply_parser(packet)
            count = count + 1
        excess_nr_samples = ( self.old_dataset_counter - self.prev_dataset_counter ) - self.required_nr_samples

        # if number of samples > required, remove the excess
        if excess_nr_samples > 0:                           
            for number in range(0, excess_nr_samples):
                self.leadII_values.pop()
                #self.leadIII_values.pop()
                                       
        # if number of samples < required, pad with zeros
        elif excess_nr_samples < 0:
            for number in range(0, -(excess_nr_samples)):
                self.leadII_values.append(0)
                #self.leadIII_values.append(0)
        self.actual_readings = self.real_val(self.leadII_values)
        Biosignal_ECG = BioSignal('II',  'CM',        'mV',      -43,    43,      0,     32767,   'None',   100,     self.leadII_values)
        #########################   ^      ^            ^          ^      ^        ^       ^         ^       ^               ^
        ######################### label sensor-type   phys.     phys.   phys.   digi.    digi.     pre-    Nsamples    digital readings
        #########################                   dimension   min     max     min      max     filtering            for edf generation

        self.parentPanel.BioSignals.append(Biosignal_ECG)
        print "Returned ECG"
        print "DAQ ended at:", time.ctime()                      # get end time

    def real_val(self, digital_readings):
        """convert digital readings into the actual readings using resolution"""
        
        actual_readings = [ (digiVal*self.resolution) for digiVal in digital_readings ]
        return actual_readings
    
    def stop_ecg(self):
        """stop ecg transmission"""

        print 
        print "***Stop ECG Transmission***"
        self.request(self.STOP_ECG_TRANSMISSION)                # 15. Stop ECG transmission
        self.ecg.write(self.Request)
        packet = self.ecgreply()                                # 16. Get reply from ECG module: To ACKNOWLEDGE last received packet
        destuffed_reply = self.byte_destuff(packet)
        #print "reply from ecg module:", destuffed_reply
        if self.packet_num == 0:
            last_received_packet = 255
        else:
            last_received_packet = self.packet_num - 1
        #print "last received packet:", last_received_packet
        if (packet[2]== chr(0x0)) and (packet[3]==chr(0x2)) and \
           (packet[4]==chr(last_received_packet)):                          
            print "REPLY: Stop_ECG_TRANSMISSION ACK"
    
    def get(self):
        """acquire ecg readings from EMI12 ECG module every 15 seconds"""
        
        if self.start_flag == 0:                                # send start_ecg request only once
            
            self.reset()
            self.config_analog()
            self.set_ecm_threshold()
            self.start_ecm()
            self.ecm_status = self.get_ecm()
            print "ECM STATUS:", self.ecm_status
            print
            self.stop_ecm()
            if self.ecm_status == 0:
                print "Timeout: Cannot get correct ECM. Please attach the electrodes properly."
                self.ecg.close()
                print "Serial port closed."
            elif self.ecm_status == 1:
                self.inquiry()
                self.config_analog()
                self.start_ecg()
                self.start_flag = 1
                ### Added for Plotting
                CallAfter(self.parentPanel.startPlotThread)

        if self.ecm_status == 1:
            self.get_ecg()

    def stop(self):
        """stop acquisition of ecg readings and close the serial port"""

        if self.ecm_status == 1:   
            self.stop_ecg()
            self.ecg.close()
            print "Serial port for EMI12 ECG closed."
            #self.start_flag = 0

class SPO2:
    """manages data request and acquistion from the ChipOx OEM module"""
    
    def __init__(self, parent, port=11,baud=9600,timeout=None):
        """initialize port settings and request according to the specified setting for ChipOx"""

        #self.parentFrame = parent
        #self.index = 0
        
        #default: port=0,baud=9600,bytesize=8,parity='N',stopbits=1,xon_xoff=0,timeout=None
        self.port = port                #set port number
        self.baudrate = baud            #set baud rate
        self.timeout = timeout          #set timeout
       
        #default setting: request sequence asks for SPO2, pulse rate, signal quality, gain, 10 plethysmogram samples) every 100ms
        self.command = [0x7f, 0xd1, 0x01, 0x01, 0x01, 0x02, 0x01, 0x03, 0x01, 0x11, 0x01, 0x04, 0x0a]

        self.daqduration = 15                                       # duration of daq in seconds
        self.required_nr_samples = self.daqduration * 10            # based on self.command, no. of values per block = 10
        self.spo2 = 0
        self.pulse_rate = 0
        self.signal_quality = 0
        self.Request = ''                                           #initialize request as a string
        self.start_flag = 0
        self.stop_flag = 0
    
        self.parentPanel = parent

        try:
            self.bpm = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=0)      
        except serial.SerialException:
            print "Unable to open COM port", 9, "\nPlease check serial port settings."
            
    def checksum(self, data_seq):
        """
        calculate the checksum from the ChipOx request/reply data sequence
        return the data_sequence with the appended checksum, CS higher byte goes first """

        #16-bit checksum or 'CS' is composed of the CS-Hi and CS-Lo bytes     
        CS = int(0x0000)        #initial value for checksum or 'CS'
        CS_Hi = int(0x00)       #initial value for CS High byte
        CS_Lo = int(0x00)       #initial value for CS Low byte

        data_seq_cs = [chr(elem) for elem in data_seq]
       
        #checksum derived from the command sequence - character by character;
        #CS=CS+character;   CS-Hi=CS-Hi+(CS-Lo XOR character)
        for char in data_seq:
            CS_Hi = ((CS_Hi<<8)&int(0xFF00))
            CS = CS_Hi + CS_Lo
            CS = CS + int(char)
            CS_Lo = CS&int(0xFF)
            CS_Hi = (CS>>8)&int(0xFF)
            CS_Hi = CS_Hi + (CS_Lo^(int(char)))
            CS_Hi = (CS_Hi&int(0xFF))

        data_seq_cs.append(chr(CS_Hi))
        data_seq_cs.append(chr(CS_Lo))
        return data_seq_cs
    
    def byte_stuff(self, data_seq_wchecksum):
        """
        filter the data stream for reserved flags
        return a list (of char strings) for byte-stuffed data sequence"""

        #------------------------------------------------------------------------------------------------
        # Rid packets of reserved flags like 0xA8 and 0xA9. Special flags are AND-linked with '0xDF':
	# 0xA8 replaced with 0xA9 0x88
	# 0xA9 replaced with 0xA9 0x89
        #------------------------------------------------------------------------------------------------    
        encoded_sequence = []  
        for char in data_seq_wchecksum:
            if char == chr(0xa8):                                  
                encoded_sequence.append(chr(0xa9))
                encoded_sequence.append(chr(0x88))
            elif char == chr(0xa9):
                encoded_sequence.append(chr(0xa9))
                encoded_sequence.append(chr(0x89))
            else:
                encoded_sequence.append(char)
        return encoded_sequence                                     # return a list containing the byte-stuffed data sequence
            
    def request(self, command):
        """
        arrange the request packet for sending to ChipOx Pulse Oximeter
        accept a list of char strings"""
        
        data_seq2 = [elem for elem in command]
        data_wchecksum = self.checksum(data_seq2)
        data_wbyte_stuff = self.byte_stuff(data_wchecksum)
        request = [elem for elem in data_wbyte_stuff]
        request.insert(0,chr(0xa8))                                 # insert start flag at the begining of request sequence  
        request.append(chr(0xa8))                                   # append end flag at the end of request
        self.Request = ''.join(request)                             # convert request into string
        #print "Request:", request
        
    def spo2reply(self):
        """
        Wait for complete reply packet from ECG module; return a string called packet
        Usage: packet = ECG().ecgreply()"""
        
        reply = ''
        basetime = time.time()
        flag_counter = 0
        while (flag_counter < 2) and (time.time()<(basetime+3)):
            byte = self.bpm.read(1)
            reply = reply + byte
            if byte == chr(0xa8):
                flag_counter = flag_counter + 1
        if time.time()>(basetime+3):
            print "Timeout! Reply packet incomplete:",reply
        return reply

    def byte_destuff(self, raw_packet):
        """
        Detect and decodes byte-stuffed data in reply packet; return a list of char strings called destuffed
        Accept a string called raw_packet"""
        
        #---------------------------------------------------------------------------
        # If reserved character 0xa9 is found in a reply packet it is to be ignored
        # and the following character is OR-linked with 0x20 and saved
        #---------------------------------------------------------------------------

        destuffed = [chr(0xa8)]                                 # initialize list for 'destuffed' reply packet; list already contains start flag
        skip_counter = 0                                        # initialize skip for going to next char
        
        for index in range(1, (len(raw_packet)-1)):             # end flag excluded (next last character is the last candidate for destuffing)
            if skip_counter == 1:                               # re-initialize skip_counter
                skip_counter = 0                                # reset skip_counter to 0                                 
                continue                                        # another skip
            elif skip_counter == 0:
                if raw_packet[index] == chr(0xa9):
                    destuffed.append(chr( ord(raw_packet[index+1])|int(0x20) ))       # append next char(OR-linked with 0x20) to 'destuffed' data_stream list
                    skip_counter+= 1                                                  # move to next next char
                    continue                                                          # skip
                else:
                    destuffed.append(chr( ord(raw_packet[index]) ))                   # char is not 0xa9, simply append it to 'destuffed' data_stream list        
                    continue
        destuffed.append(chr(0xa8))                             # append end flag
        return destuffed                                        # return the 'destuffed' reply packet as a list of char strings

    def reply_parser(self, destuffed_packet):
        """
        extract the readings for sp02, pulse rate & signal quality
        accept the 'destuffed' reply packet from the pulse oximeter """

        destuff = [elem for elem in destuffed_packet]
        CHIPOX_channel = ord(destuff[1])
        if CHIPOX_channel == 127:                                   # CHIPOX channel
            sig_quality = ord(destuff[6])   
            #print "signal quality:", sig_quality, "%"
            if (sig_quality <= 100):                                # if CHIPOX channel is ok and signal quality is not erroneous
                spo2 = ord(destuff[3])
                bpm = (ord(destuff[4])<<8) + ord(destuff[5])
                sig_amp = ord(destuff[7])
                #print "spo2 reading:", spo2
                #print "pulse_rate:", bpm, "bpm"
            else:                                                   # if signal quality is erroneous
                if len(self.spo2_values)>0:                         # if self.spo2 list already contains something
                    prev_spo2 = self.spo2_values[len(self.spo2_values)-1]
                    prev_pulse_rate = self.pulserate_values[len(self.pulserate_values)-1]
                else:                                               # if self.spo2 list does not contain anything yet
                    prev_spo2 = 0
                    prev_pulse_rate = 0
                #print "Warning: Signal quality is erroneous. Get previous readings"
                #print "Previous spo2 reading:", prev_spo2
                #print "Previous pulse_rate:", prev_pulse_rate, "bpm"
                spo2 = prev_spo2
                bpm = prev_pulse_rate
                
        elif CHIPOX_channel == 13:                                  # SYSTEM ERROR channel
            sig_quality = 0
            #print "Signal quality not determined."
            if len(self.spo2_values)>0:                             # if self.spo2 list already contains something
                prev_spo2 = self.spo2[len(self.spo2)-1]
                prev_pulse_rate = self.pulserate_values[len(self.pulserate_values)-1]
            else:                                                   # if self.spo2 list does not contain anything yet
                prev_spo2 = 0
                prev_pulse_rate = 0
            print "Error: Please make sure the sensor is fitted propery. Get previous readings"
            #print "Previous spo2 reading:", prev_spo2
            #print "Previous pulse_rate:", prev_pulse_rate, "bpm"
            spo2 = prev_spo2
            bpm = prev_pulse_rate
        else:
            # "UNKNOWN CHANNEL"
            spo2 = 0
            bpm = 0
            sig_quality = 0
            pass
            
        CallAfter(self.parentPanel.updateSPO2Display, str(spo2))
        CallAfter(self.parentPanel.updateBPMDisplay, str(bpm))
        
        # update values
        self.spo2 = spo2
        self.pulse_rate = bpm
        self.signal_quality = sig_quality
        
    def get_spo2(self):
        """get SpO2, pulse rate (and signal qaulity) readings"""
        
        basetime = time.time()
        print
        print "Acquiring spo2 readings..."
        print "15-sec DAQ started at:", time.ctime()                # get start time
        count = 0
        self.spo2_values = []
        self.pulserate_values = []
        while (time.time() - basetime <= self.daqduration) and (self.stop_flag != 1 ):
            raw_packet = self.spo2reply()                           # get reply packet; raw_packet is a string
            packet = self.byte_destuff(raw_packet)                  # raw_packet undergoes byte-destuffing
            self.reply_parser(packet)                               # updates values for self.spo2 and self.pulse_rate
            self.spo2_values.append(self.spo2)
            self.pulserate_values.append(self.pulse_rate)
            count = count + 1
            
        if self.stop_flag == 1:
            print "Stopped SpO2 DAQ."
        elif self.stop_flag == 0:
            #print "spo2 count:", count
            actual_nr_samples = len(self.spo2_values)
            #print "ACTUAL SpO2 in list:", actual_nr_samples
            excess_nr_samples = ( actual_nr_samples - self.required_nr_samples )
            #print "EXCESS SpO2 in list:", excess_nr_samples
        
            # if number of samples > required, remove the excess
            if excess_nr_samples > 0:                           
                for number in range(0, excess_nr_samples):
                    self.spo2_values.pop()
                    self.pulserate_values.pop()
                                       
            # if number of samples < required, pad with zeros
            elif excess_nr_samples < 0:
                for number in range(0, -(excess_nr_samples)):
                    self.spo2_values.append(0)
                    self.pulserate_values.append(0)     
        
        
            Biosignal_SPO2 = BioSignal('SpO2 finger', 'IR-Red sensor',    '%',      0,    100,    0,    100,    'None',     10,  self.spo2_values)
            ##########################       ^               ^             ^        ^      ^      ^      ^        ^          ^            ^
            ##########################     label        sensor-type     physical   phys.  phys.  digi.  digi     pre-     Nsamples       list
            ##########################                                 dimension   min    max    min    max    filtering

            Biosignal_BPM = BioSignal('SpO2 finger', 'IR-Red sensor',   'bpm',      0,    300,    0,    300,    'None',    10,   self.pulserate_values)
            #########################        ^               ^             ^        ^      ^      ^     ^        ^         ^               ^
            #########################     label        sensor-type     physical   phys.  phys.  digi.  digi     pre-    Nsamples         list
            #########################                                 dimension   min    max    min    max    filtering
        
            self.parentPanel.BioSignals.append(Biosignal_SPO2)
            self.parentPanel.BioSignals.append(Biosignal_BPM)

            print "DAQ ended at:", time.ctime()                         # get end time
         
    def status(self):
        """check status of spo2 device (connection? ready or not?)"""
        pass
    
    def reset(self):
        """reset serial port input buffer"""
        self.bpm.flushInput()           #data currently stored in the input buffer is flushed and operation continues
       
    def get(self):
        """continuously acquire 15-second sp02 and bpm readings from Chipox module"""

        if self.start_flag == 0:                                    # send start_ecg request only once
            self.request(self.command)
            self.reset()
            self.bpm.write(self.Request)
            time.sleep(0.2)                                         # delay = 0.2sec because initial reply of ChipOx comes after (100ms + configured time interval in request,100ms = 200ms)
            self.get_spo2()
            self.start_flag = 1
        elif self.start_flag == 1:
            self.get_spo2()
        
    def stop(self):
        """stop acquisition of SpO2 readings by closing the serial port"""

        self.bpm.close()
        print "Serial port for ChipOx closed."

class BP:
    """manages data request and processes reply packets to/from NIBP module"""

    def __init__(self, parent, port=7, baud=4800, timeout=None):
        """initializes port settings and request data sequence according to specified setting for EMI12"""
        
        self.port = port                
        self.baudrate = baud            
        self.timeout = timeout
        self.startflag = 0x02
        self.endflag = 0x03
        self.measurement_interval = 120         # time interval in seconds of successive bp measurements
        self.inflate_deflate_time = 0
        self.psystole = 0
        self.pdiastole = 0
        self.pmean = 0
        self.tx_status = 0
        self.return_flag = 0
        self.stop_flag = 0
        self.cycle_flag = 0

        self.SELECT_MANUAL_MODE = [0x02, 0x30, 0x33, 0x3B, 0x3B, 0x44, 0x39, 0x03]
        self.SELECT_5MIN_CYCLE_MODE = [0x02, 0x30, 0x38, 0x3B, 0x3B, 0x44, 0x45, 0x03]
        self.SELECT_MANOMETER_MODE = [0x02, 0x31, 0x34, 0x3B, 0x3B, 0x44, 0x42, 0x03]
        self.REBOOT = [0x02, 0x31, 0x35, 0x3B, 0x3B, 0x44, 0x43, 0x03]
        self.START_LEAKAGE_TEST = [0x02, 0x31, 0x37, 0x3B, 0x3B, 0x44, 0x45, 0x03]
        self.START_MEASUREMENT = [0x02, 0x30, 0x31, 0x3B, 0x3B, 0x44, 0x37, 0x03]
        self.READ_STATUS = [0x02, 0x31, 0x38, 0x3B, 0x3B, 0x44, 0x46, 0x03]
        self.SET_140mmHg_PRESSURE = [0x02, 0x32, 0x31, 0x3B, 0x3B, 0x44, 0x39, 0x03]
        self.SET_160mmHg_PRESSURE = [0x02, 0x32, 0x32, 0x3B, 0x3B, 0x44, 0x41, 0x03]
        self.SET_180mmHg_PRESSURE = [0x02, 0x32, 0x33, 0x3B, 0x3B, 0x44, 0x42, 0x03]
        self.SELECT_ADULT_MODE = [0x02, 0x32, 0x34, 0x3B, 0x3B, 0x44, 0x43, 0x03]
        self.ABORT = 0x58
        self.END_OF_CUFF_TRANSMISSION = [0x02, 0x39, 0x39, 0x39, 0x03, 0x0D]
        
        self.parentPanel = parent

        # open port 'self.port w/ baudrate=self.baud & timeout=self.timeout:
        try:
            self.nibp = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=0)      
        except serial.SerialException:
            print "Unable to open COM port", 8, "\nPlease check serial port settings."
        
    def check_status(self):
        """check connectivity; confirm if device is ready"""
        pass

    def reset(self):
        """reset serial port input buffer"""
        self.nibp.flushInput()

    def reset_bp(self):
        """software reset for the nibp device"""
        pass
        
    def request(self, command):
        """
        Arranges the request packet for sending to NIBP2010 BP Monitor
        Accepts a list of hex numbers called command"""

        request = [chr(elem) for elem in command]
        bprequest = ''.join(request)
        return bprequest
        
    def bpreply(self):
        """
        Wait for complete reply packet from NIBP module; return a string called packet
        Usage: packet = NIBP().bpreply()"""

        reply = ''
        #2ndlast_byte = chr(0x00)
        last_byte = chr(0x00)
        basetime = time.time()
        #while (2ndlast_byte != chr(self.endflag)) and (time.time()<(basetime+3)):
        while (last_byte != chr(0x0D)) and (time.time()<(basetime+3)):
            last_byte = self.nibp.read(1)
            reply = reply + last_byte
        if time.time()>(basetime+3):
            print "Timeout! Reply packet incomplete:",reply
        return reply

    def start_bp(self):
        """start bp transmission"""

        print
        print "***Start BP Measurement***"
        self.nibp.write(self.request(self.START_MEASUREMENT))

    def get_cuffpressure(self):
        """continuously acquires cuff pressure readings"""

        print
        print "***Acquiring cuff pressure readings...***"
        end_tx = self.request(self.END_OF_CUFF_TRANSMISSION)
        reply = 'string to initialize'
        basetime = time.time()
        while (reply != end_tx) and (time.time()< (basetime+70)):
            reply = self.bpreply()
            self.extract_cuffpressure(reply)
        if (reply == end_tx):
            print "***END of Cuff Pressure Transmission***"
            tx_status = 1
        elif time.time()>(basetime+60):
            print "Timeout! Did not reach END OF TRANSMISSION"
            tx_status = 0
        else:
            print "Did not reach END OF CUFF PRESSURE TRANSMISSION"
            tx_status = 0
        return tx_status
            
    def extract_cuffpressure(self, reply):
        """get current cuff pressure"""

        packet = reply
        if (packet[0]==chr(0x02)) and (packet[4]== chr(0x43)) and \
            (packet[5]==chr(0x30)) and (packet[6]==chr(0x53)) and \
            (packet[7]==chr(0x33)):
            d0 = ord(packet[1]) - int(0x30)
            d1 = ord(packet[2]) - int(0x30)
            d2 = ord(packet[3]) - int(0x30)
            cuff_pressure = (100*d0) + (10*d1) + (d2)
            #print "Current Cuff Pressure:", cuff_pressure, "mmHg"
            return cuff_pressure
    
    def get_bp(self):
        """acquire bp reading from NIBP BP Monitor"""

        self.start_bp()
        basetime = time.time()
        self.tx_status = self.get_cuffpressure()
        inflate_deflate_time = time.time()- basetime
        if (self.tx_status == 1):
            self.read_status()
            self.nibp.write(chr(self.ABORT))
            print "Abort request sent... BP device now in standby mode."
        else:
            print "Transmission status: Failed."
            self.stop()
        return inflate_deflate_time     
    
    def read_status(self):
        """check current status of bp module and read current bp readings"""

        print
        print "***Read BP Measurement***"
        self.nibp.write(self.request(self.READ_STATUS))
        status = self.bpreply()
        if status[4]==chr(0x41) and status[5]==chr(0x30) and \
           status[12]==chr(0x30) and ( status[13]==chr(0x30) or status[13]==chr(0x33) ) and \
           status[15]==chr(0x50):
            self.psystole = ((ord(status[16]) - int(0x30))*100) + ((ord(status[17]) - int(0x30))*10) + (ord(status[18]) - int(0x30))
            self.pdiastole = ((ord(status[19]) - int(0x30))*100) + ((ord(status[20]) - int(0x30))*10) + (ord(status[21]) - int(0x30))
            self.pmean = ((ord(status[22]) - int(0x30))*100) + ((ord(status[23]) - int(0x30))*10) + (ord(status[24]) - int(0x30))
            print "Measuring mode: ADULT"
            print "Systolic Pressure:", self.psystole, "mmHg"
            print "Diastolic Pressure:", self.pdiastole, "mmHg"
            print "Mean Pressure:", self.pmean, "mmHg"
        else:
            print "ERROR in measurement!"
            self.stop()
            self.psystole = '-'
            self.pdiastole = '-'
            self.pmean = '-'
            
        pressure = str(self.psystole) + "/" + str(self.pdiastole)
        CallAfter(self.parentPanel.updateBPDisplay, pressure)
    
    def getnow(self):
        """acquire bp reading one-shot"""

        print
        print "*** ONE-SHOT BP ***"
        request=self.request(self.SELECT_ADULT_MODE)
        self.nibp.write(request)
        self.inflate_deflate_time = self.get_bp()
        if self.cycle_flag == 0:
            self.stop()

    def bpEDF(self):
        """packages BP reading for edf generation"""

        self.systole_values = []
        self.diastole_values = []

        for second in range(0,15):
            self.systole_values.append(self.psystole)
            self.diastole_values.append(self.pdiastole)
            
        Biosignal_pSys = BioSignal('bpsystole', 'NIBP2010',   'mmHg',     0,    300,    0,   300,     'None',     1,     self.systole_values)
        #########################      ^            ^           ^         ^      ^      ^     ^         ^         ^               ^
        #########################    label     sensor-type   physical    phys.  phys.  digi.  digi     pre-    Nsamples          list
        #########################                            dimension   min    max    min    max    filtering
        
        Biosignal_pDias = BioSignal('bpdiastole', 'NIBP2010',    'mmHg',    0,   300,    0,    300,    'None',     1,   self.diastole_values)
        ##########################      ^            ^             ^        ^     ^      ^      ^        ^         ^            ^
        ##########################    label      sensor-type    physical   phys. phys.  digi  digi     pre-     Nsamples       list
        ##########################                             dimension   min   max    min    max    filtering

        self.parentPanel.BioSignals.append(Biosignal_pSys)
        self.parentPanel.BioSignals.append(Biosignal_pDias)

        self.return_flag = 1
        print "returned bp \n"

    def get(self):
        """implements pseudo-cycle mode for BP measurement"""
        
        self.cycle_flag = 1
        self.getnow()
        self.cycle_flag = 0
        self.bpEDF()
        if self.tx_status == 1:
            waiting_time = self.measurement_interval - self.inflate_deflate_time
            remaining_time = waiting_time
            while (remaining_time > 0) and (self.stop_flag != 1):
                #print "Time remaining before next measurement:", remaining_time
                remaining_time = remaining_time - 1
                time.sleep(1)
            if self.stop_flag == 1:
                print "Stop BP measurement. Cancel countdown timer."
            self.tx_status = 0          # re-initialize to 0
        elif self.tx_status == 0:
            print "BP DAQ has stopped."
            
    def stop(self):
        """stop acquisition of nibp readings and close the serial port"""
           
        self.nibp.write(chr(self.ABORT))
        self.nibp.close()
        print "Serial port for NIBP closed."
        self.cycle_flag = 0


