import ConfigParser
import datetime
import traceback
import os

from States.State import *
from RxboxFrame import *

class InitState(State):
    def __init__(self, engine, *args, **kwds):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        self._logger = logging.getLogger(self.__name__())

    def __name__(self):
        return 'InitState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        ecgport=''
        spoport=''
        bpport=''
        os.system('mv rxbox.bk rxbox.cfg')
        self._config.read('rxbox.cfg')
#        try:
#            comm = subprocess.Popen("dmesg%s"%self._config.get('SPO2', 'dynamic'), shell=True, stdout=subprocess.PIPE)
#            spoport=comm.stdout.read().split('ttyUSB')[-1].strip()
#            self._logger.info('SPO2: /dev/ttyUSB%s'%spoport[0])
#            self._config.set('SPO2', 'port', '/dev/ttyUSB%s'%spoport[0])
#            spoport='/dev/ttyUSB'+spoport[0]
#        except:
#            self._logger.error(ERROR('SPO2 Dynamic Port Allocation Failed'))   

#        try:
#            comm = subprocess.Popen("dmesg%s"%self._config.get('BP', 'dynamic'), shell=True, stdout=subprocess.PIPE)
#            bpport=comm.stdout.read().split('ttyUSB')[-1].strip()
#            self._logger.info('BP: /dev/ttyUSB%s'%bpport[0])
#            self._config.set('BP', 'port', '/dev/ttyUSB%s'%bpport[0])
#            bpport='/dev/ttyUSB'+bpport[0]
#        except:
#            self._logger.error(ERROR('BP Dynamic Port Allocation Failed'))   
     
       
        self._frame = RxboxFrame(self._engine, None, -1, "")
        self._mgr = self._frame._mgr
        self._engine._frame = self._frame
        self._panel = self._frame._panel

        #initialize perspectives
        self._frame._perspectives.append(self._config.get('Perspective', 'default'))
        self._frame._perspectives.append(self._config.get('Perspective', 'defaultrefer'))
        try:
            self._mgr.LoadPerspective(self._config.get('Perspective', 'onoff'))
            self._logger.error('Load Perspective')
        except:
            self._logger.error(ERROR('Failed to load perspective'))

        #initialize window

        self._frame.Maximize(True)
        self._frame.Show()
        
#        try:
#            ecgport = self._panel['ecg'].get_port()
#            if ecgport:
#                self._logger.info('ECG: %s'%ecgport)
#                self._config.set('ECG', 'port', '%s'%ecgport)
#                self._config.write(open('rxbox.cfg', 'w'))
#                self._config.read('rxbox.cfg')
#                self._panel['ecg'].load_config()
#            else: self._logger.error(ERROR('ECG Dynamic Port Allocation Failed'))
#        except:
#            self._config.set('ECG', 'port', '%s'%ecgport)
#            self._config.write(open('rxbox.cfg', 'w'))
#            self._logger.error(ERROR('ECG Dynamic Port Allocation Failed'))

#        ports=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2']
#        port2check=self.port_priority(spoport,ports)
#        print port2check
#        spo2_port=self._panel['spo2'].find_port(port2check)
#        if spo2_port!=None:
#            self._config.set('SPO2', 'port', spo2_port)
#            self._config.write(open('rxbox.cfg', 'w'))
#            ports.remove(spo2_port)
#            self._panel['spo2'].minor_check()

#        port2check=self.port_priority(bpport,ports)
#        print port2check
#        bp_port=self._panel['bp'].find_port(port2check)
#        if bp_port!=None:
#            self._config.set('BP', 'port', bp_port)
 #           self._config.write(open('rxbox.cfg', 'w'))
     
            

        #init bp since bp needs to be active at init state
#        if self._panel['bp'].minor_check() == False:
#            print "BP not initialized, check connection"
        print 'Hellow'
        self._engine.change_state('TestState')

    def port_priority(self,mainport,portlist):
        try:
            portlist.remove(mainport)
            portlist.insert(0,mainport)
            return portlist
        except ValueError:
            return portlist
        
        
    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
