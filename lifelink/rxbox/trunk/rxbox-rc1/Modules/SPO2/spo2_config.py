import wx
from spo2_cgui import SPO2_config_frame
import ConfigParser
import os
path=os.getcwd()
if path[len(path)-13:]=='Configuration':
    path='../'
else:
    path=os.getcwd()+'/'

class SPO2_Configurationmain(SPO2_config_frame):
    def __init__(self, parent,*args, **kwds):
        SPO2_config_frame.__init__(self, parent,*args, **kwds)
        #self.path=path+'/SPO2/'
        self.config=ConfigParser.ConfigParser()
        self.config.read(path+'rxbox.cfg')
        self.get_data()

    def get_data(self):
        if self.config.get('SPO2','simulated') == 'false':
            self.spo2sim_checkbox.SetValue(False)
        else:
            self.spo2sim_checkbox.SetValue(True)

        if self.config.get('SPO2','bpm_simtype') == 'Low':
            self.bpm_cbox.SetSelection(0)
        elif self.config.get('SPO2','bpm_simtype') == 'Normal':
            self.bpm_cbox.SetSelection(1)
        else:
            self.bpm_cbox.SetSelection(2)

        if self.config.get('SPO2','bo_simtype') == 'Low':
            self.oxysat_cbox.SetSelection(0)
        elif self.config.get('SPO2','bo_simtype') == 'Normal':
            self.oxysat_cbox.SetSelection(1)
        else:
            self.oxysat_cbox.SetSelection(2)
        
        self.spo2_porttxt.SetValue(self.config.get('SPO2','port'))
        
        if self.config.get('SPO2','debug') == 'false':
            self.spo2debug_checkbox.SetValue(False)
        else:
            self.spo2debug_checkbox.SetValue(True)


    def set_data(self):
        self.config.read(path+'rxbox.cfg')
        if self.spo2sim_checkbox.GetValue() == True:
            self.config.set('SPO2','simulated','true')
        else:
            self.config.set('SPO2','simulated','false')

        if self.bpm_cbox.GetValue == 'Low':
            self.config.set('SPO2','bpm_simtype','Low')
        elif self.bpm_cbox.GetValue == 'Normal':
            self.config.set('SPO2','bpm_simtype','Normal')
        else:
            self.config.set('SPO2','bpm_simtype','High')

        if self.oxysat_cbox.GetValue == 'Low':
            self.config.set('SPO2','bo_simtype','Low')
        elif self.oxysat_cbox.GetValue == 'Normal':
            self.config.set('SPO2','bo_simtype','Normal')
        else:
            self.config.set('SPO2','bo_simtype','High')

        self.config.set('SPO2','port',self.spo2_porttxt.GetValue())

        if self.spo2debug_checkbox.GetValue() == True:
            self.config.set('SPO2','debug','true')
        else:
            self.config.set('SPO2','debug','false')

        configfile = open(path+'rxbox.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(path+'rxbox_backup.cfg')

        if self.config.get('SPO2','simulated') == 'false':
            self.spo2sim_checkbox.SetValue(False)
        else:
            self.spo2sim_checkbox.SetValue(True)

        if self.config.get('SPO2','bpm_simtype') == 'Low':
            self.bpm_cbox.SetSelection(0)
        elif self.config.get('SPO2','bpm_simtype') == 'Normal':
            self.bpm_cbox.SetSelection(1)
        else:
            self.bpm_cbox.SetSelection(2)

        if self.config.get('SPO2','bo_simtype') == 'Low':
            self.oxysat_cbox.SetSelection(0)
        elif self.config.get('SPO2','bo_simtype') == 'Normal':
            self.oxysat_cbox.SetSelection(1)
        else:
            self.oxysat_cbox.SetSelection(2)
        
        self.spo2_porttxt.SetValue(self.config.get('SPO2','port'))
        
        if self.config.get('SPO2','debug') == 'false':
            self.spo2debug_checkbox.SetValue(False)
        else:
            self.spo2debug_checkbox.SetValue(True)

        self.config.read(path+'rxbox.cfg')

