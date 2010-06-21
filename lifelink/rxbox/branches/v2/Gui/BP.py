import serial
import threading
import time
import wx
from threading import Thread
import copy

class BP:
    """manages data request and processes reply packets to/from NIBP module"""

    def __init__(self, parent, port="COM5", baud=4800, timeout=None):
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
        #self.pb = pBar(self)
        self.runBP = False
        #self.pb.run()
        self.sys_list=15*[0]
        self.dias_list=15*[0]
        """ Initialize Serial Port Settings """
        self.SerialPort = port
        self.SerialBaudRate = baud
        self.SerialTimeout = timeout
        self.DataPacket = []
        #self.OpenSerial()
        #self.gauge = Gauge(None,-1,"Cuff Pressure")

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
        
        self.parent = parent
        self.device_message = 'Device Ready.'

        # open port 'self.port w/ baudrate=self.baud & timeout=self.timeout:
        try:
            self.nibp = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=0)      
        except serial.SerialException:
            print "Unable to open COM port", 8, "\nPlease check serial port settings."
        
    def reset(self):
        """reset serial port input buffer"""
        self.nibp.flushInput()

    def request(self, command):
        """
        Arranges the request packet for sending to NIBP2010 BP Monitor
        Accepts a list of hex numbers called command"""

        request = [chr(elem) for elem in command]
        bprequest = ''.join(request)
        return bprequest
        
    def send_request(self):
        """Method writes a packet to the serial port"""
        print "*** ONE-SHOT BP ***"
        request=self.request(self.SET_180mmHg_PRESSURE)
        self.nibp.write(request)
        print "***Start BP Measurement***"
        self.nibp.write(self.request(self.START_MEASUREMENT))
        print
        print "***Acquiring Cuff Pressure***"
        
    def get(self):
        """implements pseudo-cycle mode for BP measurement"""
        #self.runBP = True
        #self.run()
        print
        print "***Extracting Status of Operation***"
        self.patient_ready()
        if self.PatientReady:
            self.extract_bp()
        #else:
        #    print "Patient NOT ready."

    def extract_bp(self):
        """Method extracts Blood pressure readings from the current packet received."""
        for item in range(len(self.PatientStatus)):
            if self.PatientStatus[item] == 'P':
                self.bp_systolic = int(self.PatientStatus[item+1:item+4])
                self.bp_diastolic = int(self.PatientStatus[item+7:item+10])
                break
        print "Systolic Pressure: ",self.bp_systolic
        print "Diastolic Pressure: ",self.bp_diastolic
        self.sys_list=15*[self.bp_systolic]
        self.dias_list=15*[self.bp_diastolic]
            
    def checksum(data):
        """
            Computes the checksum of a given string, data.
               data -> string of characters
               [to be later replaced by list from  pseudo data]

            checksum computation:
                1. Sum the hex or dec values of the characters
                   in the data (excluding STX and Checksum values).
                2. The checksum is equal to the sum of the values
                    transmitted modulo 256(in decimal).
        """
        self.checksum = sum(data,0)    # get the sum of list 'data', start index = 0
        self.checksum = (hex(self.checksum % 256)).upper() # do modulo 256 over the sum
        self.checksum = self.checksum[2:] # checksum is a string
            
    def POST(self):
        """ POST()

            This method resets the BP module. After reset, the reply packet
            is read and method test_power is called to check whether the BP
            module is powered on and is transmitting data to the RxBox.
        """
        self.PowerStatus = False
        self.test_power() # Check if module
        #self.nibp.close()
        return self.PowerStatus
	

    def test_power(self):
        """ test_power()

            Checks if the module transmitted a valid packet. If packet is
            invalid, an appropriate message is displayed in the command
            shell of python. If the packet is valid, EPROM version is saved.
        """
        self.Command = '\x0229;;E1\x03' # combine packets into one string
        #self.nibp.flushOutput() # flush output buffer of serial port
        # Command the module to Reset BP's hardware component
        self.nibp.write(self.Command) # print/output command via serial port to SPO2 module
        #self.nibp.flushInput() # flush input buffer of serial port
        self.EPROMVersion = self.get_reply()
        if self.EPROMVersion == None:
            print "ERROR: Module does not reply."
            print "Please check power or serial port settings."
            self.PowerStatus = False
        else:
            self.EPROMVersion = self.EPROMVersion[2:len(self.EPROMVersion)-1]
            print "BP Module Powered On."
            print "EPROM Version:",self.EPROMVersion
            self.PowerStatus = True        

    def verify_checksum(self,packet):
        """ verify_checksum(packet) -> parsed packet data

            Method determines the validity of the packet by checking the
            checksum of the packet against the data contained in the
            packet. If data is valid, parsed data is returned. If not,
            the method returns None type.
        """
        reply = []; print packet
        if packet == None:
            print "Transmit Error: Incomplete Packet."
            return None
        elif packet[0] == '\x02' and packet[len(packet)-1]=='\x03':
            reply = [ord(item) for item in data]
            reply = reply[1:len(reply)-1]
            self.ComputeChecksum(reply[:-2])
            if self.checksum == reply[-2:]:
                return reply
            else:
                print 'Checksum Error.'
                return None

    def get_reply(self):
        """ get_reply() -> string of complete packet

            Method acquires data from the module and gets a complete
            packet using the start and end flags. Once a complete
            packet is acquired, it is returned. If the serial port
            times out, a Nony type is returned to distuingish the error.
        """
        reply = ''; flag_counter = 0;
        while (flag_counter < 2):
            byte = self.nibp.read(1)
            if byte == '':
                break
            elif byte == '\x02':
                reply = reply + byte
                flag_counter = 1
            elif byte == '\x03':
                reply = reply + byte
                flag_counter = 2
            else:
                reply = reply + byte
        if byte == '':
            return None
        else:
            #print reply
            return reply

    def string_to_packet(self, string):
        """ string_to_packet(string) -> equivalent list of binary data of string

            Method converts the replies transmitted by the module to
            a list of bytes. The data read from the serial port is
            string so it needs to be converted to a list to be able
            to process the data contained by the packets.
        """
        if string == None:
            return None
        else:
            packet = [ord(item) for item in string]
            return packet

    def device_ready(self):
        """ device_ready()

            Method determines if the device is ready for telemetry. A
            command for leakage test to assess the status of the sensor
            is transmitted first. After the leakage test, the status
            of the device will be checked.
        """
        #self.leakage_test()
        #self.runBP = True
        #self.pb.run()
        self.DeviceStatus = False
        self.test_device()
        return self.DeviceStatus

    def leakage_test(self):
        """ leakage_test()

            Method initiates a leakage test to determine the status of
            the BP cuff. Once initiated, the leakage test will inflate
            and the deflate the cuff for status checking.
        """
        #self.reset()
        self.Command = '\x0217;;DE\x03' # combine packets into one string
        # Command the module to Reset it's hardware component
        self.nibp.write(self.Command) # print/output command via serial port to SPO2 module
        
    def test_device(self):
        """ test_device()

            Method checks the status of the device by inquiring to
            the module. The status from the module will be evaluated
            by check_device_status method. Method also checks if serial
            port times out for error checking.
        """
        self.Command = '\x0218;;DF\x03' # combine packets into one string
        #self.nibp.flushOutput() # flush output buffer of serial port
        # Command the module to Reset it's hardware component
        self.nibp.write(self.Command) # print/output command via serial port to SPO2 module
        #self.nibp.flushInput() # flush input buffer of serial port
        self.DeviceStatus = self.get_reply()
        if self.DeviceStatus == None:
            print "ERROR: Module does not reply."
            print "Please check power or serial port settings."
            self.DeviceStatus = False
        else:
            self.check_device_status()

    def check_device_status(self):
        """ check_device_status()

            Method evaluates the status transmitted by the module.
            It only checks for cases for device ready method.
        """
        for item in range(len(self.DeviceStatus)):
            if self.DeviceStatus[item] == 'M':
                status = self.DeviceStatus[item+1:item+3]
        status = int(status)
        if status == 00:
            self.device_message = 'Device ready.'
            self.DeviceStatus = True
        elif status == 8:
            self.device_message = 'Pneumatics Faulty.'
            self.DeviceStatus = False
            print "Please call RxBox hotline."
        elif status == 14:
            self.device_message = 'Leakage during leakage test.'
            self.DeviceStatus = False
            print "Please check or replace cuff."
        elif status == 15:
            self.device_message = 'System error.'
            self.DeviceStatus = False
            print "Please call RxBox hotline."
        else:
            self.DeviceStatus = True

    def patient_ready(self):
        """ patient_ready()

            Method determines if the patient is ready for telemetry. A
            command for leakage test to assess the status of the sensor
            is transmitted first. After the leakage test, the status
            of the sensor and the patient will be checked.
        """
        self.test_sensor()

    def test_sensor(self):
        """ test_sensor()

            Method checks the status of the sensor by inquiring to
            the module. The status from the module will be evaluated
            by check_patientd_status method. Method also checks if serial
            port times out for error checking.
        """
        self.Command = '\x0218;;DF\x03' # combine packets into one string
        self.nibp.flushOutput() # flush output buffer of serial port
        # Command the module to Reset it's hardware component
        self.nibp.write(self.Command) # print/output command via serial port to SPO2 module
        self.nibp.flushInput() # flush input buffer of serial port
        self.PatientStatus = self.get_reply()
        self.PatientReady = False
        if self.PatientStatus == None:
            print "ERROR: Module does not reply."
            print "Please check power or serial port settings."
            self.PatientReady = False
        else:
            self.check_patient_status()
        return self.PatientReady

    def check_patient_status(self):
        """ check_patient_status()

            Method evaluates the status transmitted by the module.
            It only checks for cases for patient_ready method.
        """
        for item in range(len(self.PatientStatus)):
            if self.PatientStatus[item] == 'M':
                status = self.PatientStatus[item+1:item+3]
                break
        status = int(status)
        if status == 00:
            print "Patient ready."
            self.PatientReady = True
        elif status == 06:
            print "Patient Not Ready: Time for pumping exceeded."
            print "Please check if the cuff is connected or fitted properly."
            self.PatientReady = False
        elif status == 11:
            print "Too many motion artefact."
            self.PatientReady = False
        elif status == 15:
            print "Patient Not Ready: System error."
            print "Please call RxBox hotline."
            self.PatientReady = False

    def run(self):
        print "runbp"
        while self.runBP:
            #self.reset()
            print "get pressure"
            press = self.get_reply()
            self.nibp.read(1)
            press = press[1:4]
            while int(press) != 999:
                print "Current Pressure: ",press
                self.parent.bp_pressure_indicator.SetValue(int(press))
                self.parent.bp_infolabel.SetLabel(press+' mmHg')
                press = self.get_reply()
                self.nibp.read(1)
                press = press[1:4]
            self.parent.bp_pressure_indicator.SetValue(0)
            self.parent.bp_infolabel.SetLabel('BP Acquired')
            self.runBP = False
        print "exit pressure"
            
                
