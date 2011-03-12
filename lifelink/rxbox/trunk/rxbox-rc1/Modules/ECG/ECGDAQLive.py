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
import array
import time
import serial

CRC = (0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,\
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
        0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0)
CONFIG_ANALOG_REQ = [0x01, 0x09, 0x02, 0x05]           # 0x02 = 12 lead; 0x05 = 500Hz sampling rate
SET_ECM_THRESHOLD_REQ = [0x18, 0x09, 0x00, 0x9F, 0x24]
START_OFFLINE_ECM = [0x26, 0x09, 0x01]
STOP_OFFLINE_ECM = [0x26, 0x09, 0x00]
PROTOCOL_VERSION_INQUIRY = [0x00, 0x08, 0x00, 0x01]
FIRMWARE_VERSION_INQUIRY = [0x00, 0x08, 0x50, 0x01]
IDENTIFICATION_INQUIRY = [0x00, 0x08, 0x00, 0x05]
SELFTEST_INQUIRY = [0x00, 0x08, 0x00, 0x06]
START_ECG_TRANSMISSION = [0x05, 0x09, 0x01]
STOP_ECG_TRANSMISSION = [0x05, 0x09, 0x00]

LEAD_KEYS = []
ECM_KEYS1 = ['C1','C2','C3','C4','C5','C6','N','F','R','L']
ECM_KEYS2 = ['N','F','L','R','C6','C5','C4','C3','C2','C1']


class ECGDAQ:
    def __init__(self, port='/dev/ttyUSB0', baud=230400, mode='12lead', freq=500, timeout=3, daqdur=1, debug=True, logger=''):
        self.port = port
        self.baud = baud
        self.mode = mode
        self.freq = freq
        self.timeout = timeout
        self.daqdur = daqdur
        self.debug = debug
        self._logger = logger

        self.dataset_counter = 0
        self.packet_num = 0
        self.getecg = False
        
        self.firmwareversion = ''
        
        global LEAD_KEYS
        global CONFIG_ANALOG_REQ
        if mode=='3lead':
            CONFIG_ANALOG_REQ[2] = 0x01
            self.ecg_lead = {'I':[],'II':[],'III':[]}
            LEAD_KEYS = ['II','III']            
        else:
            CONFIG_ANALOG_REQ[2] = 0x02
            self.ecg_lead = {'I':[],'II':[],'III':[],'V1':[],'V2':[],'V3':[],'V4':[],'V5':[],'V6':[],'VR':[],'VL':[],'VF':[]}
            LEAD_KEYS = ['II','III','V1','V2','V3','V4','V5','V6']
            
        if freq == 100: CONFIG_ANALOG_REQ[3] = 0x01
        elif freq == 200: CONFIG_ANALOG_REQ[3] = 0x02
        elif freq == 1000: CONFIG_ANALOG_REQ[3] = 0x0A
        else: CONFIG_ANALOG_REQ[3] = 0x05
        
        self.ecm_stat = {}
        for i in ECM_KEYS1: self.ecm_stat[i]=False
        
        #self.status = self.Open()

    def Print(self, string=''):
        if self.debug and self._logger=='':
            print string
        elif self.debug:
            self._logger.debug(string)
    
    def Check(self, port):
        self.ecgserial = serial.Serial(port, baudrate=self.baud, timeout=1, xonxoff=0)
        self.ecgrequest(SELFTEST_INQUIRY)
        if len(self.ecgreply())>900: return False
        FIX = [self.selftest, self.stop_ecg, self.selftest, self.stop_ecm,  self.selftest, self.stop_ecg, self.selftest]
        for i in FIX:
            self.flushout()
            if i(): 
                self.Close()
                return True
        self.Close()        
        return False

    def Open(self):
        data = self.ecg_lead
        for key in data:
            del data[key][:]
            data[key] = [0]*7500

        self.ecgserial = serial.Serial(self.port, baudrate=self.baud, timeout=self.timeout, xonxoff=0)
        FIX = [self.selftest, self.stop_ecg, self.selftest, self.stop_ecm,  self.selftest, self.stop_ecg, self.selftest]
        for i in FIX:
            self.flushout()
            if i(): 
                self.status = True
                return True
        self.status = False
        return False

    def ecgrequest(self, bits):
        tpacket = [self.packet_num] + bits
        crc = 0xffff
        for i in tpacket:
            tmp = (crc>>8)^i                          # calculate index called tmp for corresponding crc_polynomial in crctttab
            crc = ((crc<<8)&0xffff)^(CRC[tmp])        # Or-link shifted version of crc(get 16bits only) with the crc_polynomial referenced by the index
        tpacket += [crc&0xff,crc>>8]                  # get high-byte of checksum
        packet = [0xfc]
        for i in tpacket:
            if i == 0xfc: packet += [0xfe,0xdc]
            elif i == 0xfe: packet += [0xfe,0xdd]
            elif i == 0xfd: packet += [0xfe,0xde]
            else: packet.append(i)
        packet.append(0xfd)
        
        self.ecgserial.write(array.array('B',packet).tostring())
        self.packet_num = (self.packet_num+1)%256

    def ecgreply(self):
        buff = ''
        end = chr(0xfd)
        mid = chr(0xfe)
        read = self.ecgserial.read
        buff2 = ''
        while True:
            temp = read(1)
            if temp == '':
                self.Print('Packet Timeout')
                break
            elif temp == end:
                buff += end
                buff2 += end
                break
            elif temp == mid:
                buff2 += temp
                temp2 = read(1)
                buff += chr(ord(temp2)^0x20)
                buff2 += temp2
            else:
                buff += temp
                buff2 += temp
            if len(buff)>1000: break
        return array.array('B',buff).tolist()

    def flushout(self):
        for i in xrange(10):
            if not self.ecgreply(): break

    def firmware(self):
        self.Print()
        self.Print("***Firmware Version Inquiry***")
        self.ecgrequest(FIRMWARE_VERSION_INQUIRY)
        packet = self.ecgreply()
        if packet[2] == 0x50 and packet[3] == 0x01:
            self.firmwareversion = array.array('B',packet[4:15]).tostring()
            self.Print('Firmware Version: %s' % self.firmwareversion)
            return True
        else:
            self.Print('Error: Firmware Unidentified')
            return False
            
    def protocol(self):
        self.Print() 
        self.Print("***Protocol Version Inquiry***")
        self.ecgrequest(PROTOCOL_VERSION_INQUIRY)
        packet = self.ecgreply()
        if packet[2] == 0x00 and packet[3] == 0x01:
            self.Print('Protocol Version: %d' % packet[4])
            return True
        else:
            self.Print('Error: Unknown Protocol Version')
            return False
            
    def device_id(self):
        self.Print()
        self.Print("***Device Identification Inquiry***")
        self.ecgrequest(IDENTIFICATION_INQUIRY)
        packet = self.ecgreply()
        if packet[2]==0x00 and packet[3]==0x05 and packet[4]==0x01 and packet[5]== 0x1e:
            self.Print('Manufacturer ID: Corscience')
            self.Print('Device ID: OEM Board')
            return True
        else:
            self.Print('Error: Unknown Device')
            return False
            
    def selftest(self):
        try:
            self.Print()
            self.Print("***Integrated Self Test Inquiry***")
            self.ecgrequest(SELFTEST_INQUIRY)
            packet = self.ecgreply()
            if packet[2]==0x00 and packet[3]==0x06 and packet[4]==0xe4 and packet[5]==0x20:
                self.Print('Device Successfully Passed!')
                return True
            elif packet[2]== 0x00 and packet[3]==0x06:
                if packet[4]&128!=128: self.Print('Error: RAM Test Failed!')
                elif packet[4]&64!=64: self.Print('Error: int_FLASH Test Failed!')
                elif packet[4]&32!=32: self.Print('Error: PLD/ADC Test Failed!')
                return False
            else:
                self.Print("Error: Self Test Error!")
                return False
        except Exception, e:
            return False

    def set_ecm_threshold(self):
        """set electrode contact measurement (ecm) threshold for the ecg module"""
        
        self.Print()
        self.Print("***Set ECM Threshold Request***")
        self.ecgrequest(SET_ECM_THRESHOLD_REQ)          
        packet = self.ecgreply()                        
        if packet[2]==0x18 and packet[3]==0x07 and packet[4]==0x00 and \
           packet[5]==0x9f and packet[6]==0x24:                          
            self.Print('Set ECM Threshold Request Confirmed')

    def start_ecm(self):
        """start offline electrode contact measurement (ecm)"""

        self.Print()
        self.Print("***Start Offline ECM***")
        self.ecgrequest(START_OFFLINE_ECM)               
        packet = self.ecgreply()                         
        if packet[2]==0x00 and packet[3]==0x02 and packet[4]==(self.packet_num-1)%256:                          
            self.Print('Start_Offline_ECM ACK')
            return True
        return False
            
    def stop_ecm(self):
        """stop offline electrode contact measurement (ecm)"""
        try:
            self.Print()
            self.Print("***Stop Offline ECM***")
            self.ecgrequest(STOP_OFFLINE_ECM)                
            packet = self.ecgreply()
            if packet[2]==0x00 and packet[3]==0x02 and packet[4]==(self.packet_num-1)%256:                          
                self.Print("REPLY: Stop_Offline_ECM ACK")
                return True
        except:
            pass
        return False
            
    def get_ecm(self):
        self.Print()
        packet = self.ecgreply()
        ecm_data = {}
        ecm_stat = self.ecm_stat
        if packet[2] == 0x26 and packet[3] == 0x07:             # 0x0726 - offline ecm
            index = 6
            for key in ECM_KEYS2:
                ecm_data[key] = (packet[index+2]<<16)+(packet[index+1]<<8)+packet[index]
                index += 3
                self.Print("ECM for lead %s: %d"%(key, ecm_data[key]))
            ecmbyte = ((packet[4]&0x07)<<7) + (packet[5]&0x7f)
            for key in ECM_KEYS1:
                if ecmbyte%2==1:
                    ecm_stat[key] = True
                    self.Print("--->>electrode %s has contact"%key)
                else:
                    ecm_stat[key] = False
                    self.Print("--->>electrode %s has no contact"%key)
                ecmbyte /= 2
            if ecm_stat['N'] and ecm_stat['F'] and ecm_stat['L'] and ecm_stat['R']:
                return True
        return False
            
    def config_analog(self):
        self.Print()
        self.Print('***Configure Analog Request***')
        cf = CONFIG_ANALOG_REQ
        self.ecgrequest(cf)            
        packet = self.ecgreply()                              
        if packet[2]==cf[0] and packet[3]==cf[1] and packet[4]==cf[2] and packet[5]==cf[3]:
            self.Print('Configure Analog Request Confirmed')
            self.Print('ECG Type: 12-lead Sampling Rate: 500Hz')

    def start_ecg(self):
        """start ecg transmission"""
        self.Print()
        self.Print("***Start ECG Transmission***")
        self.ecgrequest(START_ECG_TRANSMISSION)               
        packet = self.ecgreply()                              
        if packet[2]==0x00 and packet[3]==0x02 and packet[4]==(self.packet_num-1)%256:
            self.Print("REPLY: Start_ECG_TRANSMISSION ACK")
            return True
        return False

    def stop_ecg(self):
        """stop ecg transmission"""
        try:
            self.Print()
            self.Print("***Stop ECG Transmission***")
            self.ecgrequest(STOP_ECG_TRANSMISSION)                
            packet = self.ecgreply()
            if packet[2]==0x00 and packet[3]==0x02 and packet[4]==(self.packet_num-1)%256:
                self.Print("REPLY: Stop_ECG_TRANSMISSION ACK")
                return True
        except:
            pass
        return False
            
    def payload_parser(self, packet):
        new_dataset_counter = (packet[-4]<<14)+(packet[-5]<<7)+packet[-6]
        frames = new_dataset_counter - self.dataset_counter
        
        data = self.ecg_lead
        lead3 = self.mode!='3lead'
        index = 9
        for frame in xrange(frames):
            for key in LEAD_KEYS:
                p1 = packet[index]
                if p1%2 == 1:
                    tmp = (((p1&0x7e)<<7)+packet[index+1])
                    if p1 > 0x7f: tmp -= 0x3fff
                    index += 2
                else:
                    tmp = ((p1&0x7e)>>1)
                    if p1 > 0x7f: tmp -= 0x3f
                    index += 1
                data[key].append(tmp)
            l2 = data['II'][-1]
            l3 = data['III'][-1]
            data['I'].append(l2-l3)
            if lead3:
                data['VR'].append(0.5*l3-l2)
                data['VL'].append(0.5*l2-l3)
                data['VF'].append(0.5*(l2+l3))
        self.dataset_counter = new_dataset_counter
        return data
        
    def get_ecg(self):
        self.getecg = True
        Basetime = time.time()+self.daqdur
        self.Print("Acquiring ECG readings...")
        self.Print("DAQ started at: %s"%time.ctime())                 # get start time
        while time.time()<Basetime and self.getecg:
            raw_packet = self.ecgreply()
            self.payload_parser(raw_packet)
        self.Print("DAQ ended at: %s"%time.ctime())                   # get end time
    
    def patient_ready(self):
        if not self.getecg:
            self.config_analog()
            self.start_ecg()
        self.get_ecg()
        
    def Close(self):
        self.ecgserial.close()
        
    def Pop(self,start=0,end=0):
        data = self.ecg_lead
        for key in data:
            del data[key][start:end]
    
    def abort_ecg(self):
        self.getecg = False
