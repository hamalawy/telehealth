"""
Project LifeLink: ecgplotter Module

The module is a collection of two classes, Plotter and PlotThread,
which are responsible for the creation of the medical standard ECG
grid, embed in the GUI, and the actual process of plotting the ECG
samples on the grid. 

Authors: Julius Miguel J. Broma
         Arlan Roie A. Santos
         Luis G. Sison, PhD
         ------------------------------------------------
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         ------------------------------------------------
         March 2009

"""

import filters
import datetime
import threading
import time

import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import FigureManager, NavigationToolbar2Wx
from matplotlib.dates import drange
from matplotlib.figure import Figure
from matplotlib.pyplot import axes
from matplotlib.ticker import LinearLocator
import matplotlib.widgets

from pylab import date2num, num2date

ECG_BUFFER = 300            # good for 3 sec if sampling frequency is 100Hz

class Plotter():

    def __init__(self, parent):
        """ create the figure and canvas to be redrawn and initialize plotting parameters """

        self.parentPanel = parent
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.figure.subplots_adjust(bottom = 0.25)
        self.canvas = FigureCanvas(self.parentPanel, -1, self.figure)

        self.xvalues = []
        self.yvalues = []
        self.ybuffer = []
        self.timeaxis = []

        # y-axis range (in mV)
        self.ymax = 1.5
        self.ymin = -0.5

        # count the number of ECG samples received
        self.samples_counter = 0
        self.ysamples_counter = 0

        self.setTicks()
        
    def setTicks(self):
        """ set x and y axes major and minor tick locators, formatters and labels """

        # define tick locators
        self.xMajor = LinearLocator(numticks = 16)
        self.xMinor = LinearLocator(numticks = 76)
        self.yMajor = LinearLocator(numticks = 5)
        self.yMinor = LinearLocator(numticks = 17)

        self.starttime = datetime.datetime.today()
        self.starttime_tick = time.mktime(self.starttime.timetuple())
        self.currenttime = self.starttime + datetime.timedelta(seconds = 3)
        self.currenttime_tick = time.mktime(self.currenttime.timetuple())
        self.lines = self.axes.plot([self.starttime], [0], 'r-')

        # set tick locators
        self.axes.xaxis.set_major_locator(self.xMajor)
        self.axes.xaxis.set_minor_locator(self.xMinor)
        self.axes.yaxis.set_major_locator(self.yMajor)
        self.axes.yaxis.set_minor_locator(self.yMinor)

        self.axes.set_xlim((date2num(self.starttime),date2num(self.currenttime)))
        # create x-axis tick labels (seconds)
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime_tick), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')
        self.axes.set_ylim(self.ymin,self.ymax)
        # create y-axis tick labels (mV)
        self.axes.yaxis.set_ticklabels(self.createYTickLabels(self.ymin), size = 'smaller', name = 'Calibri')

        # set the properties of the minor axes
        self.axes.grid(color = 'lightgrey', linewidth = 0.05, linestyle = ':', which = 'minor')
        # set the properties of the major axes
        self.axes.grid(color = 'slategrey', linewidth = 0.5, linestyle = '-', which = 'major')

    def clearPlot(self):
        """ clears the plotter """

        # clear all the contents of the x-axis, y-axis and time-value arrays
        self.xvalues = []
        self.yvalues = []
        self.ybuffer = []
        self.timeaxis = []

        # set the position of the slider to its initial position
        self.time_scroller.reset()
        self.time_scroller.disconnect(self.time_scroller.on_changed(self.updateWindow))

        # re-initialize y-axis limits
        self.ymax = 2
        self.ymin = -4

        # re-initialize number of samples plotted
        self.samples_counter = 0
        self.ysamples_counter = 0

        # redraw the canvas to plot null data
        self.lines[0].set_data([0], [0])
        self.canvas.draw()
        self.canvas.gui_repaint()

        

    def initPlot(self):
        """ redraw the canvas to set the initial x and y axes when plotting starts """

        # set the reference time of plotting
        self.starttime = datetime.datetime.today()
        self.starttime_tick = time.mktime(self.starttime.timetuple())

        # set the current time of plotting (located at the end point of the plotter window)
        self.currenttime = self.starttime + datetime.timedelta(seconds = 3)
        self.currenttime_tick = time.mktime(self.currenttime.timetuple())

        # set the time-value array for 15-second (equivalent to a duration of 1 EDF file)
        self.endtime = self.starttime + datetime.timedelta(seconds = 15)
        self.timeaxis = num2date(drange(self.starttime, self.endtime, datetime.timedelta(milliseconds = 10)))

        # append samples of x and y-axes to be plotted
        self.xvalues.append(self.timeaxis[0])
        self.yvalues.append(self.parentPanel.myECG.ecg_leadII[0])

        self.ybuffer = self.yvalues

        # set the new data to be plotted (based from the updated values of xvalues and yvalues array)
        self.lines[0].set_data(self.xvalues, self.yvalues)

        # set the plotter window limit to 3-second
        self.axes.set_xlim((date2num(self.starttime),date2num(self.currenttime)))

        # update the x-axis ticklabels depending on the current time of plotting
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime_tick), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

        self.samples_counter += 1
        self.ysamples_counter += 1
        self.buff_counter = 1

        #for filtering
        self.startfil = 0
        self.endfil = 1500

    def plot(self):
        """ plots the ecg samples from the ecg module to the created ecg grid """
        
        print "started plotting \n"
        # continue doing this method until the length of yvalues list is DIVISIBLE by 1500 (this happens for every "15 seconds")
        while len(self.ybuffer) != 0 and len(self.ybuffer) % 1500 != 0:
            # check if  buff_counter exceeds the current length of the raw ecg samples
            try:
                # continue doing this method until 300 (ECG_BUFFER) samples are plotted
                while(self.buff_counter < ECG_BUFFER):
                    # update the value of the xvalues and yvalues array    
                    self.yvalues.append(self.parentPanel.myECG.ecg_leadII[self.ysamples_counter])
                    self.xvalues.append(self.timeaxis[self.samples_counter])
                    
                    # update the counter for number of samples plotted
                    self.samples_counter += 1
                    self.ysamples_counter += 1
                    self.buff_counter += 1
            
                self.buff_counter = 0
                # set the new data to be plotted (based from the updated values of xvalues and yvalues array)
                self.lines[0].set_data(self.xvalues, self.yvalues)
                # then plot
                self.canvas.draw()

                # after 300 samples or first 3-second worth of data, start to scroll the window
                if (self.samples_counter > 300):

                    # adjust the end point of the plotter window depending on the current time of plotting
                    self.currenttime = self.timeaxis[self.samples_counter]
                    self.currenttime_tick = time.mktime(self.currenttime.timetuple())
                    # adjust the start point of the plotter window depending on 3 seconds prior to the current time of plotting
                    self.newstarttime = self.currenttime + datetime.timedelta(seconds = -3)
                    # update the x-axis ticklabels depending on the current time of plotting
                    self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime_tick), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

                self.ybuffer = self.yvalues

            # the buff_counter exceeded the current length of the raw ecg samples
            except IndexError:

                self.ybuffer = self.yvalues
                # check if data acquisition has been stopped
                if len(self.parentPanel.acquirelist) == 0:

                    # set the time range of the plotter window
                    self.currenttime = self.timeaxis[self.samples_counter - 1]
                    self.currenttime_tick = time.mktime(self.currenttime.timetuple())
                    self.newstarttime = self.currenttime + datetime.timedelta(seconds = -3)
                    self.axes.set_xlim((date2num(self.newstarttime), date2num(self.currenttime)))
                    # update the x-axis ticklabels depending on the current time of plotting
                    self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime_tick), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

                    # set the new data to be plotted (based from the updated values of xvalues and yvalues array)
                    self.lines[0].set_data(self.xvalues, self.yvalues)
                    # then plot
                    self.canvas.draw()
                    
                    self.buff_counter = 0
                    break
                
                # if not, then the buff_counter just exceeded the current length of the dynamic list (ecg_leadII)
                # continue doing the plot method
                pass

        # this remaining block of code is called whenever the plotter has been stopped
        # set the time range of the plotter window
        self.currenttime = self.timeaxis[self.samples_counter - 1]
        self.currenttime_tick = time.mktime(self.currenttime.timetuple())
        self.newstarttime = self.currenttime + datetime.timedelta(seconds = -3)
        self.axes.set_xlim((date2num(self.newstarttime), date2num(self.currenttime)))
        # update the x-axis ticklabels depending on the current time of plotting
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime_tick), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

        #filters the data before displaying it on the GUI
        self.yvalues[len(self.yvalues)-1500:len(self.yvalues)] =(filters.hanning(filters.lowpassfilter(self.yvalues[len(self.yvalues)-1500:len(self.yvalues)])))

        # set the new data to be plotted (based from the updated values of xvalues and yvalues array)
        self.lines[0].set_data(self.xvalues, self.yvalues)
        # then plot
        self.canvas.draw()

        # clear up the buffer for checking
        self.ybuffer = [0]
        print "Plot Thread stopped"

    def createXTickLabels(self, currenttime):
        """ set the x-axis in seconds.milliseconds format relative to the start time of recording """

        # list containing the strings of x-axis labels
        ticklabels = []

        # checks the interval when this function is called relative to the reference time of plotting
        delta = currenttime - self.starttime_tick
        
        for i in range(16):
            # up to 2 significant decimal places only
            ticklabels.insert(0, '%.2f' % delta)
            # every 0.2 second interval
            delta -= 0.2
        return ticklabels


    def createYTickLabels(self, ymin):
        """ set the x-axis in voltage values of the ECG samples """

        # list containing the strings of x-axis labels
        ticklabels = []
        for i in range(5):
            ticklabels.append(ymin)
            # every 0.5 mV increment
            ymin += 0.5
        return ticklabels

    def addSlider(self, valmax):
        """ put a slider widget to navigate through the whole ECG plot """

        self.axtime = self.figure.add_axes([0.125, 0.1, 0.775, 0.03])
        # create a Slider object
        self.time_scroller = matplotlib.widgets.Slider(self.axtime, '', date2num(self.starttime), date2num(valmax), valinit = date2num(self.starttime))
        # associate the updateWindow function to the Slider
        self.time_scroller.on_changed(self.updateWindow)

    def updateWindow(self, val):
        """ redraw the canvas based from the slider position """

        # get the current value of the slider based from its position
        # then set the time range of the plotter window based from this value
        self.updatestarttime = self.time_scroller.val
        self.updatecurrenttime = date2num(num2date(self.updatestarttime) + datetime.timedelta(seconds = 3))
        self.updatecurrenttime_tick = time.mktime(num2date(self.updatecurrenttime).timetuple())
        self.axes.set_xlim((self.updatestarttime, self.updatecurrenttime))
        # update the x-axis ticklabels depending on the current time of plotting
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.updatecurrenttime_tick), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

        # update the plotting window based from the slider position
        self.canvas.draw()
        self.canvas.gui_repaint()


class PlotThread(threading.Thread):
    """a thread that is called once the ECG connections has passed
       the ECM check. starts the plotting of the ECG samples acquired
       from the module."""

    def __init__(self, parent):

        print "initializing PlotThread"
        threading.Thread.__init__(self)
        self.stopPlotThread = threading.Event()
        self.stopPlotThread.clear()

        self.parentFrame = parent
        self.check()

    def stop(self):
        """ stop the thread """

        self.stopPlotThread.set()

    def check(self):
        """ perform a preliminary step to check if the ecg_leadII list (dynamic list) has already been created by the rxsensor ECG class"""

        # check if the ECG rxsensor object has already been instantiated 
        try:
            
            # wait for the dynamic list to have an element
            while len(self.parentFrame.myECG.ecg_leadII) == 0:
                if self.stopPlotThread.isSet():
                    break
                    
            # once the dynamic list has an element, start plotting
            if not self.stopPlotThread.isSet():
                self.parentFrame.ecgplotter.initPlot()
                
        # continue doing this method until ECG rxsensor object is created
        except AttributeError:
            self.check()
            
    def run(self):
        """ start ECG plotting """

        # continue doing this method until DAQ is stopped
        while not self.stopPlotThread.isSet():

            # call the plot method to start plotting
            self.parentFrame.ecgplotter.plot()
            # check if the thread has been stopped. if yes, no need to update endtime. 
            if not self.stopPlotThread.isSet():
                self.parentFrame.ecgplotter.endtime += datetime.timedelta(seconds = 15)
                # initialize the time size (nagiiba kase after every 15 seconds. needs to be extended
                self.parentFrame.ecgplotter.timeaxis = num2date(drange(self.parentFrame.ecgplotter.starttime, self.parentFrame.ecgplotter.endtime, datetime.timedelta(milliseconds = 10)))
                
            else:
                break
            
        # add slider at the end of plotting only
        self.parentFrame.ecgplotter.addSlider(self.parentFrame.ecgplotter.endtime)
        # redraw the plotting window to make the slider appear
        self.parentFrame.ecgplotter.canvas.draw()
        self.parentFrame.ecgplotter.canvas.gui_repaint()
        

        
            


            



