import subprocess, os
import wx
CPlotterMode = {'small':(308,162,4,80,297,'smallgrid.bmp'), \
                'normal':(1120,380,16,188,1080,'normalgrid.bmp'), \
                'extend':(924,162,13,80,897,'extendgrid.bmp') }

class CPlotter:
    def __init__(self, panel=None, mode='normal', sample_time=1, plot_timelength=3, cont=True, filterOn = True, data=False):
        self.panel = panel
        self.mode = mode
        self.sample_time = sample_time
        self.plot_timelength = plot_timelength
        self.cont = cont
        self.filterOn = filterOn
        
        self.woffset = CPlotterMode[self.mode][2]
        self.center = CPlotterMode[self.mode][3]
        self.walen = CPlotterMode[self.mode][4]
        self.on = False
        self.scale = 12.0/5.0/0.00263/CPlotterMode[self.mode][1]
        
        if self.panel:
        	self.hwnd = self.panel.GetHandle()
        	os.environ['SDL_WINDOWID'] = str(self.hwnd)
        self.Open()
        if not data:
            self.Plot([0]*(self.walen*sample_time/plot_timelength))
        else:
            self.Plot(data)
        self.Close()
                                            
    def Open(self):
        self.Close()
        if not self.on:
            self.on = True
            self.comm = subprocess.Popen("./Modules/ECG/CPlotter/plotter", shell=True, stdin=subprocess.PIPE)
            self.comm.stdin.write("%d,%d,%d,%d,%d,%d,Modules/ECG/CPlotter/%s\n"%(CPlotterMode[self.mode][0],\
                                                CPlotterMode[self.mode][1],\
                                                self.woffset,self.center,\
                                                self.cont,self.filterOn,\
                                                CPlotterMode[self.mode][5]))
                                                
    def Plot(self, data, xs=0):
        if self.on:
            inc = 1.0*self.walen/self.plot_timelength*self.sample_time/len(data)
            for i in data:
                self.comm.stdin.write("%d,%d\n"% \
                          (self.woffset+int(xs),\
                           int(round((i)/self.scale))))
                xs = (xs+inc)%self.walen
        return xs
        
    def Close(self):
        if self.on:
            self.comm.stdin.write("%d\n"%CPlotterMode[self.mode][0])
            self.comm.stdin.close()
            self.on = False
            
    def Calibrate(self,xls=0,xle=0):
        if xls==0 and xle==0:
            xls = self.woffset
            xle = xls + self.walen
        for i in xrange(xls,xle+1):
            self.comm.stdin.write("%d,%d\n"%(i,0))
