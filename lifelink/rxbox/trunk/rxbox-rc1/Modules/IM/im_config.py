import wx
from im_cgui import IM_config_frame
import ConfigParser

class IM_Configurationmain(IM_config_frame):
    def __init__(self, parent,path,*args, **kwds):
        IM_config_frame.__init__(self, parent,*args, **kwds)
        self.path=path+'/IM/'
        self.config=ConfigParser.ConfigParser()
        self.config.read(self.path+'im.cfg')
        self.get_data()

    def get_data(self):
        if self.config.get('im','simulated') == 'false':
            self.imsim_checkbox.SetValue(False)
        else:
            self.imsim_checkbox.SetValue(True)
        self.im_domaintxt.SetValue(self.config.get('im','domain'))
        self.im_recepienttxt.SetValue(self.config.get('im','recepient'))
        self.im_passwordtxt.SetValue(self.config.get('im','passwd'))

    def set_data(self):
        if self.imsim_checkbox.GetValue() == True:
            self.config.set('im','simulated','true')
        else:
            self.config.set('im','simulated','false')
        
        self.config.set('im','domain',self.im_domaintxt.GetValue())
        self.config.set('im','recepient',self.im_recepienttxt.GetValue())
        self.config.set('im','passwd',self.im_passwordtxt.GetValue())
        self.config.set('im','rxboxid',self.rxboxid)
        configfile = open(self.path+'im.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(self.path+'im_backup.cfg')
        if self.config.get('im','simulated') == 'false':
            self.imsim_checkbox.SetValue(False)
        else:
            self.imsim_checkbox.SetValue(True)
        self.im_domaintxt.SetValue(self.config.get('im','domain'))
        self.im_recepienttxt.SetValue(self.config.get('im','recepient'))
        self.im_passwordtxt.SetValue(self.config.get('im','passwd'))
        self.config.read(self.path+'im.cfg')



