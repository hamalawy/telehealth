"""Project LifeLink: RxBox GUI Simulator

Authors:    Chiong, Charles Hernan
            Cornillez, Dan Simone
            Luis Sison, PhD
            ------------------------------------------------
            Instrumentation, Robotics and Control Laboratory
            University of the Philippines - Diliman
            ------------------------------------------------
            October 2009
"""

import wx
from rxboxGUI import RxFrame
from rxboxGUI import DAQPanel
from rxboxGUI import ReferPanel
from createrecord import CreateRecordDialog
from deviceDialog import DeviceDialog
from edf import BioSignal,EDF
from wx import CallAfter
import time
import edf
import datetime
from lead12dialog import Lead12Dialog
import wx.lib.plot as plot
from ecgplotter import Plotter
from ecgplotter import extendPlotter

import Image
import tempfile
import cStringIO
from ctypes_opencv import *

import dicom
import numpy
import scipy
import threading
import rxsensor
import steth

from BP import BP
from SPO2 import SPO2
from network import ping
from network import mailcheck
from rxstatbar import RxStatusBar
from rxsensor import ECG
from scipy.misc import fromimage


class RxFrame2(RxFrame, threading.Thread):
    def __init__(self, *args, **kwds):
        RxFrame.__init__(self, *args, **kwds)
        threading.Thread.__init__(self)
        self.DAQPanel=DAQPanel2(self,self,-1)
        self.info_daq_sizer.Add(self.DAQPanel, 1, wx.ALL|wx.EXPAND,4)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        #Taskbar icon added on the status bar
        self.RxFrame_StatusBar = RxStatusBar(self)
        
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        self.RxBoxLogin("Please enter username:", "username")

        # added for camera
        self.prev_snapshot.Enable(False)
        self.next_snapshot.Enable(False)
        self.count = self.current = 0
        self.temp_bmp = []
        self.img = wx.StaticBitmap(self.snapshot_panel, -1)
        self.SetClientSize((320,240))
        self.cap = highgui.cvCreateCameraCapture(0)
        

        # added for DICOM
        self.DICOM = dicom.read_file("Photos/template.dcm")
        self.DICOM.PixelData = ''
        self.DICOM.pixel_array = []
        self.DICOM.NumberofFrames = 0
        self.DICOM.Columns = 320
        self.DICOM.Rows = 240
        self.pic = []
        self.pix = ''

        # Create a steth instance
        self.steth = steth.steth(self)
        self.steth_status = None
        self.stop_button.Enable(False)
        self.record_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.record_audio, self.record_timer)
        self.play_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.play_audio, self.play_timer)

##        self.vid_timer.Start(20)
        self.start()
       

    def RxBoxLogin(self, message, text):
        self.username = "lifelink"
        
        dlg = wx.TextEntryDialog(self, message, "RxBox - Philippine General Hospital: User Authentication", defaultValue = text)
        dlg.CenterOnScreen()        

        if dlg.ShowModal() == wx.ID_OK:
            if dlg.GetValue() == self.username:
                print "User Authenticated"
                statusECG = ECG(self).device_ready()
                print statusECG
##                statusSPO2 = SPO2(self,'COM7').POST()
##                print statusSPO2
##                statusBP = BP(self).POST()
##                print statusBP
                status ='ECG: \n'+ statusECG#+'\n\nSPO2:\n\n'+statusSPO2+\
                                 #'\n\nBP:\n\n'+statusBP
                device_ready = DeviceDialog2(status,self)
                
               
                device_ready.ShowModal()
                self.SetTitle("RxBox - Philippine General Hospital" + ' - ' + self.username)
                #del bp
                dlg.Destroy()

            else:
                print "Invalid"
                self.TextEntry("Invalid!\nPlease enter username:", "")
        else:
        # when cancel is clicked
            print 'Main Window closed'
            dlg.Destroy()
            self.Close()
        
    def CreateReferPanel(self):
        self.ReferPanel=ReferPanel(self,-1)
        self.mainhorizontal_sizer.Add(self.ReferPanel, 1, wx.ALL|wx.EXPAND,4)
        self.Layout()
        
    def onClose(self,evt):
        dlg = wx.MessageDialog(self,'Do you want to save data?','', wx.YES_NO | wx.ICON_QUESTION |wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            print "Data is saved"
            dlg.Destroy()
        
        else:
            dlg.Destroy()
            self.Destroy()
            
    def DestroyReferPanel(self):

        try:
            self.ReferPanel.Destroy()
            self.Layout()

        except AttributeError:
            pass

    def onPrevSnapshot(self, event): # wxGlade: RxFrame.<event_handler>
        self.current = self.current - 1
        
        #resize image
        img = wx.ImageFromBitmap(self.temp_bmp[self.current-1])
        img.Rescale(120, 90) # Resize image
        bitmap = wx.BitmapFromImage( img ) # Convert Image to Bitmap

        self.img.SetBitmap(bitmap)
        if self.current == 1:
            self.prev_snapshot.Enable(False)
        self.next_snapshot.Enable(True)
        print "count: ",self.count, "current: ",self.current

    def onNextSnapshot(self, event): # wxGlade: RxFrame.<event_handler>
        if self.current < self.count:
            self.current = self.current + 1
            #resize image
            img = wx.ImageFromBitmap(self.temp_bmp[self.current-1])
            img.Rescale(120, 90) # Resize image
            bitmap = wx.BitmapFromImage( img ) # Convert Image to Bitmap
            self.img.SetBitmap(bitmap)
            
        if self.current == self.count:
            self.next_snapshot.Enable(False)
        self.prev_snapshot.Enable(True)
        print "count: ",self.count, "current: ",self.current

    def onSnapshot(self, event): # wxGlade: RxFrame.<event_handler>
        self.file = 'Photos/snap'+str(self.count)+'.jpg'
        temp = 'Photos/snaptemp.jpg'
        #fd, fname = tempfile.mkstemp('.jpg')
        img = highgui.cvQueryFrame(self.cap)
        highgui.cvSaveImage(temp,img)
        self.rename_tempfile(temp,self.file)

        # added for DICOM
        self.DICOM.NumberofFrames = self.DICOM.NumberofFrames + 1
        temp = fromimage(Image.open(self.file))
        self.pic.append(temp)
        self.DICOM.pixel_array = self.pic
        self.DICOM.PixelData = self.DICOM.PixelData + temp.tostring()
        self.DICOM.save_as("Photos/new.dcm")
        print "DICOM generated"
        
        self.temp_bmp.append(wx.Image(self.file,wx.BITMAP_TYPE_JPEG).ConvertToBitmap())

        #resize image
        img = wx.ImageFromBitmap(self.temp_bmp[self.count])
        img.Rescale(120, 90) # Resize image
        bitmap = wx.BitmapFromImage( img ) # Convert Image to Bitmap
        
        self.img.SetBitmap(bitmap)
        self.count = self.count+1
        self.current = self.count
        if self.count > 1:
            self.prev_snapshot.Enable(True)
        if self.count == 1:
            self.img.SetBitmap(bitmap)
        self.next_snapshot.Enable(False)
        print "count: ",self.count, "current: ",self.current

    def run(self):
        while(True):
            self.on_vid_display()                  

    def on_vid_display(self):
        self.vidfile = 'Photos/vidtemp.jpg'
        #fd, fname = tempfile.mkstemp('.jpg')
        img = highgui.cvQueryFrame(self.cap)
        highgui.cvSaveImage(self.vidfile,img)
        #self.rename_tempfile(fname,self.vidfile)
        #del fname, fd
        self.displayImage()
        #event.RequestMore()

    def displayImage(self, offset=(0,0)):
        infile = open(self.vidfile, "rb")
        data = infile.read()
        stream = cStringIO.StringIO(data)
        infile.close()
        img = wx.ImageFromStream( stream )
        img.Rescale(160, 120) # Resize image
        bitmap = wx.BitmapFromImage( img ) # Convert Image to Bitmap
        dc = wx.ClientDC(self.video_panel)
        dc.DrawBitmap(bitmap, offset[0], offset[1])

    def rename_tempfile(self, src, dst):
        pfile = open(src,'rb')
        data = pfile.read()
        pfile.close()
        pfile = open(dst,'wb')
        pfile.write(data)
        pfile.close()

    def on_steth_record(self, event): # wxGlade: RxFrame.<event_handler>
        print "Steth Recording... "
        self.stop_button.Enable(True)
        self.play_button.Enable(False)
        self.record_button.Enable(False)
        self.steth_status = 'Record'
        self.steth.init_record()
        self.record_timer.Start(10)

    def on_steth_play(self, event): # wxGlade: RxFrame.<event_handler>
        print "Steth Sound Playing... "
        self.stop_button.Enable(True)
        self.record_button.Enable(False)
        self.play_button.Enable(False)
        self.steth_status = 'Play'
        self.steth.init_play()
        self.play_timer.Start(10)

    def on_steth_stop(self, event): # wxGlade: RxFrame.<event_handler>
        if self.steth_status == 'Record':
            self.record_timer.Stop()
            self.steth.stop_record()
        elif self.steth_status == 'Play':
            self.steth.stop_play()
        self.steth_status = None
        self.play_button.Enable(True)
        self.record_button.Enable(True)
        self.stop_button.Enable(False)

    def record_audio(self, evt):
        if self.steth_status == 'Record':
            data = self.steth.steth_stream.read(self.steth.chunk)
            self.steth.steth_record.append(data)

    def play_audio(self, evt):
        if self.steth_status == 'Play':
                if self.steth.steth_wave_data != '':
                    self.steth.steth_stream.write(self.steth.steth_wave_data)
                    self.steth.steth_wave_data = self.steth.steth_wave_file.readframes(self.steth.chunk)
                else:
                    self.on_steth_stop(None)

class DeviceDialog2(DeviceDialog):
    def __init__(self, status, *args, **kwds):
        DeviceDialog.__init__(self, *args, **kwds)
        self.status = status
        self.Device_info.SetLabel(self.status)
        
    def onDeviceCheck(self):
        statusECG = ECG().device_ready()
        statusSPO2 = SPO2(self,'COM7').POST()
        statusBP = BP(self,'COM6').POST()
        self.Device_info.SetLabel('ECG: \n'+ statusECG+'\n\nSPO2:\n\n'+statusSPO2+\
                                  '\n\nBP:\n\n'+statusBP)

class DAQPanel2(DAQPanel):

    def __init__(self, parent,*args, **kwds):
        DAQPanel.__init__(self, *args, **kwds)
        self.parentFrame = parent

        self.sizersize = self.ecg_vertical_sizer.GetSize()
        self.plotter = Plotter(self,(1080,380))
        self.plotter.plotter.SetEnableZoom(False)
        self.ecg_vertical_sizer.Add(self.plotter.plotpanel,1,\
                                    wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)

        self.timer1 = wx.Timer(self)
        self.timer2 = wx.Timer(self)
        self.timerEDF = wx.Timer(self)
        self.pressure_timer = wx.Timer(self)
        #self.timerSend = wx.Timer(self)
        #self.timerECG_refresh = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer1, self.timer1)
        self.Bind(wx.EVT_TIMER, self.get_bp, self.timer2)
        self.Bind(wx.EVT_TIMER, self.make_edf, self.timerEDF)
        self.Bind(wx.EVT_TIMER, self.pressure_update, self.pressure_timer)
        #self.Bind(wx.EVT_TIMER, self.onSend, self.timerSend)
        #self.Bind(wx.EVT_TIMER, self.displayECG, self.timerECG_refresh)
        self.parentFrame.isEstimated.Bind(wx.EVT_CHECKBOX, self.onEstimate)

        self.timerECG = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.getECGdata, self.timerECG)

        self.plotinterval = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.plotnext, self.plotinterval)

        self.ECGdata =[]
        #for i in range(0,7500):
         #   self.ECGdata.append(0)
        
        self.Biosignals = []
        self.ECGcount = 0
        
        self.patient1 = edf.Patient('1','Timothy','Cena','Ebido','Servan',\
                                    'Male','09.27.89','19')
                                    
        self.bp_infolabel.SetLabel('BP ready')
        self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
        self.spo2_infolabel.SetLabel('Pulse Ox ready')
        self.bp_isCyclic = 0
        self.ecg_counter = 0
        self.ecg_first = 0
        self.on_check = 0
        #self.getlead = ECG().ecg_lead()

        self.bp = BP(self,'COM6')
        self.bp_fresh = True
        self.spo2 = SPO2(self,'COM7')
        self.spo2_fresh = True

        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 250, size=(20, 100),style=wx.GA_VERTICAL)
        
        self.parentFrame.AgeValue.Enable(False)
        self.parentFrame.AgeCombo.Enable(False)
        self.bp_pressure_indicator.Enable(False)

        #self.SPO2_status_check()
        #self.BP_status_check()

    def onStartStop(self, event):

        self.referflag = 0
        self.panel = 0
        self.sendcount=0
        self.sendtoggled=0
        
        if self.StartStop_Label.GetLabel() == "Start":
            
            self.Call_Label.SetLabel("Call")
            self.bpvalue_label.Enable(True)
            self.bpmvalue_label.Enable(True)
            self.spo2value_label.Enable(True)
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.bpNow_Button.Enable(True)
            self.Send_Button.Enable(True)
            self.Send_Label.Enable(True)
            self.lead12_button.Enable(True)
            self.parentFrame.stop_button.Enable(False)
            self.parentFrame.play_button.Enable(False)
            self.parentFrame.record_button.Enable(False)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/StopButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Stop RxBox session")
            self.StartStop_Label.SetLabel("Stop")
            self.bp_isCyclic = 1
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")

            self.checkTelehealth()
            self.checkGmail()

            if self.bp_fresh:
                self.bp_fresh = False
            else:
                self.bp.OpenSerial()

            if self.spo2_fresh:
                self.spo2_fresh = False
            else:
                self.spo2.OpenSerial()


            self.onBPCyclic()
            self.get_bp()     
            self.timer1.Start(1000)
            self.timerEDF.Start(15000)
            self.timerECG.Start(40000)
            
            
        else:
            self.bpNow_Button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Label.SetLabel("Start")
            self.bpNow_Button.Enable(True)
            self.Call_Button.Enable(False)
            self.Send_Button.Enable(False)
            self.lead12_button.Enable(False)
            self.parentFrame.stop_button.Enable(True)
            self.parentFrame.play_button.Enable(True)
            self.parentFrame.record_button.Enable(True)
            self.bp_isCyclic = 0
            self.refreshECMbitmap()

            self.timer1.Stop()
            self.timer2.Stop()       
            self.timerEDF.Stop()    
            self.timerECG.Stop()
            self.plotinterval.Stop()
            self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
            self.spo2_infolabel.SetLabel('Pulse Ox Ready')

            self.bp.nibp.close()
            self.spo2.CloseSerial()
            
            self.SaveQuery()
            
            CallAfter(self.parentFrame.DestroyReferPanel)

    def checkTelehealth(self):

        ip ='one.telehealth.ph'
        checknet = ping(ip,self.parentFrame)
        average = checknet.start()
       
        Txtime = []
        #self.parentFrame.RxFrame_StatusBar.SetStatusText("\t\t Connecting...",1)
        print average
##   
##        if average==0:
##            self.parentFrame.RxFrame_StatusBar.neticon.SetBitmap(wx.Bitmap("Icons/telehealth_down.png",wx.BITMAP_TYPE_ANY))
##            dlg = wx.MessageDialog(self,"Reconnect?","Telehealth Server Unavailable",wx.YES_NO | wx.ICON_QUESTION)
##            if dlg.ShowModal() == wx.ID_YES:
##                #self.parentFrame.RxFrame_StatusBar.SetStatusText("\t\t Reconnecting...",1)
##                self.checkTelehealth()
##            else:
##                #self.parentFrame.RxFrame_StatusBar.SetStatusText("\t\t Not Connected!",1)
##                dlg.Destroy()
##                
##                
##                
##            #self.parentFrame.RxFrame_StatusBar.SetStatusText("\t\t Not cionnected!",1)
##           
##        else:          
##            self.parentFrame.RxFrame_StatusBar.neticon.SetBitmap(wx.Bitmap("Icons/telehealth_up.png",wx.BITMAP_TYPE_ANY))
##           # self.parentFrame.RxFrame_StatusBar.SetStatusText("\t Ave:%dms"%average,1)
##            self.parentFrame.RxFrame_StatusBar.neticon.SetToolTipString("Network Available\n%s"%checknet.info)

    def checkGmail(self):

        server = mailcheck(self.parentFrame)
        status = server.start()

##        if status==True:
##            self.parentFrame.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_up.png",wx.BITMAP_TYPE_ANY))
##
##
##        else:
##            self.parentFrame.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
##
    def refreshECMbitmap(self):
        
        self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_initial.png"))
        self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_initial.png"))
        self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png"))
        self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_initial.png"))
        self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_initial.png"))
        self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_initial.png"))
        self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png"))
        self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_initial.png"))
        self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png"))
        self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_initial.png"))

    def plotnext(self,evt):
        
        print 'ECG data counter =',self.ECGcount
       
        self.ECGcount = self.ECGcount+1
        if self.ECGcount == 1:
            self.plotter.plot(self.ECGdata[0:1500])
            print '0-3sec'
        elif self.ECGcount == 2:
            self.plotter.plot(self.ECGdata[500:2000])
            print '1-4sec'
        elif self.ECGcount == 3:
            self.plotter.plot(self.ECGdata[1000:2500])
            print '2-5sec'
        elif self.ECGcount == 4:
            self.plotter.plot(self.ECGdata[1500:3000])
            print '3-6sec'
        elif self.ECGcount == 5:
            self.plotter.plot(self.ECGdata[2000:3500])
            print '4-7sec'
        elif self.ECGcount == 6:
            self.plotter.plot(self.ECGdata[2500:4000])
            print '5-8sec'
        elif self.ECGcount == 7:
            self.plotter.plot(self.ECGdata[3000:4500])
            print '6-9sec'
        elif self.ECGcount == 8:
            self.plotter.plot(self.ECGdata[3500:5000])
            print '7-10sec'
        elif self.ECGcount == 9:
            self.plotter.plot(self.ECGdata[4000:5500])
            print '8-11sec'
        elif self.ECGcount == 10:
            self.plotter.plot(self.ECGdata[4500:6000])
            print '9-12sec'
        elif self.ECGcount == 11:
            self.plotter.plot(self.ECGdata[5000:6500])
            print '10-13sec'
        elif self.ECGcount == 12:
            self.plotter.plot(self.ECGdata[5500:7000])
            print '11-14sec'
        elif self.ECGcount == 13:
            self.plotter.plot(self.ECGdata[6000:7500])
            print '12-15sec'
        else:
            self.ECGcount = 0
            self.plotinterval.Stop()
        

    def getECGdata(self,evt):
    #def getECGdata(self,threading.Thread)
        
        
        self.myECG  = rxsensor.ECG(self)
        self.myECG.get()
        
        print len(self.myECG.ecg_leadII)
        self.ECGdata = self.myECG.ecg_leadII
        if len(self.ECGdata)<7500:
            for i in range(0,7500-len(self.ECGdata)):
                self.ECGdata.append(0)

        elif len(self.ECGdata)>7500:
            for i in range(0,len(self.ECGdata)-7500):
                self.ECGdata.pop()
        print len(self.ECGdata)

        
        self.plotinterval.Start(500)
        self.myECG.stop()

    def SaveQuery(self):
        
        dlg = wx.MessageDialog(self,'Do you want to save data?','', wx.YES_NO | wx.ICON_QUESTION |wx.CANCEL)
        dlg.ShowModal()
        
            
    def onEstimate(self,evt):
        
        self.on_check ^= 1
        
        if (self.on_check == 1):
            self.parentFrame.BirthMonth.Enable(False)
            self.parentFrame.BirthDayCombo.Enable(False)
            self.parentFrame.BirthYear.Enable(False)
            self.parentFrame.AgeValue.Enable(True)
            self.parentFrame.AgeCombo.Enable(True)
            
        if (self.on_check == 0):
            self.parentFrame.AgeValue.Enable(False)
            self.parentFrame.AgeCombo.Enable(False)
            self.parentFrame.BirthMonth.Enable(True)
            self.parentFrame.BirthDayCombo.Enable(True)
            self.parentFrame.BirthYear.Enable(True)
        
    def on_timer1(self,evt):
        
        self.spo2.get()    
        print 'Spo2 data acquired'
        
    def get_bp(self):
        self.bp_pressure_indicator.Enable(True)
        self.bpNow_Button.Enable(False)
        self.setBPmins_combobox.Enable(False)
        self.bp.send_request()
        self.pressure_timer.Start(200)

    def pressure_update(self, evt):
        print "timer for pressure"
        #self.bp.OpenSerial()
        press = self.bp.get_reply()
        self.bp.nibp.read(1)
        press = int(press[1:4])
        print "pressure: ", press, " mmHg"
        if press != 999:
            self.bpNow_Button.Enable(False)
            self.setBPmins_combobox.Enable(False)
            self.bp_pressure_indicator.SetValue(press)
            self.bp_infolabel.SetLabel(str(press)+' mmHg')                
            #self.bp_pressure_indicator.SetValue(press)
        else:
            self.bp_pressure_indicator.SetValue(0)
            self.bp_infolabel.SetLabel('BP Acquired')
            self.bp_pressure_indicator.Enable(False)
            self.bpNow_Button.Enable(True)
            self.setBPmins_combobox.Enable(True)
            self.bp.get()
            self.pressure_timer.Stop()
        
    def make_edf(self,evt):

        self.Endtime = datetime.datetime.today()
        self.Starttime = self.Endtime + datetime.timedelta(seconds = -15)
        self.strDate = self.Starttime.strftime("%d.%m.%y")
        self.strStarttime = self.Starttime.strftime("%H.%M.%S")
        self.strY2KDate = self.Starttime.strftime("%d-%b-%Y")
        
        print len(self.spo2data.spo2_list)
        print len(self.spo2data.bpm_list)
        print len(self.bpdata.systole_sim_values)
        print len(self.bpdata.diastole_sim_values)
        print len(self.ecgdata.ecg_list_scaled)
        
        nDataRecord = 3
        
        Biosignal_SPO2 = BioSignal('SpO2 finger','IR-Red sensor',\
                                '%',0,100,0,100,'None',15,self.spo2data.spo2_list)
        Biosignal_BPM = BioSignal('SpO2 finger','IR-Red sensor',\
                                'bpm',0,300,0,300,'None',15,self.spo2data.bpm_list)
        self.spo2data.spo2_list = []
        self.spo2data.bpm_list = []
        self.Biosignals.append(Biosignal_SPO2)
        self.Biosignals.append(Biosignal_BPM) 
        
        if (self.bpdata.systole_sim_values != 0):
            Biosignal_pSys = BioSignal('bpsystole', 'NIBP2010','mmHg',\
                                        0,300,0,300,'None',15,self.bpdata.systole_sim_values)
            Biosignal_pDias = BioSignal('bpdiastole','NIBP2010','mmHg',\
                                        0,300,0,300,'None',15,self.bpdata.diastole_sim_values)
            self.Biosignals.append(Biosignal_pSys)
            self.Biosignals.append(Biosignal_pDias)
            nDataRecord = 5   
            
        Biosignal_ECG = BioSignal('II','CM','mV',-43,43,0,32767,'None',7500,self.ecgdata.ecg_list_scaled)
        self.Biosignals.append(Biosignal_ECG)
        
        myedf = edf.EDF(self.patient1,self.Biosignals,self.strDate,self.strStarttime,self.strY2KDate + \
                        ': LifeLink 15 second data of CorScience modules', \
                        nDataRecord, 15)
        myedf.get(self.patient1)
        print 'EDF creation finished'

        self.Biosignals = []

    def onCall(self, event): # wxGlade: DAQPanel_Parent.<event_handler>

        if (self.Call_Label.GetLabel() == "Call") and (self.referflag == 0):   
#            CreateDialog = CreateRecordDialog2(self.parentFrame,self)
#            CreateDialog.ShowModal()
            CallAfter(self.parentFrame.CreateReferPanel)
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Requesting connection to triage...")
            self.Call_Label.SetLabel(">>  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.referflag = 1
            self.panel = 1
            
        elif (self.Call_Label.GetLabel() == "<<  ") and (self.referflag == 1):   
            self.parentFrame.ReferPanel.Show()
            self.Call_Label.SetLabel(">>  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 1
            self.parentFrame.Layout()               
        else:
            self.Call_Button.Enable(False)
            self.Call_Label.Enable(False)
            self.parentFrame.ReferPanel.Hide()
            self.Call_Label.SetLabel("<<  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 0
            self.parentFrame.Layout()
    def onSend(self, event): # wxGlade: DAQPanel.<event_handler>
        self.timerSend.Start(5000)
        self.sendcount = self.sendcount + 1
        print self.sendcount
        if (self.sendcount == 2):
            self.SendStatus(self)
         
    
    def SendStatus(self,event):
        if (self.sendtoggled == 0): 
#            RxFrame_StatusBar_fields = ["success"]
#            for i in range(len(RxFrame_StatusBar_fields)):
#                self.RxFrame_StatusBar.SetStatusText(RxFrame_StatusBar_fields[i], i)        
            print "Send to Server Successful"
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Send to Server Successful")
            self.sendtoggled = 1
        elif (self.sendtoggled == 1):  
            print "Send to Server Failed"
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Send to Server Failed")
            self.sendtoggled = 0     
        self.timerSend.Stop()    
        self.sendcount = 0

    def onBPNow(self, event): # wxGlade: MyPanel1.<event_handler>
#        self.bpNow_Button.Enable(False)
##        self.bpdata.get()
        if self.bp_fresh:
            self.bp_fresh = False
        else:
            self.bp.OpenSerial()
        self.get_bp()
        self.pressure_timer.Start(20)

    def SPO2_status_check(self):
        message1= message2 = ''
        self.spo2.POST()
        #print self.spo2.device_message
        #time.sleep(2)
        self.spo2.device_ready()
        #time.sleep(2)
        #self.spo2.patient_ready()
        message1 = 'FV:'+self.spo2.FirmwareVersion+'\n'+self.spo2.dm
        print self.spo2.patient_message
        message2 = 'SN:'+self.spo2.SerialNumber+'\n'+self.spo2.dm
        print self.spo2.device_message
        self.heartrate_infolabel.SetLabel(message1)
        self.spo2_infolabel.SetLabel(message2)

    def BP_status_check(self):
        self.bp.POST()
        #time.sleep(2)
        self.bp.device_ready()
        #time.sleep(2)
        self.bp_infolabel.SetLabel('FV:'+str(self.bp.EPROMVersion)+'\n'+self.bp.device_message)

    def onBPCyclic(self):
        reload_bp_str = self.setBPmins_combobox.GetValue()
        reload_bp = int(reload_bp_str[0:2])*60000
        self.timer2.Start(reload_bp)
        
    def updateSPO2Display(self, data):
        self.spo2value_label.SetLabel(data)
        

    def updateBPMDisplay(self, data):
        self.bpmvalue_label.SetLabel(data)
        
        
    def updateBPDisplay(self, data):
        self.bpvalue_label.SetLabel(data)
        
        
    def startSaveThread (self):
##        """ calls makeEDF.SaveThread.run() """
        event.Skip()

    def on12Lead(self, event): # wxGlade: DAQPanel.<event_handler>
        """event handler of the 12 lead button. When 12 lead button is pressed
        calls the 12 lead dialog window for plotting
        """
        #self.lead12_button.Enable(False)
        CreateDialog2 = Lead12Dialog2(self,self)
        CreateDialog2.ShowModal()

class CreateRecordDialog2(CreateRecordDialog):

    def __init__(self, parent,*args, **kwds):
        CreateRecordDialog.__init__(self, *args, **kwds)
        self.parentFrame = parent
        self.PatientFirstName_TextCtrl.SetValue(self.parentFrame.FirstNameValue.GetValue())
        self.PatientMiddleName_TextCtrl.SetValue(self.parentFrame.MiddleNameValue.GetValue())
        self.PatientLastName_TextCtrl.SetValue(self.parentFrame.LastNameValue.GetValue())
        self.PatientAddress_TextCtrl.SetValue(self.parentFrame.AddressValue.GetValue())
        self.PatientPhoneNumber_TextCtrl.SetValue(self.parentFrame.PhoneNumberValue.GetValue())
        self.PatientGender_Combo.SetValue(self.parentFrame.GenderCombo.GetValue())  
        
    def OnCreateRecord(self, event): # wxGlade: CreateRecordDialog.<event_handler>

        FirstName = self.PatientFirstName_TextCtrl.GetValue()
        MiddleName = self.PatientMiddleName_TextCtrl.GetValue()
        LastName = self.PatientLastName_TextCtrl.GetValue()
        Gender = self.PatientGender_Combo.GetValue()
        Age = self.PatientAge_TextCtrl.GetValue()
        DMY = self.PatientAgeDMY_Combo.GetValue()
        Validity = self.PatientAgeValidity_Combo.GetValue()
        Address = self.PatientAddress_TextCtrl.GetValue()
        Phone = self.PatientPhoneNumber_TextCtrl.GetValue()
        
        PatientName = FirstName + ' ' + MiddleName + ' ' + LastName
        self.parentFrame.PatientInfo_Label.SetLabel(PatientName+'\n'+ 'Gender: ' + Gender + '\nAge: ' + Age + ' ' + DMY + ' ' + Validity +\
                                               '\nAddress: ' + Address + '\nPhone: ' + Phone)

        self.Destroy()
        
class Lead12Dialog2(Lead12Dialog):
    """Creates the 12 Lead Dialog Window where the 12 leads will be plotted
    """
    
    def __init__(self, parent, *args, **kwds):
        """ initializes the placement of the plotter to the 12 lead dialog window

        Parameters
        ----------
        parent  :  the main window which calls the creation of the dialog window

        """
        
        Lead12Dialog.__init__(self, *args, **kwds)
        self.parent=parent
        sizersize = self.leadI_sizer.GetSize()
        print sizersize
        bigsizer = self.leadII_sizer.GetSize()
        print bigsizer
        self.plotter_I=Plotter(self,(308,162))
        self.plotter_II=Plotter(self,(308,162))
        self.plotter_III=Plotter(self,(308,162))
        self.plotter_aVR=Plotter(self,(308,162))
        self.plotter_aVL=Plotter(self,(308,162))
        self.plotter_aVF=Plotter(self,(308,162))
        self.plotter_V1=Plotter(self,(308,162))
        self.plotter_V2=Plotter(self,(308,162))
        self.plotter_V3=Plotter(self,(308,162))
        self.plotter_V4=Plotter(self,(308,162))
        self.plotter_V5=Plotter(self,(308,162))
        self.plotter_V6=Plotter(self,(308,162))
        self.plotter_bigII=extendPlotter(self,(1500,162)) 
        
        self.leadI_sizer.Add(self.plotter_I.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.small_leadII_sizer.Add(self.plotter_II.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.leadIII_sizer.Add(self.plotter_III.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.aVR_sizer.Add(self.plotter_aVR.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.aVL_sizer.Add(self.plotter_aVL.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.aVF_sizer.Add(self.plotter_aVF.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.V1_sizer.Add(self.plotter_V1.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.V2_sizer.Add(self.plotter_V2.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.V3_sizer.Add(self.plotter_V3.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.V4_sizer.Add(self.plotter_V4.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.V5_sizer.Add(self.plotter_V5.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.V6_sizer.Add(self.plotter_V6.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)

##        self.plotter_I.plot(self.parent.getlead[0])
##        self.plotter_II.plot(self.parent.getlead[1])
##        self.plotter_III.plot(self.parent.getlead[2])
##        self.plotter_aVR.plot(self.parent.getlead[3])
##        self.plotter_aVL.plot(self.parent.getlead[4])
##        self.plotter_aVF.plot(self.parent.getlead[5])
##        self.plotter_V1.plot(self.parent.getlead[6])
##        self.plotter_V2.plot(self.parent.getlead[7])
##        self.plotter_V3.plot(self.parent.getlead[8])
##        self.plotter_V4.plot(self.parent.getlead[9])
##        self.plotter_V5.plot(self.parent.getlead[10])
##        self.plotter_V6.plot(self.parent.getlead[11])
        


        self.plotter_I.plot(self.parent.myECG.ecg_leadI[500:2000])
        self.plotter_II.plot(self.parent.myECG.ecg_leadII[500:2000])
        self.plotter_III.plot(self.parent.myECG.ecg_leadIII[500:2000])
        self.plotter_aVR.plot(self.parent.myECG.ecg_leadaVR[500:2000])
        self.plotter_aVL.plot(self.parent.myECG.ecg_leadaVL[500:2000])
        self.plotter_aVF.plot(self.parent.myECG.ecg_leadaVF[500:2000])
        self.plotter_V1.plot(self.parent.myECG.ecg_leadV1[500:2000])
        self.plotter_V2.plot(self.parent.myECG.ecg_leadV2[500:2000])
        self.plotter_V3.plot(self.parent.myECG.ecg_leadV3[500:2000])
        self.plotter_V4.plot(self.parent.myECG.ecg_leadV4[500:2000])
        self.plotter_V5.plot(self.parent.myECG.ecg_leadV5[500:2000])
        self.plotter_V6.plot(self.parent.myECG.ecg_leadV6[500:2000])

             
        #self.plotter_bigII=extendedPlotter(self,bigsizer,self.parent.myECG.ecg_leadII[500:6500])
        self.leadII_sizer.Add(self.plotter_bigII.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        self.plotter_bigII.extendplot(self.parent.myECG.ecg_leadII[500:6500])
# end of rxboxGUI classes

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = RxFrame2(None, -1, "")
    app.SetTopWindow(rx_frame)
    rx_frame.Maximize(True)
    rx_frame.Show()
    app.MainLoop()



        
