import wx
from errorlog_cgui import ERRORLOG_config_frame
import ConfigParser
import os

path=os.getcwd()
if path[len(path)-13:]=='Configuration':
    path='../'
else:
    path=os.getcwd()+'/'

class ERRORLOG_Configurationmain(ERRORLOG_config_frame):
    def __init__(self, parent,*args, **kwds):
        ERRORLOG_config_frame.__init__(self, parent,*args, **kwds)
        self.config=ConfigParser.ConfigParser()
        self.config.read(path+'rxbox.cfg')
        self.get_data()

    def get_data(self):
        self.errorlog_emailtxt.SetValue(self.config.get('ERRORLOG','email'))

    def set_data(self):
        self.config.read(path+'rxbox.cfg')
        self.config.set('ERRORLOG','email',self.errorlog_emailtxt.GetValue())
        configfile = open(path+'rxbox.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(path+'rxbox_backup.cfg')
        self.errorlog_emailtxt.SetValue(self.config.get('ERRORLOG','email'))
        self.config.read(path+'rxbox.cfg')
