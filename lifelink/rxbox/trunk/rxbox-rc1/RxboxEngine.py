import wx
import sys
import traceback
import logging.handlers
import os

from multiprocessing import Process

# Update Test

def splash():
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    SPLASH_SCREEN_TIMEOUT = 3000
    splash_image = wx.Bitmap('Splash.bmp', wx.BITMAP_TYPE_BMP)
    wx.SplashScreen(splash_image, 
                    wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 
                    SPLASH_SCREEN_TIMEOUT, None, -1)
    app.MainLoop()
    print 'End Splash Screen'
    
p = Process(target=splash)
p.start()
        
import ConfigParser
import States.All as States
from Modules import rxboxdb
from Modules.Util import *

class RxboxEngine:
    """Engine/Controller class for Rxbox"""
    def run(self):
        """Run engine and start up GUI"""
        self._app = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        self._config = ConfigParser.ConfigParser()
        os.system('mv rxbox.bk rxbox.cfg')
        self._config.read('rxbox.cfg')
        
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler = logging.handlers.RotatingFileHandler(
              'Logs/rxbox.log', backupCount=5)
        handler.doRollover()
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)

        self._frame = None
        self._myedf = None
        
        self.dbuuid = ''
        self.rxboxDB = rxboxdb.rxboxDB()
        self.rxboxDB.dbconnect()
        self.rxboxDB.dbcreatetables()
        
        logging.info('RxboxEngine Start')
        self.state = None
        self.change_state('InitState')
        
        global p
        if p:
            p.terminate()
            p = False
            
        self._app.MainLoop()
        
    def change_state(self, state, *args):
        """Change state to state"""
        try:
            if self.state is not None:
                self.state.stop()
                
            if state is None:
                logging.info('RxboxEngine Exit')
                logging.shutdown()
                self._app.Exit()
                sys.exit()
            else:
                self.state = getattr(States, state)(self, *args)
                self.state.start()
        except Exception, e:
            logging.error(ERROR('Change State Error'))
            self.state = getattr(States, 'StandbyState')(self, *args)
            self.state.start()
        
if __name__ == '__main__':
    try:
        engine = RxboxEngine()
        engine.run()
    except:
        logging.error(ERROR('Engine Crashed'))
        logging.shutdown()
