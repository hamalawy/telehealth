from reader import Reader
import time
from wx import CallAfter

class spo2_sim:

    def __init__(self,parent):

        self.DataPacket = []
        self.SpO2 = 0
        self.PulseRate = 0
        self.SignalQuality = 0
        self.Read = Reader()
        self.File = self.Read.OpenFile()
        self.spo2_values = []
        self.pulserate_values = []
        self.parent = parent
        self.count = 0

    def Destuff(self,packet):
        
        """
        Detect and decodes byte-stuffed data in reply packet; return a list of char strings called destuffed
        Accept a string called raw_packet
        """
        
        #---------------------------------------------------------------------------
        # If reserved character 0xa9 is found in a reply packet it is to be ignored
        # and the following character is OR-linked with 0x20 and saved
        #---------------------------------------------------------------------------

        destuffed = [chr(0xa8)]                                 # initialize list for 'destuffed' reply packet; list already contains start flag
        skip_counter = 0                                        # initialize skip for going to next char
        
        for index in range(1, (len(packet)-1)):             # end flag excluded (next last character is the last candidate for destuffing)
            if skip_counter == 1:                               # re-initialize skip_counter
                skip_counter = 0                                # reset skip_counter to 0                                 
                continue                                        # another skip
            elif skip_counter == 0:
                if packet[index] == chr(0xa9):
                    destuffed.append(chr( ord(packet[index+1])|int(0x20) ))       # append next char(OR-linked with 0x20) to 'destuffed' data_stream list
                    skip_counter+= 1                                                  # move to next next char
                    continue                                                          # skip
                else:
                    destuffed.append(chr( ord(packet[index]) ))                   # char is not 0xa9, simply append it to 'destuffed' data_stream list        
                    continue
        destuffed.append(chr(0xa8))                             # append end flag
        
        
        return destuffed                                        # return the 'destuffed' reply packet as a list of char strings

    def ReplyParser(self, Packet):
        """
        extract the readings for sp02, pulse rate & signal quality
        accept the 'destuffed' reply packet from the pulse oximeter """

        destuff = [elem for elem in Packet]
        CHIPOX_channel = ord(destuff[1])
        print ord(destuff[1])
        if CHIPOX_channel == 127:                                   # CHIPOX channel
            sig_quality = ord(destuff[6])   
            print "signal quality:", sig_quality, "%"
            if (sig_quality <= 100):                                # if CHIPOX channel is ok and signal quality is not erroneous
                spo2 = ord(destuff[3])
                bpm = (ord(destuff[4])<<8) + ord(destuff[5])
                sig_amp = ord(destuff[7])
                print "spo2 reading:", spo2
                print "pulse_rate:", bpm, "bpm"
                print "sig_amp:",sig_amp
            else:                                                   # if signal quality is erroneous
                if len(self.spo2_values)>0:                         # if self.spo2 list already contains something
                    prev_spo2 = self.spo2_values[len(self.spo2_values)-1]
                    prev_pulse_rate = self.pulserate_values[len(self.pulserate_values)-1]
                else:                                               # if self.spo2 list does not contain anything yet
                    prev_spo2 = 0
                    prev_pulse_rate = 0
                print "Warning: Signal quality is erroneous. Get previous readings"
                print "Previous spo2 reading:", prev_spo2
                print "Previous pulse_rate:", prev_pulse_rate, "bpm"
                spo2 = prev_spo2
                bpm = prev_pulse_rate
                
        elif CHIPOX_channel == 13:                                  # SYSTEM ERROR channel
            sig_quality = 0
            print "Signal quality not determined."
            if len(self.spo2_values)>0:                             # if self.spo2 list already contains something
                prev_spo2 = self.spo2[len(self.spo2)-1]
                prev_pulse_rate = self.pulserate_values[len(self.pulserate_values)-1]
            else:                                                   # if self.spo2 list does not contain anything yet
                prev_spo2 = 0
                prev_pulse_rate = 0
            print "Error: Please make sure the sensor is fitted propery. Get previous readings"
            print "Previous spo2 reading:", prev_spo2
            print "Previous pulse_rate:", prev_pulse_rate, "bpm"
            spo2 = prev_spo2
            bpm = prev_pulse_rate
        else:
            # "UNKNOWN CHANNEL"
            spo2 = 0
            bpm = 0
            sig_quality = 0
                  
        # update values
        self.SpO2 = spo2
        self.PulseRate = bpm
        self.signal_quality = sig_quality

        strSpO2=str(self.SpO2)
        strPulseRate=str(self.PulseRate)

        self.parent.spo2value_label.SetLabel(strSpO2)
        self.parent.bpmvalue_label.SetLabel(strPulseRate)

    def get(self):

        RawPacket = self.Read.ReadLine(self.File)
        Packet = self.Destuff(RawPacket)
        print Packet
        self.ReplyParser(Packet)
        self.spo2_values.append(self.SpO2)
        self.pulserate_values.append(self.PulseRate)

        self.count=self.count+1
        
        #looping file
        if self.count == 40:
            self.File = self.Read.OpenFile()
            self.count = 0
        
        
        return Packet


