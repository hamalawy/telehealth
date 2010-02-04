""" simsensors.py

simsensors module contains the simulated sensor classes:
    Spo2sim - simulated blood oxygen saturation
    BpSim - simulated blood pressure
    EcgSim - simulated ECG
    stethplay - simulated stethoscope sounds
    
Author: Tim Ebido and Thomas Rodinel Soler
2009-2010
"""

import ConfigParser
from string import split
import threading

import wx
import wave
import pyaudio
from matplotlib import pyplot

import filters
from reader import Reader
from matplotlib import pyplot

class Spo2sim:
    """ Class for simulator for pulse oximeter module
    
    Methods:
        __init__(RxFrame)
        instantiate_file()
        update_spo2_display()
        get()
    """

    def __init__(self,parent):
        """Initializes simulator for pulse oximeter module
        
        - Interprets the configuration file
        - Loads the corresponding simulator text file
        - Initializes variables
        
        Arguments: __init__(RxFrame)
        """
        
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')   
        
        self.parent_panel = parent
        self.spo2sim_counter = 0
        self.spo2 = 0
        self.bpm = 0        
        self.spo2_list = []
        self.bpm_list = []
        self.instantiate_file()
    
    def instantiate_file(self):
        """Acquires options from the configuration file and initializes
        the corresponding text file containing heart rate and spo2 data
        """
        
        self.spo2_read = Reader()
        filename_spo2 = self.config.get('spo2', 'spo2_sim_type')
        filename_hr = self.config.get('spo2', 'hr_sim_type')
        self.spo2file = self.spo2_read.OpenFile('simulators/spo2' + filename_spo2.lower() + '.txt')
        self.hrfile = self.spo2_read.OpenFile('simulators/hr' + filename_hr.lower() + '.txt')

    def update_spo2_display(self):
        """Displays extracted heart rate and spo2 data to their corresponding
        data panel
        """

        self.parent_panel.spo2value_label.SetLabel(self.spo2_value)
        self.parent_panel.bpmvalue_label.SetLabel(self.hr_value)
    
    def get(self):
        """Extracts heart rate and spo2 data from text files and calls
        update_spo2_display() to display datas
        """
        
        self.parent_panel.heartrate_infolabel.SetLabel('Acquiring pulse rate')
        self.parent_panel.spo2_infolabel.SetLabel('Acquiring Spo2')

        self.hr_value = self.spo2_read.ReadLine(self.spo2file)
        self.spo2_value = self.spo2_read.ReadLine(self.hrfile)
        
        if self.hr_value == '':
            self.instantiate_file()
            self.get()
            
        if self.spo2_value == '':
            self.instantiate_file()
            self.get()
      
        self.update_spo2_display()
        self.spo2sim_counter += 1
        
        self.spo2_list.append(int(self.spo2_value))
        
        if (self.spo2sim_counter % 15) == 0:
            self.spo2sim_counter = 0
        
class BpSim:
    """ Class for simulator for blood pressure module
    
    Methods:
        __init__(RxFrame)
        instantiate_file()
        update_bp_display()
        get()
        bp_finished()
    """
    
    def __init__(self,parent):
        """Initializes simulator for blood pressure module
        
        - Interprets the configuration file
        - Loads the corresponding simulator text file
        - Initializes variables
        
        Arguments: __init__(RxFrame)
        """
        
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')        
        self.parent_panel = parent
        self.bpsim_counter = 0

        self.bpvalue = ''
        self.sys_list = []
        self.dias_list = []
        self.instantiate_file()
        
        self.systolic_value = '--'
        self.diastolic_value = '--'

    def instantiate_file(self):
        """Acquires options from the configuration file and initializes
        the corresponding text file containing blood pressure
        """
                
        self.bpread = Reader()
        filename = self.config.get('bp', 'sim_type')
        self.bpfile = self.bpread.OpenFile('simulators/bp'+ filename.lower() +'.txt')

    def update_bp_display(self):
        """Displays extracted blood pressure data to their corresponding
        data panel
        """
        
        if self.parent_panel.refer_panel_shown == 0:
            self.parent_panel.bpvalue_label.SetLabel(self.systolic_value + '/' + self.diastolic_value)
        else:
            self.parent_panel.bpvalue_label.SetLabel(self.systolic_value + '/' + self.diastolic_value)

    def get(self):
        """Initial method that will start acquisition of simulated bp data
        using the following steps:
        
        - Disables NOW button
        - Determines cyclic time interval and enables simulated blood pressure bar
        """
        
        self.parent_panel.bp_infolabel.SetLabel('Getting BP')
        self.parent_panel.bpNow_Button.Enable(False)
        reload_bp_str = self.parent_panel.setBPmins_combobox.GetValue()
        self.reload_bp = int(reload_bp_str[0:2])*1000*60
        
        #5min -> 15seconds
        #15min -> 45seconds
        #30min -> 90seconds
        #60min -> 180seconds

        self.parent_panel.bp_pressure_indicator.Enable(True)
        self.parent_panel.file = open('pressure.txt','r')
        self.parent_panel.pressure_timer.Start(20)
        
    def bp_finished(self):
        """Method that is called after bp acquistion is finished:
        
        - Enables NOW button
        - Extracts systolic and diastolic value from text files
        - Calls update_bp_display() to display data
        """
        
        print 'Bp acquired'
        self.sys_list = []
        self.dias_list = []
        
        self.parent_panel.bp_infolabel.SetLabel('BP acquired')
        self.parent_panel.bpNow_Button.Enable(True)
        
        self.systolic_value = self.bpread.ReadLine(self.bpfile)
        self.diastolic_value = self.bpread.ReadLine(self.bpfile)
        
        if self.systolic_value == '':
            self.instantiate_file()
            self.bp_finished()
            
        if self.diastolic_value == '':
            self.instantiate_file()
            self.bp_finished()

        self.sys_list.append(int(self.systolic_value))
        self.dias_list.append(int(self.diastolic_value))

        self.update_bp_display()        
        self.bpsim_counter += 1
        
        if self.parent_panel.bp_isCyclic == 1:
            self.parent_panel.timer_bp.Start(self.reload_bp)

        if (self.bpsim_counter % 15) == 0:
            self.bpsim_counter = 0
        
class EcgSim:
    """ Class for simulator for electrocardiography (ECG) module
    
    Methods:
        __init__(RxFrame)
        get_plot()
    """
    
    def __init__(self, parent):
        """Initializes simulator for ECG module
        
        - Interprets the configuration file
        - Loads the corresponding simulator text file
        - Initializes variables
        
        Arguments: __init__(RxFrame)
        """
        
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')


        
    def get_plot(self):
        """This method will do the following, if simulated data comes from MIT
        physiobank:
        
        - Determines file path of data text file
        - Extract ecg data and store it in a list
        """
        
        ecg_file = open(self.config.get('ecg', 'sim_type'), 'r')
        done = 0
        temp_list = []
        self.ecg_list = []
        
        ecg_file.readline()
        ecg_file.readline()
        
        while not done:
            value = ecg_file.readline()
            value = ecg_file.readline()
            if value != '':
                sample = value.split()
                temp_list.append(float(sample[1]))
            else:
                done = 1

        ecg_file.close()
        temp_list = filters.besselfilter(temp_list)
        self.ecg_list = temp_list[:7500]
        
        return temp_list
        
class stethplay(threading.Thread):
    """ Class for simulator for electrocardiography (ECG) module
    
    Methods:
        __init__(RxFrame)
        run()
        stop()
        
    Arguments: threading module
    """
    
    def __init__(self,parent):
        """Initializes simulator for stethoscope
        
        - Interprets threading
        - Interprets configuration file
        - Sets necessary variables
        
        Arguments: __init__(RxFrame)
        """
        
        threading.Thread.__init__(self)
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')
        self.data = 0
        self.stream = None
        self.p = None
        self.wf = None           
        self.parent_frame = parent
        self.chunk = 1024
        
    def run(self):
        """Primary method of stehoscope thread:
        
        - Opens the desired wav file and creates PyAudio instance
        - Create a stream of data consisting of the audio file and plays it
        - Close the stream after playing the data
        """
        
        self.wf = wave.open(self.parent_frame.openwav, 'rb')
        self.p = pyaudio.PyAudio()
        # open stream
        self.stream = self.p.open(format =
                        self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels = self.wf.getnchannels(),
                        rate = self.wf.getframerate(),
                        output = True)

        # read data
        self.data = self.wf.readframes(self.chunk)
        # play stream
        while (self.data != '') and (self.play_steth == 1):
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.chunk)
        self.stream.close()
        self.p.terminate()
        self.parent_frame.record_button.Enable(True)
        self.parent_frame.play_button.Enable(True)
        
    def stop(self):
        """
        """
        print 'Stop pressed'
        self.play_steth = 0
