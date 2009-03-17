import wx
import threading
import edf
import time

import socket


class makeEDFThr(threading.Thread):

    def __init__(self, ParentWindow, StartTime):

        threading.Thread.__init__(self)
        self.stopmakeEDFThr = threading.Event()
        self.stopmakeEDFThr.clear()

        self.ParentWindow = ParentWindow
#        self.BioSignals = BioSignals
        self.StartTime = StartTime


    def stop(self):
        self.stopmakeEDFThr.set()

    def run(self):

        while True:

            if self.stopmakeEDFThr.set():
                print 'break'
                break
#            print self.ParentWindow.BioSignals
#            print'Check if BioSignal is equal to 3'
#            if (len(self.ParentWindow.BioSignals) == 3):
            if (len(self.ParentWindow.BioSignals) == 2):
                print ' creating EDF file '
                myPatient = edf.Patient('39309', 'Julius Miguel', 'Juarez', 'Broma', 'Rosal', 'Male', '03.17.86', 22)

                myEDF = edf.EDF(myPatient, self.ParentWindow.BioSignals, time.strftime("%d.%m.%y"), self.StartTime, time.strftime("%d-%b-%Y") + \
                            '15 second data of CorScience Pulse Oximeter module', \
                            '15', '1')
        #        edffile = open('C:/Users/ARLAN ROIE SANTOS/Desktop/SPO2EDF' + str(self.ParentWindow.count) + '.edf', 'wb+')
                edffile = open('ECG_SPO2_BPM' + str(self.ParentWindow.count) + '.edf', 'wb+')
                edffile.write(myEDF.get())
                edffile.close()
                self.ParentWindow.count += 1

                self.StartTime = time.strftime("%H.%M.%S")
                self.ParentWindow.BioSignals = []

                print len(self.ParentWindow.BioSignals)
#                print 'Calling ContinueDAQ'
#                wx.CallAfter(self.ParentWindow.ContinueDAQ)
       
