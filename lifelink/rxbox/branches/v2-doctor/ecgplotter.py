""" ecgplotter module:

Create an embedded real-time ECG plotter with proper ECG grids.

revisions:
- having problems with after 15 seconds of data. not entering the loop
- defined a ybuffer variable serving as a flag. could have had a better algo. think!

- slider will be called at the end of plotting na lang
"""


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

        ### FIX THIS: Depends on the typical range of values of ECG module
        # y-axis range (in mV)
        self.ymax = 2
        self.ymin = -4
        # count the number of ECG samples received
        self.samples_counter = 0
        self.ysamples_counter = 0

        self.setTicks()
        
    def setTicks(self):
        """ set x and y axes major and minor tick locators, formatters and labels """

        # set tick locators
        self.xMajor = LinearLocator(numticks = 16)
        self.xMinor = LinearLocator(numticks = 76)
        self.yMajor = LinearLocator(numticks = 13)
        self.yMinor = LinearLocator(numticks = 61)

        self.starttime = datetime.datetime.today()
        self.currenttime = self.starttime + datetime.timedelta(seconds = 3)

        self.lines = self.axes.plot([self.starttime], [0], 'r-')

        self.axes.xaxis.set_major_locator(self.xMajor)
        self.axes.xaxis.set_minor_locator(self.xMinor)
        self.axes.yaxis.set_major_locator(self.yMajor)
        self.axes.yaxis.set_minor_locator(self.yMinor)

        self.axes.set_xlim((date2num(self.starttime),date2num(self.currenttime)))
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')
        self.axes.set_ylim(self.ymin,self.ymax)
        self.axes.yaxis.set_ticklabels(self.createYTickLabels(self.ymin), size = 'smaller', name = 'Calibri')

        self.axes.grid(color = 'lightgrey', linewidth = 0.05, linestyle = ':', which = 'minor')
        self.axes.grid(color = 'slategrey', linewidth = 0.5, linestyle = '-', which = 'major')


    def initPlot(self):
        """ redraw the canvas to set the initial x and y axes when plotting starts """
        
        self.starttime = datetime.datetime.today()
        self.currenttime = self.starttime + datetime.timedelta(seconds = 3)
        self.endtime = self.starttime + datetime.timedelta(seconds = 15)
        self.timeaxis = num2date(drange(self.starttime, self.endtime, datetime.timedelta(milliseconds = 10)))
        
        self.xvalues.append(self.timeaxis[0])
        self.yvalues.append(self.parentPanel.myECG.ecg_leadII[0])

        # for counter purposes only 
        self.ybuffer = self.yvalues

        self.lines[0].set_data(self.xvalues, self.yvalues)

        self.axes.set_xlim((date2num(self.starttime),date2num(self.currenttime)))
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

        self.samples_counter += 1
        self.ysamples_counter += 1
        
        self.buff_counter = 1

        #self.addSlider(self.endtime)
        
    def plot(self):

        print "started plotting \n"

        # continue doing this method until the length of yvalues list is DIVISIBLE by 1500 (this happens for every "15 seconds")
        print len(self.ybuffer)
        while len(self.ybuffer) != 0 and len(self.ybuffer) % 1500 != 0:
            # check if  buff_counter exceeds the current length of the raw ecg samples
            try:

                #buff_counter = 0
                while(self.buff_counter < ECG_BUFFER):
                    self.yvalues.append(self.parentPanel.myECG.ecg_leadII[self.ysamples_counter])
                    self.xvalues.append(self.timeaxis[self.samples_counter])
                    self.samples_counter += 1
                    self.ysamples_counter += 1
                    self.buff_counter += 1
                    # to synchronize with the sampling frequency
                    #time.sleep(0.01)

                #self.yvalues.extend(self.ECGbuffer)
                #self.ECGbuffer = []

                # print "new plotting values set \n"
                self.buff_counter = 0
                self.lines[0].set_data(self.xvalues, self.yvalues)
                self.canvas.draw()

                # after 300 samples or first 3-second worth of data, start to scroll the window
                if (self.samples_counter > 300):

                    self.currenttime = self.timeaxis[self.samples_counter]
                    self.newstarttime = self.currenttime + datetime.timedelta(seconds = -3)
                    self.axes.set_xlim((date2num(self.newstarttime), date2num(self.currenttime)))
                    self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

                #self.canvas.draw()
                self.ybuffer = self.yvalues
                
                

            except IndexError:

                self.ybuffer = self.yvalues
                # check if data acquisition has been stopped
                if len(self.parentPanel.acquirelist) == 0:
                    self.currenttime = self.timeaxis[self.samples_counter - 1]
                    self.newstarttime = self.currenttime + datetime.timedelta(seconds = -3)
                    self.axes.set_xlim((date2num(self.newstarttime), date2num(self.currenttime)))
                    self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

                    self.lines[0].set_data(self.xvalues, self.yvalues)
                    self.canvas.draw()
                    self.buff_counter = 0

                    break
                
                # if not, then the buff_counter exceeded the current length of the dynamic list (ecg_leadII)
                pass

        # plot remaining samples, then exit plot method
        # para san to uli?
        self.currenttime = self.timeaxis[self.samples_counter - 1]
        self.newstarttime = self.currenttime + datetime.timedelta(seconds = -3)
        self.axes.set_xlim((date2num(self.newstarttime), date2num(self.currenttime)))
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(self.currenttime), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')

        self.lines[0].set_data(self.xvalues, self.yvalues)
        self.canvas.draw()

        # clear up the buffer for checking
        self.ybuffer = [0]
        self.ysamples_counter = 0
        print "Plot Thread stopped"

    def createXTickLabels(self, currenttime):
        """ set the x-axis in seconds.milliseconds format relative to the start time of recording """
        ticklabels = []

        startInSec = str(self.starttime.second)
        startInmSec = str(self.starttime.microsecond/1000)
        start = float(startInSec + '.' + startInmSec)

        currentInSec = str(currenttime.second)
        currentInmSec = str(currenttime.microsecond/1000)
        current = float(currentInSec + '.' + currentInmSec)

        delta = current - start
        
        for i in range(16):
            ticklabels.insert(0, '%.2f' % delta)
            delta -= 0.2
        return ticklabels


    def createYTickLabels(self, ymin):
        """ set the x-axis in voltage values of the ECG samples """
        ticklabels = []
        for i in range(18):
            ticklabels.append(ymin)
            ymin += 0.5
        return ticklabels

    def addSlider(self, valmax):
        """ put a slider widget to navigate through the whole ECG plot """
        ### FIX ME: Make all time objects as parameters??? (for flexibility)
        ### Maybe the self.endtime? Kase constant lagi ang starting point
        ### added valmax as the endtime parameter
        self.axtime = self.figure.add_axes([0.125, 0.1, 0.775, 0.03])
        self.time_scroller = matplotlib.widgets.Slider(self.axtime, '', date2num(self.starttime), date2num(valmax), valinit = date2num(self.starttime))
        self.time_scroller.on_changed(self.updateWindow)

    def updateWindow(self, val):
        """ redraw the canvas based from the slider position """
        self.updatestarttime = self.time_scroller.val
        self.updatecurrenttime = date2num(num2date(self.updatestarttime) + datetime.timedelta(seconds = 3))
        self.axes.set_xlim((self.updatestarttime, self.updatecurrenttime))
        self.axes.xaxis.set_ticklabels(self.createXTickLabels(num2date(self.updatecurrenttime)), rotation = 30, ha = "right", size = 'smaller', name = 'Calibri')
        ### FIX ME: Is there a conflict here?
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

        #while not self.stopPlotThread.isSet():

        try:
            
            # wait for the dynamic list to have an element
            while len(self.parentFrame.myECG.ecg_leadII) == 0:
                if self.stopPlotThread.isSet():
                    break
                    
            # once the dynamic list has an element, start plotting
            if not self.stopPlotThread.isSet():
                self.parentFrame.ecgplotter.initPlot()

        except AttributeError:
            self.check()
            
    def run(self):
        """ start ECG plotting """
        
        while not self.stopPlotThread.isSet():
            
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
        self.parentFrame.ecgplotter.canvas.draw()
        self.parentFrame.ecgplotter.gui_repaint()
        ### FIX ME: Plot the interrupted yvalues if any

        
            


            



