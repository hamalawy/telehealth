import wx
import wx.lib.plot as plot

def Plotter(parent,sizersize,lead):
        
    if wx.VERSION[1] < 7:
        plotter = plot.PlotCanvas(parent, size=sizersize)
    else:    
        plotter = plot.PlotCanvas(parent)
        plotter.SetInitialSize(size=sizersize)
    plotter.SetEnableZoom(True)
    #self.plotter.SetEnableGrid(True)
    
    plotter.SetXSpec(type='none')
    plotter.SetYSpec(type='none')
    
    # list of (x,y) data point tuples
    
    initial_xvalues = range(0,300)
    xvalues=[]
    for i in range(len(initial_xvalues)):
        xvalues.append(initial_xvalues[i]/100.0)     
   
    data = ()
    for i in range(0,300):
        a = (xvalues[i],lead[i]),
        data = data + a
    
    ecg_ticks = createticks()
    line = plot.PolyLine(data, colour='red', width=2)
    ecg_ticks.append(line)
            
    # set up text, axis and draw
    gc = plot.PlotGraphics(ecg_ticks)
    plotter.Draw(gc, xAxis=(-0.02,3.02),yAxis=(-1.52,1.52))
    return plotter

def extendedPlotter(parent,sizersize,lead):
        
    if wx.VERSION[1] < 7:
        plotter = plot.PlotCanvas(parent, size=sizersize)
    else:    
        plotter = plot.PlotCanvas(parent)
        plotter.SetInitialSize(size=sizersize)
    plotter.SetEnableZoom(True)
    #self.plotter.SetEnableGrid(True)
    
    plotter.SetXSpec(type='none')
    plotter.SetYSpec(type='none')
    
    # list of (x,y) data point tuples
    
    xvalues = []
    for i in range(0,len(lead)):
            xvalues.append(i/500.0)
        
    print len(lead)
    data = ()
    for i in range(0,len(lead)):
        a = (xvalues[i],lead[i]),
        data = data + a
    
    ecg_ticks = createticks_extended()
    line = plot.PolyLine(data, colour='red', width=2)
    ecg_ticks.append(line)
            
    # set up text, axis and draw
    gc = plot.PlotGraphics(ecg_ticks)
    plotter.Draw(gc, xAxis=(0,12.02),yAxis=(-1.52,1.5))
    return plotter

def createticks():
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

def createticks_extended():
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



