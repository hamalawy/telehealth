import wx
from errorlog_cgui import ERRORLOG_config_frame
import ConfigParser

class ERRORLOG_Configurationmain(ERRORLOG_config_frame):
    def __init__(self, parent,*args, **kwds):
        ERRORLOG_config_frame.__init__(self, parent,*args, **kwds)
        self.config=ConfigParser.ConfigParser()
        self.config.read('errorlog.cfg')
        self.get_data()

    def get_data(self):
        self.errorlog_emailtxt.SetValue(self.config.get('ERRORLOG','email'))

    def set_data(self):
        self.config.set('ERRORLOG','email',self.errorlog_emailtxt.GetValue())
        configfile = open('errorlog.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read('errorlog_backup.cfg')
        self.errorlog_emailtxt.SetValue(self.config.get('ERRORLOG','email'))
        self.config.read('errorlog.cfg')
