import wx
import wx.lib.plot as plot

#ECG_LEN = 1500          # 3 seconds data
#ECG_FS = 500            # sampling rate
ECG_MAX_SAMPLE = 3000
ECG_LEN = 300
ECG_FS = 100


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
		
    def plot_main(self,lead):

        self.yvalues=lead

        self.data = ()
        for i in range(0,1500):
            a = (self.xvalues[i],self.yvalues[i]),
            self.data = self.data + a

        grided_data = self.setGrid()
        #add the data to the grid lines
        line = plot.PolyLine(self.data, colour='red', width = 2)
        grided_data.append(line)

        #set up text, axis and draw
        self.gc = plot.PlotGraphics(grided_data)
        self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))
