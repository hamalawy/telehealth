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
import random

LEAD_KEYS = []
ECM_KEYS1 = ['C1','C2','C3','C4','C5','C6','N','F','R','L']
ECM_KEYS2 = ['N','F','L','R','C6','C5','C4','C3','C2','C1']


class ECGDAQ:
    def __init__(self, port='/dev/ttyUSB0', baud=230400, mode='12lead', freq=500, timeout=3, daqdur=1, debug=True):
        self.port = port
        self.baud = baud
        self.mode = mode
        self.freq = freq
        self.timeout = timeout
        self.daqdur = daqdur
        self.debug = debug
        
        self.dataset_counter = 0
        self.packet_num = 0
        self.getecg = False
        
        self.firmwareversion = ''
        
        global LEAD_KEYS
        if mode=='3lead':
            self.ecg_lead = {'I':[],'II':[],'III':[]}
            LEAD_KEYS = ['II','III']            
        else:
            self.ecg_lead = {'I':[],'II':[],'III':[],'V1':[],'V2':[],'V3':[],'V4':[],'V5':[],'V6':[],'VR':[],'VL':[],'VF':[]}
            LEAD_KEYS = ['II','III','V1','V2','V3','V4','V5','V6']

        self.ecm_stat = {}
        for i in ECM_KEYS1: self.ecm_stat[i]=False
        
        self.status = self.Open()

    def Print(self, string=''):
        if self.debug:
            print string
            
    def Open(self):
        self.ecgserial = open(self.port,'r')
        self.buff = self.ecgserial.read()
        self.strind = 0
        self.strlen = len(self.buff)
        FIX = [self.selftest, self.stop_ecg, self.selftest, self.stop_ecm, self.selftest]
        for i in FIX:
            time.sleep(1)
            if i(): return True
        return False

    def ecgrequest(self, bits):
        pass

    def ecgreply(self):
        buff = ''
        end = chr(0xfd)
        mid = chr(0xfe)
        while True:
            temp = self.buff[self.strind]
            self.strind = (self.strind+1)%self.strlen
            if temp == '':
                self.Print('Packet Timeout')
                break
            elif temp == end:
                buff += end
                break
            elif temp == mid: 
                buff += chr(ord(self.buff[self.strind])^0x20)
                self.strind = (self.strind+1)%self.strlen
            else: buff += temp
        return array.array('B',buff).tolist()

    def firmware(self):
        self.Print()
        self.Print("***Firmware Version Inquiry***")
        self.Print('Firmware Version: Simulated')
        return True
            
    def protocol(self):
        self.Print() 
        self.Print("***Protocol Version Inquiry***")
        self.Print('Protocol Version: Simulated')
        return True
            
    def device_id(self):
        self.Print()
        self.Print("***Device Identification Inquiry***")
        self.ecgrequest(IDENTIFICATION_INQUIRY)
        self.Print('Device ID: Simulated')
        return True
            
    def selftest(self):
        self.Print()
        self.Print("***Integrated Self Test Inquiry***")
        self.Print('Device Successfully Passed! Simulated')
        return True

    def set_ecm_threshold(self):
        """set electrode contact measurement (ecm) threshold for the ecg module"""
        self.Print()
        self.Print("***Set ECM Threshold Request***")
        self.Print('Set ECM Threshold Request Confirmed')
        return True

    def start_ecm(self):
        """start offline electrode contact measurement (ecm)"""
        self.Print()
        self.Print("***Start Offline ECM***")                          
        self.Print('Start_Offline_ECM ACK')
        return True
            
    def stop_ecm(self):
        """stop offline electrode contact measurement (ecm)"""
        self.Print()
        self.Print("***Stop Offline ECM***")
        self.Print("REPLY: Stop_Offline_ECM ACK")
        return True
            
    def get_ecm(self):
        time.sleep(0.5)
        self.Print()
        ecm_data = {}
        ecm_stat = self.ecm_stat
        for key in ECM_KEYS2:
            self.Print("ECM for lead %s: %d"%(key, 200000))
        for key in ECM_KEYS1:
            if (random.randint(0,1)==1 or ecm_stat[key]) and random.randint(0,30)!=1:
                ecm_stat[key] = True
                self.Print("--->>electrode %s has contact"%key)
            else:
                ecm_stat[key] = False
                self.Print("--->>electrode %s has no contact"%key)
        if ecm_stat['N'] and ecm_stat['F'] and ecm_stat['L'] and ecm_stat['R']:
            return True
        return False
            
    def config_analog(self):
        self.Print()
        self.Print('***Configure Analog Request***')
        self.Print('Configure Analog Request Confirmed')
        self.Print('ECG Type: 12-lead Sampling Rate: 500Hz')
        return True

    def start_ecg(self):
        """start ecg transmission"""
        self.Print()
        self.Print("***Start ECG Transmission***")
        self.Print("REPLY: Start_ECG_TRANSMISSION ACK")
        return True

    def stop_ecg(self):
        """stop ecg transmission"""
        self.Print()
        self.Print("***Stop ECG Transmission***")
        self.Print("REPLY: Stop_ECG_TRANSMISSION ACK")
        return True
            
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
                    if p1 > 0x7f: tmp -= 0x7f
                    index += 1
                data[key].append(tmp)
            l2 = data['II'][-1]
            l3 = data['III'][-1]
            data['I'].append(l2-l3)
            if lead3:
                data['VR'].append(0.5*(l3-l2))
                data['VL'].append(0.5*l2-l3)
                data['VF'].append(0.5*(l2+l3))
        self.dataset_counter = new_dataset_counter
        return data
        
    def get_ecg(self):
        self.getecg = True
        Basetime = time.time()+self.daqdur
        self.Print("Acquiring ECG readings...")
        self.Print("DAQ started at: %s"%time.ctime())                 # get start time
        old = self.dataset_counter
        data = 0
        while data<500 and self.getecg:
            raw_packet = self.ecgreply()
            if(old > self.dataset_counter): old = 0
            data += self.dataset_counter-old
            old = self.dataset_counter
            if not raw_packet: break
            self.payload_parser(raw_packet)
        time.sleep(1)
        self.Print("DAQ ended at: %s"%time.ctime())                   # get end time
    
    def Close(self):
        self.ecgserial.close()
        
    def Pop(self,start=0,end=0):
        data = self.ecg_lead
        for key in data:
            del data[key][start:end]
    
    def abort_ecg(self):
        self.getecg = False
