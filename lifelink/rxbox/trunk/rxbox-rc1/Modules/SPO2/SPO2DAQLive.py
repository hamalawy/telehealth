import serial
import time
import copy
from threading import Thread

class SPO2DAQ:
    """manages data request and processes reply packets to/from the SPO2 module"""
    def __init__(self, parent, port="/dev/ttyUSB0",baud=9600,timeout=5,debug=True,logger=''):
        """ Initialize port settings and request according
            to the specified setting for ChipOx"""
        self._logger=logger
        self.debug=True
        # Initialize Serial Port Settings
        self.SerialPort = port
        self.SerialBaudRate = baud
        self.SerialTimeout = timeout
        self.DataPacket = []
        #Thread.__init__(self)
        #self.OpenSerial()
        self.device_message = self.dm = "Device Ready."
        self.patient_message = "Patient Ready."
        self.parent = parent
        self.spo2_list=15*[0]
        self.bpm_list=15*[0]
        self.current_spo2=0
        self.current_bpm=0
        # Request Command: transmit SPO2 and BPM every 100 ms
        self.command = [0x7f, 0xd1, 0x01, 0x01, 0x01, 0x02,\
                        0x01, 0x03, 0x01]

        self.spo2 = []
        self.pulse_rate = []
        self.signal_quality = []
        self.current_spo2=0
        self.current_bpm =0
        self.send_request()

    def Print(self, string=''):
        if self.debug and self._logger=='':
            print string
        elif self.debug:
            self._logger.debug(string)

    def send_request(self):
        """ Continuously acquire SPO2 and BPM readings from the module """
        self.OpenSerial()
        request = []
        self.checksum(self.command)
        for item in self.command:
            request.append(item)
        request.append(self.CShi)
        request.append(self.CSlo)
        request = self.byte_stuff(request)
        request.insert(0,0xa8)                                 # insert start flag at the begining of request sequence  
        request.append(0xa8)                                   # append end flag at the end of request
        request = [chr(item) for item in request]
        request = ''.join(request)
        self.reset()
        self.SerPort.write(request)
        self.CloseSerial()

    def reset(self):
        """reset serial port input buffer"""
        self.SerPort.flushInput()
        self.SerPort.flushOutput()

    def byte_destuff(self,data):
        """Extracts SPO2 and BPM reading from packet 'data'. Data are stored
        in an instance attribute
		"""
        destuffed = []
        for i in range(len(data)):
            if data[i] == 0xa9 and data[i+1] == 0x88:
                destuffed.append(0xa8)
                i = i+1
            elif data[i] == 0xa9 and data[i+1] == 0x89:
                destuffed.append(0xa9)
                i = i+1
            else:
                destuffed.append(data[i])
        return destuffed

    def byte_stuff(self, data):
        """
        filter the data stream for reserved flags
        return a list (of char strings) for byte-stuffed data sequence"""

        encoded_sequence = []  
        for item in data:
            if item == 0xa8:                                  
                encoded_sequence.append(0xa9)  # Replace Flag 0xa8
                encoded_sequence.append(0x88)  # with 0xa9, 0x88
            elif item == 0xa9:
                encoded_sequence.append(0xa9)  # Replace Flag 0xa9
                encoded_sequence.append(0x89)  # with 0xa9, 0x89
            else:
                encoded_sequence.append(item)
        return encoded_sequence

    def get(self):
        #while self.parent.start:
        self.OpenSerial()
        if self.status is None:
            self.reset()
            raw_data = self.get_reply()
            data_packet = raw_data
            if data_packet == None:
                self.Print('None Type Returned')
                self.spo2_temp=copy.copy(self.spo2_list)
                self.bpm_temp=copy.copy(self.bpm_list)
                self.spo2_temp.append(0)
                self.bpm_temp.append(0)
                self.spo2_temp.pop(0)
                self.bpm_temp.pop(0)
                self.spo2_list=copy.copy(self.spo2_temp)
                self.bpm_list=copy.copy(self.bpm_temp)
                self.current_spo2 = 0
                self.current_bpm = 0
                self.CloseSerial()
                return
            data_packet = self.verify_checksum(data_packet)
            #self.Print(str(data_packet)+' part1')
            if data_packet == None:
                self.Print('SPO2: Checksum Failed, Dropping Data')
                self.spo2_temp=copy.copy(self.spo2_list)
                self.bpm_temp=copy.copy(self.bpm_list)
                self.spo2_temp.append(self.spo2_temp[-1])
                self.bpm_temp.append(self.bpm_temp[-1])
                self.spo2_temp.pop(0)
                self.bpm_temp.pop(0)
                self.spo2_list=copy.copy(self.spo2_temp)
                self.bpm_list=copy.copy(self.bpm_temp)
                self.CloseSerial()
                return
            data_packet = self.byte_destuff(data_packet)
            #self.Print(str(list(data_packet))+' part2')
            self.Print(str(list(data_packet)))
            self.parse_packet(data_packet)
            self.spo2_temp=copy.copy(self.spo2_list)
            self.bpm_temp=copy.copy(self.bpm_list)
            self.spo2_temp.append(self.current_spo2)
            self.bpm_temp.append(self.current_bpm)
            self.spo2_temp.pop(0)
            self.bpm_temp.pop(0)
            self.spo2_list=copy.copy(self.spo2_temp)
            self.bpm_list=copy.copy(self.bpm_temp)
            #print self.spo2_list
            #print self.bpm_list
            self.CloseSerial()
        else:
            self.Print( str(self.status) )

    def parse_packet(self,packet):
        """Checks if packet is not empty and the signal quality is < 100.
        Corresponding packet numbers for spo2 and bpm are retrieved and 
        appended to self.current_spo2 and self.current_bpm respectively
        """
        if packet == []:
            pass
        elif packet[0] == 127:
            sig_quality = packet[5]
            if sig_quality <= 100:
                self.current_spo2 = packet[2]
                self.current_bpm = (packet[3]<<8)+packet[4]
                self.spo2.append(packet[2])
                self.pulse_rate.append((packet[3]<<8)+packet[4])
                self.signal_quality.append(sig_quality)
                
            
    def OpenSerial(self):
        """Method will try to open a serial port for communication if possible.
        If not, error is printed in the python shell
        """
        try:
            self.SerPort = serial.Serial(port=self.SerialPort,
                                baudrate=self.SerialBaudRate,
                                timeout=self.SerialTimeout)
            self.status = None
        except serial.SerialException:
            self.status =  "ERROR: Unable to open Com Port - "+ str(self.SerialPort)
            self.Print("Please check serial port settings or the device.")

    def CloseSerial(self):
        """Method closes an open serial port instance"""
        self.SerPort.close()

    def get_reply(self):
        """ get_reply() -> returns one complete packet

            Method reads data from the serial port and requires a complete
            packet to return to the call. If serial port times out, None type
            is returned to indicate the time out.
        """
        reply = ''; flag_counter = 0; start = time.time()
        count = 2; start_found = False
        bit_count=0
        a=[]
        while (flag_counter < 2):
            byte = self.SerPort.read(1)
            if byte == '':
                break
            if flag_counter == 1 and byte != chr(0xa8):
                reply = reply + byte
            if byte == chr(0xa8):
                bit_counter=0
                if flag_counter == 0:
                    next = self.SerPort.read(1)
                    if next == chr(0xa8) and flag_counter == 0:
                        reply = reply + next
                    else:
                        reply = reply + byte + next
                else:
                    reply = reply+byte
                flag_counter = flag_counter + 1
            if bit_count>15:
                return None
            bit_count+=1
        if byte == '':
            return None
        else:
            #print self.string_to_packet(reply)
            return reply
           


    def verify_checksum(self,packet):
        """ verify_checksum(packet) -> data contained in the packet

            Method checks if the checksum contained in the packet
            corresponds to the data that the packet contains. If not,
            None type is returned. If packet is valid, the data will
            be returned.
        """
        if packet[0] == chr(0xa8) and packet[-1]==chr(0xa8):
            data = self.string_to_packet(packet[1:-1])
            reply = data[:-2]
            dataCShi = data[-2]
            dataCSlo = data[-1]
            self.checksum(reply)
            if len(reply) != 6:
                return None
            if dataCShi == self.CShi and dataCSlo == self.CSlo:


                return reply
            else:
               # print 'Checksum Error.'
                return None
        else:
            self.Print("Transmit Error: Incomplete Packet.")
            return None

    def checksum(self,packet):
        """ checksum(packet) -> [CShi, CSlo]

            Calculates the CRC for a list of data from the ChipOx module.
            A packet for the SPO2 module generally consists of:
            [ <Start Flag><data><checksum><End Flag>]
            
            Input: data in packet -> a list of data in hex
            Outputs: [CShi, CSlo] -> checksum bytes in hex

            Method:
                CS = checksum = sum of Higher byte shifted 8 bits to the
                right AND with 0xFF00 + Lower byte AND with 0x00FF  +
                current hex data value
                CSlo = lower byte = lower byte of checksum
                CShi = higher byte of checksum + (CSlo XOR current hex data) """
        # CS, CShi, CSlo are all initially equal to zero
        self.CS = self.CShi = self.CSlo = 00
        for data in packet: # traverse the list to compute for CS values
            self.CS = (((self.CShi<<8)&(0xFF00))+self.CSlo) + data
            self.CSlo = self.CS & 0xFF
            self.CShi = (((self.CS>>8)&0xFF) + (self.CSlo ^ data)) & 0xFF
        #return CShi, CSlo

    def packet_to_string(self, packet):
        """ packet_to_string(packet) -> string equivalent of list packet

            Method is used to convert a packet to be transmitted to
            the module to a string. Writing to the serial port requires
            a string so the list of commands should be converted first
            before it is transmitted.
        """
        if packet == None:
            return None
        else:
            string = [chr(item) for item in packet]
            string = ''.join(string)
            return string

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
            
    def port_check(self):
        status=self.OpenSerial()
        if self.status is None:
            status = self.get_reply()
            if status==None:
                self.CloseSerial()
                return False
            elif status[0]=='\xa8':
                self.CloseSerial()
                return True
            else:
                self.CloseSerial()
                return False
        else:
            return False

    def POST(self):
        """ self.POST() -> 'True' if module is powered on, 'False' otherwise

            This method resets the SPO2 module. After reset, the reply packet is read and method
            test_power is called to check whether the SPO2 module is powered on and is transmitting
            data to the RxBox. If module is powered on, Serial number and Firmware version
            are extracted from the reply and method returns 'True' logic value. Otherwise,
            'False' is returned.
        """
        self.OpenSerial()
        if self.status is None:
            self.Power = False
            self.checksum([0x7f, 0xb2]) # Compute for checksum
            self.DataPacket = [0xa8, 0x7f, 0xb2, self.CShi, self.CSlo, 0xa8] # Organize data packet
            self.DataPacket = [chr(item) for item in self.DataPacket] # convert hex values to char
            self.Command = ''.join(self.DataPacket) # combine packets into one string
            # Command the module to Reset it's hardware component
            if self.test_power():
                self.check_power()
            self.CloseSerial()
        return self.status

    def test_power(self):
        """ self.test_power()

            Method receives reply to from the module and determines whether a the
            serial port timed out or there is a packet received.
        """
        self.SerPort.flushOutput() # flush output buffer of serial port
        self.SerPort.write(self.Command) # print/output command via serial port to SPO2 module
        self.SerPort.flushInput() # flush input buffer of serial port
        self.FirmwareVersion = self.get_reply()
        self.SerialNumber = self.get_reply()
        if self.FirmwareVersion == None:
            self.status = "POWER TEST FAIL: SPO2 not powered on."
            print "Error: Serial Number not found."
            print "Error: Firmware Version not found."
            return False
        else:
            self.FirmwareVersion = self.verify_checksum(self.FirmwareVersion)
            self.SerialNumber = self.verify_checksum(self.SerialNumber)
            self.status = "SPO2 Powered ON."
            return True

    def check_power(self):
        """ self.check_power()

            Method determines if the packet received from the module are valid
            or if the packet is complete.
        """
        if self.FirmwareVersion[0] == 127  and self.FirmwareVersion[1] == 0x21:
            self.FirmwareVersion = self.packet_to_string(self.FirmwareVersion[2:])
            self.Power = True
            print "Firmware Version: ", self.FirmwareVersion
        else:
            #self.FirmwareVersion = None
            print "Firmware Version not found in packet."
        if self.SerialNumber[0] == 127 and self.SerialNumber[1] == 0x23:
            self.SerialNumber = self.packet_to_string(self.SerialNumber[2:])
            self.Power = True
            print "Serial Number: ", self.SerialNumber
        else:
            #self.SerialNumber = None
            print "Serial Number not found in packet."

    def device_ready(self):
        """ device_ready()

            Method determines if the the sensor is properly attached to
            the module. A status check is initiated by the module
            to determine the state of the device and the sensor.
        """
        self.DeviceReady = False
        self.OpenSerial()
        if self.status is None:
            self.checksum([0x7f, 0x88, 0x00]) # Compute for checksum
            self.DataPacket = [0xa8, 0x7f, 0x88, 0x00, self.CShi, self.CSlo, 0xa8] # Organize data packet
            self.DataPacket = [chr(item) for item in self.DataPacket] # convert hex values to char
            self.Command = ''.join(self.DataPacket) # combine packets into one string
            self.DeviceReady = False
            self.test_device_ready()
            self.device_message = 'Device READY.'
            self.CloseSerial()
        return self.DeviceReady

    def test_device_ready(self):
        """ test_device_ready()
            Method gets reply from the module and determines if the
            the reply is valid or if the serial port timed out.
        """
        self.SerPort.flushOutput() # flush output buffer of serial port
        self.SerPort.flushInput() # flush input buffer of serial port
        self.SerPort.write(self.Command) # print/output command via serial port to SPO2 module
        self.DeviceStatus = self.get_reply()
        if self.DeviceStatus == None or self.DeviceStatus == []:
            print "POWER TEST FAIL: SPO2 not powered on."
            print "Please check power or serial settings of module."
        else:
            self.DeviceStatus = self.verify_checksum(self.DeviceStatus)
            self.check_device_status()

    def check_device_status(self):
        """ check_device_status()

            Method determines the status of the device based on the
            status transmitted by the module. Method will only check
            bits that are related to device ready cases and NOT for
            the patient ready case.
        """
        self.DeviceReady = False
        found = False
        self.DeviceReady = True
        self.device_message = "Device READY."
        if self.DeviceStatus[0:2] == [0x7f, 0x08]:
            status = (self.DeviceStatus[2] << 8) + self.DeviceStatus[3]
            if (status & 0x01) == 0x01:
                self.DeviceReady = False
                found = True
                self.device_message = "Sensor is OFF!"
                print "Please connect the finger sensor to the module."
            if ((status>>10) & 0x01) == 0x01:
                self.DeviceReady = False
                found = True
                self.device_message = "Sensor is DEFECTIVE!"
                print "Please replace the finger sensor."
            if ((status>>11) & 0x01) == 0x01:
                self.DeviceReady = False
                found = True
                self.device_message = "Power Supply out of range!"
            if ((status>>12) & 0x01) == 0x01:
                self.DeviceReady = False
                found = True
                self.device_message = "Module overheated!"
            if ((status>>13) & 0x01) == 0x01:
                self.DeviceReady = False
                found = True
                self.device_message = "WRONG Sensor!"
            if ((status>>14) & 0x01) == 0x01:
                self.DeviceReady = False
                found = True
                print "Device Not Ready: Measurement Error!"
            if not found:
                self.DeviceReady = True
                self.device_message = "Device READY."

    def patient_ready(self):
        """ patient_ready()

            Method determines if the the sensor is properly attached to
            the patient. A status check is initiated by the module
            to determine the state of the patient and the sensor.
        """
        self.PatientReady = False
        self.OpenSerial()
        if self.status is None:
            self.checksum([0x7f, 0x88, 0x00]) # Compute for checksum
            self.DataPacket = [0xa8, 0x7f, 0x88, 0x00, self.CShi, self.CSlo, 0xa8] # Organize data packet
            self.DataPacket = [chr(item) for item in self.DataPacket] # convert hex values to char
            self.Command = ''.join(self.DataPacket) # combine packets into one string
            self.PatientReady = False
            self.device_message = ''
            if self.test_patient_ready():
                #print "check_patient_status"
                self.check_patient_status()
            self.CloseSerial()
        return self.PatientReady

    def test_patient_ready(self):
        """ test_patient_ready()

            Method gets reply from the module and determines if the
            the reply is valid or if the serial port timed out.
        """
        self.SerPort.flushOutput() # flush output buffer of serial port
        self.SerPort.flushInput() # flush input buffer of serial port
        self.SerPort.write(self.Command) # print/output command via serial port to SPO2 module
        self.PatientStatus = self.get_reply()
        if self.PatientStatus == None:
            print "POWER TEST FAIL: SPO2 not powered on."
            print "Please check power or serial settings of module."
            return False
        else:
            self.PatientStatus = self.verify_checksum(self.PatientStatus)
            return True
            
    def check_patient_status(self):
        """ check_device_status()

            Method determines the status of the sensor based on the
            status transmitted by the module. Method will only check
            bits that are related to patient ready cases and NOT for
            the device ready case.
        """
        found = False
        if self.PatientStatus[0:2] == [0x7f, 0x08]:
            status = (self.PatientStatus[2] << 8) + self.PatientStatus[3];
            if ((status>>1) & 0x01) == 0x01 and not found:
                self.PatientReady = False
                found = True
                self.patient_message = "Finger is out!"
                self.parent.heartrate_infolabel.SetLabel(self.patient_message)
                self.parent.spo2_infolabel.SetLabel(self.patient_message)
                print "Please connect the finger sensor to the patient."
            if ((status>>4) & 0x01) == 0x01 and not found:
                self.PatientReady = False
                found = True
                self.patient_message = "Pulse Search takes too long!"
                self.parent.heartrate_infolabel.SetLabel(self.patient_message)
                self.parent.spo2_infolabel.SetLabel(self.patient_message)
            if ((status>>5) & 0x01) == 0x01 and not found:
                self.PatientReady = False
                found = True
                self.patient_message = "Low pulsation strength."
                self.parent.heartrate_infolabel.SetLabel(self.patient_message)
                self.parent.spo2_infolabel.SetLabel(self.patient_message)
                print "Please ask the patient to sit properly."
            if ((status>>6) & 0x01) == 0x01 and not found:
                self.PatientReady = False
                found = True
                self.patient_message = "Low signal strength received."
                self.parent.heartrate_infolabel.SetLabel(self.patient_message)
                self.parent.spo2_infolabel.SetLabel(self.patient_message)
                print "Please attach the sensor properly to the patient."
            if ((status>>7) & 0x01) == 0x01 and not found:
                self.PatientReady = False
                found = True
                self.patient_message = "Too much ambient light."
                self.parent.heartrate_infolabel.SetLabel(self.patient_message)
                self.parent.spo2_infolabel.SetLabel(self.patient_message)
                print "Please attach the sensor properly to the patient."
            if ((status>>8) & 0x01) == 0x01 and not found:
                self.PatientReady = False
                found = True
                self.patient_message = "Too many disturbances."
                self.parent.heartrate_infolabel.SetLabel(self.patient_message)
                self.parent.spo2_infolabel.SetLabel(self.patient_message)
                print "Please ask the patient to sit comfortably."
            if ((status>>9) & 0x01) == 0x01 and not found:
                self.PatientReady = False
                found = True
                self.patient_message = "Too many motion artifacts."
                self.parent.heartrate_infolabel.SetLabel(self.patient_message)
                self.parent.spo2_infolabel.SetLabel(self.patient_message)
                print "Please ask the patient to sit comfortably."
        if not found:
            self.PatientReady = True
            self.patient_message = "Patient READY."
            self.parent.heartrate_infolabel.SetLabel(self.patient_message)
            self.parent.spo2_infolabel.SetLabel(self.patient_message)
                
