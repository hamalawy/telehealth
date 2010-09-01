import ConfigParser
import datetime

from RxboxFrame import *
from Modules import rxboxdb

class InitState:
    def __init__(self, engine, *args):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config

    def __name__(self):
        return 'InitState'
    
    def start(self):
        print 'State Machine: InitState Start'

        try:
            #dynamic port allocation
            comm = subprocess.Popen("dmesg%s"%self._config.get('ECG', 'dynamic'), shell=True, stdout=subprocess.PIPE)
            ecgport=comm.stdout.read().split('ttyUSB')[-1].strip()
            print 'ECG: /dev/ttyUSB%s'%ecgport[0]
            self._config.set('ECG', 'port', '/dev/ttyUSB%s'%ecgport[0])
            
            comm = subprocess.Popen("dmesg%s"%self._config.get('SPO2', 'dynamic'), shell=True, stdout=subprocess.PIPE)
            spoport=comm.stdout.read().split('ttyUSB')[-1].strip()
            print 'SPO2: /dev/ttyUSB%s'%spoport[0]
            self._config.set('SPO2', 'port', '/dev/ttyUSB%s'%spoport[0])
            
            comm = subprocess.Popen("dmesg%s"%self._config.get('BP', 'dynamic'), shell=True, stdout=subprocess.PIPE)
            bpport=comm.stdout.read().split('ttyUSB')[-1].strip()
            print 'BP: /dev/ttyUSB%s'%bpport[0]
            self._config.set('BP', 'port', '/dev/ttyUSB%s'%bpport[0])

            self._config.write(open('rxbox.cfg', 'w'))
        except:
            pass
       
        self._frame = RxboxFrame(self._engine, None, -1, "")
        self._mgr = self._frame._mgr
        self._engine._frame = self._frame
        self._panel = self._frame._panel

        #initialize perspectives
        self._frame._perspectives.append(self._config.get('Perspective', 'default'))
        self._frame._perspectives.append(self._config.get('Perspective', 'defaultrefer'))
        try:
            self._mgr.LoadPerspective(self._config.get('Perspective', 'onoff'))
        except:
            print 'No Default SetUp'

        #initialize window
        self._frame.Maximize(True)
        self._frame.Show()
 
        #init bp since bp needs to be active at init state
        if self._panel['bp'].minor_check() == False:
            print "BP not initialized, check connection"
        self._engine.change_state('StandbyState')
        
    def stop(self):
        print 'State Machine: InitState Stop'
