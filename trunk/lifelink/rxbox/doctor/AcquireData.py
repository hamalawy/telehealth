import wx
import threading
#import serial
import socket
import TriageClient as tc
import edfviewer as edf

RQT_MSSG        = 'TELEMED'
PKY_MSSG        = '1234'
WEL_MSSG        = RQT_MSSG + ' ' + PKY_MSSG
VFY_MSSG        = 'READY TO RECEIVE'
REF_MSSG        = 'CONNECTION REFUSED'
FIN_MSSG        = 'FINISHED TRANSMISSION'

BUFSIZ 			= 1024
BUF_SAMPLES     = 30            


#INPUT_FILE      = open('testfile0.edf', 'rb')
#INPUT_FILE      = INPUT_FILE.read()
#print type(INPUT_FILE)
#INPUT_FILE      = 'x'

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
        self.sent = 0
        
    def stop(self):
        self.stopAcquireThr.set()
       
    def run(self):
        input_method = self.setInputSource()
        print 'SetInputSource: transmit_addr = ', self.window.transmit_addr

        if (input_method == 'Serial Port'):
            while True:
                if self.stopAcquireThr.isSet():
                    break
                self.setInput()
                self.processData()
        elif (input_method == 'Saved File'):
            while True:
                if self.stopAcquireThr.isSet():
                    break
                self.stopAcquireThr.wait(0.01)
                self.setInput()
                self.processData()
        elif (input_method == 'USB Port'):
            print 'USB Port not Ready'            
        elif (input_method == 'Web Service'):
            INPUT_FILE = tc.Triage().getBinEDF('39309',1232986728)
            x = edf.EDF_File(INPUT_FILE)
            self.ecg_data = x.parseDataRecords()
            t = self.window.datapanel.ecg_plotter.t
            
            self.window.datapanel.ecg_plotter.line.set_data(range(len(self.ecg_data)), self.ecg_data)
            a = min(self.ecg_data)
            b = max(self.ecg_data)
            c = 0.05*abs(b-a)
            self.window.datapanel.ecg_plotter.axes.set_ylim(a - c, b + c)
            
            self.window.datapanel.updatePlots(None)
            
        try:
            self.file_output.close()
            wx.CallAfter(self.window.raiseMessage, " \nData saved at " + self.user_config['file_output'])
            self.window.user_config['file_output'] = ''
        except:
            pass
        wx.CallAfter(self.window.onClickStop)
        self.sent -= 1
        
    def setInputSource(self):
        if self.user_config['input_method'] == 'Serial Port':
            port = self.user_config['serial_port']
            baud = int(self.user_config['baud_rate'])
#            try:
#                self.input_source = serial.Serial(port, baud, timeout=1)
#                self.input_source.flushInput()
#                return 'Serial Port'
#            except serial.SerialException:
#                wx.CallAfter(self.window.raiseMessage, " \nUnable to open " + port + ".\nPlease check serial port settings.")
            wx.CallAfter(self.window.raiseMessage, " \nUnable to open " + port + ".\nPlease check serial port settings.")
        elif self.user_config['input_method'] == 'Saved File':
            filepath = self.user_config['file_input']
            try:
                self.input_source = open(filepath,'r')
                return 'Saved File'
            except IOError:
                wx.CallAfter(self.window.raiseMessage, " \nUnable to open " + filepath  + ".\nPlease check file name.")
        elif self.user_config['input_method'] == 'USB Port':
            return 'USB Port'
        elif self.user_config['input_method'] == 'Web Service':
            #self.input_source = INPUT_FILE
            pass
#            self.timestamp = ''
#            self.input_start = 0
            return 'Web Service'
        return ''   # all errors encountered will return a null string
        
    def setInput(self):
        try:
            self.input = self.input_source.readline()
        except AttributeError:
#            self.input = tc.RxData().viewRxData(self.input_source)
#            self.input = "b%s" % (self.input,)
#            print self.input
            x = edf.EDF_File(INPUT_FILE)
            self.input = x.getEdfSignal()
#        except IndexError:
#            pass
        self.input = self.input.strip('\r\n')
        
    def processData(self):
        if (self.window.user_config['file_output'] != ''):
            try:
                self.file_output.write(self.input + '\n')
            except AttributeError:
                filepath = self.user_config['file_output']
                self.file_output = open(filepath,'w')
                self.file_output.write(self.input + '\n')

        try:
            a, type, data = self.input.partition(self.input[0])
            print 'classified'
            self.classifyData(type, data)
            
            if (self.window.addr != None):
                try:
                    self.window.data_sock.sendto(self.input, self.window.transmit_addr)
                    #print 'Sent:', self.input 
                except socket.error:
                    pass
        except IndexError:
            self.stopAcquireThr.set()
            if self.user_config['input_method'] == 'Saved File':
                if (self.window.addr != None):
                    self.window.data_sock.sendto(self.finished, self.transmit_addr)
                wx.CallAfter(self.window.raiseMessage, " \nEnd of File reached.")
            
    def classifyData(self, type, data):
        if self._is_float(data):
            pass
        elif not self._is_float(data):
            try:
                data = int(data, 16)
            except:
                return

        if type == 'c':     # ECG
            del self.ecg_data[0]
            self.ecg_data.append(data)
            self.ecg_buf -= 1
            if self.ecg_buf <= 0:
                #self.input_source.flushInput()
                self.ecg_buf = BUF_SAMPLES
                self.window.datapanel.ecg_plotter.line.set_data(self.window.datapanel.ecg_plotter.t, self.ecg_data)

        elif type == 's':   # SpO2
            wx.CallAfter(self.window.datapanel.UpdateSpO2Display, data)
                        
        elif type == 'b':   # heart rate
            wx.CallAfter(self.window.datapanel.UpdateBPMDisplay, data)

    def _is_float(self, data):
        # checks if string is convertible to a floating-point notation
        try:
            float(data)
            return True
        except:
            return False

