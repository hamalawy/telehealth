""" simsensors.py

simsensors module contains the simulated sensor classes:
    Spo2sim - simulated blood oxygen saturation
    Bpsim - simulated blood pressure
    EcgSim - simulated ECG

Author: Tim Ebido
August 2009
"""

import time
import wx
import filters
from reader import Reader
from matplotlib import pyplot
from string import split
import ConfigParser
import wave
import pyaudio
import threading


class Spo2sim:

    def __init__(self,parent):
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
        
        self.spo2_read = Reader()
        filename_spo2 = self.config.get('spo2', 'spo2_sim_type')
        filename_hr = self.config.get('spo2', 'hr_sim_type')
        self.spo2file = self.spo2_read.OpenFile('simulators/spo2' + filename_spo2.lower() + '.txt')
        self.hrfile = self.spo2_read.OpenFile('simulators/hr' + filename_hr.lower() + '.txt')

    def update_spo2_display(self):

        self.parent_panel.spo2value_label.SetLabel(self.spo2_value)
        self.parent_panel.bpmvalue_label.SetLabel(self.hr_value)
    
    def get(self):
        
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
        
        if (self.spo2sim_counter % 15) == 0:
            self.spo2sim_counter = 0
        
class BpSim:
    
    def __init__(self,parent):
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')        
        self.parent_panel = parent
        self.bpsim_counter = 0

        self.bpvalue = ''
        self.sys_list = []
        self.dias_list = []
        self.instantiate_file()

    def instantiate_file(self):
                
        self.bpread = Reader()
        filename = self.config.get('bp', 'sim_type')
        self.bpfile = self.bpread.OpenFile('simulators/bp'+ filename.lower() +'.txt')

    def update_bp_display(self):
        self.parent_panel.bpvalue_label.SetLabel('     '+self.systolic_value + '/' + self.diastolic_value)

    def get(self):
        
        self.parent_panel.bp_infolabel.SetLabel('Getting BP')
        self.parent_panel.bpNow_Button.Enable(False)
        reload_bp_str = self.parent_panel.setBPmins_combobox.GetValue()
        self.reload_bp = int(reload_bp_str[0:2])*1000*3 #60
        
        #5min -> 15seconds
        #15min -> 45seconds
        #30min -> 90seconds
        #60min -> 180seconds

        self.parent_panel.bp_pressure_indicator.Enable(True)
        self.parent_panel.file = open('pressure.txt','r')
        self.parent_panel.pressure_timer.Start(5)
        
    def bp_finished(self):
        
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
    
        self.update_bp_display()        
        self.bpsim_counter += 1
        
        if self.parent_panel.bp_isCyclic == 1:
            self.parent_panel.timer_bp.Start(self.reload_bp)

        if (self.bpsim_counter % 15) == 0:
            self.bpsim_counter = 0
        
class EcgSim:
    
    def __init__(self, parent):
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')
        
        self.ecgfile = open('ecg.txt','r')
        self.ecg_sim_values = []
        self.ecg_list_scaled = []
        for line in self.ecgfile:
            line = line[:6]
            self.ecg_sim_values.append(float(line))
        self.ecgfile.close()
        self.ecg_sim_values = filters.besselfilter(self.ecg_sim_values)
        
    def get_plot(self):
        
        ecg_file = open(self.config.get('ecg', 'sim_type'), 'r')
        done = 0
        temp_list = []
        
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
        
        return temp_list
        
    def get(self):
        
        self.ecg_list = self.ecg_sim_values[500:8000]
        ave = sum(self.ecg_list)/7500
        for x in range(0,7500):
            self.ecg_list[x] = self.ecg_list[x] - ave
        
        for x in range(0,len(self.ecg_list)):
            self.ecg_list_scaled.append(int(self.ecg_list[x]*1000))
         
        
class stethplay(threading.Thread):        
    def __init__(self,parent):
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
        while self.data != '':
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.chunk)
        self.stream.close()
        self.p.terminate()
        self.parent_frame.record_button.Enable(True)
        self.parent_frame.play_button.Enable(True)
        
    def stop(self):
        self.stopEvent.set()
