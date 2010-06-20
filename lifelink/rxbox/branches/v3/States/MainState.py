import os, sys
sys.path.append(os.getcwd().replace('States',''))
from RxboxFrame import *
from Modules.ECG.CPlotter import *

class MainState:
    def __init__(self, engine):
        self.engine = engine
        self.app = self.engine.app
        self.config = self.engine.config
        self.frame = RxboxFrame(self.config, None, -1, "")
        self.frameOn = False
        
    def start(self):
        self.frame.Maximize(True)
        self.frame.Show()
        self.frameOn = True        
        self.frame._panel['ecg'].plotter = CPlotter(panel=self.frame._panel['ecg'].plot_panel,mode='normal',time=3,cont=True,data=[0]*1500)
        self.frame._panel['comm'].setGui('standby')
        print 'MainState Start'
        
    def stop(self):
        pass
        
    def restart(self):
        self.frame.Destroy()
        self.frameOn = False
        print 'MainState Stop'