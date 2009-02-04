#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# generated by wxGlade 0.6.1 on Sat Nov 24 08:01:52 2007

import sys
sys.path.append('../modules')

import wx
import threading
#import serial
import os
import time
import matplotlib

import Dialogs
import AcquireData

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg,Toolbar

from matplotlib.figure  import Figure
from matplotlib.numerix import arange

from Linphone import Linphone
from Messenger import Messenger
from TriageClient import Triage

LINEWIDTH       = 3.0           # line width for the plot
LINECOLOR       = '#FF351A'     # line color for the plot (red color)
SAMPLES         = 1000          # x-axis
BUF_SAMPLES     = 30            # number of buffer samples before redrawing the matplotlib canvas

SERIAL_PORT     = '/dev/ttyS1'
BAUDRATE        = 57600
SOCK_HOST       = ''
DATA_SOCK_PORT  = 50014
IM_SOCK_PORT    = 50015
BUFSIZ          = 8192
VIDEO_HOST      = ''
VIDEO_PORT      = 1234

RQT_MSSG        = 'TELEMED'
PKY_MSSG        = '1234'
WEL_MSSG        = RQT_MSSG + ' ' + PKY_MSSG
VFY_MSSG        = 'READY TO RECEIVE'
REF_MSSG        = 'CONNECTION REFUSED'
FIN_MSSG        = 'FINISHED TRANSMISSION'

CONN_TIMEOUT    = 20
DATA_TIMEOUT    = 10

PGH_DOMAIN	= '192.168.0.102'
PGH_JID		= '2001@192.168.0.102'
PGH_PWD		= '12345'
IMFONTSIZE	= 10


class Plotter():
    def __init__(self, parent):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.t = arange(0.0, SAMPLES, 1)
        self.data = [0.0 for i in range (SAMPLES)]
        self.line, = self.axes.plot(self.t, self.data, 'r', linewidth = LINEWIDTH, color = LINECOLOR)
        self.canvas = FigureCanvas(parent, -1, self.figure)
        self.axes.grid(True)


class MyPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
                
        self.sizer_4    = wx.StaticBox(self, -1, "")
        self.sizer_5    = wx.StaticBox(self, -1, "")
        self.sizer_6    = wx.StaticBox(self, -1, "")
        self.sizer_2    = wx.StaticBox(self, -1, "")
        self.ecg_header     = wx.StaticText(self, -1, "ECG Waveform", style=wx.ALIGN_CENTRE)
        self.spo2_header    = wx.StaticText(self, -1, "Blood-Oxygen \nSaturation", style=wx.ALIGN_CENTRE)
        self.spo2           = wx.StaticText(self, -1, "00", style=wx.ALIGN_CENTRE)
        self.spo2_unit      = wx.StaticText(self, -1, "%SpO2", style=wx.ALIGN_RIGHT)
        self.bp_header      = wx.StaticText(self, -1, "Blood Pressure", style=wx.ALIGN_CENTRE)
        self.bp             = wx.StaticText(self, -1, "0/0", style=wx.ALIGN_CENTRE)
        self.bp_unit        = wx.StaticText(self, -1, "mmHg", style=wx.ALIGN_RIGHT)
        self.bpm_header     = wx.StaticText(self, -1, "Heart Rate", style=wx.ALIGN_CENTRE)
        self.bpm            = wx.StaticText(self, -1, "00", style=wx.ALIGN_CENTRE)
        self.bpm_unit       = wx.StaticText(self, -1, "bpm", style=wx.ALIGN_RIGHT)

        self.ecg_plotter = Plotter(self)
        self.ecg_plotter.axes.set_ylim(0.1, 2.1)
        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_PAINT, self.updatePlots)
	
    # updates the value of SpO2, BPM and ECG data   
    def updatePlots(self, event):
        self.ecg_plotter.canvas.draw()
        if event is not None:
            event.Skip()

    def UpdateSpO2Display(self, data):
        self.spo2.SetLabel(data)
        
    def UpdateBPMDisplay(self, data):
        self.bpm.SetLabel(data)	
         
    def __set_properties(self):
        self.ecg_plotter.canvas.SetMinSize((100, 200))
        self.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.ecg_header.SetMinSize((60, 20))
        self.ecg_header.SetBackgroundColour(wx.Colour(216, 191, 216))
        self.ecg_header.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.spo2_header.SetMinSize((60, 30))
        self.spo2_header.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2_header.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.spo2.SetMinSize((60, 40))
        self.spo2.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.spo2_unit.SetMinSize((60, 20))
        self.spo2_unit.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2_unit.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bp_header.SetMinSize((60, 30))
        self.bp_header.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bp_header.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bp.SetMinSize((60, 40))
        self.bp.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bp.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bp_unit.SetMinSize((60, 20))
        self.bp_unit.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bp_unit.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bpm_header.SetMinSize((60, 30))
        self.bpm_header.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpm_header.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bpm.SetMinSize((60, 40))
        self.bpm.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpm.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bpm_unit.SetMinSize((60, 20))
        self.bpm_unit.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpm_unit.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.StaticBoxSizer(self.sizer_6, wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5, wx.VERTICAL)
        sizer_4 = wx.StaticBoxSizer(self.sizer_4, wx.VERTICAL)
        sizer_2 = wx.StaticBoxSizer(self.sizer_2, wx.VERTICAL)
        sizer_2.Add(self.ecg_header, 0, wx.ALL|wx.EXPAND, 2)
        sizer_2.Add(self.ecg_plotter.canvas, 1, wx.ALL|wx.EXPAND, 2) # add canvas
        sizer_4.Add(self.spo2_header, 0, wx.ALL|wx.EXPAND, 2)
        sizer_4.Add(self.spo2, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 2)
        sizer_4.Add(self.spo2_unit, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 2)
        sizer_5.Add(self.bp_header, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_5.Add(self.bp, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_5.Add(self.bp_unit, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 2)
        sizer_6.Add(self.bpm_header, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_6.Add(self.bpm, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_6.Add(self.bpm_unit, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 2)
        sizer_3.Add(sizer_4, 1, wx.LEFT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_3.Add(sizer_5, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_3.Add(sizer_6, 1, wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_1.Add((20, 2), 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 0, wx.ALL|wx.EXPAND, 4)
        sizer_1.Add((20, 2), 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        
class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.phone = Linphone(self)
	self.messenger = Messenger(self, PGH_JID, PGH_PWD)
	self.messenger.start()
        self.threads = []
        self.video_threads = []
        self.conn_threads = []
        self.count = 0
        self.video_count = 0
        self.im_count = 0
        self.conn_count = 0
        
        self.user_config = {'input_method':'Web Service',
                            'serial_port':SERIAL_PORT,
                            'baud_rate':str(BAUDRATE),
                            'file_input':'',
                            'file_output': '',
                            'ip_host':SOCK_HOST,
                            'ip_port':str(DATA_SOCK_PORT),
                            'video_ip_port':str(VIDEO_PORT)}
        self.addr =  None
        self.data_sock = None
        self.im_sock = None
        self.newsock = None        

        # copy to __init__ of Telemed 2 code : start
        self.Tab_General = wx.Notebook(self, -1, style=0)
        self.Tab_Patient = wx.Panel(self.Tab_General, -1, style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.Tab_Hospital = wx.Panel(self.Tab_General, -1, style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.Tab_Interlocutor = wx.Panel(self.Tab_General, -1, style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        self.Tab_Referral = wx.Panel(self.Tab_General, -1, style=wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)
        # copy to __init__ of Telemed 2 code : end
        
        self.__set_menu()               # define menu bar
        self.__set_init_statusdisplay() # status bar
        self.__set_textdisplay()        # define text display & sizers
        self.__set_properties()         # set display properties
        self.__do_layout()              # gui layout
        self.__bind_events()

    def __set_menu(self):
        self.Main_Menu = wx.MenuBar()
        self.SetMenuBar(self.Main_Menu)
        
        self.File = wx.Menu()
        self.Help = wx.Menu()
                
        self.Start_Videoconf    = wx.MenuItem(self.File, wx.NewId(),    "Start &Videoconference", "",       wx.ITEM_NORMAL)
        self.Start_Acquire      = wx.MenuItem(self.File, wx.NewId(),    "Start Data &Acquisition\tf2", "",  wx.ITEM_NORMAL)
        self.Save_To_File       = wx.MenuItem(self.File, wx.NewId(),    "Save To &File\tf12", "",           wx.ITEM_NORMAL)
        self.Stop_Acquire       = wx.MenuItem(self.File, wx.NewId(),    "Sto&p Data Acquisition\tf3", "",   wx.ITEM_NORMAL)
        self.Exit               = wx.MenuItem(self.File, wx.NewId(),    "E&xit\tCtrl-q", "",                wx.ITEM_NORMAL)
        self.About              = wx.MenuItem(self.Help,wx.NewId(),     "&About","",                        wx.ITEM_NORMAL)

        self.Main_Menu.Append(self.File, "&File")
        self.Main_Menu.Append(self.Help, "&Help")
        self.File.AppendItem(self.Start_Videoconf)
        self.File.AppendSeparator()
        self.File.AppendItem(self.Start_Acquire)
        self.File.AppendItem(self.Save_To_File)
        self.File.AppendItem(self.Stop_Acquire)
        self.File.AppendSeparator()
        self.File.AppendItem(self.Exit)
        self.Help.AppendItem(self.About)
        
    def __set_init_statusdisplay(self):
        self.statusbar = self.CreateStatusBar(1, 0)
        self.statusbar.SetStatusText("Program Ready.", 0)

    def __set_textdisplay(self):
        self.sizer_19_staticbox = wx.StaticBox(self, -1, "")
        self.sizer_20_staticbox = wx.StaticBox(self, -1, "")
        self.sizer_17_staticbox = wx.StaticBox(self, -1, "")
        self.sizer_5_staticbox  = wx.StaticBox(self, -1, "")   

        # copy to __set_textdisplay of Telemed 2 code : start
        self.Label_ReferralTopic = wx.StaticText(self.Tab_Referral, -1, "Topic of Referral")
        self.TextCtrl_ReferralTopic = wx.TextCtrl(self.Tab_Referral, -1, "")
        self.Label_ReferralReason = wx.StaticText(self.Tab_Referral, -1, "Reason of Referral")
        self.Choice_ReferralReason = wx.Choice(self.Tab_Referral, -1, choices=["Case", "Incident", "Request"])
        self.Label_InterlocutorFirstName = wx.StaticText(self.Tab_Interlocutor, -1, "First Name")
        self.TextCtrl_InterlocutorFirstName = wx.TextCtrl(self.Tab_Interlocutor, -1, "")
        self.Label_InterlocutorLastName = wx.StaticText(self.Tab_Interlocutor, -1, "Last Name", style=wx.ALIGN_RIGHT)
        self.TextCtrl_InterlocutorLastName = wx.TextCtrl(self.Tab_Interlocutor, -1, "")
        self.Label_InterlocutorPhoneNumber = wx.StaticText(self.Tab_Interlocutor, -1, "PhoneNumber")
        self.TextCtrl_InterlocutorPhoneNumber = wx.TextCtrl(self.Tab_Interlocutor, -1, "")
        self.Label_HospitalName = wx.StaticText(self.Tab_Hospital, -1, "Name")
        self.TextCtrl_HospitalName = wx.TextCtrl(self.Tab_Hospital, -1, "")
        self.Label_HospitalNumber = wx.StaticText(self.Tab_Hospital, -1, "Phone Number")
        self.TextCtrl_HospitalNumber = wx.TextCtrl(self.Tab_Hospital, -1, "")
        self.Label_HospitalAddress = wx.StaticText(self.Tab_Hospital, -1, "Address")
        self.TextCtrl_HospitalAddress = wx.TextCtrl(self.Tab_Hospital, -1, "", style=wx.TE_MULTILINE)
        self.Label_HospitalCity = wx.StaticText(self.Tab_Hospital, -1, "City", style=wx.ALIGN_RIGHT)
        self.TextCtrl_HospitalCity = wx.TextCtrl(self.Tab_Hospital, -1, "")
        self.Label_PatientLastName = wx.StaticText(self.Tab_Patient, -1, "Last Name")
        self.TextCtrl_PatientLastName = wx.TextCtrl(self.Tab_Patient, -1, "")
        self.Label_PatientFirstName = wx.StaticText(self.Tab_Patient, -1, "First Name")
        self.TextCtrl_PatientFirstName = wx.TextCtrl(self.Tab_Patient, -1, "")
        self.Label_PatientMI = wx.StaticText(self.Tab_Patient, -1, "MI", style=wx.ALIGN_RIGHT)
        self.TextCtrl_PatientMI = wx.TextCtrl(self.Tab_Patient, -1, "")
        self.Label_PatientAge = wx.StaticText(self.Tab_Patient, -1, "Age")
        self.TextCtrl_PatientAge = wx.TextCtrl(self.Tab_Patient, -1, "")
        self.Choice_PatientAgeDMY = wx.Choice(self.Tab_Patient, -1, choices=["Days", "Months", "Years"])
        self.Choice_PatientAgeValidity = wx.Choice(self.Tab_Patient, -1, choices=["Known", "Unknown", "Estimated"])
        self.Label_PatientGender = wx.StaticText(self.Tab_Patient, -1, "Gender", style=wx.ALIGN_RIGHT)
        self.Choice_PatientGender = wx.Choice(self.Tab_Patient, -1, choices=["Male", "Female"])
        self.Label_PatientAddress = wx.StaticText(self.Tab_Patient, -1, "Address")
        self.TextCtrl_PatientAddress = wx.TextCtrl(self.Tab_Patient, -1, "", style=wx.TE_MULTILINE)
        self.Label_PatientNumber = wx.StaticText(self.Tab_Patient, -1, "Phone Number")
        self.TextCtrl_PatientNumber = wx.TextCtrl(self.Tab_Patient, -1, "")
        # copy to __set_textdisplay of Telemed 2 code : end

        self.video_header   = wx.StaticText(self, -1, "Video Conference", style=wx.ALIGN_CENTRE)
        self.im_header      = wx.StaticText(self, -1, "Instant Messenger", style=wx.ALIGN_CENTRE)
        self.start_button   = wx.Button(self, -1, "Start")
        self.stop_button    = wx.Button(self, -1, "Stop")
        self.save_button    = wx.Button(self, -1, "Save")
        self.video_button   = wx.Button(self, -1, "Awaiting call..")
        self.datapanel      = MyPanel(self, -1)
        self.im_panel       = wx.Panel(self, -1, style=wx.TAB_TRAVERSAL)
        self.video_panel   = wx.Panel(self, -1, style=wx.TAB_TRAVERSAL)
        self.reply_text     = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.im_messages  = wx.TextCtrl(self.im_panel, -1, style=wx.TE_MULTILINE)
	self.im_messages.SetEditable(False)

        self.stop_button.Enable(False)
        self.start_button.Enable(False)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("TeleMed III - Doctor's Workstation")
        self.SetSize((1000, 700))       # changed from 640 to 700
        self.SetBackgroundColour(wx.Colour(239, 235, 239))

        # copy to __set_properties of Telemed 2 code : start
        self.Label_ReferralTopic.SetMinSize((140, 16))
        self.Label_ReferralTopic.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_ReferralTopic.SetMinSize((365, 24))
        self.TextCtrl_ReferralTopic.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_ReferralReason.SetMinSize((140, 16))
        self.Label_ReferralReason.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.Choice_ReferralReason.SetMinSize((100, 24))
        self.Choice_ReferralReason.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Choice_ReferralReason.SetSelection(0)
        self.Tab_Referral.SetMinSize((504, 96))
        self.Tab_Referral.SetBackgroundColour(wx.Colour(202, 201, 255))
        self.Label_InterlocutorFirstName.SetMinSize((50, 16))
        self.Label_InterlocutorFirstName.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_InterlocutorFirstName.SetMinSize((190, 24))
        self.TextCtrl_InterlocutorFirstName.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_InterlocutorLastName.SetMinSize((75, 16))
        self.Label_InterlocutorLastName.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_InterlocutorLastName.SetMinSize((120, 24))
        self.TextCtrl_InterlocutorLastName.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_InterlocutorPhoneNumber.SetMinSize((95, 16))
        self.Label_InterlocutorPhoneNumber.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_InterlocutorPhoneNumber.SetMinSize((90, 24))
        self.TextCtrl_InterlocutorPhoneNumber.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Tab_Interlocutor.SetBackgroundColour(wx.Colour(202, 201, 255))
        self.Label_HospitalName.SetMinSize((50, 16))
        self.Label_HospitalName.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_HospitalName.SetMinSize((220, 24))
        self.TextCtrl_HospitalName.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_HospitalNumber.SetMinSize((95, 16))
        self.Label_HospitalNumber.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_HospitalNumber.SetMinSize((115, 24))
        self.TextCtrl_HospitalNumber.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_HospitalAddress.SetMinSize((50, 16))
        self.Label_HospitalAddress.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_HospitalAddress.SetMinSize((220, 45))
        self.TextCtrl_HospitalAddress.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_HospitalCity.SetMinSize((45, 16))
        self.Label_HospitalCity.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_HospitalCity.SetMinSize((115, 24))
        self.TextCtrl_HospitalCity.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Tab_Hospital.SetBackgroundColour(wx.Colour(202, 201, 255))
        self.Label_PatientLastName.SetMinSize((68, 16))
        self.Label_PatientLastName.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_PatientLastName.SetMinSize((115, 24))
        self.TextCtrl_PatientLastName.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_PatientFirstName.SetMinSize((70, 16))
        self.Label_PatientFirstName.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_PatientFirstName.SetMinSize((160, 24))
        self.TextCtrl_PatientFirstName.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_PatientMI.SetMinSize((25, 16))
        self.Label_PatientMI.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_PatientMI.SetMinSize((30, 24))
        self.TextCtrl_PatientMI.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_PatientAge.SetMinSize((68, 16))
        self.Label_PatientAge.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_PatientAge.SetMinSize((33, 21))
        self.TextCtrl_PatientAge.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Choice_PatientAgeDMY.SetMinSize((65, 21))
        self.Choice_PatientAgeDMY.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Choice_PatientAgeDMY.SetSelection(0)
        self.Choice_PatientAgeValidity.SetMinSize((75, 21))
        self.Choice_PatientAgeValidity.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Choice_PatientAgeValidity.SetSelection(0)
        self.Label_PatientGender.SetMinSize((120, 16))
        self.Label_PatientGender.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.Choice_PatientGender.SetMinSize((73, 21))
        self.Choice_PatientGender.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Choice_PatientGender.SetSelection(0)
        self.Label_PatientAddress.SetMinSize((68, 16))
        self.Label_PatientAddress.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_PatientAddress.SetMinSize((210, 24))
        self.TextCtrl_PatientAddress.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Label_PatientNumber.SetMinSize((95, 16))
        self.Label_PatientNumber.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.TextCtrl_PatientNumber.SetMinSize((110, 24))
        self.TextCtrl_PatientNumber.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.Tab_Patient.SetMinSize((504, 96))
        self.Tab_Patient.SetBackgroundColour(wx.Colour(202, 201, 255))
        self.Tab_General.SetMinSize((512, 125))
        self.Tab_General.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.Tab_General.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        # copy to __set_properties of Telemed 2 code : end

        self.video_header.SetMinSize((60, 20))
        self.video_header.SetBackgroundColour(wx.Colour(255, 251, 159))
        self.video_header.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.im_header.SetMinSize((60, 20))
        self.im_header.SetBackgroundColour(wx.Colour(255, 214, 0))
        self.im_header.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.start_button.SetMinSize((79, 30))
        self.start_button.SetBackgroundColour(wx.Colour(209, 255, 111))
        self.start_button.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.stop_button.SetMinSize((79, 30))
        self.stop_button.SetBackgroundColour(wx.Colour(255, 90, 119))
        self.stop_button.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.save_button.SetMinSize((79, 30))
        self.save_button.SetBackgroundColour(wx.Colour(185, 209, 255))
        self.save_button.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.video_button.SetMinSize((160, 30))
        self.video_button.SetBackgroundColour(wx.Colour(252, 255, 111))
        self.video_button.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
	self.video_button.Enable(False)
        self.im_panel.SetMinSize((270, 190))
        self.video_panel.SetMinSize((352, 288))
        self.reply_text.SetMinSize((275, 45))
	self.im_messages.SetBackgroundColour(wx.Colour(255, 252, 239))
        self.im_messages.SetMinSize((270, 185))
        self.im_messages.SetFont(wx.Font(IMFONTSIZE, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Courier"))

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1     = wx.BoxSizer(wx.VERTICAL)
        sizer_2     = wx.BoxSizer(wx.VERTICAL)
        sizer_17    = wx.StaticBoxSizer(self.sizer_17_staticbox, wx.HORIZONTAL)
        sizer_3     = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18    = wx.BoxSizer(wx.VERTICAL)
        sizer_20    = wx.StaticBoxSizer(self.sizer_20_staticbox, wx.VERTICAL)
        sizer_19    = wx.StaticBoxSizer(self.sizer_19_staticbox, wx.VERTICAL)
        sizer_4     = wx.BoxSizer(wx.VERTICAL)
        sizer_12    = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_im = wx.BoxSizer(wx.VERTICAL)
        sizer_3_im = wx.BoxSizer(wx.VERTICAL)
	sizer_4     = wx.BoxSizer(wx.VERTICAL)

        # copy to __do_layout of Telemed 2 code : start
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_7 = wx.FlexGridSizer(1, 4, 0, 0)
        grid_sizer_6 = wx.FlexGridSizer(1, 6, 0, 0)
        grid_sizer_5 = wx.FlexGridSizer(1, 6, 0, 0)
        grid_sizer_4 = wx.FlexGridSizer(2, 4, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(2, 4, 0, 0)
        grid_sizer_1 = wx.FlexGridSizer(2, 2, 0, 0)
        
        grid_sizer_1.Add(self.Label_ReferralTopic, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.TextCtrl_ReferralTopic, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 4)
        grid_sizer_1.Add(self.Label_ReferralReason, 0, wx.ALL, 4)
        grid_sizer_1.Add(self.Choice_ReferralReason, 1, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        self.Tab_Referral.SetSizer(grid_sizer_1)
        grid_sizer_2.Add(self.Label_InterlocutorFirstName, 0, wx.ALL, 4)
        grid_sizer_2.Add(self.TextCtrl_InterlocutorFirstName, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_2.Add(self.Label_InterlocutorLastName, 0, wx.ALL, 4)
        grid_sizer_2.Add(self.TextCtrl_InterlocutorLastName, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_2.Add(self.Label_InterlocutorPhoneNumber, 0, wx.ALL, 4)
        grid_sizer_2.Add(self.TextCtrl_InterlocutorPhoneNumber, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_2.Add((20, 20), 0, 0, 0)
        grid_sizer_2.Add((20, 20), 0, 0, 0)
        self.Tab_Interlocutor.SetSizer(grid_sizer_2)
        grid_sizer_4.Add(self.Label_HospitalName, 0, wx.ALL, 4)
        grid_sizer_4.Add(self.TextCtrl_HospitalName, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_4.Add(self.Label_HospitalNumber, 0, wx.ALL, 4)
        grid_sizer_4.Add(self.TextCtrl_HospitalNumber, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_4.Add(self.Label_HospitalAddress, 0, wx.ALL, 4)
        grid_sizer_4.Add(self.TextCtrl_HospitalAddress, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_4.Add(self.Label_HospitalCity, 0, wx.ALL|wx.ALIGN_RIGHT, 4)
        grid_sizer_4.Add(self.TextCtrl_HospitalCity, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        self.Tab_Hospital.SetSizer(grid_sizer_4)
        grid_sizer_5.Add(self.Label_PatientLastName, 0, wx.ALL, 4)
        grid_sizer_5.Add(self.TextCtrl_PatientLastName, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_5.Add(self.Label_PatientFirstName, 0, wx.ALL, 4)
        grid_sizer_5.Add(self.TextCtrl_PatientFirstName, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        grid_sizer_5.Add(self.Label_PatientMI, 0, wx.ALL, 4)
        grid_sizer_5.Add(self.TextCtrl_PatientMI, 0, wx.RIGHT|wx.TOP|wx.BOTTOM, 4)
        sizer_11.Add(grid_sizer_5, 1, wx.EXPAND, 0)
        grid_sizer_6.Add(self.Label_PatientAge, 0, wx.LEFT|wx.RIGHT|wx.TOP, 4)
        grid_sizer_6.Add(self.TextCtrl_PatientAge, 0, wx.RIGHT|wx.TOP, 4)
        grid_sizer_6.Add(self.Choice_PatientAgeDMY, 0, wx.RIGHT|wx.TOP, 4)
        grid_sizer_6.Add(self.Choice_PatientAgeValidity, 0, wx.RIGHT|wx.TOP, 4)
        grid_sizer_6.Add(self.Label_PatientGender, 0, wx.LEFT|wx.RIGHT|wx.TOP, 4)
        grid_sizer_6.Add(self.Choice_PatientGender, 0, wx.RIGHT|wx.TOP, 4)
        sizer_11.Add(grid_sizer_6, 1, 0, 0)
        grid_sizer_7.Add(self.Label_PatientAddress, 0, wx.LEFT|wx.RIGHT, 4)
        grid_sizer_7.Add(self.TextCtrl_PatientAddress, 0, wx.RIGHT, 4)
        grid_sizer_7.Add(self.Label_PatientNumber, 0, wx.RIGHT, 4)
        grid_sizer_7.Add(self.TextCtrl_PatientNumber, 0, wx.RIGHT, 4)
        sizer_11.Add(grid_sizer_7, 1, wx.BOTTOM|wx.EXPAND, 2)
        self.Tab_Patient.SetSizer(sizer_11)
        self.Tab_General.AddPage(self.Tab_Referral, "Referral")
        self.Tab_General.AddPage(self.Tab_Interlocutor, "Interlocutor")
        self.Tab_General.AddPage(self.Tab_Hospital, "Hospital/Institution/Organization")
        self.Tab_General.AddPage(self.Tab_Patient, "Patient's Information")
        sizer_5.Add(self.Tab_General, 0, wx.ALL, 4)
        # copy to __do_layout of Telemed 2 code : end
        
        sizer_2.Add((20, 10), 0, wx.EXPAND, 0)
        sizer_3.Add((10, 10), 0, wx.EXPAND, 0)
        
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_4.Add((20, 10), 0, wx.EXPAND, 0)
        sizer_4.Add(self.datapanel, 0, wx.EXPAND)
        sizer_4.Add(sizer_12, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_3.Add((20, 10), 0, wx.EXPAND, 0)
        sizer_19.Add(self.video_header, 0, wx.ALL|wx.EXPAND, 4)
        sizer_18.Add(sizer_19, 0, wx.EXPAND, 0)
        sizer_18.Add((20, 10), 0, wx.EXPAND, 0)
        sizer_3_im.Add(self.im_messages, 0, wx.ALL|wx.EXPAND, 4)
        self.im_panel.SetSizer(sizer_3_im)
        sizer_4_im.Add(self.reply_text, 0, wx.ALL|wx.EXPAND, 4)
        sizer_20.Add(self.im_header, 0, wx.ALL|wx.EXPAND|wx.GROW, 4)
        sizer_20.Add(self.im_panel, 1, wx.EXPAND, 0)
        sizer_19.Add(self.video_panel, 1, wx.EXPAND, 0)
        sizer_3.Add((10, 4), 0, wx.EXPAND, 0)
        sizer_20.Add(sizer_4_im, 0, wx.EXPAND, 0)
        sizer_18.Add(sizer_20, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_18, 1, wx.EXPAND, 0)
        sizer_3.Add((10, 10), 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_2.Add((20, 10), 0, wx.EXPAND, 0)
        sizer_17.Add(self.start_button, 0, wx.ALL, 2)
        sizer_17.Add((30, 20), 0, wx.EXPAND, 0)
        sizer_17.Add(self.stop_button, 0, wx.ALL, 2)
        sizer_17.Add((30, 20), 0, wx.EXPAND, 0)
        sizer_17.Add(self.save_button, 0, wx.ALL, 2)
        sizer_17.Add((485, 20), 0, 0, 0)
        sizer_17.Add((30, 20), 0, wx.EXPAND, 0)
        sizer_17.Add(self.video_button, 0, wx.ALL, 2)
        sizer_2.Add(sizer_17, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        sizer_2.Add((20, 10), 0, 0, 0)
        sizer_1.Add(sizer_2, 1, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(sizer_1)
        self.Layout()

    def __init_connection(self):
        self.statusbar.SetStatusText("Waiting for RxBox...", 0)
	
	#ALL Threads removed, please reinstate necessary threads --jerome
       	# connthread = InitConn.InitConnThread(self.conn_count, self)
       	#self.conn_threads.append(connthread)
       	#connthread.start()

    
    def __bind_events(self):
        self.Bind(wx.EVT_MENU,      self.onStartAcquire_MenuClick,      self.Start_Acquire)
        self.Bind(wx.EVT_MENU,      self.onStopAcquire_MenuClick,       self.Stop_Acquire)
        self.Bind(wx.EVT_MENU,      self.onSaveToFile_MenuClick,        self.Save_To_File)
        self.Bind(wx.EVT_MENU,      self.onStartVideoconf_MenuClick,    self.Start_Videoconf)
        self.Bind(wx.EVT_MENU,      self.onAbout_MenuClick,             self.About)
        self.Bind(wx.EVT_MENU,      self.onCloseWindow,                 self.Exit)
        self.Bind(wx.EVT_BUTTON,    self.onStartAcquire_MenuClick,      self.start_button)
        self.Bind(wx.EVT_BUTTON,    self.onStopAcquire_MenuClick,       self.stop_button)
        self.Bind(wx.EVT_BUTTON,    self.onSaveToFile_MenuClick,        self.save_button)
        self.Bind(wx.EVT_BUTTON,      self.onStartVideoconf_MenuClick,    self.video_button)
        self.Bind(wx.EVT_TEXT_ENTER,self.onIMReply_ButtonClick,         self.reply_text)
        self.Bind(wx.EVT_CLOSE,     self.onCloseWindow)

        #Bind phone events
        self.Bind(self.phone.EVT_CALL_INCOMING, self.onCallIncoming)
        self.Bind(self.phone.EVT_CALL_TERMINATED, self.onCallTerminated)
        self.Bind(self.phone.EVT_CALL_FAILED, self.onCallFailed)
        self.Bind(self.phone.EVT_CALL_ANSWERED, self.onCallAnswered)


    def onCallIncoming(self, event):
        self.Start_Videoconf.Enable(True)
        self.video_button.Enable(True)
	self.video_button.SetLabel(label='Answer incoming call')
	
	self.messenger.setRecipient(event.caller + '@' + PGH_DOMAIN)
	
	## While ringinng, patient info should be fetched ##
	## FIXME: Patient id and case id should come from the signalling protocol ##
	#The following are temporary methods:
	#triage.getLatestPatient()
	#triage.getLatestCase(ofpatient)
	
	#This web service method is temporary until a signaling protocol
	# is drafted --jerome
	data = Triage().getLatestPatient()
	self.TextCtrl_PatientLastName.SetValue(data[3])
        self.TextCtrl_PatientFirstName.SetValue(data[1])
        self.TextCtrl_PatientMI.SetValue(data[2])
        self.TextCtrl_PatientAge.SetValue(data[7])
        self.Choice_PatientAgeValidity.SetStringSelection(data[8])
        self.Choice_PatientGender.SetStringSelection(data[5])
        self.TextCtrl_PatientAddress.SetValue(data[9])
	
	#This web service method is temporary until a signaling protocol
	# is drafted --jerome
	data = Triage().getLatestCase()
	self.TextCtrl_ReferralTopic.SetValue(data[1])
	self.Choice_ReferralReason.SetValue(data[2])
	self.TextCtrl_HospitalName.SetValue(data[5])       

	

    def onCallAnswered(self, event):
	self.video_button.SetLabel(label='Disengage')
	self.im_messages.Clear()
	
	## Start acquiring telemetry data ##
	self.count += 1
        print 'count = ', self.count
        self.statusbar.SetStatusText("Acquiring Data...", 0)
      
        # creating a thread
        thread = AcquireData.AcquireDataThr(self.count, self)
        self.threads.append(thread)
        # starting the thread
        thread.start()
        self.onClickStart()
	        
	
    def onCallTerminated(self, event):
        self.video_button.SetLabel(label='Awaiting call..')
	self.Start_Videoconf.Enable(False)
        self.video_button.Enable(False)
	
    def onCallFailed(self, event):
        self.video_button.SetLabel(label='Awaiting call..')
	
	
    def startPhone(self):
	os.environ['SDL_VIDEODRIVER']='x11'
        os.environ['SDL_WINDOWID']=str(self.video_panel.GetHandle())
	self.phone.start()

    def onStartAcquire_MenuClick(self, event):
        self.count += 1
        print 'count = ', self.count
        self.statusbar.SetStatusText("Acquiring Data...", 0)
      
        # creating a thread
        thread = AcquireData.AcquireDataThr(self.count, self)
        self.threads.append(thread)
        # starting the thread
        thread.start()
        self.onClickStart()

    def onStopAcquire_MenuClick(self, event):
        self.stopThreads()
        self.onClickStop()

    def onSaveToFile_MenuClick(self, event):
        # open window asking in what file will data be saved
        wildcard = "Textfile (*.txt)|*.txt"
        dialog = wx.FileDialog(self, 'Save to File', os.getcwd(), '', wildcard, wx.SAVE | wx.OVERWRITE_PROMPT)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            mypath = dialog.GetPath()
        dialog.Destroy()
        if result == wx.ID_CANCEL:
            return
        self.user_config['file_output'] = mypath

    def onStartVideoconf_MenuClick(self, event):
        if(self.phone.isOnCall()):
            self.phone.terminateCall()
        else:
            self.phone.answer()

    def onAbout_MenuClick(self,event):
        wx.MessageBox(" \nCopyright 2008\nTeleMed II Group\nInstrumentation, Robotics, & Control Laboratory\nUP - Diliman",
                      "TeleMed II", wx.OK | wx.ICON_INFORMATION, self)
    def onCloseWindow(self, event):
        #self.stopThreads()
	self.phone.stop()
        print "Main Window Closed"
        self.Destroy()

    def onIMReply_ButtonClick(self, event):
        msg = self.reply_text.GetValue()

	if(self.phone.isOnCall() == True):
		self.messenger.sendMessage(msg)
	else:
		self.UpdateIMText("No RxBox is connected.")

    def onClickStart(self):
        self.Start_Acquire.Enable(False)
        self.Stop_Acquire.Enable(True)
        self.Save_To_File.Enable(False)
        self.start_button.Enable(False)
        self.stop_button.Enable(True)
        self.save_button.Enable(False)
    
    def onClickStop(self):
        self.Start_Acquire.Enable(True)
        self.Stop_Acquire.Enable(False)
        self.Save_To_File.Enable(True)
        self.start_button.Enable(True)
        self.stop_button.Enable(False)
        self.save_button.Enable(True)
        self.statusbar.SetStatusText("Program Ready", 0)

    def stopThreads(self):
        # kill all threads
        while self.threads:
            thread = self.threads[0]
            thread.stop()
            self.threads.remove(thread)
        
    def UpdateIMText(self, msg):
	self.im_messages.AppendText('PGH: ' + msg + '\n')
        self.reply_text.Clear()

    def UpdateIMRcvText(self, msg):	
	if (msg is not None):
        	self.im_messages.AppendText('RXBOX: ' + msg + '\n')
       
    def raiseMessage(self, message):
        wx.MessageBox(message,"TeleMed v2", wx.OK | wx.ICON_EXCLAMATION, self)
    
    def raiseStatus(self, message):
        self.statusbar.SetStatusText(message, 0)
    

class MyApp(wx.PySimpleApp):
    def OnInit(self):
        wx.InitAllImageHandlers()
        print "Starting TeleMed II - Doctor's Workstation..."

        self.frame_1 = MyFrame(None, -1, "")
        self.SetTopWindow(self.frame_1)
        self.frame_1.ShowFullScreen(True, style=wx.FULLSCREEN_NOTOOLBAR|wx.FULLSCREEN_NOBORDER|wx.FULLSCREEN_NOCAPTION)
	self.frame_1.startPhone()

        return 1

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
