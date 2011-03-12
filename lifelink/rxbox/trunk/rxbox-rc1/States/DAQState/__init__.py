import uuid
import datetime
import wx
import traceback
import time
import subprocess

from States.State import *
from Modules.EDF import *

class DAQState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        self.dbuuid = self._engine.dbuuid
        self.rxboxDB = self._engine.rxboxDB
        
    def __name__(self):
        return 'DAQState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        
        #record the session
        self.dbuuid = str(uuid.uuid1())
        self._logger.info('Session uuid = %s'%self.dbuuid)
        self.rxboxDB.dbinsert('sessions', 'uuid', self.dbuuid)
        self.rxboxDB.dbupdate('sessions', 'starttime', str(datetime.datetime.today()), 'uuid', self.dbuuid)

        #update the gui
        self._panel['comm'].setGui('lock')
        wx.Yield()
        
        #start daq for each module
        self._panel['ecg'].Start()
        self._panel['spo2'].Start()
        self._panel['comm'].setGui('acquire')
        [self._panel[i].setGui('unlock') for i in ['ecg', 'bp', 'spo2']]

    def stop(self):
        #process bar
        dlg = wx.ProgressDialog("Stopping DAQ Session",
                       "Stopping DAQ Session... Please Wait...",
                       maximum = 8,
                       parent=self._frame,
                       style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                        )
        try:
            #stop the modules
            dlg.Update(1,"Stopping ECG")
            self._panel['ecg'].Stop()
            dlg.Update(2,"Stopping SPO2")
            self._panel['spo2'].Stop()
            dlg.Update(3,"Stopping BP")
            self._panel['bp'].Stop()
            dlg.Update(4,"Generating EDF")
            self.make_edf()
            dlg.Update(6,"Saving to Database")
            #no yet implemented
            #reset the gui
            dlg.Update(7,"Updating")
        except:
            ERROR(comment='DAQ Stop ERROR',logger=self._logger,frame=self._frame)
            
        self._panel['ecg'].ecm_statreset()
        self._panel['comm'].setGui('standby')
        [self._panel[i].setGui('lock') for i in ['ecg', 'bp', 'spo2']]
        dlg.Update(8,"Done")
        dlg.Destroy()
        self._logger.info('State Machine: %s Stop'%self.__name__())
                
    def make_edf(self):
        try:
            self._logger.info('Generate EDF Start')
            patientpanel = self._panel['patientinfo']
            bday = '.'.join([str(patientpanel.BirthMonth.GetSelection() + 1), str(patientpanel.BirthDayCombo.GetSelection() + 1), patientpanel.BirthYear.GetValue()[-2:]])
            if bday[-1] == '.': bday = ''
            patient = Patient('1', str(patientpanel.FirstNameValue.GetValue()), str(patientpanel.MiddleNameValue.GetValue()), str(patientpanel.LastNameValue.GetValue()), '', str(patientpanel.GenderCombo.GetValue()), str(bday), 20)
            
            Endtime = datetime.datetime.today()
            Starttime = Endtime + datetime.timedelta(seconds= -15)
            strDate = Starttime.strftime("%d.%m.%y")
            strStarttime = Starttime.strftime("%H.%M.%S")
            strY2KDate = Starttime.strftime("%d-%b-%Y")
            Biosignal = []
            nDataRecord = 0
            
            Biosignal.append(BioSignal('SpO2 finger', 'IR-Red sensor', \
                                    '%', 0, 100, 0, 100, 'None', 15,self._panel['spo2'].spo2data.spo2_list))
            Biosignal.append(BioSignal('SpO2 finger', 'IR-Red sensor', \
                                    'bpm', 0, 300, 0, 300, 'None', 15, self._panel['spo2'].spo2data.bpm_list))
            Biosignal.append(BioSignal('bpsystole', 'NIBP2010', 'mmHg', \
                                            0, 300, 0, 300, 'None', 15, self._panel['bp'].bp.sys_list))
            Biosignal.append(BioSignal('bpdiastole', 'NIBP2010', 'mmHg', \
                                            0, 300, 0, 300, 'None', 15, self._panel['bp'].bp.dias_list))
            #ecg = [int(round(i + 16384)) for i in besselfilter(self._panel['ecg'].ECGData.ecg_lead['II'], ft=500)] 
            comm = subprocess.Popen("./Modules/ECG/FIRfilter/filter", shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            comm.stdin.write(self._panel['ecg'].ECGData.ecg_lead['II'].__str__()[1:-1]+',*')
            scale = 1.0*self._panel['ecg'].scale[0]/self._panel['ecg'].scale[1]
            ecg = [int(round(float(i)*scale)) for i in comm.stdout.read()[:-1].split(',')]

            Biosignal.append(BioSignal('II', 'CM', 'mV', -43, 43, 0, 32767, 'None', len(ecg), ecg))
            
            nDataRecord = 5
            
            myedf = EDF(patient, Biosignal, strDate, strStarttime, strY2KDate + ': LifeLink 15 second data of CorScience modules', nDataRecord, 15)
            myedf.get(patient)

            self._engine._myedf = myedf
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'EDF creation finished')
            #self.EDFtoDB(myedf)
            self._logger.info('Generate EDF Done')
        except:
            ERROR(comment='EDF Generation Failed',logger=self._logger,frame=self._frame)

    def EDFtoDB(self, myedf):
        """Stores newly created EDF file to the rxbox database"""
        edf_inst = EDF_File(myedf.edfilename)# edf file input
        parsededf = edf_inst.parseDataRecords()
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'edf', myedf.edfilename[4:-4], parsededf)
