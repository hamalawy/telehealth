import wx
from db_cgui import DB_config_frame
import ConfigParser
import os
path=os.getcwd()

if path[len(path)-13:]=='Configuration':
    path='../'
else:
    path=os.getcwd()+'/'

print os.getcwd()

class DB_Configurationmain(DB_config_frame):
    def __init__(self, parent,*args, **kwds):
        DB_config_frame.__init__(self, parent,*args, **kwds)
        self.config=ConfigParser.ConfigParser()
        self.config.read(path+'rxbox.cfg')
        self.get_data()

    def get_data(self):
        self.db_passwordtxt.SetValue(self.config.get('Database','password'))

    def set_data(self):
        self.config.read(path+'rxbox.cfg')
        self.config.set('Database','password',self.db_passwordtxt.GetValue())
        configfile = open(path+'rxbox.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(path+'rxbox_backup.cfg')
        self.db_passwordtxt.SetValue(self.config.get('Database','password'))
        self.config.read(path+'rxbox.cfg')



