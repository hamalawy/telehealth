import ConfigParser
import datetime
import traceback
import os

from States.State import *
from RxboxFrame import *
config = ConfigParser.ConfigParser()
config.read('rxbox.cfg')


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
        #stop all plotter program
        comm = subprocess.Popen("pidof plotter", shell=True, stdout=subprocess.PIPE)
        os.system('kill %s'%comm.stdout.read())

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
        stat= config.get('GENINFO', 'testscreen')
        if stat=='True':
            self._engine.change_state('TestState')
        else:
            self._engine.change_state('StandbyState')
        

    def port_priority(self,mainport,portlist):
        try:
            portlist.remove(mainport)
            portlist.insert(0,mainport)
            return portlist
        except ValueError:
            return portlist
        
        
    def stop(self):
        self._logger.info('State Machine: %s Stop'%self.__name__())
