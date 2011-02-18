import serial
import time
import wx

class BPDAQ:
    """manages data request and processes reply packets to/from NIBP module"""

    def __init__(self, parent, port="COM5", baud=4800, timeout=3, coeff = (1,0,0,0,1,0)):
        """initializes port settings and request data sequence according to specified setting for EMI12"""
        self.parent = parent
        """ Initialize Serial Port Settings """
        self.port = port                
        self.baudrate = baud            
        self.timeout = timeout
        self.coeff = coeff
        
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
        self.SET_200mmHg_PRESSURE = [0x02, 0x33, 0x33, 0x3B, 0x3B, 0x44, 0x43, 0x03]
        self.SET_220mmHg_PRESSURE = [0x02, 0x33, 0x34, 0x3B, 0x3B, 0x44, 0x44, 0x03]
        self.SET_240mmHg_PRESSURE = [0x02, 0x33, 0x35, 0x3B, 0x3B, 0x44, 0x45, 0x03]

        self.Command_Pressure={'140':self.SET_140mmHg_PRESSURE,'160':self.SET_160mmHg_PRESSURE,'180':self.SET_180mmHg_PRESSURE,'200':self.SET_200mmHg_PRESSURE,\
                                '220':self.SET_220mmHg_PRESSURE,'240':self.SET_240mmHg_PRESSURE}
        self.SELECT_ADULT_MODE = [0x02, 0x32, 0x34, 0x3B, 0x3B, 0x44, 0x43, 0x03]
        
        self.device_message = 'Device Ready.'
        self.bp_systolic = 0
        self.bp_diastolic = 0
        self.DataPacket = []
        self.sys_list=15*[0]
        self.dias_list=15*[0]
        self.list_reply=[]
        self.bpstatus= 'Retry Again'
        self.rawsys = 0
        self.rawdias=0
        self.retry=0
        
    
    def stop(self):
        command = '\x02X\x03' # combine packets into one string
        self.nibp.write(command)
        #print 'deflating'

    def request(self, command):
        """
        Arranges the request packet for sending to NIBP2010 BP Monitor
        Accepts a list of hex numbers called command"""

        request = [chr(elem) for elem in command]
        bprequest = ''.join(request)
        return bprequest
        
    def send_request(self,value):
        
        
   
        print "*** ONE-SHOT BP ***"
        self.nibp.flushInput()
        self.nibp.flushOutput()
        request=self.request(self.Command_Pressure[value])
        self.nibp.write(request)
        print "***Start BP Measurement***"
        self.nibp.write(self.request(self.START_MEASUREMENT))
        print "***Acquiring Cuff Pressure***"

        
    def get(self):
        """implements pseudo-cycle mode for BP measurement"""

        print "***Extracting Status of Operation***"
        self.patient_ready()
        if self.PatientReady:
            self.extract_bp()


    def extract_bp(self):
        for item in range(len(self.PatientStatus)):
            if self.PatientStatus[item] == 'P':
                if self.PatientStatus[item+1:item+4] == '---':
                    self.bp_systolic = 0
                    self.bp_diastolic = 0
                else:
                    self.rawsys = int(self.PatientStatus[item+1:item+4])
                    self.rawdias = int(self.PatientStatus[item+7:item+10])
                    coeff = self.coeff
                    self.bp_systolic = int(round(coeff[0]*self.rawsys+coeff[1]*self.rawdias+coeff[2]))
                    self.bp_diastolic = int(round(coeff[3]*self.rawsys+coeff[4]*self.rawdias+coeff[5]))
                    print "Raw Systolic Pressure:",self.rawsys
                    print "Raw Diastolic Pressure:",self.rawdias
                break
        print "Systolic Pressure: ",self.bp_systolic
        print "Diastolic Pressure: ",self.bp_diastolic
        self.sys_list=15*[self.bp_systolic]
        self.dias_list=15*[self.bp_diastolic]
            
	
    def init_status_check(self):
        
        status=self.OpenSerial()
        if status == False:
            return False
        self.stop()
        command='\x0218;;DF\x03'
        self.nibp.write(command)

        status = self.get_reply()
        if status == None:
            print "ERROR: Module does not reply."
            print "Please check power or serial port settings."
            self.CloseSerial()
            return False

        if self.retry == 5:
            print 'Device not ready, Cannot Proceed'
            self.CloseSerial()
            return False

        if (status[1:3] !='S1'):
            self.list_reply=[]
            self.retry+=1
            self.CloseSerial()
            print 'BP HAVING HARD TIME TO PROCEED'
            self.init_status_check()
        
        try:
            status = int(status[12:14])
        except ValueError:
            self.CloseSerial()
            self.retry = 4
            self.init_status_check()

        if status == 00:
            # 'Device is ready'
            self.CloseSerial()
            return True
        elif status == 15:
            print 'System error.'
            self.stop()
            self.CloseSerial()
            print "Please call RxBox hotline."
            return False
        else:
            return True
    
    def port_check(self):
        
        status=self.OpenSerial()
        if status == False:
            return False
        self.stop()
        command='\x0218;;DF\x03'
        self.nibp.write(command)

        status= self.get_reply()
        print status
        self.CloseSerial()
        if status == None:
            print "ERROR: Module does not reply."
            print "Please check power or serial port settings."
            return False
        count=0
        stat=True
        passed=0
        if(self.list_reply[0]=='\x02' and self.list_reply[-1]=='\x03'):
            passed=1
            print self.list_reply
            print 'hello'
            while(not(self.list_reply[0]=='\x02' and self.list_reply[1:3]==['S','1'] )):
                print self.list_reply
                print 'hi'
                self.ready_module()
                
                if count > 5:
                    stat=False
                    break
                count+=1
                print 'Initializing BP, Please wait'+str(count)
                print count
        print stat
        print passed
        if passed == 0:
            return False
        else:
            if(stat==False):
                return False
            else:
                return True

    def ready_module(self):
        self.OpenSerial()
        command='\x0218;;DF\x03'
        self.nibp.write(command)
        print 'popop'
        status= self.get_reply()
        self.CloseSerial()

    def init_firmware_version(self):
        """ 
            Checks if the module transmitted a valid packet. If packet is
            invalid, an appropriate message is displayed in the command
            shell of python. If the packet is valid, EPROM version is saved.
        """   
        status=self.OpenSerial()
        if status == False:
            return False

        command = '\x0229;;E1\x03'
        self.nibp.write(command)

        EPROMVersion = self.get_reply()
        if EPROMVersion == None:
            print "ERROR: Module does not reply."
            print "Please check power or serial port settings."
            self.CloseSerial()
            return False
        else:
            print "BP Firmware Acquired."
            print "EPROM Version:",EPROMVersion[2:len(EPROMVersion)-1]
            self.CloseSerial()
            return True  


    def OpenSerial(self):
        """Method will try to open a serial port for communication if possible.
        If not, error is printed in the python shell
        """
        try:
            self.nibp = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout, xonxoff=0)
            return True
        except serial.SerialException:
            print "Please check serial port settings or the device."
            return False

    def CloseSerial(self):
        """Method closes an open serial port instance"""
        self.nibp.close()  

    def get_reply(self):
        """ get_reply() -> string of complete packet

            Method acquires data from the module and gets a complete
            packet using the start and end flags. Once a complete
            packet is acquired, it is returned. If the serial port
            times out, a Nony type is returned to distuingish the error.
        """
        self.nibp.flushInput()
        self.nibp.flushOutput()
        reply = '' 
        flag_counter = 0
        read=self.nibp.read
        bit_count=0
        self.list_reply=[]
        while (flag_counter < 2):
            byte = read(1)
            if byte == '':
                break
            elif byte == '\x02':
                self.list_reply.append(byte)
                reply = reply + byte
                flag_counter = 1
                bit_count=0
                continue
            elif byte == '\x03':
                if flag_counter==1:
                    self.list_reply.append(byte)
                    reply = reply + byte
                    flag_counter = 2
                else:
                    continue
            if flag_counter == 1:
                reply = reply + byte
                self.list_reply.append(byte)
            if bit_count>42:
                return None
            bit_count+=1
        if byte == '':
            return None
        else:
            print self.list_reply
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
        self.Command = '\x0217;;DE\x03' # combine packets into one string
        self.nibp.write(self.Command) # Command the module to Reset it's hardware component
        
 

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

        self.nibp.flushOutput() # flush output buffer of serial port
        self.nibp.write('\x0218;;DF\x03') # print/output command via serial port to SPO2 module
        self.nibp.flushInput() # flush input buffer of serial port
        self.PatientStatus = self.get_reply()
        print list(self.PatientStatus), "this is the status of the patient"
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
            if self.PatientStatus[item] == 'S':
                acquire_status = self.PatientStatus[item+1:item+2]
#                print acquire_status
                break
        if int(acquire_status)==1:
            print "Patient ready."
            self.bpstatus= "BP Acquired"
            self.PatientReady = True
        elif int(acquire_status)==2:
            for item in range(len(self.PatientStatus)):
                if self.PatientStatus[item] == 'M':
                    status = self.PatientStatus[item+1:item+3]
#                    print status
                    break
            status = int(status)
            
            if status == 06:
                self.bpstatus= "Check Cuff Connection,Loose connection"
                self.PatientReady = False
                self.stop()
            elif status == 07:
                self.bpstatus= "Check Cuff Connection,Leakage occured"
                self.PatientReady = False
                self.stop()
            elif status == 9:
                self.bpstatus= "Measuring Time Exceeded:Less Oscillations Detected"
                self.PatientReady = False
                self.stop()
            elif status == 11:
                self.bpstatus= "Patient Needs To Relax, Too much movement"
                self.PatientReady = False
                self.stop()
            elif status == 12:
                self.bpstatus= "Maximum Pressure Exceeded"
                self.PatientReady = False
                self.stop()
            elif status == 15:
                self.bpstatus= "Module Error: Call RxBox Hotline"
                self.PatientReady = False
                self.stop()

            
                
