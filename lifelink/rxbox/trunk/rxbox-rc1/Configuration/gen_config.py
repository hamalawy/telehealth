import wx
from gen_cgui import Geninfo_config_frame
import ConfigParser
import os
path=os.getcwd()

if path[len(path)-13:]=='Configuration':
    path='../'
else:
    path=os.getcwd()+'/'


class Geninfo_Configurationmain(Geninfo_config_frame):
    def __init__(self, parent,*args, **kwds):
        Geninfo_config_frame.__init__(self, parent,*args, **kwds)
        self.config=ConfigParser.ConfigParser()
        self.config.read(path+'rxbox.cfg')
        self.get_data()

    def get_data(self):
        self.gen_versiontxt.SetValue(self.config.get('GENINFO','version'))
        self.gen_modeltxt.SetValue(self.config.get('GENINFO','model'))
        self.gen_IDtxt.SetValue(self.config.get('GENINFO','rxboxid'))
        if self.config.get('GENINFO','testscreen') == 'False':
            self.startup_checkbox.SetValue(False)
        else:
            self.startup_checkbox.SetValue(True)

    def set_data(self):
        self.config.read(path+'rxbox.cfg')
        self.config.set('GENINFO','version',self.gen_versiontxt.GetValue())
        self.config.set('GENINFO','model',self.gen_modeltxt.GetValue())
        self.config.set('GENINFO','rxboxid',self.gen_IDtxt.GetValue())
        self.rxboxid=self.gen_IDtxt.GetValue()
        if self.startup_checkbox.GetValue():
            self.config.set('GENINFO','testscreen','True')
            print self.startup_checkbox.GetValue()
        else:
            self.config.set('GENINFO','testscreen','False')
        self.config.write(open(path+'rxbox.cfg', 'w'))

    def default_data(self):
        self.config.read(path+'rxbox_backup.cfg')
        self.gen_versiontxt.SetValue(self.config.get('GENINFO','version'))
        self.gen_modeltxt.SetValue(self.config.get('GENINFO','model'))
        self.gen_IDtxt.SetValue(self.config.get('GENINFO','rxboxid'))
        if self.config.get('GENINFO','testscreen') == 'False':
            self.startup_checkbox.SetValue(False)
        else:
            self.startup_checkbox.SetValue(True)
        self.config.read(path+'rxbox.cfg')
