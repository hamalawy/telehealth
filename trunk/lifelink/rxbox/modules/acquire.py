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

        while not self.stopGetThread.isSet():

            # call get() method of the sensor
            # called every 15 seconds
            self.sensor.get()

            # checks if the BP module is active and has returned a reading
            if self.sensor.parentPanel.myBP.return_flag == 1:
                # needs 5 BioSignal objects before creating an EDF file can be started
                if (len(self.sensor.parentPanel.BioSignals) == 5):
                    # calls a seperate thread for creating and sending an EDF file
                    wx.CallAfter(self.sensor.parentPanel.startSaveThread)
                    self.sensor.parentPanel.myBP.return_flag = 0

            # if the BP module is in idle state,
            # only 3 BioSignal objects are needed before creating an EDF file can be started
            else:
                if (len(self.sensor.parentPanel.BioSignals) == 3):
                    # calls a seperate thread for creating and sending an EDF file
                    wx.CallAfter(self.sensor.parentPanel.startSaveThread) 
            
        # stop DAQ of every module
        self.sensor.stop()
        self.sensor.index = 0

        
