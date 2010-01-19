"""Project LifeLink: RxBox GUI Simulator

Authors:    Chiong, Charles Hernan
            Cornillez, Dan Simone
            Timothy John Ebido
            Thomas Rodinel Soler
            Luis Sison, PhD
            ------------------------------------------------
            Instrumentation, Robotics and Control Laboratory
            University of the Philippines - Diliman
            ------------------------------------------------
            September 2009
"""

"""
This simulator follows the following script when PLAY button is pressed:
- BP, HR, and SpO2 panels activate
- ECM Electrodes Blink for 5 seconds (checking all electrodes)
- ECM electrodes turn green in sequence until all electrodes turn green(i.e. ECM check passed)
- ECG plots on the grid
"""


import wx

from GUIrxframe import RxFrame
from GUIdaqpanel import DAQPanel
from GUIreferpanel import ReferPanel
from CreateRecordDialog import CreateRecordDialog
from edf import BioSignal, EDF
from wx import CallAfter
import time
import simsensors
import edf
import datetime
import ConfigParser
from lead12dialog import Lead12Dialog
import wx.lib.plot as plot
from ecglogfile import ECG
from ecgplotter import Plotter
#from ecgplot import Plotter
from ecgplot import extendedPlotter
from matplotlib import pyplot

import sys
sys.path.append('triage/')
sys.path.append('voip/')
sys.path.append('im')
import triage
import linphone
import messenger
import Image
import tempfile
import cStringIO
import wave
import pyaudio

from MySQLdb import connect
import datetime
import uuid
import rxboxdb
#import threading
#try:                   #weeeeeeeeeeeee
#    from opencv import *
#except ImportError:
#    from ctypes_opencv import *

import dicom           
from scipy.misc import fromimage #wooooooooo
# This class will implement the callback functions
# for Linphone events   

class LinphoneHandle(linphone.Linphone):
    def __init__(self):
        linphone.Linphone.__init__(self)

    def handle_incoming(self):
        print self.caller , " is calling."
        self.answer()

    def handle_terminated(self):
        print "Call ended."
        #you may put GUI codes here (callafter function maybe?)

    def handle_answered(self):
        print "Call answered"
        #you may put GUI codes here (callafter function maybe?)

    def handle_failed(self):
        print "Call failed"
        #you may put GUI codes here (callafter function maybe?)


class RxFrame2(RxFrame):
    def __init__(self, *args, **kwds):
        RxFrame.__init__(self, *args, **kwds)
        self.DAQPanel = DAQPanel2(self, self, -1)
        self.playwav = simsensors.stethplay(self)
        self.info_daq_sizer.Add(self.DAQPanel, 1, wx.ALL | wx.EXPAND, 4)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.topic = ''
        self.body = ''

        self.temp_bmp = []
        self.img = wx.StaticBitmap(self.snapshot_panel, -1)
        self.prev_snapshot.Enable(False)
        self.next_snapshot.Enable(False)
        self.imgcount = 1
        self.imgcurrent = 1
        self.SetClientSize((320,240))
        # Create a steth instance
#        self.steth = steth.steth(self)

        self.steth_status = None
        self.stop_button.Enable(False)
#        self.record_timer = wx.Timer(self)
#        self.Bind(wx.EVT_TIMER, self.record_audio, self.record_timer)
#        self.play_timer = wx.Timer(self)
#        self.Bind(wx.EVT_TIMER, self.play_audio, self.play_timer)


    def __set_properties(self):
        RxFrame.__set_properties(self)
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        
    def CreateReferPanel(self):
        """Creates the refer panel window and initializes and starts linphone process"""
        self.ReferPanel = ReferPanel(self, -1)
        self.mainhorizontal_sizer.Add(self.ReferPanel, 1, wx.ALL | wx.EXPAND, 4)
        if self.DAQPanel.config.getint('im', 'simulated') == 1:
            self.ReferPanel.IMreply_Text.Bind(wx.EVT_TEXT_ENTER, self.updateIM)
        else:
            self.ReferPanel.IMreply_Text.Bind(wx.EVT_TEXT_ENTER, self.sendMessage)        
        self.Layout()

        self.l = LinphoneHandle()
        wid = self.ReferPanel.video_panel.GetHandle()
        self.l.set_window(wid)

        self.l.spawn()
        self.l.start()

        if self.DAQPanel.config.getint('im', 'simulated') == 0:
            self.m = messenger.Messenger('1001@one.telehealth.ph', 'telehealth')
            self.m.handler_new_message = self.onMsgRcvd
            self.m.handler_sent_message = self.onMsgSent
            self.m.set_recipient('1000@one.telehealth.ph')

            self.m.connect()
            self.m.start()


    def onMsgRcvd(self, conn, msg):
        self.ReferPanel.IMtexts_Text.AppendText('DE1: ' + msg.getBody() + '\n')
       
    def onMsgSent(self, msg):
        self.ReferPanel.IMtexts_Text.AppendText('RXBOX: ' + msg + '\n')
        self.ReferPanel.IMreply_Text.Clear()

    def sendMessage(self, event):
        msg = self.ReferPanel.IMreply_Text.GetValue()
        self.m.set_recipient('1000@one.telehealth.ph')
        self.m.send_message(msg)
       
    def onClose(self, evt):
        """Displays a dialog prompt that asks the user to save data when user attempts to destroy the frame"""
        dlg = wx.MessageDialog(self, 'Do you want to save data?', 'Exit', \
                                wx.YES_NO | wx.ICON_QUESTION | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_CANCEL:
            dlg.Destroy()
        else:
            dlg.Destroy()
            self.Destroy()   
            
    def updateIM(self, evt):
        """Copy the contents of the im text input box and show it to an another text box"""

        prev = self.ReferPanel.IMreply_Text.GetValue()
        self.ReferPanel.IMtexts_Text.AppendText('RxBox: ' + prev + '\nDE: ' + prev + '\n')
        self.ReferPanel.IMreply_Text.Clear() 
        
    def DestroyReferPanel(self):
        """Destroys the refer panel and stops linphone process"""
        try:
            self.l.stop()
            self.l.join()

            self.m.stop()
            self.m.join()

            self.ReferPanel.Destroy()
            self.Layout()

        except AttributeError:
            pass
            
    def onPrevSnapshot(self, event): # wxGlade: RxFrame.<event_handler>
        self.RxFrame_StatusBar.SetStatusText("Snapshot previous button toggled...")
        print "Snapshot previous button toggled..."
        self.imgcurrent = self.imgcurrent - 1
        #resize image
        img = wx.ImageFromBitmap(self.temp_bmp[self.imgcurrent - 1])
        img.Rescale(120, 90) # Resize image
        bitmap = wx.BitmapFromImage(img) # Convert Image to Bitmap

        self.img.SetBitmap(bitmap)
        if self.imgcurrent < 2:
            self.prev_snapshot.Enable(False)
        self.next_snapshot.Enable(True)
       
        print "count: ", self.imgcount, "current: ", self.imgcurrent   

    def onNextSnapshot(self, event): # wxGlade: RxFrame.<event_handler>
        self.RxFrame_StatusBar.SetStatusText("Snapshot next button toggled...")
        print "Snapshot next button toggled..."
        if self.imgcurrent < self.imgcount:
            self.imgcurrent = self.imgcurrent + 1
            #resize image
            img = wx.ImageFromBitmap(self.temp_bmp[self.imgcurrent - 1])
            img.Rescale(120, 90) # Resize image
            bitmap = wx.BitmapFromImage(img) # Convert Image to Bitmap
            self.img.SetBitmap(bitmap)
            
        if self.imgcurrent == self.imgcount:
            self.next_snapshot.Enable(False)
        self.prev_snapshot.Enable(True)
        print "count: ", self.imgcount, "current: ", self.imgcurrent

    def onSnapshot(self, event): # wxGlade: RxFrame.<event_handler>
        self.RxFrame_StatusBar.SetStatusText("Snapshot main button toggled...")
        print "Snapshot main button toggled..."
        print self.imgcount
        self.file = 'snapdemo/' + str(self.imgcount) + '.jpg'
        self.temp_bmp.append(wx.Image(self.file, wx.BITMAP_TYPE_JPEG).ConvertToBitmap())
        img = wx.ImageFromBitmap(self.temp_bmp[self.imgcount - 1])
        img.Rescale(120, 90)
        bitmap = wx.BitmapFromImage(img) # Convert Image to Bitmap
        
        self.img.SetBitmap(bitmap)
        self.imgcount = self.imgcount + 1
        self.imgcurrent = self.imgcount
        
        if self.imgcount > 1:
            self.prev_snapshot.Enable(True)
        if self.imgcount == 1:
            self.img.SetBitmap(bitmap)
        if self.imgcount == 7:
            self.imgcount = 1
            self.img.SetBitmap(bitmap)
        self.next_snapshot.Enable(False)    
        print "count: ", self.imgcount, "current: ", self.imgcurrent

    def on_vid_display(self):
        pass

    def displayImage(self, offset=(0, 0)):
        pass


    def on_steth_record(self, event): # wxGlade: RxFrame.<event_handler>
        print "Steth Recording... "
        self.RxFrame_StatusBar.SetStatusText("Steth Sound Recording...")
        self.stop_button.Enable(True)
        self.play_button.Enable(False)
        self.record_button.Enable(False)
        self.steth_status = 'Record'

    def on_steth_play(self, event): # wxGlade: RxFrame.<event_handler>
        print "Steth Sound Playing... "
        self.RxFrame_StatusBar.SetStatusText("Steth Sound Playing...")
        self.stop_button.Enable(True)
        self.record_button.Enable(False)
        self.play_button.Enable(False)
        self.steth_status = 'Play'
        self.filename_hr = self.DAQPanel.config.get('spo2', 'hr_sim_type')
        if self.filename_hr == 'High':
            self.openwav = 'stethdemo/Heartbeat100bpm.wav'
        elif self.filename_hr == 'Low':
            self.openwav = 'stethdemo/Heartbeat60bpm.wav'
        else :
            self.openwav = 'stethdemo/Heartbeat80bpm.wav'
        self.playwav.start()
        self.playwav.stop()    
        self.playwav.join()         
        
    def on_steth_stop(self, event): # wxGlade: RxFrame.<event_handler>
    
        self.play_button.Enable(True)
        self.record_button.Enable(True)
        self.stop_button.Enable(False)

        if self.steth_status == 'Record':
            self.RxFrame_StatusBar.SetStatusText("Stopping Steth Record...")
        elif self.steth_status == 'Play':
            self.RxFrame_StatusBar.SetStatusText("Stopping Steth Play...")
            self.playwav.stop()    
            self.playwav.join()    
        self.steth_status = 'Stop'
        
    def record_audio(self, evt):
        pass

class DAQPanel2(DAQPanel):

    def __init__(self, parent, *args, **kwds):
        DAQPanel.__init__(self, *args, **kwds)
        self.RxFrame = parent
        self.rxboxDB = rxboxdb.rxboxDB()
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel, -1, 110, \
                                                size=(20, 120), style=wx.GA_VERTICAL)    
#        self.ecg_vertical_sizer = self.RxFrame.ecg_vertical_sizer     

        self.init_ecglive()
        self.init_daqtimers()
        self.init_config()
        self.init_simsensors()

        self.RxFrame.BirthMonth.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.RxFrame.BirthDayCombo.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.RxFrame.BirthYear.Bind(wx.EVT_TEXT, self.birthday_update)    
        
        if self.config.get('ecg', 'sim_type') != 'Normal':
            self.ecgdata.ecg_list = self.ecgdata.get_plot()
        
        self.patient1 = edf.Patient('1', 'Timothy', 'Cena', 'Ebido', 'Servan', \
                                    'Male', '09.27.89', '19')
        self.rxboxDB.dbconnect()
        self.rxboxDB.dbcreatetables()                            
        self.bp_infolabel.SetLabel('BP ready')
        self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
        self.spo2_infolabel.SetLabel('Pulse Ox ready')
        self.bp_isCyclic = 0
        self.ecg_counter = 0
        self.on_send = 0
        self.with_patient_info = 0
        self.ClearPatient()
        
    def init_daqtimers(self):
        """Initializes various timers for DAQ Panel of RxBox"""
        
        self.timer_spo2 = wx.Timer(self)
        self.timer_bp = wx.Timer(self)
        self.timerEDF = wx.Timer(self)
        self.pressure_timer = wx.Timer(self)
        self.timerSend = wx.Timer(self)
        self.timerECG_refresh = wx.Timer(self)
        self.timerECGNodeCheck = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer_spo2, self.timer_spo2)
        self.Bind(wx.EVT_TIMER, self.on_timer_bp, self.timer_bp)
        self.Bind(wx.EVT_TIMER, self.make_edf, self.timerEDF)
        self.Bind(wx.EVT_TIMER, self.pressure_update, self.pressure_timer)
        self.Bind(wx.EVT_TIMER, self.onSend, self.timerSend)
        self.Bind(wx.EVT_TIMER, self.displayECG, self.timerECG_refresh)
        self.Bind(wx.EVT_TIMER, self.onECGNodeCheck, self.timerECGNodeCheck)
        
    def init_config(self):
        """Initializes configuration file for Rxbox"""

        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')
        
    def init_ecglive(self):
        """Initializes ecgplotter GUI"""
        
        self.sizersize = self.ecg_vertical_sizer.GetSize()
        self.plotter = Plotter(self, (1120, 380))
        self.ecg_vertical_sizer.Add(self.plotter.plotpanel, 1, \
                                    wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.getlead = ECG().ecg_lead() 
        self.ECGplotcounter = 0
        
    def init_simsensors(self):
        """Initializes simsensors"""
        
        self.Biosignals = []
        
        self.spo2data = simsensors.Spo2sim(self)
        self.bpdata = simsensors.BpSim(self)
        self.ecgdata = simsensors.EcgSim(self)

    def onStartStop(self, event):

        self.referflag = 0
        self.panel = 0
        self.sendcount = 0
        self.sendtoggled = 0
        self.nodetimer = 0
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
        if self.StartStop_Label.GetLabel() == "Start":
            #creates universally unique identifier and add it to database as primary key
            self.dbuuid = ""
            self.dbuuid = str(uuid.uuid1())
            print "uuid = ", self.dbuuid
            self.rxboxDB.dbinsert('sessions','uuid',self.dbuuid)
            #set start time in table: sessioninfo
            dbstart = str(datetime.datetime.today())
            self.rxboxDB.dbupdate('sessions','starttime',dbstart,'uuid',self.dbuuid)
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','BP Ready')
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Pulse Ox Ready')
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Pulse Ox Ready')       
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
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/StopButton.png", wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Stop RxBox session")
            self.StartStop_Label.SetLabel("Stop")
            self.bp_isCyclic = 1
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Acquiring biomedical readings...')
            self.spo2data.get()
            self.bpdata.get()
            self.onECGNodeCheck(self)
   
            self.timer_spo2.Start(1000)
            self.timerEDF.Start(15000)
            
        else:

            self.RxFrame.RxFrame_StatusBar.SetStatusText("RxBox Ready")
            self.bpNow_Button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png", wx.BITMAP_TYPE_ANY))
            self.StartStop_Label.SetLabel("Start")
            self.bpNow_Button.Enable(True)
            self.Call_Button.Enable(False)
            self.Send_Button.Enable(False)
            self.lead12_button.Enable(False)
            self.bp_isCyclic = 0
            self.referflag = 0
            self.panel = 0
            self.timer_spo2.Stop()
            self.timer_bp.Stop()       
            self.timerEDF.Stop()    
            self.timerSend.Stop()  
            self.timerECG_refresh.Stop()
            self.timerECGNodeCheck.Stop() 
            self.Call_Label.SetLabel("Call")          
            self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
            self.spo2_infolabel.SetLabel('Pulse Ox Ready')
            self.RxFrame.DAQPanel.RemarkValueDaq.SetValue('')            
            self.SaveQuery()
            self.ClearPatient()
            self.with_patient_info = 0
            print 'stopping...'
            CallAfter(self.RxFrame.DestroyReferPanel)

    def SaveQuery(self):
        """Displays a dialog box that prompts the user to save data"""
        
        dlg = wx.MessageDialog(self, 'Do you want to save data?', '', \
                                wx.YES_NO | wx.ICON_QUESTION | wx.CANCEL)
        dlg.ShowModal()
        CallAfter(self.RxFrame.DestroyReferPanel)
        
    def ClearPatient(self):
        """Clear patient information panel"""
        
        self.RxFrame.FirstNameValue.SetValue("")
        self.RxFrame.MiddleNameValue.SetValue("")
        self.RxFrame.LastNameValue.SetValue("")
        self.RxFrame.AddressValue.SetValue("") 
        self.RxFrame.PhoneNumberValue.SetValue("")
        self.RxFrame.GenderCombo.SetValue("")
        self.RxFrame.AgeValue.SetValue("")
        self.RxFrame.AgeCombo.SetValue("")
        self.RxFrame.BirthYear.SetValue("")
        self.RxFrame.BirthMonth.SetValue("")        
        self.RxFrame.BirthDayCombo.SetValue("")
            
    def onEstimate(self, evt):
        
        self.on_check ^= 1
        
        if (self.on_check == 1):
            self.RxFrame.BirthMonth.Enable(False)
            self.RxFrame.BirthDayCombo.Enable(False)
            self.RxFrame.BirthYear.Enable(False)
            self.RxFrame.AgeValue.Enable(True)
            self.RxFrame.AgeCombo.Enable(True)
            
        if (self.on_check == 0):
            self.RxFrame.AgeValue.Enable(False)
            self.RxFrame.AgeCombo.Enable(False)
            self.RxFrame.BirthMonth.Enable(True)
            self.RxFrame.BirthDayCombo.Enable(True)
            self.RxFrame.BirthYear.Enable(True)

    def displayECG(self, evt):
        """ Calls the ecg_lead() method of the ecglogfile module to extract
            the 12 leads then passes it to the ecgplotter module for plotting
        """
        self.ECGplotcounter = self.ECGplotcounter + 1
        ecg_plot = []
        ecg_plot2 = []

        if self.config.get('ecg', 'sim_type') == 'Normal':
            self.ecgdata.ecg_list = []
        
            for y in range(0, 4):
                for i in range(100, 400):
                    self.ecgdata.ecg_list.append(self.getlead[1][i])

        if self.ECGplotcounter == 1:
            self.plotter.plot(self.ecgdata.ecg_list[0:300])
        elif self.ECGplotcounter == 2:
            self.plotter.plot(self.ecgdata.ecg_list[50:350])
        elif self.ECGplotcounter == 3:
            self.plotter.plot(self.ecgdata.ecg_list[100:400])
        elif self.ECGplotcounter == 4:
            self.plotter.plot(self.ecgdata.ecg_list[150:450])
        elif self.ECGplotcounter == 5:
            self.plotter.plot(self.ecgdata.ecg_list[200:500])
        elif self.ECGplotcounter == 6:
            self.plotter.plot(self.ecgdata.ecg_list[250:550])
        elif self.ECGplotcounter == 7:
            self.plotter.plot(self.ecgdata.ecg_list[300:600])
        else:
            self.ECGplotcounter = 0

        ecg_plot = []
        ecg_plot2 = []
                
    def birthday_update(self, evt):
        year_temp = self.RxFrame.BirthYear.GetValue()
        month_temp = self.RxFrame.BirthMonth.GetSelection()
        day_temp = self.RxFrame.BirthDayCombo.GetSelection()

        age = 0
        
        if len(year_temp) == 4:
            date = datetime.datetime.today()
            year_now = date.year
            age = int(year_now) - int(year_temp)
            if int(date.month) < int(month_temp):
                age = age - 1
            if int(date.month) == int(month_temp):
                if int(date.day) < int(day_temp) + 1:
                    age = age - 1
            self.RxFrame.AgeValue.SetValue(str(age))

        
    def on_timer_spo2(self, evt):
        
        self.spo2data.get()
        print 'Spo2 data acquired'
        self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Spo2 data acquired')
       
    def on_timer_bp(self, evt):
        
        self.bpdata.get()
        print 'BP data acquired'
        self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','BP data acquired')
               
    def pressure_update(self, evt):
        """Method that handles the inflating bar of blood pressure"""
        
        press = int(self.file.readline())
        if press != 999:
            self.bp_pressure_indicator.SetValue(press)
        else:
            self.file.close()
            self.pressure_timer.Stop()
            self.bp_pressure_indicator.Enable(False)
            self.bpNow_Button.Enable(True)
            self.setBPmins_combobox.Enable(True)
            self.bpdata.bp_finished()
        
    def make_edf(self, evt):

        self.Endtime = datetime.datetime.today()
        self.Starttime = self.Endtime + datetime.timedelta(seconds= -15)
        self.strDate = self.Starttime.strftime("%d.%m.%y")
        self.strStarttime = self.Starttime.strftime("%H.%M.%S")
        self.strY2KDate = self.Starttime.strftime("%d-%b-%Y")
        
#        print len(self.spo2data.spo2_list)
#        print len(self.spo2data.bpm_list)
#        print len(self.bpdata.systole_sim_values)
#        print len(self.bpdata.diastole_sim_values)
#        print len(self.ecgdata.ecg_list_scaled)
        
        nDataRecord = 3
        
        Biosignal_SPO2 = BioSignal('SpO2 finger', 'IR-Red sensor', \
                                '%', 0, 100, 0, 100, 'None', 15, self.spo2data.spo2_list)
        Biosignal_BPM = BioSignal('SpO2 finger', 'IR-Red sensor', \
                                'bpm', 0, 300, 0, 300, 'None', 15, self.spo2data.bpm_list)
        self.spo2data.spo2_list = []
        self.spo2data.bpm_list = []
        self.Biosignals.append(Biosignal_SPO2)
        self.Biosignals.append(Biosignal_BPM) 
        
        if (self.bpdata.systole_sim_values != 0):
            Biosignal_pSys = BioSignal('bpsystole', 'NIBP2010', 'mmHg', \
                                        0, 300, 0, 300, 'None', 15, self.bpdata.systole_sim_values)
            Biosignal_pDias = BioSignal('bpdiastole', 'NIBP2010', 'mmHg', \
                                        0, 300, 0, 300, 'None', 15, self.bpdata.diastole_sim_values)
            self.Biosignals.append(Biosignal_pSys)
            self.Biosignals.append(Biosignal_pDias)
            nDataRecord = 5   
            
        Biosignal_ECG = BioSignal('II', 'CM', 'mV', -43, 43, 0, 32767, 'None', 7500, self.ecgdata.ecg_list_scaled)
        self.Biosignals.append(Biosignal_ECG)
        
        myedf = edf.EDF(self.patient1, self.Biosignals, self.strDate, self.strStarttime, self.strY2KDate + \
                        ': LifeLink 15 second data of CorScience modules', \
                        nDataRecord, 15)
#        myedf.get(self.patient1)
        print 'EDF creation finished'

        self.Biosignals = []

    def onCall(self, event):
        self.on_send = 0
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Requesting connection to triage...")
        self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Requesting connection to triage...')
        if (self.Call_Label.GetLabel() == "Call") and (self.referflag == 0):    
            self.bp_label.SetLabel("BP ")
            self.heartrate_label.SetLabel("HR ") 
            self.spo2_label.SetLabel("SpO2 ")
            self.RxFrame.video_panel.Hide()         
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.referflag = 1
            self.panel = 1
            if self.with_patient_info == 0:
                CreateDialog = CreateRecordDialog2(self.RxFrame, self)
                CreateDialog.ShowModal()
            CallAfter(self.RxFrame.CreateReferPanel)
            self.Call_Label.SetLabel(">>  ")
            self.RxFrame.Layout()             
        elif (self.Call_Label.GetLabel() == "<<  ") and (self.referflag == 1) : 
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings... Call Panel Shown.")
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Acquiring biomedical readings... Call Panel Shown.')
            self.RxFrame.ReferPanel.Show()
            self.RxFrame.video_panel.Hide()
            self.Call_Label.SetLabel(">>  ") 
            self.bp_label.SetLabel("BP ") 
            self.heartrate_label.SetLabel("HR ") 
            self.spo2_label.SetLabel("SpO2 ")             
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 1
            self.RxFrame.Layout()               
        else:
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquring biomedical readings... Call Panel Hidden.")
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Acquring biomedical readings... Call Panel Hidden.')
            self.RxFrame.ReferPanel.Hide()
            self.RxFrame.video_panel.Show()
            self.Call_Button.Enable(False)
            self.Call_Label.Enable(False)
            self.Call_Label.SetLabel("<<  ")  
            self.bp_label.SetLabel("Blood Pressure ") 
            self.heartrate_label.SetLabel("Heart Rate ") 
            self.spo2_label.SetLabel("Blood Oxygen Saturation ")          
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 0
            self.RxFrame.Layout()

    def sendEmail(self):
        
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Sending Data to Server...")
        self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Sending Data to Server...')
        t = triage.Triage('triage/email.cfg')
        t.login()
        headers = {'Subject': self.config.get('email', 'mode') + ' ' + self.RxFrame.topic, 'X-Eccs-Priority': 'emergency',
                        'X-Eccs-Rxboxextension': '2001'}
        body = self.RxFrame.body
        afilename = ['triage/Ebido_113056.edf']
        attach = {}
        for i in afilename:
                f = open(i, 'r')
                attach[i] = f.read()
                f.close()

        print "sending..\n"
        t.request(headers, body, attach)
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Data Sent...")
        self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Data Sent...')
        print "sent";

    def onSend(self, event): # wxGlade: DAQPanel.<event_handler>

        self.on_send = 1
        self.sendcount += 1
        print 'SENDING'
        print self.sendcount
        
        if self.with_patient_info == 0:
            CreateDialog = CreateRecordDialog2(self.RxFrame, self)
            CreateDialog.ShowModal()
            
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Sending Data to Server...")
        self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Sending Data to Server...')

        if self.sendcount == 2:
            
            self.timerSend.Stop()
            
            if (self.config.getint('email', 'simulated') == 0):
                self.sendEmail()
                self.show_email_success()
            
            elif (self.config.getint('email', 'simulated') == 1):
                self.SendStatus(self)
    
    def show_email_success(self):
        
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Send to Server Successful")
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Send to Server Successful')
            dlg = wx.MessageDialog(self, "Send to Server Successful", "Send to Server Successful", wx.OK | wx.ICON_QUESTION)
            dlg.ShowModal()
    
    def SendStatus(self, event):
        
        if (self.config.getint('email', 'connection') == 1): 
            print "Send to Server Successful"
            self.show_email_success()

        else:
            print "Send to Server Failed"
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Send to Server Failed")
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Send to Server Failed')
            dlg = wx.MessageDialog(self, "Would you like to resend data?", "Send to Server Failed", wx.YES_NO | wx.ICON_QUESTION)
            
            if dlg.ShowModal() == wx.ID_YES:
                self.RxFrame.RxFrame_StatusBar.SetStatusText("Resending data to server...")
                self.sendcount = 1
                self.timerSend.Start(5000)

        self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")              
        self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Acquiring biomedical readings...')
    def onBPNow(self, event): # wxGlade: MyPanel1.<event_handler>
        self.bpNow_Button.Enable(False)
        self.bpdata.get()
        
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
        CreateDialog2 = Lead12Dialog2(self, self)
        CreateDialog2.ShowModal()
        
    def onECGNodeCheck(self, x): 
        """Simulated electrode contact measurement (ECM)"""
        
        self.timerECGNodeCheck.Start(250)
        self.nodetimer = self.nodetimer + 1
        if (self.nodetimer == 1):
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Checking Node Placement of ECG...")
            self.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.dbuuid,'status message','','Checking Node Placement of ECG...')
            self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_connected.png", wx.BITMAP_TYPE_ANY))
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_connected.png", wx.BITMAP_TYPE_ANY))
            self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_connected.png", wx.BITMAP_TYPE_ANY))
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_connected.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_connected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_connected.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 2):
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_initial.png", wx.BITMAP_TYPE_ANY))
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 3):
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 4):
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_connected.png", wx.BITMAP_TYPE_ANY))
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY)) 
        elif (self.nodetimer == 5):
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))  
        elif (self.nodetimer == 6):
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))        
        elif (self.nodetimer == 7):
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))              
        elif (self.nodetimer == 8):
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_connected.png", wx.BITMAP_TYPE_ANY))       
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))  
        elif (self.nodetimer == 9):     
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 10):      
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 11):     
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))            
        elif (self.nodetimer == 12):
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_connected.png", wx.BITMAP_TYPE_ANY))   
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))  
        elif (self.nodetimer == 13):  
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY)) 
        elif (self.nodetimer == 14):  
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY)) 
        elif (self.nodetimer == 15): 
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))             
        elif (self.nodetimer == 16):
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_connected.png", wx.BITMAP_TYPE_ANY))
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")            
            self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.RxFrame.DAQPanel.dbuuid,'status message','','Acquiring biomedical readings...')
            self.timerECGNodeCheck.Stop()    
            self.nodetimer = 0
#            self.ecgdata.get()
            self.timerECG_refresh.Start(125)         

class CreateRecordDialog2(CreateRecordDialog):

    def __init__(self, parent, *args, **kwds):
        CreateRecordDialog.__init__(self, *args, **kwds)
        self.RxFrame = parent
        self.PatientFirstName_TextCtrl.SetValue(self.RxFrame.FirstNameValue.GetValue())
        self.PatientMiddleName_TextCtrl.SetValue(self.RxFrame.MiddleNameValue.GetValue())
        self.PatientLastName_TextCtrl.SetValue(self.RxFrame.LastNameValue.GetValue())
        self.PatientAddress_TextCtrl.SetValue(self.RxFrame.AddressValue.GetValue())
        self.PatientPhoneNumber_TextCtrl.SetValue(self.RxFrame.PhoneNumberValue.GetValue())
        self.PatientGender_Combo.SetValue(self.RxFrame.GenderCombo.GetValue())
        self.PatientAge_TextCtrl.SetValue(self.RxFrame.AgeValue.GetValue())
        self.PatientBirth_Combo.SetValue(self.RxFrame.AgeCombo.GetValue())
        self.RemarkValue.SetValue(self.RxFrame.DAQPanel.RemarkValueDaq.GetValue())
        
    def OnCreateRecord(self, event): # wxGlade: CreateRecordDialog.<event_handler>

        FirstName = self.PatientFirstName_TextCtrl.GetValue()
        MiddleName = self.PatientMiddleName_TextCtrl.GetValue()
        LastName = self.PatientLastName_TextCtrl.GetValue()
        Gender = self.PatientGender_Combo.GetValue()
        Age = self.PatientAge_TextCtrl.GetValue()
        Birth = self.PatientBirth_Combo.GetValue()
        Validity = self.PatientAgeValidity_Combo.GetValue()
        Address = self.PatientAddress_TextCtrl.GetValue()
        Phone = self.PatientPhoneNumber_TextCtrl.GetValue()        
        PatientName = FirstName + ' ' + MiddleName + ' ' + LastName

        self.RxFrame.topic = self.ReferralTopic_TextCtrl.GetValue()
        self.RxFrame.body = self.RemarkValue.GetValue()

        self.RxFrame.FirstNameValue.SetValue(FirstName)
        self.RxFrame.MiddleNameValue.SetValue(MiddleName)
        self.RxFrame.LastNameValue.SetValue(LastName)
        self.RxFrame.AddressValue.SetValue(Address) 
        self.RxFrame.PhoneNumberValue.SetValue(Phone)
        self.RxFrame.GenderCombo.SetValue(Gender)
        self.RxFrame.AgeValue.SetValue(Age)
        self.RxFrame.AgeCombo.SetValue(Birth)
        self.RxFrame.DAQPanel.RemarkValueDaq.SetValue(self.RemarkValue.GetValue())     
        self.Destroy()
        self.RxFrame.DAQPanel.with_patient_info = 1
        self.RxFrame.DAQPanel.rxboxDB.dbpatientinsert('patients','lastname', 'firstname', \
            'middlename', 'address', 'phonenumber', 'age', 'birth', 'gender', 'uuid', \
            LastName, FirstName, MiddleName, Address, Phone, Age, Birth, Gender, self.RxFrame.DAQPanel.dbuuid)
        if self.RxFrame.DAQPanel.on_send == 0:
 #           CallAfter(self.RxFrame.CreateReferPanel)
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings... Call Panel Initiated.")
            self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals','uuid','type','filename','content',self.RxFrame.DAQPanel.dbuuid,'status message','','Acquiring biomedical readings... Call Panel Initiated.')
            
        if self.RxFrame.DAQPanel.on_send == 1:
            self.RxFrame.DAQPanel.timerSend.Start(5000)
        
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
        self.parent = parent
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

        self.plotter_I.plot(self.parent.getlead[0])
        self.plotter_II.plot(self.parent.getlead[1])
        self.plotter_III.plot(self.parent.getlead[2])
        self.plotter_aVR.plot(self.parent.getlead[3])
        self.plotter_aVL.plot(self.parent.getlead[4])
        self.plotter_aVF.plot(self.parent.getlead[5])
        self.plotter_V1.plot(self.parent.getlead[6])
        self.plotter_V2.plot(self.parent.getlead[7])
        self.plotter_V3.plot(self.parent.getlead[8])
        self.plotter_V4.plot(self.parent.getlead[9])
        self.plotter_V5.plot(self.parent.getlead[10])
        self.plotter_V6.plot(self.parent.getlead[11])
        
        self.plotter_bigII = extendedPlotter(self, bigsizer, self.parent.getlead[1])
        self.leadII_sizer.Add(self.plotter_bigII, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        
            
# end of rxboxGUI classes

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = RxFrame2(None, -1, "")
    app.SetTopWindow(rx_frame)
    rx_frame.Maximize(True)
    rx_frame.Show()
    app.MainLoop()



        


