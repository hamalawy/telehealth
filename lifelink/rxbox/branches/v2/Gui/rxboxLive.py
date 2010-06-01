#!/usr/bin/env python
"""Project LifeLink: RxBox Software (Live and Simulator)

Authors:    Chiong, Charles Hernan
            Cornillez, Dan Simone
            Timothy John Ebido
            Thomas Rodinel Soler
            Luis Sison, PhD
            ------------------------------------------------
            Instrumentation, Robotics and Control Laboratory
            University of the Philippines - Diliman
            ------------------------------------------------
            March 2010


When PLAY button is pressed, the following scripts are done:
- BP, HR, and SpO2 panels activate
- ECM Electrodes Blink (checking all electrodes) and ECG plots on the grid
- Database and tables are created (if already existing method is skipped)
- Updates session, biomedical and patients information in the database
"""
ECGPORT = '/dev/ttyUSB0'
SPO2PORT = '/dev/ttyUSB1'
BPPORT = '/dev/ttyUSB2'

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
import edfviewer
from pylab import *
import datetime
import ConfigParser
from lead12dialog import Lead12Dialog
import wx.lib.plot as plot
import copy

from CPlotter import *
from ecgplotter import Plotter
#from ecgplot import Plotter
from ecgplot import extendedPlotter
from matplotlib import pyplot

import sys
sys.path.append('triage/')
sys.path.append('voip/')
sys.path.append('im')
sys.path.append('simulators/')
sys.path.append('splash_screen/')

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
import os

#import splash
#from splash import SplashApp
import splash2
from splash2 import Splash

import threading
from multiprocessing import Process
from subprocess import Popen, PIPE

from SPO2 import SPO2
from BP import BP
from ecglogfile import ECG
import ECGLive
#from config import *

#import threading
#try:                   
#    from opencv import *
#except ImportError:
#    from ctypes_opencv import *

import dicom           
from scipy.misc import fromimage
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
                
class SplashApp2(Splash):
    
    def __init__(self, *args, **kwds):
        Splash.__init__(self, *args, **kwds)
        self.loaded = 0
        self.image_num = 1
        self.ret_value = 0
        self.init_loadingbar()

        
    def init_loadingbar(self):
        self.bar = wx.Gauge(self.gauge, -1, 100, size=(525,30), style=wx.GA_HORIZONTAL)
        self.bar_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.inc_bar, self.bar_timer)
        self.value = 0
        self.bar_timer.Start(50)
        self.ret_value = self.ShowModal()        

    def inc_bar(self, event):
        
        if (self.value != 100):
            self.bar.SetValue(self.value)
            self.value += 1
            
        else:
            self.bar_timer.Stop()
            self.loaded = 1

    def on_skip(self, event): # wxGlade: Splash.<event_handler>
        
        self.EndModal(self.ret_value)
        self.Destroy()
        
    def on_next(self, event):

        if self.image_num == 4:
            self.image_num = 0
        self.image_num += 1
        filename = 'splash_screen/screenshots/' + str(self.image_num) + '.png'
        self.title.SetBitmap(wx.Bitmap(filename, wx.BITMAP_TYPE_ANY))

    def on_prev(self, event):
        
        if self.image_num == 1:
            self.image_num = 5
        self.image_num -= 1
        filename = 'splash_screen/screenshots/' + str(self.image_num) + '.png'
        self.title.SetBitmap(wx.Bitmap(filename, wx.BITMAP_TYPE_ANY))


class RxFrame2(RxFrame):
    """ Class for RxFrame GUI instance and methods
    
    Methods:
        __init__(RxFrame)       DestroyReferPanel
        __set_properties        onPrevSnapshot
        CreateReferPanel        onNextSnapshot
        onMsgRcvd               onSnapshot
        onMsgSent               on_steth_record
        sendMessage             on_steth_play
        onClose                 on_steth_stop
        updateIM
         
    """
    def __init__(self, *args, **kwds):
        """Initializes RxFrame GUI
        
        - Sets necessary variables
        
        Arguments: __init__(RxFrame)
        """        
        
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
        self.imgcount = 0
        self.imgcurrent = 0
        self.SetClientSize((320, 240))
        # Create a steth instance

        self.steth_status = None
        self.stop_button.Enable(False)

        self.DAQPanel.refer_panel_shown = 0
        self.simvideo_run = 0
        self.timer_video_start = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.init_simvideo, self.timer_video_start)
        self.pid = int()


    def __set_properties(self):
        RxFrame.__set_properties(self)
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        
    def CreateReferPanel(self):
        """Creates the refer panel window and initializes and starts linphone process"""
        
#        self.timer_video_start.Start(5000)
        self.ReferPanel = ReferPanel(self, -1)
        self.mainhorizontal_sizer.Add(self.ReferPanel, 1, wx.ALL | wx.EXPAND, 4)
        
        self.DAQPanel.refer_panel_shown = 1
        
        
        if self.DAQPanel.config.getint('im', 'simulated') == 1:
            self.ReferPanel.IMreply_Text.Bind(wx.EVT_TEXT_ENTER, self.updateIM)
        else:
            self.ReferPanel.IMreply_Text.Bind(wx.EVT_TEXT_ENTER, self.sendMessage)        
            
        self.Layout()        


        if self.DAQPanel.config.getint('voip', 'simulated') == 0:
            self.l = LinphoneHandle()
            wid = self.ReferPanel.video_panel.GetHandle()
            self.l.set_window(wid)
            self.l.spawn()
            self.l.start()
        else:
            self.timer_video_start.Start(5000)
            wid = self.ReferPanel.video_panel.GetHandle()
            print wid
            self.command = 'mplayer -wid ' + str(wid) + ' water-and-wind.ogv'
            print self.command

        if self.DAQPanel.config.getint('im', 'simulated') == 0:
            self.m = messenger.Messenger('1001@one.telehealth.ph', 'telehealth')
            self.m.handler_new_message = self.onMsgRcvd
            self.m.handler_sent_message = self.onMsgSent
            self.m.set_recipient('1000@one.telehealth.ph')

            self.m.connect()
            self.m.start()

        self.mplayer = Process(target=self.init_video)
        print 'ReferPanel initialized'

    def init_simvideo(self, event):
        """Starts mplayer"""
        self.timer_video_start.Stop()
        self.mplayer.start()
        
    def init_video(self):
        """Links the video demo to mplayer for playing"""
        self.simvideo_run = 1
        wid = self.ReferPanel.video_panel.GetHandle()
        self.command = 'mplayer -wid ' + str(wid) + ' simulators/video/water-and-wind.ogv'
        os.system(self.command)

        
    def terminate_video(self):
        """Terminates simulated video"""

        self.simvideo_run = 0
        self.pid = self.mplayer.pid + 2
        cmd = 'kill -15 ' + str(self.pid)
        print cmd
        os.system('kill -15 ' + str(self.pid))
        print 'VIDEO TERMINATED'


    def onMsgRcvd(self, conn, msg):
        """Shows message received in the IM panel"""
        time = self.get_time()
        msgrcvd = 'DE1: ' + msg.getBody()
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'IM', '', msgrcvd)
        self.ReferPanel.IMtexts_Text.AppendText('('+time+')\n'+'DE1: ' + msg.getBody() + '\n')
       
    def onMsgSent(self, msg):
        """Shows message sent in the IM panel"""
        time = self.get_time()
        msgsent = 'RXBOX: ' + msg
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'IM', '', msgsent)
        self.ReferPanel.IMtexts_Text.AppendText('('+time+')\n'+'RXBOX: ' + msg + '\n')
        self.ReferPanel.IMreply_Text.Clear()
        
    def get_time(self):
        """Get current date and time"""
        time = datetime.datetime.today()
        time = time.strftime("%H:%M:%S")
        return str(time)

    def sendMessage(self, event):
        """Sends the message to a specified destination (address)"""
        msg = self.ReferPanel.IMreply_Text.GetValue()
        self.m.set_recipient('1000@one.telehealth.ph')
        self.m.send_message(msg)
       
    def onClose(self, evt):
        """Displays a dialog prompt that asks the user to save data when user attempts to destroy the frame"""
        
        try:
            self.terminate_video()
        except:
            pass
        
        dlg = wx.MessageDialog(self, 'Do you want to save data?', 'Exit', \
                                wx.YES_NO | wx.ICON_QUESTION | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_CANCEL:
            dlg.Destroy()
        else:
            dlg.Destroy()
            self.Destroy()   
            
    def updateIM(self, evt):
        """Copy the contents of the im text input box and show it to an another text box"""

        time = self.get_time()
        prev = self.ReferPanel.IMreply_Text.GetValue()
        imupdate = "RxBox: "+ prev
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'IM', '', imupdate)
        imupdate = "DE : "+ prev
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'IM', '', imupdate)
        self.ReferPanel.IMtexts_Text.AppendText('(' + time + ')' + '\nRxBox: ' + prev + '\nDE: ' + prev + '\n')
        self.ReferPanel.IMreply_Text.Clear() 
        
    def DestroyReferPanel(self):
        """Destroys the refer panel and stops linphone process"""
        
        print 'Destroying Refer Panel'
        self.DAQPanel.refer_panel_shown = 0
#        self.DAQPanel.timerECG_refresh.Start(125)
        
        try:
            self.l.stop()
            self.l.join()
            

            self.m.stop()
            self.m.join()

        except AttributeError:
            pass
            
        try:
            self.terminate_video()
            self.mplayer.join()
        except:
            pass
        
#        self.simvideo_run = 0
        self.ReferPanel.Destroy()
#        self.terminate_video()
        
        self.Layout()
            
    def onPrevSnapshot(self, event): # wxGlade: RxFrame.<event_handler>
        """Displays previously captured images in the snapshot image panel.
           Enabled once the capture button is toggled.
           Disabled when the oldest image captured is displayed.
        """
        self.RxFrame_StatusBar.SetStatusText("Snapshot previous button toggled...")
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'status message', '', 'Snapshot previous button toggled...')
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
        """Enabled once the previous button is toggled.
           Disabled when the latest image is displayed.
        """
        self.RxFrame_StatusBar.SetStatusText("Snapshot next button toggled...")
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'status message', '', 'Snapshot next button toggled...')
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
        """Captures an image.
        """
        self.RxFrame_StatusBar.SetStatusText("Snapshot main button toggled...")
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'status message', '', 'Snapshot main button toggled...')
        print "Snapshot main button toggled..."
        self.imgcount = self.imgcount + 1
        self.imgcurrent = self.imgcount

        if self.imgcount == 7:
            self.imgcount = 1
            self.imgcurrent = 1
        if self.imgcurrent > 1:
            self.prev_snapshot.Enable(True)
        if self.imgcurrent == 1:
            self.prev_snapshot.Enable(False)
            
        print self.imgcount
        self.file = 'snapdemo/' + str(self.imgcount) + '.jpg'
        self.temp_bmp.append(wx.Image(self.file, wx.BITMAP_TYPE_JPEG).ConvertToBitmap())
        img = wx.ImageFromBitmap(self.temp_bmp[self.imgcount - 1])
        img.Rescale(120, 90)
        bitmap = wx.BitmapFromImage(img) # Convert Image to Bitmap 
        self.img.SetBitmap(bitmap)  
        self.next_snapshot.Enable(False)    
        print "count: ", self.imgcount, "current: ", self.imgcurrent

    def on_vid_display(self):
        pass

    def displayImage(self, offset=(0, 0)):
        pass

    def on_steth_record(self, event): # wxGlade: RxFrame.<event_handler>
        """Record bodily sounds.
           Disables the stethoscope play button.
        """
        print "Steth Recording... "
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'status message', '', 'Snapshot next button toggled...')
        self.RxFrame_StatusBar.SetStatusText("Steth Sound Recording...")
        self.stop_button.Enable(True)
        self.play_button.Enable(False)
        self.record_button.Enable(False)
        self.steth_status = 'Record'

    def on_steth_play(self, event): # wxGlade: RxFrame.<event_handler>
        """Plays recorded sounds.
           Disables the stethoscope record button.
        """    
        print "Steth Sound Playing... "
        self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'status message', '', 'Steth Sound Playing...')
        self.RxFrame_StatusBar.SetStatusText("Steth Sound Playing...")
        self.stop_button.Enable(True)
        self.record_button.Enable(False)
        self.play_button.Enable(False)
        self.steth_status = 'Play'

        self.filename_hr = self.DAQPanel.config.get('spo2', 'hr_sim_type')
        
        if self.filename_hr == 'High':
            self.openwav = 'stethdemo/heartbeatfast.wav'
        elif self.filename_hr == 'Low':
            self.openwav = 'stethdemo/heartbeatslow.wav'
        else :
            self.openwav = 'stethdemo/heartbeatnormal.wav'

        self.playwav.play_steth = 1
        self.playwav.start() 

    def on_steth_stop(self, event): # wxGlade: RxFrame.<event_handler>
        """Stops stethoscope record or play methods.
        """   
        self.play_button.Enable(True)
        self.record_button.Enable(True)
        self.stop_button.Enable(False)

        if self.steth_status == 'Record':
            self.RxFrame_StatusBar.SetStatusText("Stopping Steth Record...")
            self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'status message', '', 'Stopping Steth Record...')
        elif self.steth_status == 'Play':
            self.RxFrame_StatusBar.SetStatusText("Stopping Steth Play...")
            self.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.DAQPanel.dbuuid, 'status message', '', 'Snapshot next button toggled...')
            self.playwav.stop()    
            self.playwav.join()    
        self.steth_status = 'Stop'
        
    def record_audio(self, evt):
        pass

class DAQPanel2(DAQPanel):
    """ Class for DAQPanel GUI instance and methods
    
    Methods:
        __init__(DAQPanel)       displayECG
        init_daqtimers           birthday_update
        init_config              make_edf
        init_ecglive             on12Lead
        init_simsensors_ecg      init_livebp
        init_simsensors_bp       init_liveecg   
        init_simsensors_spo2     init_livespo2
        get_bp                   get_bpcyclic
        onStartStop              onCall
        SaveQuery                onECGNodeCheck
        ClearPatient             onSend
        DisablePatient           cyclicbpdemo
        EnablePatient            acquirespo2
        pressure_update          sendEmail
        show_email_success       startSaveThread 
        onBPNow                  updateBPDisplay 
    """
    def __init__(self, parent, *args, **kwds):
        """Initializes DAQPanel2 GUI, timers
        
        - Sets necessary variables
        
        Arguments: __init__(DAQPanel)
        """
        DAQPanel.__init__(self, *args, **kwds)
        self.RxFrame = parent
        self.rxboxDB = rxboxdb.rxboxDB()
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel, -1, 200, \
                                                size=(20, 120), style=wx.GA_VERTICAL)    
#        self.ecg_vertical_sizer = self.RxFrame.ecg_vertical_sizer     
        self.init_config()
        self.ECGsimulated = self.config.get('ecg', 'simulated') == '1'
        
        self.init_ecgplotter()
        self.init_daqtimers()

        if self.config.get('spo2', 'simulated') == '0':
            self.init_livespo2()
        else:
            self.init_simsensors_spo2()
        if self.config.get('bp', 'simulated') == '0':
            self.init_livebp()
        else:
            self.init_simsensors_bp()
        
        self.RxFrame.BirthMonth.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.RxFrame.BirthDayCombo.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.RxFrame.BirthYear.Bind(wx.EVT_TEXT, self.birthday_update)    
        
        #ECG INIT START
        if not self.ECGsimulated:
            print 'Actual ECG'
            self.init_liveecg()
            
        else:
            print 'Simulated ECG'
            self.init_simsensors_ecg()
            if self.config.get('ecg', 'sim_type') != 'Normal':
                self.ECGDAQ.ecg_list = self.ECGDAQ.get_plot()
        #ECG INIT END
        
        self.patient1 = edf.Patient('1', '', '', '', '', \
                                    '', '', 0)
                                    
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
        self.referflag = 0    
        self.pressure_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.pressure_update, self.pressure_timer)
        self.bp_pressure_indicator.Enable(False)
        self.dbuuid = ""
        self.dbuuid = str(uuid.uuid1())
        print "uuid = ", self.dbuuid
        self.rxboxDB.dbinsert('sessions', 'uuid', self.dbuuid)
        #set start time in table: sessioninfo
        dbstart = str(datetime.datetime.today())
        self.rxboxDB.dbupdate('sessions', 'starttime', dbstart, 'uuid', self.dbuuid)
        self.rxboxinitialized = 1
        
    def init_daqtimers(self):
        """Initializes timers for DAQ Panel of RxBox"""
        
        self.timer_spo2 = wx.Timer(self)
        self.timer_bpdemo = wx.Timer(self)
        #self.timerEDF = wx.Timer(self)
        self.pressure_timer = wx.Timer(self)
        self.timerSend = wx.Timer(self)
        self.timerECG_refresh = wx.Timer(self)
        self.timerECGNodeCheck = wx.Timer(self)
        self.timer_bpcyclic = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.acquirespo2, self.timer_spo2)
        self.Bind(wx.EVT_TIMER, self.cyclicbpdemo, self.timer_bpdemo)
        #self.Bind(wx.EVT_TIMER, self.make_edf, self.timerEDF)
        self.Bind(wx.EVT_TIMER, self.pressure_update, self.pressure_timer)
        self.Bind(wx.EVT_TIMER, self.onSend, self.timerSend)
        self.Bind(wx.EVT_TIMER, self.displayECG, self.timerECG_refresh)
        self.Bind(wx.EVT_TIMER, self.onECGNodeCheck, self.timerECGNodeCheck)
        self.Bind(wx.EVT_TIMER, self.get_bpcyclic, self.timer_bpcyclic)
        
    def init_config(self):
        """Initializes configuration file for Rxbox"""

        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')
        
    def init_ecgplotter(self):
        """Initializes ecgplotter GUI"""
        
        self.sizersize = self.ecg_vertical_sizer.GetSize()
        if self.ECGsimulated: 
            self.plotter = Plotter(self, (1120, 380))
            self.ecg_vertical_sizer.Add(self.plotter.plotpanel, 1, \
                                    wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        else:
            self.plotpanel = wx.Panel(self)
            self.ecg_vertical_sizer.Add(self.plotpanel, 1, \
                                    wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        self.plotind = 0
        self.ECGplotcounter = 0
        
    def init_simsensors_ecg(self):
        """Initializes ecg simsensor"""
        
        self.Biosignals = []
        self.getlead = ECG().ecg_lead()
        self.ECGDAQ = simsensors.EcgSim(self)

    def init_liveecg (self):
        """ Initialize live ecg """
        self.Biosignals = []
        self.ECGDAQ = ECGLive.ECG(panel=self,port='/dev/ttyUSB0',daqdur=1,ecmcheck=0,debug=True)
        self.ECGDAQ.device_ready()
        self.ECGDAQ.stop()
        
    def init_livespo2(self):
        """ Initialize live spo2 """
        self.spo2data=SPO2(self,port=SPO2PORT)

    def init_simsensors_spo2(self):
        """Initializes spo2 simsensor"""
        self.spo2data = simsensors.Spo2sim(self)
        
    def init_livebp(self):
        """ Initialize live BP """
        self.bp=BP(self,port=BPPORT)
        
        
    def init_simsensors_bp(self):
        """Initializes bp simsensor"""
        self.bpdata = simsensors.BpSim(self)


    def onStartStop(self, event):
        """Triggers the start or end of the RxBox session."""

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
        self.EnablePatient()
        if self.StartStop_Label.GetLabel() == "Start":
            #creates universally unique identifier and add it to database as primary key

            if self.rxboxinitialized == 0:
                self.dbuuid = ""
                self.dbuuid = str(uuid.uuid1())
                print "uuid = ", self.dbuuid
                self.rxboxDB.dbinsert('sessions', 'uuid', self.dbuuid)
                dbstart = str(datetime.datetime.today())
                self.rxboxDB.dbupdate('sessions', 'starttime', dbstart, 'uuid', self.dbuuid)
            elif self.rxboxinitialized == 1:
                self.rxboxinitialized = 0
            
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'BP Ready')
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Pulse Ox Ready')
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Pulse Ox Ready')       
#            self.Call_Label.SetLabel("Call")
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
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Acquiring biomedical readings...')
            
            if self.config.get('bp', 'simulated') == '0':
                self.get_bp()
            else:
                self.bpdata.get()
            
            if not self.ECGsimulated:
                self.ECGDAQ = ECGLive.ECG(panel=self,port=ECGPORT,daqdur=1,ecmcheck=0,debug=True)
                self.plotter = CPlotter(self,panel=self.plotpanel,mode='normal',cont=True,time=3,data=[0])
                self.plotter.Open()
                self.alive = True
                self.get_thread = threading.Thread(target=self.Get_ECG)
                self.get_thread.start()
            self.onECGNodeCheck(self)
   
            self.timer_spo2.Start(1000)
            #self.timerEDF.Start(15000)
            
        else:

            self.RxFrame.RxFrame_StatusBar.SetStatusText("RxBox Ready")
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'RxBox Ready')
            self.bpNow_Button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png", wx.BITMAP_TYPE_ANY))
            self.StartStop_Label.SetLabel("Start")
            self.bpNow_Button.Enable(True)
            self.Call_Button.Enable(False)
            self.Send_Button.Enable(False)
            self.lead12_button.Enable(False)
            self.timer_spo2.Stop()
            self.timer_bpdemo.Stop()       
            #self.timerEDF.Stop()    
            self.timerSend.Stop()  
            self.timerECG_refresh.Stop()
            self.timerECGNodeCheck.Stop()
            if self.bp_isCyclic == 1:
				self.timer_bpcyclic.Stop()
				self.bp_isCyclic = 0
            if not self.ECGsimulated:
                self.alive = False
                self.ECGDAQ.stop()
                self.plotter.Close()
                 
#            self.Call_Label.SetLabel("Call")          
            self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
            self.spo2_infolabel.SetLabel('Pulse Ox Ready')
            self.RxFrame.DAQPanel.RemarkValueDaq.SetValue('')
#            CallAfter(self.RxFrame.DestroyReferPanel)
#            self.RxFrame.DestroyReferPanel()

            self.SaveQuery()
            print 'stopping...'
    

    def SaveQuery(self):
        """Displays a dialog box that prompts the user to save data
           If yes: patient information panel retains data
           If no: patient information is cleared
        """
        dlg2 = wx.MessageDialog(self, 'Do you want to save data?', '', \
                                    wx.YES_NO | wx.ICON_QUESTION | wx.CANCEL)
        SaveOption = dlg2.ShowModal()
        if SaveOption == wx.ID_YES:
            self.Call_Label.SetLabel("Call") 
#            print "YES"
            self.EnablePatient()
            if self.referflag == 0:
                self.with_patient_info = 0
#                print "NOT REFERRED"
            if self.referflag == 1:
                self.referflag = 0
                self.bp_label.SetLabel("Blood Pressure ") 
                self.heartrate_label.SetLabel("Heart Rate ") 
                self.spo2_label.SetLabel("Blood Oxygen\nSaturation ")
                self.with_patient_info = 0
#                print "REFER BUTTON TOGGLED"
                self.RxFrame.DestroyReferPanel()
                print 'Refer Panel Destroyed'
        elif SaveOption == wx.ID_NO:
            self.Call_Label.SetLabel("Call") 
#            print "NO"
            self.ClearPatient()
            self.EnablePatient()
            self.with_patient_info = 0
            if self.referflag == 1:
#                print "REFER BUTTON TOGGLED"
                self.bp_label.SetLabel("Blood Pressure ") 
                self.heartrate_label.SetLabel("Heart Rate ") 
                self.spo2_label.SetLabel("Blood Oxygen\nSaturation ")
                self.RxFrame.DestroyReferPanel()
                print 'Refer Panel Destroyed'
            self.referflag = 0
        else:
            print "cancel"
        
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
            

    def DisablePatient(self):
        """Disable patient information panel"""
        
        self.RxFrame.FirstNameValue.Enable(False)
        self.RxFrame.MiddleNameValue.Enable(False)
        self.RxFrame.LastNameValue.Enable(False)
        self.RxFrame.AddressValue.Enable(False) 
        self.RxFrame.PhoneNumberValue.Enable(False)
        self.RxFrame.GenderCombo.Enable(False)
        self.RxFrame.AgeValue.Enable(False)
        self.RxFrame.AgeCombo.Enable(False)
        self.RxFrame.BirthYear.Enable(False)
        self.RxFrame.BirthMonth.Enable(False)        
        self.RxFrame.BirthDayCombo.Enable(False)
        
    def EnablePatient(self):
        """Enable patient information panel"""
        
        self.RxFrame.FirstNameValue.Enable(True)
        self.RxFrame.MiddleNameValue.Enable(True)
        self.RxFrame.LastNameValue.Enable(True)
        self.RxFrame.AddressValue.Enable(True) 
        self.RxFrame.PhoneNumberValue.Enable(True)
        self.RxFrame.GenderCombo.Enable(True)
        self.RxFrame.AgeValue.Enable(True)
        self.RxFrame.AgeCombo.Enable(True)
        self.RxFrame.BirthYear.Enable(True)
        self.RxFrame.BirthMonth.Enable(True)        
        self.RxFrame.BirthDayCombo.Enable(True)  

    def Get_ECG(self):
        self.ind = 0
        while self.alive:
            try:
                self.ECGDAQ.patient_ready()
                self.ind = self.plotter.Plot(self.ECGDAQ.lead_ecg['II'][-500:],xs=self.ind)
                if len(self.ECGDAQ.lead_ecg['II']) > 7500:
                    self.ECGDAQ.pop(end=(len(self.ECGDAQ.lead_ecg['II']) - 7500))
            except Exception, e:
                self.ECGDAQ = ECGLive.ECG(panel=self,port=ECGPORT,daqdur=1,ecmcheck=0,debug=True)
                print 'ECG Error', e
        print 'Thread Stopped'
                          
    def displayECG(self, evt):
        """ Calls the ecg_lead() method of the ecglogfile module to extract
            the 12 leads then passes it to the ecgplotter module for plotting
        """
        if self.ECGsimulated:
            self.ECGplotcounter = self.ECGplotcounter + 1
            ecg_plot = []
            ecg_plot2 = []

            if self.config.get('ecg', 'sim_type') == 'Normal':
                self.ECGDAQ.ecg_list = []
            
                for y in range(0, 4):
                    for i in range(100, 400):
                        self.ECGDAQ.ecg_list.append(self.getlead[1][i])

            if self.ECGplotcounter == 1:
                self.plotter.plot(self.ECGDAQ.ecg_list[0:300])
            elif self.ECGplotcounter == 2:
                self.plotter.plot(self.ECGDAQ.ecg_list[50:350])
            elif self.ECGplotcounter == 3:
                self.plotter.plot(self.ECGDAQ.ecg_list[100:400])
            elif self.ECGplotcounter == 4:
                self.plotter.plot(self.ECGDAQ.ecg_list[150:450])
            elif self.ECGplotcounter == 5:
                self.plotter.plot(self.ECGDAQ.ecg_list[200:500])
            elif self.ECGplotcounter == 6:
                self.plotter.plot(self.ECGDAQ.ecg_list[250:550])
            elif self.ECGplotcounter == 7:
                self.plotter.plot(self.ECGDAQ.ecg_list[300:600])
            else:
                self.ECGplotcounter = 0

            ecg_plot = []
            ecg_plot2 = []
                
    def birthday_update(self, evt):
        """Automatically updates the age of patient and the corresponding birth year"""
        self.year_temp = self.RxFrame.BirthYear.GetValue()
        self.month_temp = self.RxFrame.BirthMonth.GetSelection()
        self.day_temp = self.RxFrame.BirthDayCombo.GetSelection()

        age = 0
        
        if len(self.year_temp) == 4:
            date = datetime.datetime.today()
            year_now = date.year
            age = int(year_now) - int(self.year_temp)
            if int(date.month) < int(self.month_temp):
                age = age - 1
            if int(date.month) == int(self.month_temp):
                if int(date.day) < int(self.day_temp) + 1:
                    age = age - 1
            self.RxFrame.AgeValue.SetValue(str(age))
            self.RxFrame.AgeCombo.SetValue('Years')
        
    def acquirespo2(self, evt):
        """Starts spo2 data acquisition"""
        self.spo2data.get()
        print 'Acquiring Spo2 data'
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Acquiring Spo2 data')
       
    def cyclicbpdemo(self, evt):
        """Starts simulated cyclic bp data acquisition"""
        self.bpdata.get()
        print 'Acquiring BP data'
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Acquiring BP data')
               
    def make_edf(self):
        """Creates 15 second chunks of edf data"""
        
        if self.RxFrame.DAQPanel.with_patient_info == 1:
        
            self.year_temp = self.RxFrame.BirthYear.GetValue()
            self.month_temp = str(self.RxFrame.BirthMonth.GetSelection()+1)
            self.day_temp = str(self.RxFrame.BirthDayCombo.GetSelection()+1)
            self.bday = self.month_temp + '.' + self.day_temp + '.' + self.year_temp[-2:]
            
            self.patient1 = edf.Patient('1', str(self.RxFrame.FirstNameValue.GetValue()), str(self.RxFrame.MiddleNameValue.GetValue()), str(self.RxFrame.LastNameValue.GetValue()), '', str(self.RxFrame.GenderCombo.GetValue()), str(self.bday), 20)
                            
        self.Endtime = datetime.datetime.today()
        self.Starttime = self.Endtime + datetime.timedelta(seconds= -15)
        self.strDate = self.Starttime.strftime("%d.%m.%y")
        self.strStarttime = self.Starttime.strftime("%H.%M.%S")
        self.strY2KDate = self.Starttime.strftime("%d-%b-%Y")
        
        print self.spo2data.spo2_list
        print self.spo2data.bpm_list

#        print self.ECGDAQ.ecg_list_scaled
        
        nDataRecord = 3
        
        Biosignal_SPO2 = BioSignal('SpO2 finger','IR-Red sensor',\
                                '%',0,100,0,100,'None',15,self.spo2data.spo2_list)
        Biosignal_BPM = BioSignal('SpO2 finger','IR-Red sensor',\
                                'bpm',0,300,0,300,'None',15,self.spo2data.bpm_list)
        self.Biosignals.append(Biosignal_SPO2)
        self.Biosignals.append(Biosignal_BPM) 
        
        temp = []
        if not self.ECGsimulated:
            for i in self.ECGDAQ.lead_ecg['II']:
                temp.append(int(i/0.00263+16384))
            Biosignal_ECG = BioSignal('II', 'CM', 'mV', -43, 43, 0, 32767, 'None', len(temp), temp)
        else:
            for i in range(0,1200):
                temp.append(int(self.ECGDAQ.ecg_list[i]/0.00263+16384))
            Biosignal_ECG = BioSignal('II', 'CM', 'mV', -43, 43, 0, 32767, 'None', 1200, temp)
            
        self.spo2data.spo2_list = []
        self.spo2data.bpm_list = []

        if self.config.get('bp', 'simulated') == '0':
            print self.bp.sys_list
            print self.bp.dias_list
            if (self.bp.sys_list != 0):
                Biosignal_pSys = BioSignal('bpsystole', 'NIBP2010', 'mmHg', \
                                        0, 300, 0, 300, 'None', 15,self.bp.sys_list)
            
                Biosignal_pDias = BioSignal('bpdiastole', 'NIBP2010', 'mmHg', \
                                        0, 300, 0, 300, 'None', 15, self.bp.dias_list)
                                        
                self.Biosignals.append(Biosignal_pSys)
                self.Biosignals.append(Biosignal_pDias)
                print self.bp.sys_list
                print self.bp.dias_list
                nDataRecord = 5
        else:
            if (self.bpdata.sys_list != 0):
                print self.bpdata.sys_list
                print self.bpdata.dias_list
                Biosignal_pSys = BioSignal('bpsystole', 'NIBP2010', 'mmHg', \
                                        0, 300, 0, 300, 'None', 15,self.bpdata.sys_list)
            
                Biosignal_pDias = BioSignal('bpdiastole', 'NIBP2010', 'mmHg', \
                                        0, 300, 0, 300, 'None', 15,self.bpdata.dias_list)
                                        
                self.Biosignals.append(Biosignal_pSys)
                self.Biosignals.append(Biosignal_pDias)
#                self.bpdata.sys_list = []
#                self.bpdata.dias_list = []
                nDataRecord = 5
#        self.Biosignals.append(Biosignal_ECG)
        self.Biosignals.append(Biosignal_ECG) 
        self.myedf = edf.EDF(self.patient1, self.Biosignals, self.strDate, self.strStarttime, self.strY2KDate + \
                        ': LifeLink 15 second data of CorScience modules', nDataRecord, 15)
        self.myedf.get(self.patient1)
        print 'EDF creation finished'
        self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.RxFrame.DAQPanel.dbuuid, 'status message', '', 'EDF creation finished')
        self.EDFtoDB()
        self.Biosignals = []

    def EDFtoDB(self):
        """Stores newly created EDF file to the rxbox database
        """
        edf_inst=edfviewer.EDF_File(self.myedf.edfilename)# edf file input
        parsededf=edf_inst.parseDataRecords()
        self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.RxFrame.DAQPanel.dbuuid, 'edf', self.myedf.edfilename[4:-4], parsededf )
    
    def onCall(self, event):
        """Method is called when Call button is toggled
           Calls the CreatePatientRecord Dialog if Patient Information is not yet finalized.
           Shows or Hides the Call/Refer Panel which contains the IM/Video Panels           
        """
        self.on_send = 0
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Requesting connection to triage...")
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Requesting connection to triage...')
        self.timerECG_refresh.Stop()

                        
        if (self.Call_Label.GetLabel() == "<<  ") and (self.referflag == 1) : 
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings... Call Panel Shown.")
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Acquiring biomedical readings... Call Panel Shown.')
            self.RxFrame.ReferPanel.Show()
            self.RxFrame.video_panel.Hide()
            self.Call_Label.SetLabel(">>  ") 
            self.bp_label.SetLabel("BP ") 
            self.heartrate_label.SetLabel("HR ") 
            self.spo2_label.SetLabel("SpO2 ")             
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.RxFrame.Layout()
            
            self.refer_panel_shown = 1
            if self.config.get('bp', 'simulated') == '1' and self.bpdata.systolic_value != '':
                self.bpdata.update_bp_display()
            if self.config.get('bp', 'simulated') == '0' and self.bp_diastolic != '':
                self.bpvalue_label.SetLabel(str(self.bp_systolic)+'/'+str(self.bp_diastolic))

        elif (self.Call_Label.GetLabel() == ">>  ") and (self.referflag == 1) : 
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquring biomedical readings... Call Panel Hidden.")
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Acquring biomedical readings... Call Panel Hidden.')
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
            self.RxFrame.Layout()
            
            self.refer_panel_shown = 0
            if self.config.get('bp', 'simulated') == '1' and self.bpdata.systolic_value != '':
                self.bpdata.update_bp_display()
            if self.config.get('bp', 'simulated') == '0' and self.bp_diastolic != '':
                self.bpvalue_label.SetLabel(str(self.bp_systolic)+'/'+str(self.bp_diastolic))
        else:
#        if (self.Call_Label.GetLabel() == "Call") and (self.referflag == 0):    
            self.bp_label.SetLabel("BP ")
            self.heartrate_label.SetLabel("HR ") 
            self.spo2_label.SetLabel("SpO2 ")
            self.RxFrame.video_panel.Hide()         
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            if self.with_patient_info == 0:
                CreateDialog =CreateRecordDialog2(self.RxFrame, self)
                CreateDialog.ShowModal()
                self.with_patient_info = 1
#            CallAfter(self.RxFrame.CreateReferPanel)
            self.RxFrame.CreateReferPanel()
            self.Call_Label.SetLabel(">>  ")
            self.RxFrame.Layout()
            self.referflag = 1
#            self.RxFrame.init_simvideo()

    def sendEmail(self):
        """Sends an email containing an attachment of biomedical data to a remote server or an email address"""
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Sending Data to Server...")
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Sending Data to Server...')
        t = triage.Triage('triage/email.cfg')
        t.login()
        headers = {'Subject': self.config.get('email', 'mode') + ' ' + self.RxFrame.topic, 'X-Eccs-Priority': 'emergency',
                        'X-Eccs-Rxboxextension': '2001'}
        body = self.RxFrame.body
        afilename = [self.myedf.edfilename]
        attach = {}
        for i in afilename:
                f = open(i, 'r')
                attach[i] = f.read()
                f.close()

        print "sending..\n"
        t.request(headers, body, attach)
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Data Sent...")
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Data Sent...')
        print "sent";

    def onSend(self, event): # wxGlade: DAQPanel.<event_handler>
        """Method is called when Send button is toggled
           Calls the CreatePatientRecord Dialog if if Patient Information is not yet finalized.
           Calls the sendEmail and SendStatus methods. 
        """
        if self.sendcount == 1:
            self.make_edf()
        self.timerECG_refresh.Stop()
        self.on_send = 1
        self.sendcount += 1
        print 'SENDING'
        print self.sendcount
        
        if self.with_patient_info == 0:
            CreateDialog = CreateRecordDialog2(self.RxFrame, self)
            CreateDialog.ShowModal()
            self.with_patient_info = 1
        if self.RxFrame.DAQPanel.on_send == 1:
            self.RxFrame.DAQPanel.timerSend.Start(5000)
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Sending Data to Server...")
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Sending Data to Server...')

        if self.sendcount >= 2:
            self.timerSend.Stop()
            if (self.config.getint('email', 'simulated') == 0):
                self.sendEmail()
                self.show_email_success()
                self.sendcount = 1
            
            elif (self.config.getint('email', 'simulated') == 1):
                self.sendcount = 1
                self.SendStatus(self)

        self.bpNow_Button.Enable(True)
        self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png", wx.BITMAP_TYPE_ANY))
        self.StartStop_Label.SetLabel("Start")
        self.bpNow_Button.Enable(True)
        self.Call_Button.Enable(False)
        self.Send_Button.Enable(False)
        self.lead12_button.Enable(False)
        self.timer_spo2.Stop()
        self.timer_bpdemo.Stop()       
        self.timerECG_refresh.Stop()
        self.timerECGNodeCheck.Stop()
        if self.bp_isCyclic == 1:
			self.timer_bpcyclic.Stop()
			self.bp_isCyclic = 0
        if not self.ECGsimulated:
            self.alive = False
            self.ECGDAQ.stop()
            self.plotter.Close()
        self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
        self.spo2_infolabel.SetLabel('Pulse Ox Ready')
        self.RxFrame.DAQPanel.RemarkValueDaq.SetValue('')
        print 'stopping...'
    
    def show_email_success(self):
        """
        Shows a dialog box that affirms successful sending of data 
        """
        self.RxFrame.RxFrame_StatusBar.SetStatusText("Send to Server Successful")
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Send to Server Successful')
        dlg = wx.MessageDialog(self, "Send to Server Successful", "Send to Server Successful", wx.OK | wx.ICON_QUESTION)
        dlg.ShowModal()
        self.timerECG_refresh.Start(250) 

    def SendStatus(self, event):
        """Shows the status of email sending using a dialog box
        """
        if (self.config.getint('email', 'connection') == 1): 
            print "Send to Server Successful"
            self.show_email_success()

        else:
            print "Send to Server Failed"
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Send to Server Failed")
            self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Send to Server Failed')
            dlg = wx.MessageDialog(self, "Would you like to resend data?", "Send to Server Failed", wx.YES_NO | wx.ICON_QUESTION)
            
            if dlg.ShowModal() == wx.ID_YES:
                self.RxFrame.RxFrame_StatusBar.SetStatusText("Resending data to server...")
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Resending data to server...')
                self.sendcount = 1
                self.timerSend.Start(5000)

        self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")              
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Acquiring biomedical readings...')
        
    def onBPNow(self, event): # wxGlade: MyPanel1.<event_handler>
        """Called when the BP NOW button is toggled
           Calls the get() method from the BP sensor class
        """
        print "on BP now toggled"
        self.bpNow_Button.Enable(False)
        if self.config.get('bp', 'simulated') == '0':
            if self.bp_isCyclic == 1:
                print "cyclic"
                #self.timer_bpcyclic.Stop()
                self.get_bp()
            else:
                print "not cyclic"
                self.get_bp()            
        else:
            self.bpdata.get()
    def get_bpcyclic(self,event):
        """
        Get live cyclic BP reading using interval setting from BP combo box
        Makes use of get_bp() method
        """
        print "get bp cyclic"
        self.get_bp()
            
    def get_bp(self):
        """
        Acquire live one-shot BP reading
        """
        print "get bp"
        self.bp_pressure_indicator.Enable(True)
        self.bpNow_Button.Enable(False)#disable the bp acquire button until the bp reaidng is finished
        self.bp.send_request() #request bp not yet reading
        self.pressure_timer.Start(200)#one shot/ cyclic updates the readings every 200ms
        self.count=1
    
    def bp_status_check(self):
        """Runs the power-on self test (POST) and the device ready checks of BP"""
        self.bp.POST()
        self.bp.device_ready()
        self.bp_infolabel.SetLabel(self.bp.device_message)
        
    def updateBPDisplay(self, data):
	"""Updates the BP reading in the display panel"""
        self.bpvalue_label.SetLabel(data) 
        
    def pressure_update(self,event):
        """Method that handles the inflating bar of blood pressure
        If BP is cyclic, checks the BP combo box and starts BP timer
        If BP is not cyclic, gets one-shot BP reading
        """
        if self.config.get('bp', 'simulated') == '0':
			#updates only for live, 200ms interval
			press = self.bp.get_reply()
			self.bp.nibp.read(1)
			#print "pressure: ", press, " mmHg"
			if ord(press[1])==2:
				return
			press = int(press[1:4])
			#print press
			if press != 999:
				self.bpNow_Button.Enable(False)
				self.bp_pressure_indicator.SetValue(press)
				self.bp_infolabel.SetLabel(str(press)+' mmHg')
				#print str(press)
				self.count=0
				#self.bp_pressure_indicator.SetValue(press)
			else:
				self.bp_pressure_indicator.SetValue(0)
				self.bp_infolabel.SetLabel('BP Acquired')
				self.bp_pressure_indicator.Enable(False)
				self.bpNow_Button.Enable(True)
				self.bp.get() #extract systolic and diastolic pressure readings
				self.pressure_timer.Stop()
				if self.bp_isCyclic == 1:
					print "cyclic BP\n\n\n"
					self.timer_bpcyclic.Stop()
					reload_bp_str = self.setBPmins_combobox.GetValue()
					self.bpreloadlive = int(reload_bp_str[0:2])*1000*12  #60
					self.timer_bpcyclic.Start(self.bpreloadlive)
         
        else:
            #demo
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
            
        
    def startSaveThread (self):
##        """ calls makeEDF.SaveThread.run() """
        event.Skip()

    def on12Lead(self, event): # wxGlade: DAQPanel.<event_handler>
        """event handler of the 12 lead button. When 12 lead button is pressed
        calls the 12 lead dialog window for plotting
        """
        #self.lead12_button.Enable(False)
        CreateDialog2 = Lead12Dialog2(self, self.ECGsimulated, self)
        CreateDialog2.Show()
        if not self.ECGsimulated:
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_I,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['I'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_II,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['II'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_III,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['III'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_aVR,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['VR'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_aVL,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['VL'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_aVF,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['VF'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V1,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['V1'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V2,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['V2'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V3,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['V3'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V4,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['V4'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V5,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['V5'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_V6,mode='small',time=3,cont=False,data=self.ECGDAQ.lead_ecg['V6'][-1500:])
            plot1 = CPlotter(CreateDialog2,panel=CreateDialog2.plotter_bigII,mode='extend',time=15,cont=False,data=self.ECGDAQ.lead_ecg['II'][-7500:])
        
    def onECGNodeCheck(self, x): 
        """Electrode contact measurement (ECM) check"""
        self.timerECGNodeCheck.Start(250)
        if not self.ECGsimulated:
            self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")            
            self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.RxFrame.DAQPanel.dbuuid, 'status message', '', 'Acquiring biomedical readings...')
            self.timerECGNodeCheck.Stop()    
            self.nodetimer = 0
        else:
            self.timerECGNodeCheck.Start(250)
            self.nodetimer = self.nodetimer + 1
            if (self.nodetimer == 1):
                self.RxFrame.RxFrame_StatusBar.SetStatusText("Checking Node Placement of ECG...")
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Checking Node Placement of ECG...')
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
                self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.RxFrame.DAQPanel.dbuuid, 'status message', '', 'Acquiring biomedical readings...')
                self.timerECGNodeCheck.Stop()    
                self.nodetimer = 0
                self.timerECG_refresh.Start(125)         

class CreateRecordDialog2(CreateRecordDialog):
    """ Class for Create Record Dialog instance and methods
    
    Methods:
        __init__(CreateRecordDialog) 
        OnCreateRecord        
         
    """
    def __init__(self, parent, *args, **kwds):
        """Patient data from Information Panel is copied to their respective fields in the Patient Record Dialog
        - Sets necessary variables
        
        Arguments: __init__(CreateRecordDialog)
        
        """
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
        """
        Updates the Patient Information Panel when the Create Record Button is toggled
        """
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
           
        self.RxFrame.topic = self.ReferralTopic_TextCtrl.GetValue()
        self.RxFrame.reason = self.ReferralReason_Combo.GetValue()
        self.RxFrame.remarks = self.RemarkValue.GetValue()        
        check_valid = self.check_patient_valid(FirstName, MiddleName, LastName, Gender, Age,\
                                            Birth, Validity, self.RxFrame.topic, self.RxFrame.reason)
        
        if (check_valid == 1):
            self.Destroy()
            self.RxFrame.DAQPanel.DisablePatient()
            self.RxFrame.DAQPanel.with_patient_info = 1
            self.RxFrame.DAQPanel.rxboxDB.dbpatientinsert('patients', 'lastname', 'firstname', \
                'middlename', 'address', 'phonenumber', 'age', 'birth', 'gender', 'uuid', \
                LastName, FirstName, MiddleName, Address, Phone, Age, Birth, Gender, self.RxFrame.DAQPanel.dbuuid)

            if self.RxFrame.DAQPanel.on_send == 0:
 #               CallAfter(self.RxFrame.CreateReferPanel)
                self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings... Call Panel Initiated.")
                self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.RxFrame.DAQPanel.dbuuid, 'status message', '', 'Acquiring biomedical readings... Call Panel Initiated.')
            
    def check_patient_valid(self, firstname, middlename, lastname, gender, age, birth, validity, topic, reason):
        """Checks if the required fields in the create patient record are filled-up
        """
        if ((firstname == '')|(middlename == '')|(lastname == '')|(gender == '')|(age == '')|(birth == '')|(validity == '')|(topic == '')|(reason == '')):
            return 0
        else:
            return 1
        
class Lead12Dialog2(Lead12Dialog):
    """ Class that creates the 12 Lead Dialog Window where the 12 leads will be plotted
    
    Methods:
        __init__(Lead12Dialog)         
         
    """   
    def __init__(self, parent, ECGSimulated, *args, **kwds):
        """ initializes the placement of the plotter to the 12 lead dialog window

        Parameters
        ----------
        parent  :  the main window which calls the creation of the dialog window

        """
        
        Lead12Dialog.__init__(self, *args, **kwds)
        self.parent = parent
        sizersize = self.leadI_sizer.GetSize()
        bigsizer = self.leadII_sizer.GetSize()
        if ECGSimulated:
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
        else:
            self.plotter_I = wx.Panel(self)
            self.plotter_II = wx.Panel(self)
            self.plotter_III = wx.Panel(self)
            self.plotter_aVR = wx.Panel(self)
            self.plotter_aVL = wx.Panel(self)
            self.plotter_aVF = wx.Panel(self)
            self.plotter_V1 = wx.Panel(self)
            self.plotter_V2 = wx.Panel(self)
            self.plotter_V3 = wx.Panel(self)
            self.plotter_V4 = wx.Panel(self)
            self.plotter_V5 = wx.Panel(self)
            self.plotter_V6 = wx.Panel(self)
            self.plotter_bigII = wx.Panel(self)
        
            self.leadI_sizer.Add(self.plotter_I, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.small_leadII_sizer.Add(self.plotter_II, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.leadIII_sizer.Add(self.plotter_III, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.aVR_sizer.Add(self.plotter_aVR, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.aVL_sizer.Add(self.plotter_aVL, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.aVF_sizer.Add(self.plotter_aVF, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.V1_sizer.Add(self.plotter_V1, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.V2_sizer.Add(self.plotter_V2, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.V3_sizer.Add(self.plotter_V3, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.V4_sizer.Add(self.plotter_V4, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.V5_sizer.Add(self.plotter_V5, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.V6_sizer.Add(self.plotter_V6, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
            self.leadII_sizer.Add(self.plotter_bigII, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)        
            
# end of rxboxGUI classes

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = RxFrame2(None, -1, "")
    app.SetTopWindow(rx_frame)
    rx_frame.Maximize(True)
    splash_app = SplashApp2(None)
    rx_frame.Show()
    app.MainLoop()



        


