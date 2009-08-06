import time
import wx

class Spo2sim:
    
    def __init__(self,parent):
        
        self.parent_panel = parent
        self.spo2sim_counter = 0
        self.spo2_sim_values = [100,99,98,97,96,95,94,93,92,\
                                93,94,95,96,97,98,99]
        self.bpm_sim_values = [80,79,78,77,76,75,74,73,74,75,76,77,\
                                78,79,80]
        self.spo2 = 0
        self.bpm = 0        
        self.spo2_list = []
        self.bpm_list = []
        
    def update_spo2_display(self):
        
        self.parent_panel.spo2value_label.SetLabel(str(self.spo2))
        self.parent_panel.bpmvalue_label.SetLabel(str(self.bpm))
    
    def get(self):
        
        self.parent_panel.heartrate_infolabel.SetLabel('Acquiring pulse rate')
        self.parent_panel.spo2_infolabel.SetLabel('Acquiring Spo2')
        self.spo2 = self.spo2_sim_values[self.spo2sim_counter]
        self.bpm = self.bpm_sim_values[self.spo2sim_counter]
        
        self.spo2_list.append(self.spo2)
        self.bpm_list.append(self.bpm)
        
        self.update_spo2_display()
        self.spo2sim_counter += 1
        
        if (self.spo2sim_counter % 15) == 0:
            
            self.spo2sim_counter = 0
        
class BpSim:
    
    def __init__(self,parent):
        
        self.parent_panel = parent
        self.bpsim_counter = 0
        self.systole_sim_values = [120,119,120,119,120,119,120,119,120,\
                                    119,120,119,120,119,120]
        self.diastole_sim_values = [80,80,80,80,80,80,80,80,80,80,80,\
                                    80,80,80,80]
        self.sys = 0
        self.dias = 0
        self.bpvalue = ''
        self.sys_list = []
        self.dias_list = []
        
        self.timer = wx.Timer(self.parent_panel)
        self.parent_panel.Bind(wx.EVT_TIMER,self.bp_finished,self.timer)
        
    def update_bp_display(self):
        
        self.parent_panel.bpvalue_label.SetLabel(self.bpvalue)
        
    def get(self):
        
        print 'Getting bp'
        self.parent_panel.bp_infolabel.SetLabel('Getting BP')
        self.parent_panel.bpNow_Button.Enable(False)
        self.timer.Start(3000)
        
    def bp_finished(self,evt):
        
        print 'Bp acquired'
        self.sys_list = []
        self.dias_list = []
        
        self.parent_panel.bp_infolabel.SetLabel('BP acquired')
        self.parent_panel.bpNow_Button.Enable(True)
        
        self.sys = self.systole_sim_values[self.bpsim_counter]
        self.dias = self.diastole_sim_values[self.bpsim_counter]
        
        self.sys_list.append(self.sys)
        self.dias_list.append(self.dias)
                
        self.bpvalue = str(self.sys) + '/' + str(self.dias)         
        self.update_bp_display()        
        self.bpsim_counter += 1
        
        if (self.bpsim_counter % 15) == 0:
            self.bpsim_counter = 0
        
        self.timer.Stop()
        
class EcgSim:
    
    def _init__(self,parent):
        pass
        
