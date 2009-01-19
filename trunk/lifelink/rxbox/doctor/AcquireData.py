import wx
import threading
#import serial
import socket

BUF_SAMPLES     = 30

RQT_MSSG        = 'TELEMED'
PKY_MSSG        = '1234'
WEL_MSSG        = RQT_MSSG + ' ' + PKY_MSSG

VFY_MSSG        = 'READY TO RECEIVE'
REF_MSSG        = 'CONNECTION REFUSED'
FIN_MSSG        = 'FINISHED TRANSMISSION'

DATA_TIMEOUT 	= 10
BUFSIZ 		= 1024

class AcquireDataThr(threading.Thread):
    def __init__(self, threadNum, window): 
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.stopAcquireThr = threading.Event()
        self.stopAcquireThr.clear()
        
        self.window = window
        self.user_config = self.window.user_config
        self.ecg_data = self.window.datapanel.ecg_plotter.data
        self.ecg_buf = BUF_SAMPLES
        self.welcome = WEL_MSSG
        self.verify = VFY_MSSG
        self.refuse = REF_MSSG
        self.finished = FIN_MSSG
        
    def stop(self):
        self.stopAcquireThr.set()
       
    def run(self):
        self.input_source = self.window.data_sock
        while True:
            if self.stopAcquireThr.isSet():
                wx.CallAfter(self.window.onClickStop)
                break
            try:
                self.input, addr = self.input_source.recvfrom(BUFSIZ)
                if (addr[0] != self.window.user_config['ip_host']):
                    continue
                if (self.input == self.finished):
                    self.stopAcquireThr.set()
                    wx.CallAfter(self.window.raiseMessage, " \nConnection closed. Data transfer finished.")
                    continue
                self.processData()
            except:
                pass
           
        try:
            self.file_output.close()
            wx.CallAfter(self.window.raiseMessage, " \nData saved at " + self.user_config['file_output'])
            self.window.user_config['file_output'] = ''
        except:
            pass
        self.window.onClickStop()
              
    def processData(self):
        try:
            a, type, data = self.input.partition(self.input[0])
            self.classifyData(type, data)
            
        except:
            print 'Error in processing data.'
            pass
            
    def classifyData(self, type, data):
        # sample reading format: '<type><data>'
        #
        # <type> is a buffer character to determine the type of reading
        #   (a) 'c' represents an ECG reading
        #          'e' cannot be used as the notation can be confused for an exponent
        #   (b) 's' represents an SpO2 reading
        #   (c) 'b' represents a BPM reading
        #
        # <data> contains the reading, convertible to a floating-point format
        #   checking if separate lines 'merge' with each other
        #
        # the conditional statement doesn't check if the data is within the expected range
        
        if self._is_float(data):
            if type == 'c':
                del self.ecg_data[0]
                self.ecg_data.append(data)
                self.ecg_buf -= 1
                if self.ecg_buf <= 0:
                    self.ecg_buf = BUF_SAMPLES
                    self.window.datapanel.ecg_plotter.line.set_data(self.window.datapanel.ecg_plotter.t, self.ecg_data)
            elif type == 's':
                wx.CallAfter(self.window.datapanel.UpdateSpO2Display, data)                       
            elif type == 'b':
                wx.CallAfter(self.window.datapanel.UpdateBPMDisplay, data)
        elif type == 'a':
            self.window.rcvReferralTopic = data
        elif type == 'e':
            self.window.rcvInterlocutorFirstName = data
        elif type == 'f':
            self.window.rcvInterlocutorLastName = data
        elif type == 'h':
            self.window.rcvHospitalName = data
        elif type == 'j':
            self.window.rcvHospitalAddress = data
        elif type == 'k':
            self.window.rcvHospitalCity = data
        elif type == 'l':
            self.window.rcvPatientLastName = data
        elif type == 'm':
            self.window.rcvPatientFirstName = data
        elif type == 'n':
            self.window.rcvPatientMI = data
        elif type == 't':
            self.window.rcvPatientAddress = data
        else: return

        if type == 'd':
            self.window.rcvReferralReason = data
        elif type == 'g':
            self.window.rcvInterlocutorPhoneNumber = data
        elif type == 'i':
            self.window.rcvHospitalNumber = data
        elif type == 'o':
            self.window.rcvPatientAge = data
        elif type == 'p':
            self.window.rcvPatientAgeDMY = data
        elif type == 'q':
            self.window.rcvPatientAgeValidity = data
        elif type == 'r':
            self.window.rcvPatientGender = data
        elif type == 'u':
            self.window.rcvPatientNumber = data
            wx.CallAfter(self.window.UpdateInfo)

    def _is_float(self, data):
        # checks if string is convertible to a floating-point notation
        try:
            float(data)
            return True
        except:
            return False
