"""
Project LifeLink: makeEDF module

A threading class which is called every after 15 seconds
to convert all gathered telemetry from the biomedical modules
to an EDF file. This EDF file will be stored locally and then
transmitted to the Central side for diagnosis.

Authors: Julius Miguel J. Broma
         Arlan Roie A. Santos
         Luis G. Sison, PhD
         ------------------------------------------------
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         ------------------------------------------------
         March 2009
"""

from edf import EDF, Patient

import datetime
import threading
import TriageClient


class SaveThread (threading.Thread):
    """create EDF file from the telemetry, store locally then transmit to the Central side via the Web Services"""

    def __init__(self, parent):

        threading.Thread.__init__(self)
        self.stopSaveThread = threading.Event()
        self.stopSaveThread.clear()

        self.parentPanel = parent
        self.Endtime = datetime.datetime.today()
        self.Starttime = self.Endtime + datetime.timedelta(seconds = -15)

        # set formatting of time values
        self.strStarttime = self.Starttime.strftime("%H.%M.%S")
        self.strDate = self.Starttime.strftime("%d.%m.%y")
        self.strY2KDate = self.Starttime.strftime("%d-%b-%Y")
        self.timestamp = self.Starttime.strftime("%H%M%S")

    def stop(self):
        """stop making and transmitting EDF files"""
        
        self.stopSaveThread.set()

    def run(self):
        """create the EDF file"""

        myPatient = Patient('12345', 'Julius Miguel' , 'Juarez', 'Broma', 'Rosal', 'Male', '02.17.86', 22)
        myEDF     = EDF(myPatient, self.parentPanel.BioSignals, self.strDate, self.strStarttime, self.strY2KDate + \
                        ': LifeLink 15 second data of CorScience modules', \
                        '15', '1')
        edffile   = open('EDF Files/' + 'PatientX' + '_' + self.timestamp + '.edf', 'wb+')
        edfbin    = myEDF.get()
        edffile.write(edfbin)
        edffile.close()

        print "created edf file"

        # clear BioSignals
        self.parentPanel.BioSignals = []

        # check if the Refer button is disabled, meaning there is an active connection
        # sends the created EDF file to the Triage only if the Refer Button has been clicked
        if not self.parentPanel.Refer_Button.IsEnabled():
            TriageClient.Triage().sendEDF('032509', edfbin)
            print "EDF file sent\n"
   
        self.stop()
        
