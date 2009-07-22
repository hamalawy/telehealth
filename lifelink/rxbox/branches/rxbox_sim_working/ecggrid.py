import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.pyplot import axes
from matplotlib.figure import Figure
from matplotlib.ticker import LinearLocator

class ecggrid:

    def __init__(self, parent):
        """ create the figure and canvas to be redrawn and initialize plotting parameters """

        self.parentPanel = parent
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.figure.subplots_adjust(bottom = 0.25)
        self.canvas = FigureCanvas(self.parentPanel, -1, self.figure)
        
        self.ymax = 1.5
        self.ymin = -0.5
        self.samples_counter = 0
        self.ysamples_counter = 0
        
        self.SetGrid()

    def SetGrid(self):
        self.xMajor = LinearLocator(numticks = 16)
        self.xMinor = LinearLocator(numticks = 76)
        self.yMajor = LinearLocator(numticks = 5)
        self.yMinor = LinearLocator(numticks = 17)
        
        self.axes.xaxis.set_major_locator(self.xMajor)
        self.axes.xaxis.set_minor_locator(self.xMinor)
        self.axes.yaxis.set_major_locator(self.yMajor)
        self.axes.yaxis.set_minor_locator(self.yMinor)
        
        self.axes.set_ylim(self.ymin,self.ymax)
        self.axes.set_xlim(0,3)
        
        # set the properties of the minor axes
        self.axes.grid(color = 'lightgrey', linewidth = 0.05, linestyle = ':', which = 'minor')
        # set the properties of the major axes
        self.axes.grid(color = 'slategrey', linewidth = 0.5, linestyle = '-', which = 'major')
        