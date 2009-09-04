class SPO2:
    """manages data request and acquistion from the ChipOx OEM module"""
    
    def __init__(self, parent, port="COM10",baud=9600,timeout=5):
        """initialize port settings and request according to the specified setting for ChipOx"""

        #self.parentFrame = parent
        #self.index = 0
        
        #default: port=0,baud=9600,bytesize=8,parity='N',stopbits=1,xon_xoff=0,timeout=None
        self.port = port                #set port number
        self.baudrate = baud            #set baud rate
        self.timeout = timeout          #set timeout

        """ Initialize Serial Port Settings """
        self.SerialPort = port
        self.SerialBaudRate = baud
        self.SerialTimeout = timeout
        self.DataPacket = []
        #self.OpenSerial()
       
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

    def checksum(packet):
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
        CS = CShi = CSlo = 00
        for data in packet: # traverse the list to compute for CS values
            CS = (((CShi<<8)&(0xFF00))+CSlo) + data
            CSlo = CS & 0xFF
            CShi = (((CS>>8)&0xFF) + (CSlo ^ data)) & 0xFF
        return CShi, CSlo
                        
    def verify_checksum(self,packet):
        """ verify_checksum(packet) -> data contained in the packet

            Method checks if the checksum contained in the packet
            corresponds to the data that the packet contains. If not,
            None type is returned. If packet is valid, the data will
            be returned.
        """
        reply = []
        if packet[0] == chr(0xa8) and packet[len(packet)-1]==chr(0xa8):
            data = self.string_to_packet(packet[1:len(packet)-1])
            reply = data[:len(data)-2]
            self.compute_checksum(reply)
            if self.CShi==data[-2] and self.CSlo==data[-1]:
                return reply
            else:
                print 'Checksum Error.'
                return ''
        else:
            print "Transmit Error: Incomplete Packet."
            return None

    def get_reply(self):
        """ get_reply() -> returns one complete packet

            Method reads data from the serial port and requires a complete
            packet to return to the call. If serial port times out, None type
            is returned to indicate the time out.
        """
        reply = ''; flag_counter = 0; start = time.time()
        while (flag_counter < 2):
            byte = self.bpm.read(1)
            if byte == '':
                break
            if flag_counter == 1 and byte != chr(0xa8):
                reply = reply + byte
            if byte == chr(0xa8):
                reply = reply + byte
                flag_counter = flag_counter + 1
        if byte == '':
            return None
        else:
            return reply

    def POST(self):
        """ self.POST() -> 'True' if module is powered on, 'False' otherwise

            This method resets the SPO2 module. After reset, the reply packet is read and method
            test_power is called to check whether the SPO2 module is powered on and is transmitting
            data to the RxBox. If module is powered on, Serial number and Firmware version
            are extracted from the reply and method returns 'True' logic value. Otherwise,
            'False' is returned.
        """
        self.checksum([0x7f, 0xb2]) # Compute for checksum
        self.DataPacket = [0xa8, 0x7f, 0xb2, self.CShi, self.CSlo, 0xa8] # Organize data packet
        self.DataPacket = [chr(item) for item in self.DataPacket] # convert hex values to char
        self.Command = ''.join(self.DataPacket) # combine packets into one string
        self.bpm.flushOutput() # flush output buffer of serial port
        # Command the module to Reset it's hardware component
        self.bpm.write(self.Command) # print/output command via serial port to SPO2 module
        self.bpm.flushInput() # flush input buffer of serial port
        self.Power = False
        if self.test_power():
            self.check_power
        return self.Power

    def test_power(self):
        """ self.test_power()

            Method receives reply to from the module and determines whether a the
            serial port timed out or there is a packet received.
        """
        self.SerialNumber = self.get_reply()
        self.FirmwareVersion = self.get_reply()
        if self.FirmwareVersion == None:
            print "POWER TEST FAIL: SPO2 not powered on."
            print "Error: Serial Number not found."
            print "Error: Firmware Version not found."
            return False
        else:
            self.FirmwareVersion = self.packet_to_string(self.verify_checksum(self.FirmwareVersion))
            self.SerialNumber = self.packet_to_string(self.verify_checksum(self.SerialNumber))
            print "SPO2 Powered ON."
            return True
            #self.check_power()

    def check_power(self):
        """ self.check_power()

            Method determines if the packet received from the module are valid
            or if the packet is complete.
        """
        if self.FirmwareVersion[0:2] == self.packet_to_string([0x7f,0x21]):
            self.FirmwareVersion = self.FirmwareVersion[2:]
            self.Power = True
            print "Firmware Version: ", self.FirmwareVersion[:-1]
        else:
            self.FirmwareVersion = None
            print "Firmware Version not found in packet."
        if self.SerialNumber[0:2] == self.packet_to_string([0x7f,0x23]):
            self.SerialNumber = self.SerialNumber[2:]
            self.Power = True
            print "Serial Number: ", self.SerialNumber[:-1]
        else:
            self.SerialNumber = None
            print "Serial Number not found in packet."

    def device_ready(self):
        """ device_ready()

            Method determines if the the sensor is properly attached to
            the module. A status check is initiated by the module
            to determine the state of the device and the sensor.
        """
        self.compute_checksum([0x7f, 0x88, 0x00]) # Compute for checksum
        self.DataPacket = [0xa8, 0x7f, 0x88, 0x00, self.CShi, self.CSlo, 0xa8] # Organize data packet
        self.DataPacket = [chr(item) for item in self.DataPacket] # convert hex values to char
        self.Command = ''.join(self.DataPacket) # combine packets into one string
        self.bpm.flushOutput() # flush output buffer of serial port
        # Command the module to Reset it's hardware component
        self.bpm.write(self.Command) # print/output command via serial port to SPO2 module
        self.bpm.flushInput() # flush input buffer of serial port
        self.test_device_ready()
        return self.DeviceReady

    def test_device_ready(self):
        """ test_device_ready()

            Method gets reply from the module and determines if the
            the reply is valid or if the serial port timed out.
        """
        self.DeviceStatus = self.get_reply()
        if self.DeviceStatus == None:
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
        if self.DeviceStatus[0:2] == [0x7f, 0x08]:
            status = (self.DeviceStatus[2] << 8) + self.DeviceStatus[3]
            if (status & 0x01) == 0x01:
                self.DeviceReady = False
                print "Device Not Ready: Sensor is OFF!"
                print "Please connect the finger sensor to the module."
            if ((status>>10) & 0x01) == 0x01:
                self.DeviceReady = False
                print "Device Not Ready: Sensor is DEFECTIVE!"
                print "Please replace the finger sensor."
            if ((status>>11) & 0x01) == 0x01:
                self.DeviceReady = False
                print "Device Not Ready: Power Supply out of range!"
            if ((status>>12) & 0x01) == 0x01:
                self.DeviceReady = False
                print "Device Not Ready: Module overheated!"
            if ((status>>13) & 0x01) == 0x01:
                self.DeviceReady = False
                print "Device Not Ready: WRONG Sensor!"
            if ((status>>14) & 0x01) == 0x01:
                self.DeviceReady = False
                print "Device Not Ready: Measurement Error!"
            if found == 0:
                self.DeviceReady = True
                print "Device READY."
                
    def patient_ready(self):
        """ patient_ready()

            Method determines if the the sensor is properly attached to
            the patient. A status check is initiated by the module
            to determine the state of the patient and the sensor.
        """
        self.compute_checksum([0x7f, 0x88, 0x00]) # Compute for checksum
        self.DataPacket = [0xa8, 0x7f, 0x88, 0x00, self.CShi, self.CSlo, 0xa8] # Organize data packet
        self.DataPacket = [chr(item) for item in self.DataPacket] # convert hex values to char
        self.Command = ''.join(self.DataPacket) # combine packets into one string
        self.bpm.flushOutput() # flush output buffer of serial port
        # Command the module to Reset it's hardware component
        self.bpm.write(self.Command) # print/output command via serial port to SPO2 module
        self.bpm.flushInput() # flush input buffer of serial port
        self.PatientReady = False
        self.test_patient_ready()
        return self.PatientReady

    def test_patient_ready(self):
        """ test_patient_ready()

            Method gets reply from the module and determines if the
            the reply is valid or if the serial port timed out.
        """
        self.PatientStatus = self.get_reply()
        if self.PatientStatus == None:
            print "POWER TEST FAIL: SPO2 not powered on."
            print "Please check power or serial settings of module."
        else:
            self.PatientStatus = self.verify_checksum(self.PatientStatus)
            self.test_patient_ready()
            
    def check_patient_status(self):
        """ check_device_status()

            Method determines the status of the sensor based on the
            status transmitted by the module. Method will only check
            bits that are related to patient ready cases and NOT for
            the device ready case.
        """
        if self.PatientStatus[0:2] == [0x7f, 0x08]:
            status = (self.PatientStatus[2] << 8) + self.PatientStatus[3]; found = 0
            if ((status>>1) & 0x01) == 0x01:
                self.PatientReady = False
                print "Patient Not Ready: Finger is out!"
                print "Please connect the finger sensor to the patient."
            if ((status>>4) & 0x01) == 0x01:
                self.PatientReady = False
                print "Patient Not Ready: Pulse Search takes too long!"
            if ((status>>5) & 0x01) == 0x01:
                self.PatientReady = False
                print "Patient Not Ready: Low pulsation strength."
                print "Please ask the patient to sit properly."
            if ((status>>6) & 0x01) == 0x01:
                self.PatientReady = False
                print "Patient Not Ready: Low signal strength received."
                print "Please attach the sensor properly to the patient."
            if ((status>>7) & 0x01) == 0x01:
                self.PatientReady = False
                print "Patient Not Ready: Too much ambient light."
                print "Please attach the sensor properly to the patient."
            if ((status>>8) & 0x01) == 0x01:
                self.PatientReady = False
                print "Patient Not Ready: Too many disturbances."
                print "Please ask the patient to sit comfortably."
            if ((status>>9) & 0x01) == 0x01:
                self.PatientReady = False
                print "Patient Not Ready: Too many motion artifacts."
                print "Please ask the patient to sit comfortably."
            if found == 0:
                self.PatientReady = True
                print "Patient READY."
