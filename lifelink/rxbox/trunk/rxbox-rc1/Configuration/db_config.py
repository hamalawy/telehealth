import wx
from db_cgui import DB_config_frame
import ConfigParser

class DB_Configurationmain(DB_config_frame):
    def __init__(self, parent,*args, **kwds):
        DB_config_frame.__init__(self, parent,*args, **kwds)
        self.config=ConfigParser.ConfigParser()
        self.config.read('db.cfg')
        self.get_data()

    def get_data(self):
        self.db_passwordtxt.SetValue(self.config.get('DATABASE','password'))

    def set_data(self):
        self.config.set('DATABASE','password',self.db_passwordtxt.GetValue())
        configfile = open('db.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read('db_backup.cfg')
        self.db_passwordtxt.SetValue(self.config.get('DATABASE','password'))
        self.config.read('db.cfg')



