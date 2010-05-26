import wx
import wx.lib.plot as plot
import numpy.oldnumeric as _Numeric

ECG_LEN = 1500
ECG_FS = 500

class PlotCanvas2(plot.PlotCanvas):
    def _Draw(self, graphics, xAxis = None, yAxis = None, dc = None):
        """\
        Draw objects in graphics with specified x and y axis.
        graphics- instance of PlotGraphics with list of PolyXXX objects
        xAxis - tuple with (min, max) axis range to view
        yAxis - same as xAxis
        dc - drawing context - doesn't have to be specified.    
        If it's not, the offscreen buffer is used
        """

        if dc == None:
            # sets new dc and clears it 
            #dc = wx.BufferedDC(wx.ClientDC(self.canvas), self._Buffer)
            dc = wx.BufferedPaintDC(self.canvas, self._Buffer)
            dc.Clear()
            
        dc.BeginDrawing()
        
        p1= _Numeric.array([xAxis[0], yAxis[0]])    # lower left corner user scale (xmin,ymin)
        p2= _Numeric.array([xAxis[1], yAxis[1]])     # upper right corner user scale (xmax,ymax)

        self.last_draw = (graphics, _Numeric.array(xAxis), _Numeric.array(yAxis))       # saves most recient values
        
        # TextExtents for Title and Axis Labels
        titleWH, xLabelWH, yLabelWH = self._titleLablesWH(dc, graphics)
        # TextExtents for Legend
        legendBoxWH, legendSymExt, legendTextExt = self._legendWH(dc, graphics)
        
        textSize_scale= _Numeric.array([legendBoxWH[0]+yLabelWH[1],xLabelWH[1]+titleWH[1]]) # make plot area smaller by text size
        textSize_shift= _Numeric.array([yLabelWH[1], xLabelWH[1]])          # shift plot area by this amount
        scale = (self.plotbox_size-textSize_scale) / (p2-p1)* _Numeric.array((1,-1))
        shift = -p1*scale + self.plotbox_origin + textSize_shift * _Numeric.array((1,-1))

        graphics.scaleAndShift(scale, shift)
        graphics.setPrinterScale(self.printerScale)  # thicken up lines and markers if printing
        
        graphics.draw(dc)
        dc.DestroyClippingRegion()
        dc.EndDrawing()

class Plotter():
    def __init__(self, parent, plottersize, panel=False, ecg_len=ECG_LEN, ecg_fs=ECG_FS):
        """ create the figure and canvas to be redrawn and initialize plotting parameters"""
        self.parentPanel = parent
        self.ecg_len = ecg_len
        self.ecg_fs = ecg_fs
        self.timeres = ecg_len/ecg_fs
        
        if not panel:
            self.plotpanel = wx.Panel(parent)
        else:
            self.plotpanel = panel
            
        self.plotpanel.SetBackgroundColour("white")

        if wx.VERSION[1] < 7:
            self.plotter = PlotCanvas2(self.plotpanel, size=plottersize)
        else:    
            self.plotter = PlotCanvas2(self.plotpanel)
            self.plotter.SetInitialSize(size=plottersize)

        self.xvalues = []
        self.yvalues = [0]*self.ecg_len
        
        #Settings for Plot Canvas
        self.plotter.SetEnableZoom(False)
        self.plotter.SetEnableGrid(False)
        self.plotter.SetShowScrollbars(False)
        self.plotter.SetXSpec(type='none')
        self.plotter.SetYSpec(type='none')

        for i in xrange(0,self.ecg_len):
            self.xvalues.append(float(i)/self.ecg_fs)
        data = zip(self.xvalues, self.yvalues)

        #add the data to the grid lines
        self.grided_data = self.setGrid()
        self.grided_data.append(plot.PolyLine(data, colour='red', width = 2))
        
        #set up text, axis and draw
        self.gc = plot.PlotGraphics(self.grided_data)
        #self.dc = wx.PaintDC(self.plotter.canvas)
        #self.dc = wx.ClientDC(self.plotter.canvas)
        #dc2 = wx.BufferedPaintDC(self.plotter.canvas, self.plotter._Buffer)
        self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))
        
    def setGrid(self):
        """ set x and y major and minor axes grids """
        grid = []
        
        #add major grid
        initial = 0
        for i in xrange(0,1+5*self.timeres):
            grid.append(plot.PolyLine(((initial,1.5),(initial,-1.5)),colour='grey', width=1))
            initial+=0.2
        initial = -1.5
        for i in xrange(0,7):
            grid.append(plot.PolyLine(((0,initial),(self.timeres,initial)),colour='grey', width=1))
            initial+=0.5
        #add minor grid
        initial=0
        for i in xrange(0,25*self.timeres):
            grid.append(plot.PolyLine(((initial+0.04,1.5),(initial+0.04,-1.5)),colour='grey', width=1, style=wx.DOT))
            initial+=0.04
        initial=-1.4
        for i in xrange(0,30):
            grid.append(plot.PolyLine(((0,initial),(self.timeres,initial)),colour='grey', width=1, style=wx.DOT))
            initial+=0.1
        return grid
        
    def plot(self,lead):
        self.yvalues=lead
        #add the data to the grid lines
        self.grided_data[-1] = plot.PolyLine(zip(self.xvalues, self.yvalues), colour='red', width = 2)
        
        #set up text, axis and draw
        self.plotter.Draw(self.gc, xAxis=(0,3.02),yAxis=(-1.52,1.5))
