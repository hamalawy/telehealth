from ECGPanel import *
from CPlotter import *

class ECGPanel2 (ECGPanel):
    def __init__(self, *args, **kwds):
        ECGPanel.__init__(self, *args, **kwds)
        
        self.frame = args[0]
        self.config = self.frame.config
        self.simulated = self.config.getboolean('ECG','simulated')
        self.port = self.config.get('ECG','port')
        self.daqdur = self.config.getint('ECG','daqdur')
        self.baud = self.config.getint('ECG','baud')
        self.ecmcheck = self.config.getint('ECG','ecmcheck')
        
        if self.simulated:
            import ECGSim as ECG
        else:
            import ECGLive as ECG
            
        self.ECGDAQ = ECG.ECG(panel=self,port=self.port,baud=self.baud,daqdur=self.daqdur,ecmcheck=self.ecmcheck,debug=True)
        self.ECGDAQ.device_ready()
        self.ECGDAQ.stop()
        
        self.plotter = False    #init for this happens at MainState since we need the frame to be shown before we can initialize this
    
    def lead12_button_clicked(self, event): # wxGlade: ECGPanel.<event_handler>
        print "Event handler `lead12_button_clicked' not implemented!"
        event.Skip()
        
    def ecmstat_reset(self):
        self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_initial.png", wx.BITMAP_TYPE_ANY))
        self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_initial.png", wx.BITMAP_TYPE_ANY))
        self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_initial.png", wx.BITMAP_TYPE_ANY))
        self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_initial.png", wx.BITMAP_TYPE_ANY))
        self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
        self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_initial.png", wx.BITMAP_TYPE_ANY))
        self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
        self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_initial.png", wx.BITMAP_TYPE_ANY))
        self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_initial.png", wx.BITMAP_TYPE_ANY))
