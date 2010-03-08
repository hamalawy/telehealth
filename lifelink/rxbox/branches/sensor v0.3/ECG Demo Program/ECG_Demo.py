#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Jan 14 15:49:01 2010

#GUI imports
import wx
from ECG_Demo_GUI import *
from ecgplotter import Plotter
from lead12dialog import Lead12Dialog
from ecgplot import extendedPlotter

#sensor imports
import ECG

import time
from edf import *
import datetime
import threading
# begin wxGlade: extracode
# end wxGlade
        
        
DAQDUR = 3

class Lead12Dialog2(Lead12Dialog):
    """Creates the 12 Lead Dialog Window where the 12 leads will be plotted"""
    
    def __init__(self, ECGdata, *args, **kwds):
        """ initializes the placement of the plotter to the 12 lead dialog window

        """
        
        Lead12Dialog.__init__(self, *args, **kwds)
        self.ECGdata = ECGdata.ECG
        
        sizersize = self.leadI_sizer.GetSize()
        bigsizer = self.leadII_sizer.GetSize()
        self.plotter_I = Plotter(self, (308, 162))
        self.plotter_II = Plotter(self, (308, 162))
        self.plotter_III = Plotter(self, (308, 162))
        self.plotter_aVR = Plotter(self, (308, 162))
        self.plotter_aVL = Plotter(self, (308, 162))
        self.plotter_aVF = Plotter(self, (308, 162))
        self.plotter_V1 = Plotter(self, (308, 162))
        self.plotter_V2 = Plotter(self, (308, 162))
        self.plotter_V3 = Plotter(self, (308, 162))
        self.plotter_V4 = Plotter(self, (308, 162))
        self.plotter_V5 = Plotter(self, (308, 162))
        self.plotter_V6 = Plotter(self, (308, 162))
        
        self.leadI_sizer.Add(self.plotter_I.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.small_leadII_sizer.Add(self.plotter_II.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.leadIII_sizer.Add(self.plotter_III.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.aVR_sizer.Add(self.plotter_aVR.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.aVL_sizer.Add(self.plotter_aVL.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.aVF_sizer.Add(self.plotter_aVF.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V1_sizer.Add(self.plotter_V1.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V2_sizer.Add(self.plotter_V2.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V3_sizer.Add(self.plotter_V3.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V4_sizer.Add(self.plotter_V4.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V5_sizer.Add(self.plotter_V5.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.V6_sizer.Add(self.plotter_V6.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)

        self.plotter_I.plot(self.ECGdata.ecg_leadI)
        self.plotter_II.plot(self.ECGdata.ecg_leadII)
        self.plotter_III.plot(self.ECGdata.ecg_leadIII)
        self.plotter_aVR.plot(self.ECGdata.ecg_leadaVR)
        self.plotter_aVL.plot(self.ECGdata.ecg_leadaVL)
        self.plotter_aVF.plot(self.ECGdata.ecg_leadaVF)
        self.plotter_V1.plot(self.ECGdata.ecg_leadV1)
        self.plotter_V2.plot(self.ECGdata.ecg_leadV2)
        self.plotter_V3.plot(self.ECGdata.ecg_leadV3)
        self.plotter_V4.plot(self.ECGdata.ecg_leadV4)
        self.plotter_V5.plot(self.ECGdata.ecg_leadV5)
        self.plotter_V6.plot(self.ECGdata.ecg_leadV6)
        
        self.plotter_bigII = extendedPlotter(self, bigsizer, self.ECGdata.ecg_leadII)
        self.leadII_sizer.Add(self.plotter_bigII, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)

class DataGather:
    #threading
    def __init__(self, parent):
        """DataGather Init"""
        self.parent = parent
        self.alive = False
        self.patient1 = Patient('1', 'Timothy', 'Cena', 'Ebido', 'Servan', \
                                            'Male', '09.27.89', '19')
        
    def ECG_Connect(self, port='/dev/ttyUSB0', daqdur=DAQDUR):
        """Connect ECG"""
        self.ECG = ECG.ECG(port=port, daqdur=daqdur)
        self.ECG.stop()
        self.ECG = ECG.ECG(port=port, daqdur=daqdur)

        if self.ECG.serialstatus:
            self.parent.ECG_Demo_statusbar.SetStatusText('Device Detected')
            return True
        else:
            self.parent.ECG_Demo_statusbar.SetStatusText('Device Not Detected')
            return False
        
    def Start_Thread(self, port='/dev/ttyUSB0', daqdur=DAQDUR):
        """Threading for obtaining ECG data"""
        self.samples = daqdur*500
        self.daqdur = daqdur
        
        if self.ECG_Connect(port=port, daqdur=daqdur):
            if not self.ECG.Init_ECG():
            	return False
            self.alive = True
            self.statECG(self.parent)
            self.get_thread = threading.Thread(target=self.Get_ECG)
            self.get_thread.start()
            return True
        else:
            print 'Cannot Connect to ECG'
            return False
        
    def Get_ECG(self):
        """Obtain ECG data for threading"""
        while self.alive:
            try:
                #Get ECG data
                self.ECG.get_ecg()
                self.ECG.ecg_lead()
                time.sleep(0.1)
                
                #Generate EDF
                self.Endtime = datetime.datetime.today()
                self.Starttime = self.Endtime + datetime.timedelta(seconds= -3)
                self.strDate = self.Starttime.strftime("%d.%m.%y")
                self.strStarttime = self.Starttime.strftime("%H.%M.%S")
                self.strY2KDate = self.Starttime.strftime("%d-%b-%Y")
                
                temp = []    
                for i in range(-self.samples,0):
                    temp.append(int(self.ECG.ecg_leadII[i]/0.00263+16384))
                    
                Biosignals = []
                Biosignal_ECG = BioSignal('II', 'CM', 'mV', -43, 43, 0, 32767, 'None', self.samples, temp)
                Biosignals.append(Biosignal_ECG)
                
                myedf = EDF(self.patient1, Biosignals, self.strDate, self.strStarttime, self.strY2KDate + \
                                ': LifeLink 15 second data of CorScience modules', \
                                1, self.daqdur)
                myedf.get(self.patient1)
                print 'EDF creation finished'
                
            except Exception, e:
                print e
        print 'STOP'
        
    def Stop_Thread(self):
        """Stop Threading for obtaining ecg data"""
        print 'Stop ECG Thread'
        if self.alive:
            self.alive = False
            time.sleep(3)
        self.ECG.stop()
        
    def statECG(self, parent):
        try:
            if self.ECG.nodeR:
                self.parent.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_connected.png"))
            else:
                self.parent.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_unconnected.png"))
            if self.ECG.nodeL:
                self.parent.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_connected.png"))
            else:
                self.parent.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_unconnected.png"))
            if self.ECG.nodeN:
                self.parent.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_connected.png"))
            else:
                self.parent.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png"))
            if self.ECG.nodeF:
                self.parent.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_connected.png"))
            else:
                self.parent.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_unconnected.png"))
            if self.ECG.nodeC1:
                self.parent.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_connected.png"))
            else:
                self.parent.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_unconnected.png"))
            if self.ECG.nodeC2:
                self.parent.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_connected.png"))
            else:
                self.parent.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_unconnected.png"))
            if self.ECG.nodeC3:
                self.parent.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_connected.png"))
            else:
                self.parent.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png"))
            if self.ECG.nodeC4:
                self.parent.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_connected.png"))
            else:
                self.parent.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_unconnected.png"))
            if self.ECG.nodeC5:
                self.parent.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_connected.png"))
            else:
                self.parent.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png"))
            if self.ECG.nodeC6:
                self.parent.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_connected.png"))
            else:
                self.parent.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_unconnected.png"))
        except Exception,e:
            print e
            
class MyFrame2(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        self.plotter = Plotter(self, (1120, 380))
        self.plotgraph_sizer.Add(self.plotter.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.port = '/dev/ttyUSB0'
        self.ECGDemo = DataGather(self)
        self.ECGDemo.ECG_Connect()
        self.ECGDemo.ECG.device_ready()
        self.ECGDemo.Stop_Thread()
        
        self.play_toggle = False
        self.timerStat = wx.Timer(self)
        self.timerPlot = wx.Timer(self)
        #self.Bind(wx.EVT_TIMER, self.statECG, self.timerStat)
        self.Bind(wx.EVT_TIMER, self.plotECG, self.timerPlot)
        self.plotter.plot(range(0,20)+[1]*1479+[1])

    def onClose(self, evt):
        """Displays a dialog prompt that asks the user to save data when user attempts to destroy the frame"""
        dlg = wx.MessageDialog(self, 'Are you sure you want to exit?', 'Exit', wx.YES_NO | wx.CANCEL)
        response = dlg.ShowModal()
        if response == wx.ID_CANCEL or response == wx.ID_NO:
            dlg.Destroy()
        else:
            dlg.Destroy()
            self.Destroy()   
            self.Stop()

    def plotECG(self, evt):
        try:
            if len(self.ECGDemo.ECG.ecg_leadII) > 4500:
                self.plotter.plot(self.ECGDemo.ECG.ecg_leadII[0:1500])
                self.ECGDemo.ECG.Pop(end=125)
        except:
            print 'No New Data'
            
    def play_button_clicked(self, event): # wxGlade: MyFrame.<event_handler>
        if self.play_toggle:
            self.play_toggle = False
            self.Stop()
            print 'ECG Plot Stop'
        else:
            if self.Start():
                self.play_toggle = True
                print 'ECG Plot Start'

    def lead12_button_clicked(self, event): # wxGlade: MyFrame.<event_handler>
        if not self.play_toggle:
            self.Start()
            time.sleep(12.1)
        self.Stop()
        CreateDialog2 = Lead12Dialog2(self.ECGDemo,self)
        CreateDialog2.ShowModal()
        time.sleep(1)
        if self.play_toggle:
            self.Start()
        
    def Stop(self):
        #self.timerStat.Stop()
        self.timerPlot.Stop()
        self.ECGDemo.Stop_Thread()
        
    def Start(self):
        if self.ECGDemo.Start_Thread(port=self.port, daqdur=DAQDUR):
            self.timerPlot.Start(250)
            #self.timerStat.Start(5000)
            return True
        else:
            return False
# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    ECG_Demo = MyFrame2(None, -1, "")
    app.SetTopWindow(ECG_Demo)
    ECG_Demo.Show()
    app.MainLoop()
