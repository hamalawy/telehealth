"""
Project Lifelink: RxSensor Module
Facilitates Data Acqiusition (DAQ) from three biomedical modules - Pulse Oximeter, ECG & BP Meter.
    
    Julius Miguel J. Broma
    Arlan Roie A. Santos
    ------------------------------------------------
    Instrumentation, Robotics and Control Laboratory
    University of the Philippines - Diliman
    ------------------------------------------------
    January 2008        
"""

import serial
import time
from edf import BioSignal
import threading
import wx
import time

from matplotlib.dates import drange
from matplotlib.figure import Figure
from matplotlib.pyplot import axes
from matplotlib.ticker import LinearLocator
import matplotlib.widgets

from pylab import date2num, num2date

import datetime

global interval
interval = 15

global ECG_BUFFER
ECG_BUFFER = 300

global TIMER_ID
TIMER_ID = wx.NewId()
        
class SPO2(threading.Thread):
    """manages data request and acquistion from the ChipOx OEM module"""
    
    def __init__(self, ParentWindow, port=0,baud=9600,timeout=None):
        """initializes port settings and request according to the specified setting for ChipOx"""

        threading.Thread.__init__(self)
        self.stopAcquireThr = threading.Event()
        self.stopAcquireThr.clear()

        self.ParentWindow = ParentWindow
        self.index = 0
#        self.spo2_testfile = "C:/Users/ARLAN ROIE SANTOS/Desktop/spo2_testfile2.txt"
        
        #default: port=0,baud=9600,bytesize=8,parity='N',stopbits=1,xon_xoff=0,timeout=None
        #only three configurable port parameters 
        self.port = port                #set port number
        self.baudrate = baud            #set baud rate
        self.timeout = timeout          #set timeout
       
        #default setting: request sequence asks for SPO2, pulse rate, signal quality, gain, 10 plethysmogram samples) every 100ms
        sequence = ['0x7f', '0xd1', '0x01','0x01','0x01','0x02','0x01','0x03','0x01','0x11','0x01','0x04','0x0a']
        self.sequence = sequence
        self.CS_Lo_byte = []            #initialize CheckSum Low byte as a list of ASCII HEX char (e.g.'0xa5','0x51')
        self.CS_Hi_byte = []            #initialize CheckSum High byte as a list of ASCII HEX char
        self.Request = ''               #initialize request as a string          
        self.Reply = []                 #initialize reply as a list

#        self.myFile = open(self.spo2_testfile, 'r')   #open testfile containing pseaudo sp02 values
        try:
            self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=0)      
        except serial.SerialException:
            print "Unable to open COM port",self.port+1, "\nPlease check serial port settings."
            return 0
        
    def checksum(self):
        """calculates the checksum from the ChipOx request/reply data sequence"""
        #16-bit checksum or 'CS' is composed of the CS-Hi and CS-Lo bytes
        checksum = []
        CS = int('0x0000',0)        #initial value for checksum or 'CS'
        CS_Hi = int('0x00',0)       #initial value for CS High byte
        CS_Lo = int('0x00',0)       #initial value for CS Low byte

        #checksum derived from the request sequence - character by character;
        #CS=CS+character;   CS-Hi=CS-Hi+(CS-Lo XOR character)
        for char in self.sequence:
            CS_Hi = ((CS_Hi<<8)&65280)
            CS = CS_Hi + CS_Lo
            checksum.append(CS)
            CS = CS + int(char,0)
            CS_Lo = CS&255
            self.CS_Lo_byte.append(hex(CS_Lo))
            CS_Hi = (CS>>8)&255
            CS_Hi = CS_Hi + (CS_Lo^(int(char,0)))
            CS_Hi = (CS_Hi&255)
            self.CS_Hi_byte.append(hex(CS_Hi))
            
    def request(self):
        """arranges the request packet for sending to ChipOx"""
        request1=['0xa8']       #request starts with the start flag '0xa8'
        #Append the data request sequence
        for x in self.sequence:
            request1.append(x)

        self.checksum()         #calculate checksum    
        #For the CHECKSUM, append the last hex values in Lo_byte1 and Hi_byte1 to self.request
        l=len(self.CS_Hi_byte)
        request1.append(self.CS_Hi_byte[l-1])
        request1.append(self.CS_Lo_byte[l-1])
        
        #Append end flag '0xa8' to request1
        request1.append('0xa8')       
        #Convert request1(from hex) into characters:
        request2=[]
        for x in request1:
            request2.append(chr(int(x,0)))       
        #Concatenate request2 characters with no separator
        self.Request= ''.join(request2)
        print "FINAL REQUEST as characters:", self.Request
        
    def status(self):
        """get status of biomed module using specified data packet?"""
        pass
    
    def reset(self):
        """reset serial port input buffer"""
        self.ser.flushInput()            #data currently stored in the input buffer is flushed and operation continues
       
    def stop(self):
        self.stopAcquireThr.set()

    def run(self):
        """acquire pseudo spo2 readings from text file"""
        
        while True:
            if self.stopAcquireThr.isSet():
                print 'break'
                break

            self.request()              #generate request sequence to be sent to ChipOx

#            print self.ser.portstr           #check which port was really used
            self.reset()                #reset serial port input buffer
            self.ser.write(self.Request)     #writes the request string on the opened serial port
            time.sleep(0.2)             #delay = 0.2sec because initial reply of ChipOx comes after (100ms + configured time interval in request,100ms = 200ms)       
        
            flag = 0                    #flag can be 0/1--determine whether or not data field is already traversed successfully;\

            while 1:
                spo2 =[]                            #initialize list for spo2 values
                BaseTime = time.time()              #get reference time
                prev_spo2_val = 0                   #initialize spo2 values
                spo2_val=0
                while (len(spo2) != 150):
                    y = self.ser.inWaiting()             #y = number of bytes in the buffer
                    if (y==0):
                        #print "no packet in receive buffer."
                        pass              
                    elif (y>=8):
                        s = self.ser.read(y)                         #read up to as much is in the buffer
                        for i in s:                             #put every reply packet in the 'reply' list
                            self.Reply.append(hex(ord(i)))
                        for i in range(0, len(s)):              #parse each received reply packet
                            if (i == (len(s)-1)):               #checks if char is already the last in the packet; if so, cannot access s[i+1] anymore 
                                flag=0
                                continue
                            if (s[i] == chr(int('0xa8',0))) and (s[i+1] == chr(int('0x7f',0))) and \
                               (s[len(s)-1]== chr(int('0xa8',0))):              #if start flag is detected and last char is end flag
                                if ((i+7) <= (len(s)-1)):                       #if indeces of succeeding items to be accessed are still possible
                                    spo2_val = ord(s[i+3])                          #spo2 value is the 4th element in the packet-after start flag,channel id & identifier
                                    if (s[i+5] == chr(int('0xa9',0))):          #if reserved char '0xa9' is detected in the pulse rate data block, the next char is decoded
                                        pulse_rate = int((hex(ord(s[i+4]))+'00'),0) + (ord(s[i+6])^int('0x20',0))
                                        index = i+6
                                    else:                                       #no reserved char '0xa9' detected; pulse rate is just the integer equivalent of next char
                                        pulse_rate = int((hex(ord(s[i+4]))+'00'),0)+ ord(s[i+5]) 
                                        index = i+5   
                                    if (ord(s[index+1]) <= 100):                #if signal quality is possible ( less than/equal to 100% ), transfer the readings
                                        signal_quality = ord(s[index+1])
                                        #print "spo2:", spo2_val
                                        wx.CallAfter(self.ParentWindow.datapanel.UpdateSpO2Display, str(spo2_val))
                                        prev_spo2_val = spo2_val

                                        spo2.append(spo2_val)
                                        #print "pulse rate:", pulse_rate
                                        #print "signal quality:", signal_quality
                                        #print
                                        flag=1
                                    else:                                       #signal quality is erroneous, data samples are not transferred  
                                        flag=1
                                        #print "spo2(PREVIOUS):", prev_spo2_val
                                        wx.CallAfter(self.ParentWindow.datapanel.UpdateSpO2Display, str(prev_spo2_val))
                                        spo2.append(prev_spo2_val)
                                        break        
                                else:                                                            
                                    #print "string index not possible"
                                    break
                            elif ((s[i] == chr(int('0x0e',0)))and(flag==0)):
                                #print "Error: make sure the finger sensor is fitted properly. "
                                #print "spo2(PREVIOUS):", spo2_val
                                spo2.append(spo2_val)
                                continue
                            else:
                                flag=0
                                continue              
                Biosignal_SPO2 = BioSignal('SpO2 finger', 'IR-Red sensor',    '%',      0,    100,    0,    100,    'None',      10,    spo2)
                ##########################       ^               ^             ^        ^      ^      ^      ^        ^          ^       ^
                ##########################     label        sensor-type     physical   phys.  phys.  digi.  digi     pre-    Nsamples   list
                ##########################                                 dimension    min   max    min    max   filtering
                #trigger = 1
                self.ser.close()
                #print '-'*50
                #print 'Returning SPO2'
                return (self.ParentWindow.BioSignals.append(Biosignal_SPO2))
        
            self.ser.close()
                
       
class ECG(threading.Thread):
    """manages data request and acquistion from the EMI12 ECG module"""


    
    def __init__(self, ParentWindow, port=1,baud=230400,timeout=None):

        threading.Thread.__init__(self)
        self.stopAcquireThr = threading.Event()
        self.stopAcquireThr.clear()
        
        self.port = port                #set port number
        self.baudrate = baud            #set baud rate
        self.timeout = timeout          #set timeout
        
        self.ParentWindow = ParentWindow
        self.index = 0
        self.counter = 0
        
        self.samples = self.ParentWindow.RawBioSignals[0]
        self.ECGsamples = [sample * self.ParentWindow.datapanel.ecg_plotter.gain for sample in self.samples]
#        self.ecg_testfile = "C:/Users/ARLAN ROIE SANTOS/Desktop/ecg_testfile.txt"

#        self.ParentWindow.Bind(wx.EVT_TIMER, self.onTimer)
        self.Timer = self.ParentWindow.datapanel.t
    def checksum(self):
        """calculates the checksum from the EMI ECG request data sequence"""
        pass
    
    def stop(self):
        self.stopAcquireThr.set()
        
    def run(self):
        """acquire pseudo ECG reading from text file"""
        
###        self.Timer.Start(1)
        pass    

    def plotdata(self, ecgsample):
        pass
                
#    def status(self):
#        """get status of ECG module using specified data packet"""
#        pass
    
    def reset(self):
        """reset ECG module using specified data packet"""
        ser1.flushInput()               #data currently stored in the input buffer is flushed and operation continues

class PulseRate(threading.Thread):
    """manages acquisition of BPM either from ChipOx or EMI ECG module"""

    def __init__(self, ParentWindow):

        threading.Thread.__init__(self)
        self.stopAcquireThr = threading.Event()
        self.stopAcquireThr.clear()

        self.ParentWindow = ParentWindow
        self.index = 0
        
        #self.bpm_testfile = "C:/Users/ARLAN ROIE SANTOS/Desktop/bpm_testfile2.txt"
        #self.myFile = open(self.bpm_testfile, 'r')   #open testfile containing pseaudo sp02 values
        #self.ParentWindow = ParentWindow

    def stop(self):
        self.stopAcquireThr.set()
        
    def run(self):
        """acquire pseudo spo2 readings from text file"""

        while True:
            
            if self.stopAcquireThr.isSet():
                print 'break'
                break

            try:
                value = self.ParentWindow.RawBioSignals[2][self.index]
                BaseTime = time.time()              #get reference time
                count = 0                           #counts the number of edf file produced
                bpm = []

                while (len(bpm) != 150):

                    wx.CallAfter(self.ParentWindow.datapanel.UpdateBPMDisplay, str(value))
                    sample = int(value)
                    bpm.append(sample)
                    # to simulate 10Hz sampling frequency, get samples every 0.1 sec
                    self.index += 1
                    time.sleep(0.1)
                    try:
                        value = self.ParentWindow.RawBioSignals[2][self.index]
                    except IndexError:
                        break
    
                Biosignal_BPM = BioSignal('Pulse Rate', 'IR-Red sensor', 'BPM', 50, 100, 50, 100, 'None', 10, bpm)
#                print '-'*50
#                print 'Returning Pulse Rate'
                return (self.ParentWindow.BioSignals.append(Biosignal_BPM))

            except IndexError:
                wx.CallAfter(self.ParentWindow.stopThreads)

        return        

            
              

                
class BP:
    """methods & arguments are yet to be determined based on the manual(on order)"""
    def __init__(self):
        pass
    def get(self):
        pass
    def status(self):
        pass
    def reset(self):
        pass
