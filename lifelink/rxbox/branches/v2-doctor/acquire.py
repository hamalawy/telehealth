"""
Project LifeLink: acquire module

A threading class which initiates the communication between the
software GUI and the biomedical modules. Calls the get() method
of each of the instantiated class in the rxsensor module. After
15 seconds, it starts another thread to create an EDF file from
the acquired samples.

Authors: Julius Miguel J. Broma
         Arlan Roie A. Santos
         Luis G. Sison, PhD
         ------------------------------------------------
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         ------------------------------------------------
         March 2009
"""

import threading
import wx

class GetThread(threading.Thread):

    def __init__(self, sensor):
        """ initialize thread """
        # sensor is an rxsensor object

        threading.Thread.__init__(self)
        self.stopGetThread = threading.Event()
        self.stopGetThread.clear()

        self.sensor = sensor

    def stop(self):
        """ stop the thread """

        self.stopGetThread.set()

    def run(self):
        """ start data acquisition """
        print 'running:', self.sensor, 'thread'

        while not self.stopGetThread.isSet():

            # call get() method of the sensor
            # called every 15 seconds
            self.sensor.get()

            # needs 5 BioSignals before starting to create an EDF file
            #print self.sensor, ": returned BioSignal"
            #if (len(self.sensor.parentPanel.BioSignals) == 5):
                #wx.CallAfter(self.sensor.parentPanel.startSaveThread)
            
        ## FIX ME: call stop() method of the sensor here
        #self.sensor.stop()
        self.sensor.index = 0

        
