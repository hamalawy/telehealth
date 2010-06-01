import subprocess, os
import wx
CPlotterMode = {'small':(308,162,4,2,297,156,'smallgrid.bmp'), \
                'normal':(1120,380,16,5,1080,366,'normalgrid.bmp'), \
                'extend':(924,162,13,3,897,155,'extendgrid.bmp') }

class CPlotter:
    def __init__(self, parent, panel=None, mode='normal', time=3, cont=True,data=False):
        if panel:
            self.panel = panel
        else:
            self.panel = wx.Panel(parent)
        self.mode = mode
        self.time = time
        self.cont = cont
        
        self.woffset = CPlotterMode[self.mode][2]
        self.hoffset = CPlotterMode[self.mode][3]
        self.walen = CPlotterMode[self.mode][4]
        self.halen = CPlotterMode[self.mode][5]
        self.on = False
        
    	self.hwnd = self.panel.GetHandle()
    	os.environ['SDL_WINDOWID'] = str(self.hwnd)
        self.Open()
        if not data:
            self.Plot([0]*self.walen)
        else:
            self.Plot(data)
        self.Close()
                                            
    def Open(self):
        self.Close()
        if not self.on:
            self.on = True
            self.comm = subprocess.Popen("./plotter", shell=True, stdin=subprocess.PIPE)
            self.comm.stdin.write("%d,%d,%d,%d,%s\n"%(CPlotterMode[self.mode][0],\
                                                CPlotterMode[self.mode][1],\
                                                self.woffset,\
                                                self.cont,\
                                                CPlotterMode[self.mode][6]))
                                            
    def Plot(self, data, xs=0):
        if self.on:
            inc = 1.0*self.walen/self.time/500
            for i in data:
                self.comm.stdin.write("%d,%d\n"% \
                          (self.woffset+int(xs),\
                           self.hoffset+int(round(self.halen/2-self.halen*i/0.00263/32768))))
                xs = (xs+inc)%self.walen
        return xs
        
    def Close(self):
        if self.on:
            self.comm.stdin.write("%d\n"%CPlotterMode[self.mode][0])
            self.comm.stdin.close()
            self.on = False
            
    def Calibrate(self,xls=0,xle=0,yls=0,yle=0):
        if xls==0 and xle==0 and yls ==0 and yle == 0:
            xls = self.woffset
            xle = xls + self.walen
            yls = self.hoffset
            yle = yls + self.halen
        mid = (xle+xls)/2
        for i in xrange(xls,mid):
            self.comm.stdin.write("%d,%d\n"%(i,yls))
        for i in xrange(mid,xle+1):
            self.comm.stdin.write("%d,%d\n"%(i,yle))
