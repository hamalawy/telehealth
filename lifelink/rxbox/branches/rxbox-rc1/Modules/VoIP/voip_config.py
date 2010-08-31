import wx
from voip_cgui import VOIP_config_frame
import ConfigParser

class VOIP_Configurationmain(VOIP_config_frame):
    def __init__(self, parent,path,*args, **kwds):
        VOIP_config_frame.__init__(self, parent,*args, **kwds)
        self.path=path+'/VoIP/'
        self.config=ConfigParser.ConfigParser()
        self.config.read(self.path+'voip.cfg')
        self.get_data()

    def get_data(self):
        if self.config.get('voip','simulated') == 'false':
            self.voipsim_checkbox.SetValue(False)
        else:
            self.voipsim_checkbox.SetValue(True)
        self.voip_hostidtxt.SetValue(self.config.get('voip','hostid'))

    def set_data(self):
        if self.voipsim_checkbox.GetValue() == True:
            self.config.set('voip','simulated','true')
        else:
            self.config.set('voip','simulated','false')
        
        self.config.set('voip','hostid',self.voip_hostidtxt.GetValue())
        self.config.set('voip','rxboxid',self.rxboxid)
        configfile = open(self.path+'voip.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(self.path+'voip_backup.cfg')
        if self.config.get('voip','simulated') == 'false':
            self.voipsim_checkbox.SetValue(False)
        else:
            self.voipsim_checkbox.SetValue(True)
        self.voip_hostidtxt.SetValue(self.config.get('voip','hostid'))
        self.config.read(self.path+'voip.cfg')

