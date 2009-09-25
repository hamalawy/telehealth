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
import ConfigParser



class Spo2sim:

    def __init__(self,parent):
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')   
        
        self.parent_panel = parent
        self.spo2sim_counter = 0
        self.spo2_sim_values = [100,99,98,97,96,95,94,93,92,93,94,95,96,97,98,\
                                99]
        self.bpm_sim_values = [80,79,78,77,76,75,74,73,74,75,76,77,78,79,80]
        self.spo2 = 0
        self.bpm = 0        
        self.spo2_list = []
        self.bpm_list = []

        if (self.config.get('SPO2','spo2source') != '0'):
            self.spo2sample = str(self.config.get('SPO2','spo2source'))
#            self.spo2sample = 'sponormal.txt'
            self.spo2read = Reader()
            self.spo2file = self.spo2read.OpenFile(self.spo2sample)
            self.spo2sim = self.spo2read.ReadLine(self.spo2file)
            self.bpmsim = self.spo2read.ReadLine(self.spo2file)  

    def update_spo2_display(self):
    
        if (self.config.get('SPO2','spo2source') == '0'):         
            self.parent_panel.spo2value_label.SetLabel(str(self.spo2))
            self.parent_panel.bpmvalue_label.SetLabel(str(self.bpm))
        if (self.config.get('SPO2','spo2source') != '0'):     
            self.parent_panel.spo2value_label.SetLabel(str(self.spo2sim))
            self.parent_panel.bpmvalue_label.SetLabel(str(self.bpmsim))
    
    def get(self):
        
        self.parent_panel.heartrate_infolabel.SetLabel('Acquiring pulse rate')
        self.parent_panel.spo2_infolabel.SetLabel('Acquiring Spo2')
        self.spo2 = self.spo2_sim_values[self.spo2sim_counter]
        self.bpm = self.bpm_sim_values[self.spo2sim_counter]
        
        if (self.config.get('SPO2','spo2source') == '0'):        
            self.spo2_list.append(self.spo2)
            self.bpm_list.append(self.bpm)
        if (self.config.get('SPO2','spo2source') != '0'):     
            self.spo2_list.append(int(self.spo2sim))
            self.bpm_list.append(int(self.bpmsim))        
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
        self.systole_sim_values = [120,119,120,119,120,119,120,119,120,119,\
                                    120,119,120,119,120]
        self.diastole_sim_values = [80,80,80,80,80,80,80,80,80,80,80,80,80,80,\
                                    80]
        self.sys = 0
        self.dias = 0
        self.bpvalue = ''
        self.sys_list = []
        self.dias_list = []
        if (self.config.get('BP','bpsource') != '0'):        
            self.bpsample = str(self.config.get('BP','bpsource')) 
            self.bpread = Reader()
            self.bpFile = self.bpread.OpenFile(self.bpsample)
            self.syssim = self.bpread.ReadLine(self.bpFile)
            self.diassim = self.bpread.ReadLine(self.bpFile) 
        
        self.timer = wx.Timer(self.parent_panel)
        self.parent_panel.Bind(wx.EVT_TIMER,self.bp_finished,self.timer)
        
    def update_bp_display(self):
        
        self.parent_panel.bpvalue_label.SetLabel(self.bpvalue)
        
    def get(self):
        
        print 'Getting bp'
        self.parent_panel.bp_infolabel.SetLabel('Getting BP')
        self.parent_panel.bpNow_Button.Enable(False)
        reload_bp_str = self.parent_panel.setBPmins_combobox.GetValue()
        self.reload_bp = int(reload_bp_str[0:2])*1000
        self.timer.Start(3000)
        
#        self.parent_panel.bp_slider.Enable(True)
        self.parent_panel.bp_pressure_indicator.Enable(True)
        self.parent_panel.setBPmins_combobox.Enable(False)
        self.parent_panel.file = open('pressure.txt','r')
        self.parent_panel.pressure_timer.Start(20)
        
    def bp_finished(self,evt):
        
        print 'Bp acquired'
        self.sys_list = []
        self.dias_list = []
        
        self.parent_panel.bp_infolabel.SetLabel('BP acquired')
        self.parent_panel.bpNow_Button.Enable(True)
        
        self.sys = self.systole_sim_values[self.bpsim_counter]
        self.dias = self.diastole_sim_values[self.bpsim_counter]

        if (self.config.get('BP','bpsource') == '0'):        
            self.sys_list.append(self.sys)
            self.dias_list.append(self.dias)
            self.bpvalue = str(self.sys) + '/' + str(self.dias)
        if (self.config.get('BP','bpsource') != '0'):  
            self.sys_list.append(self.syssim)
            self.dias_list.append(self.diassim) 
            self.bpvalue = str(self.syssim) + '/' + str(self.diassim)
        
                  
        self.update_bp_display()        
        self.bpsim_counter += 1
        
        if self.parent_panel.bp_isCyclic == 1:
            self.parent_panel.timer2.Start(self.reload_bp)
        
        if (self.bpsim_counter % 15) == 0:
            self.bpsim_counter = 0
        
        self.timer.Stop()
        
class EcgSim:
    
    def __init__(self, parent):
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')
        
        self.ecgfile = open('ecg.txt','rb')
        self.ecg_sim_values = []
        self.ecg_list_scaled = []
        for line in self.ecgfile:
            line = line[:6]
            self.ecg_sim_values.append(float(line))
        self.ecgfile.close()
        self.ecg_sim_values = filters.besselfilter(self.ecg_sim_values)
        
    def get(self):
        
        self.ecg_list = self.ecg_sim_values[500:8000]
        ave = sum(self.ecg_list)/7500
        for x in range(0,7500):
            self.ecg_list[x] = self.ecg_list[x] - ave
        
#        pyplot.plot(self.ecg_list)
#        pyplot.show()
        
        for x in range(0,len(self.ecg_list)):
            self.ecg_list_scaled.append(int(self.ecg_list[x]*1000))
         
        
        
        
        
        
        
