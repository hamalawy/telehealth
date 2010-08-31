
      # using wxPython for plotting


      
import wx

import wx.lib.plot as plot

       
class MyFrame(wx.Frame):
    def __init__(self):
        
        self.frame1 = wx.Frame(None, title="wx.lib.plot", id=-1, size=(410, 340))
        self.panel1 = wx.Panel(self.frame1)
        self.panel1.SetBackgroundColour("yellow")
        if wx.VERSION[1] < 7:
            plotter = plot.PlotCanvas(self.panel1, size=(400, 300))
        else:
            plotter = plot.PlotCanvas(self.panel1)
            plotter.SetInitialSize(size=(400, 300))
        plotter.SetEnableZoom(True)
        data = [(1,2), (2,3), (3,5), (4,6), (5,8), (6,8), (12,10), (13,4)]
      # draw points as a line
        line = plot.PolyLine(data, colour='red', width=1)
 
      # also draw markers, default colour is black and size is 2
 
      # other shapes 'circle', 'cross', 'square', 'dot', 'plus'
        marker = plot.PolyMarker(data, marker='triangle')
  
      # set up text, axis and draw
        gc = plot.PlotGraphics([line, marker], 'Line/Marker Graph', 'x axis', 'y axis')
        plotter.Draw(gc, xAxis=(0,15), yAxis=(0,15))
  
       
 
        self.frame1.Show(True)
 
 
       
app = wx.PySimpleApp()
 
f = MyFrame()
 
app.MainLoop()
