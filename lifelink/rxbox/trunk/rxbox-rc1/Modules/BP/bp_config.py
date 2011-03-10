import wx
from bp_cgui_mod import BP_config_frame
import ConfigParser
import os

path=os.getcwd()
if path[len(path)-13:]=='Configuration':
    path='../'
else:
    path=os.getcwd()+'/'

class BP_Configurationmain(BP_config_frame):
    def __init__(self, parent,*args, **kwds):
        BP_config_frame.__init__(self, parent,*args, **kwds)
        self.config=ConfigParser.ConfigParser()
        self.config.read(path+'rxbox.cfg')
        self.get_data()

    def get_data(self):
        
        if self.config.get('BP','simulated') == 'false':
            self.bpsim_checkbox.SetValue(False)
        else:
            self.bpsim_checkbox.SetValue(True)

        if self.config.get('BP','simtype') == 'Low':
            self.bp_simtypecbox.SetSelection(0)
        elif self.config.get('BP','simtype') == 'Normal':
            self.bp_simtypecbox.SetSelection(1)
        else:  
            self.bp_simtypecbox.SetSelection(2)
        
        self.bp_porttxt.SetValue(self.config.get('BP','port'))
        
        if self.config.get('BP','debug') == 'false':
            self.bpdebug_checkbox.SetValue(False)
        else:
            self.bpdebug_checkbox.SetValue(True)

    def set_data(self):
        self.config.read(path+'rxbox.cfg')
        if self.bpsim_checkbox.GetValue() == True:
            self.config.set('BP','simulated','true')
        else:
            self.config.set('BP','simulated','false')

        if self.bp_simtypecbox.GetValue == 'Low':
            self.config.set('BP','simtype','Low')
        elif self.bp_simtypecbox.GetValue == 'Normal':
            self.config.set('BP','simtype','Normal')
        else:
            self.config.set('BP','simtype','High')
        
        self.config.set('BP','port',self.bp_porttxt.GetValue())
    
        if self.bpdebug_checkbox.GetValue() == True:
            self.config.set('BP','debug','true')
        else:
            self.config.set('BP','debug','false')

        configfile = open(path+'rxbox.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(path+'rxbox_backup.cfg')
        if self.config.get('BP','simulated') == 'false':
            self.bpsim_checkbox.SetValue(False)
        else:
            self.bpsim_checkbox.SetValue(True)

        if self.config.get('BP','simtype') == 'Low':
            self.bp_simtypecbox.SetSelection(0)
        elif self.config.get('BP','simtype') == 'Normal':
            self.bp_simtypecbox.SetSelection(1)
        else:  
            self.bp_simtypecbox.SetSelection(2)
        
        self.bp_porttxt.SetValue(self.config.get('BP','port'))
        
        if self.config.get('BP','debug') == 'false':
            self.bpdebug_checkbox.SetValue(False)
        else:
            self.bpdebug_checkbox.SetValue(True)
        self.config.read(path+'rxbox.cfg')
