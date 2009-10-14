import threading
import wx
import wx.lib.plot as plot
from filters import besselfilter

#ECG_LEN = 300
ECG_LONGLEN = 6000
ECG_LEN = 1500          # 3 seconds data
ECG_FS = 500
#ECG_FS = 500            # sampling rate
ECG_MAX_SAMPLE = 3000

class Plotter():

    def __init__(self, parent,plottersize):
        """ create the figure and canvas to be redrawn and initialize plotting parameters"""
        self.parentPanel = parent
        self.plotpanel = wx.Panel(parent)
        self.plotpanel.SetBackgroundColour("white")

        self.xvalues = []
        self.yvalues = []
        self.ybuffer = []
        #count the number of ECG samples received
        self.ysamples_counter = 0
       # self.timerPlot = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.plotThread, self.timerPlot)

        #self.timerPlot.Start(1000)
        
        if wx.VERSION[1] < 7:
            self.plotter = plot.PlotCanvas(self.plotpanel, size=plottersize)
        else:    
            self.plotter = plot.PlotCanvas(self.plotpanel)
            self.plotter.SetInitialSize(size=plottersize)

        self.plotter.SetEnableZoom(True)
        #self.plotter.SetEnableGrid(True)
        
        self.plotter.SetXSpec(type='none')
        self.plotter.SetYSpec(type='none')

        self.xvalues = list()
        for i in range(0,ECG_LEN):
            self.xvalues.insert(len(self.xvalues),float(i)/ECG_FS)

        self.yvalues = list()
        for i in range(0,ECG_LEN):
            self.yvalues.insert(len(self.yvalues),0)

        data = ()
        for i in range(0,ECG_LEN):
            a = (self.xvalues[i],self.yvalues[i]),
            data = data + a

        grided_data = self.setGrid()
        #add the data to the grid lines
        line = plot.PolyLine(data, colour='red', width = 2)
        grided_data.append(line)

        #set up text, axis and draw
        self.gc = plot.PlotGraphics(grided_data)
        self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))             
        
    def setGrid(self):
        """ set x and y major and minor axes grids """
        majorgrid=[]
        initial = 0
        for i in range(0,16):
            majorgrid.append(((initial,1.5),(initial,-1.5)))
            initial+=0.2

        initial = -1.5
        for i in range(0,7):
            majorgrid.append(((0,initial),(3,initial)))
            initial+=0.5
        
        minorgrid=[]
        initial=0
        for i in range(0,75):
            minorgrid.append(((initial+0.04,1.5),(initial+0.04,-1.5)))
            initial+=0.04
        initial=-1.4
        for i in range(0,30):
            minorgrid.append(((0,initial),(3,initial)))
            initial+=0.1
              
        drawmajor=[]
        for i in range(len(majorgrid)):
            drawmajor.append(plot.PolyLine(majorgrid[i],colour='grey', width=1))

        drawminor=[]
        for i in range(len(minorgrid)):
            drawminor.append(plot.PolyLine(minorgrid[i],colour='grey', width=1, style=wx.DOT))   
        
        return drawminor+drawmajor

    
    

    def initPlot(self):
        """ redraw the canvas to set the initial x and y axes when plotting"""

        self.yvalues.append(self.parentPanel.myECG.ecg_leadII[0])

        self.yvalues = list()
        for i in range(0,ECG_LEN):
            self.yvalues.insert(len(self.yvalues),0)

        self.ybuffer = self.yvalues

        self.ysamples_counter += 1
        self.buff_counter = 0

##    def plot(self,lead):
##
##        while self.ysamples_counter!=0 and self.ysamples_counter%7500!=0:
##        #self.yvalues=lead
##            while (self.buff_counter < ECG_LEN):
##                    self.yvalues[self.buff_counter] = lead[self.ysamples_counter]
##                    self.ysamples_counter += 1
##                    self.buff_counter +=1
##                    print self.ysamples_counter
##            print "ito yung length"
##            print len(self.yvalues)
##            print self.ysamples_counter
##            self.buff_counter = 0
##            
##            self.data = ()
##            for i in range(0,ECG_LEN):
##                a = (self.xvalues[i],self.yvalues[i]),
##                self.data = self.data + a
##
##            grided_data = self.setGrid()
##            #add the data to the grid lines
##            line = plot.PolyLine(self.data, colour='red', width = 2)
##            grided_data.append(line)
##
##            #set up text, axis and draw
##            self.gc = plot.PlotGraphics(grided_data)
##            self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))

    #def PlotThread(self,evt):
        
        
    
    def plot(self,lead):

        self.yvalues=lead

        self.data = ()
        for i in range(0,ECG_LEN):
            a = (self.xvalues[i],self.yvalues[i]),
            self.data = self.data + a

        grided_data = self.setGrid()
        #add the data to the grid lines
        line = plot.PolyLine(self.data, colour='red', width = 2)
        grided_data.append(line)

        #set up text, axis and draw
        self.gc = plot.PlotGraphics(grided_data)
        self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))

class extendPlotter():

    def __init__(self, parent,plottersize):
        """ create the figure and canvas to be redrawn and initialize plotting parameters"""
        self.parentPanel = parent
        self.plotpanel = wx.Panel(parent)
        self.plotpanel.SetBackgroundColour("white")

        self.xvalues = []
        self.yvalues = []
        self.ybuffer = []
        #count the number of ECG samples received
        self.ysamples_counter = 0
        
        if wx.VERSION[1] < 7:
            self.plotter = plot.PlotCanvas(self.plotpanel, size=plottersize)
        else:    
            self.plotter = plot.PlotCanvas(self.plotpanel)
            self.plotter.SetInitialSize(size=plottersize)

        self.plotter.SetEnableZoom(True)
        #self.plotter.SetEnableGrid(True)
        
        self.plotter.SetXSpec(type='none')
        self.plotter.SetYSpec(type='none')

        self.xvalues = list()
        for i in range(0,ECG_LONGLEN):
            self.xvalues.insert(len(self.xvalues),float(i)/ECG_FS)

        self.yvalues = list()
        for i in range(0,ECG_LONGLEN):
            self.yvalues.insert(len(self.yvalues),0)

        data = ()
        for i in range(0,ECG_LONGLEN):
            a = (self.xvalues[i],self.yvalues[i]),
            data = data + a

        grided_data = self.setGridextend()
        #add the data to the grid lines
        line = plot.PolyLine(data, colour='red', width = 2)
        grided_data.append(line)

        #set up text, axis and draw
        self.gc = plot.PlotGraphics(grided_data)
        self.plotter.Draw(self.gc, xAxis=(0,12.02),yAxis=(-1.52,1.5)) 

    def setGridextend(self):

        majorgrid=[]
        initial = 0
        for i in range(0,60):
            majorgrid.append(((initial,1.5),(initial,-1.5)))
            initial+=0.2

        initial = -1.5
        for i in range(0,7):
            majorgrid.append(((0,initial),(12,initial)))
            initial+=0.5
        
        minorgrid=[]
        initial=0
        for i in range(0,300):
            minorgrid.append(((initial+0.04,1.5),(initial+0.04,-1.5)))
            initial+=0.04
        initial=-1.4
        for i in range(0,30):
            minorgrid.append(((0,initial),(12,initial)))
            initial+=0.1
              
        # draw points as a line
        drawmajor=[]
        for i in range(len(majorgrid)):
            drawmajor.append(plot.PolyLine(majorgrid[i],colour='grey', width=1))

        drawminor=[]
        for i in range(len(minorgrid)):
            drawminor.append(plot.PolyLine(minorgrid[i],colour='grey', width=1, style=wx.DOT))   
        
        return drawminor+drawmajor

    def initPlot(self):
        """ redraw the canvas to set the initial x and y axes when plotting"""

        self.yvalues.append(self.parentPanel.myECG.ecg_leadII[0])

        self.yvalues = list()
        for i in range(0,ECG_LONGLEN):
            self.yvalues.insert(len(self.yvalues),0)

        self.ybuffer = self.yvalues

        self.ysamples_counter += 1
        self.buff_counter = 0

    def extendplot(self,lead):

        self.yvalues=lead

        self.data = ()
        for i in range(0,ECG_LONGLEN):
            a = (self.xvalues[i],self.yvalues[i]),
            self.data = self.data + a

        grided_data = self.setGridextend()
        #add the data to the grid lines
        line = plot.PolyLine(self.data, colour='red', width = 2)
        grided_data.append(line)

        #set up text, axis and draw
        self.gc = plot.PlotGraphics(grided_data)
        self.plotter.Draw(self.gc, xAxis=(0,12.02),yAxis=(-1.52,1.5))


    

##    def plot(self):
##
##        print "started plotting. data len : ", len(self.ybuffer)
##
##        while (len(self.ybuffer)!=0):
##
##            try:
##                while(self.buff_counter < ECG_LEN):
##                    self.yvalues[self.buff_counter] = self.parentPanel.myECG.ecg_leadII[self.ysamples_counter]
##                    self.ysamples_counter += 1
##                    self.buff_counter += 1
##
##                self.buff_counter = 0
##                #self.yvalues[len(self.yvalues)-300:len(self.yvalues)]=besselfilter(self.yvalues[len(self.yvalues)-300:len(self.yvalues)])
##                print "new plotting values set \n"
##                self.data = ()
##                for i in range(0,ECG_LEN):
##                    a = (self.xvalues[i],self.yvalues[i]),
##                    self.data = self.data + a
##
##                grided_data = self.setGrid()
##                #add the data to the grid lines
##                line = plot.PolyLine(self.data, colour='red', width = 2)
##                grided_data.append(line)
##
##                #set up text, axis and draw
##                self.gc = plot.PlotGraphics(grided_data)
##                self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))
##
##            except IndexError:
##                pass
##
####        print "new plotting values set \n"
####        self.data = ()
####        for i in range(0,ECG_LEN):
####            a = (self.xvalues[i],self.yvalues[i]),
####            self.data = self.data + a
####
####        grided_data = self.setGrid()
####        #add the data to the grid lines
####        line = plot.PolyLine(self.data, colour='red', width = 2)
####        grided_data.append(line)
####
####        #set up text, axis and draw
####        self.gc = plot.PlotGraphics(grided_data)
####        self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))
##        
##        print "Plot Thread stopped"
                
class PlotThread(threading.Thread):
    """a thread that is called once the ECG connections has passed ECM check
        starts the plooting of the ECG samples acquired
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
        """ perform a preliminary step to check the entry of the ecg_lead list"""

        try:

            while len(self.parentFrame.myECG.ecg_leadII) == 0:
                if self.stopPlotThread.isSet():
                    break

            if not self.stopPlotThread.isSet():
                self.parentFrame.ecgplotter.initPlot()
                print len(self.parentFrame.ecgplotter.yvalues)

        except AttributeError:
            self.check()

    def run(self):
        """ start ECG plotting """

        while not self.stopPlotThread.isSet():

            self.parentFrame.ecgplotter.plot()

            if not self.stopPlotThread.isSet():

                pass
            else:
                break
       #self.parentFrame.ecgplotter.canvas.draw()
        #self.parentFrame.ecgplotter.gui_repaint()

                
            
            
        

    
                    

                
                
                

                    
                

            

        
