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
from rxboxGUI import RxFrame
from rxboxGUI import DAQPanel
from rxboxGUI import ReferPanel
from createrecord import CreateRecordDialog
from edf import BioSignal,EDF
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

import sys
sys.path.append('triage')
import triage


class RxFrame2(RxFrame):
    def __init__(self, *args, **kwds):
        RxFrame.__init__(self, *args, **kwds)
        self.DAQPanel=DAQPanel2(self,self,-1)
        self.info_daq_sizer.Add(self.DAQPanel, 1, wx.ALL|wx.EXPAND,4)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.topic = ''
        self.body = ''

    def __set_properties(self):
        RxFrame.__set_properties(self)
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        
    def CreateReferPanel(self):
        self.ReferPanel=ReferPanel(self,-1)
        self.mainhorizontal_sizer.Add(self.ReferPanel, 1, wx.ALL|wx.EXPAND,4)
        self.ReferPanel.IMreply_Text.Bind(wx.EVT_TEXT_ENTER, self.updateIM)        
        self.Layout()
        
    def onClose(self,evt):
        dlg = wx.MessageDialog(self,'Do you want to save data?','Exit', wx.YES_NO | wx.ICON_QUESTION |wx.CANCEL)
        if dlg.ShowModal() == wx.ID_CANCEL:
            dlg.Destroy()
        else:
            dlg.Destroy()
            self.Destroy()   
            
    def updateIM(self,evt):
        prev = self.ReferPanel.IMtexts_Text.GetValue()
        reply = self.ReferPanel.IMreply_Text.GetValue() + '\n'
        self.ReferPanel.IMtexts_Text.SetValue(prev + reply)
        self.ReferPanel.IMreply_Text.SetValue("")   
        
    def DestroyReferPanel(self):

        try:
            self.ReferPanel.Destroy()
            self.Layout()

        except AttributeError:
            pass

class DAQPanel2(DAQPanel):

    def __init__(self, parent,*args, **kwds):
        DAQPanel.__init__(self, *args, **kwds)
        self.parentFrame = parent

        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 220, size=(10, 103),style=wx.GA_VERTICAL)        
        self.sizersize = self.ecg_vertical_sizer.GetSize()
        self.plotter = Plotter(self,(1120,380))
        self.ecg_vertical_sizer.Add(self.plotter.plotpanel,1,\
                                    wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)

        self.timer1 = wx.Timer(self)
        self.timer2 = wx.Timer(self)
        self.timerEDF = wx.Timer(self)
        self.pressure_timer = wx.Timer(self)
        self.timerSend = wx.Timer(self)
        self.timerECG_refresh = wx.Timer(self)
        self.timerECGNodeCheck = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer1, self.timer1)
        self.Bind(wx.EVT_TIMER, self.on_timerbp, self.timer2)
        self.Bind(wx.EVT_TIMER, self.make_edf, self.timerEDF)
        self.Bind(wx.EVT_TIMER, self.pressure_update, self.pressure_timer)
        self.Bind(wx.EVT_TIMER, self.onSend, self.timerSend)
        self.Bind(wx.EVT_TIMER, self.displayECG, self.timerECG_refresh)
        self.Bind(wx.EVT_TIMER, self.onECGNodeCheck, self.timerECGNodeCheck)
        self.parentFrame.BirthMonth.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.parentFrame.BirthDayCombo.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.parentFrame.BirthYear.Bind(wx.EVT_TEXT, self.birthday_update)    
        
        self.Biosignals = []
        
        self.spo2data = simsensors.Spo2sim(self)
        self.bpdata = simsensors.BpSim(self)
        self.ecgdata = simsensors.EcgSim(self)
        
        self.patient1 = edf.Patient('1','Timothy','Cena','Ebido','Servan',\
                                    'Male','09.27.89','19')
                                    
        self.bp_infolabel.SetLabel('BP ready')
        self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
        self.spo2_infolabel.SetLabel('Pulse Ox ready')
        self.bp_isCyclic = 0
        self.ecg_counter = 0
        self.ecg_first = 0
        self.getlead = ECG().ecg_lead() 
        self.ECGplotcounter = 0
        self.on_send = 0
        self.with_patient_info = 0
		
        self.config = ConfigParser.ConfigParser()
        self.config.read('rxbox.cfg')
        

    def onStartStop(self, event):

        self.referflag = 0
        self.panel = 0
        self.sendcount=0
        self.sendtoggled=0
        self.nodetimer = 0
        self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_initial.png",wx.BITMAP_TYPE_ANY))
        self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_initial.png",wx.BITMAP_TYPE_ANY))
        self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_initial.png", wx.BITMAP_TYPE_ANY))
        self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_initial.png", wx.BITMAP_TYPE_ANY))
        self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
        self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_initial.png", wx.BITMAP_TYPE_ANY))
        self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
        self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_initial.png", wx.BITMAP_TYPE_ANY))
        self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_initial.png", wx.BITMAP_TYPE_ANY))        
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
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/StopButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Stop RxBox session")
            self.StartStop_Label.SetLabel("Stop")
            self.bp_isCyclic = 1
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")

            self.spo2data.get()
            self.bpdata.get()
            self.onECGNodeCheck(self)
   
            self.timer1.Start(1000)
            self.timerEDF.Start(15000)

            
        else:
            self.parentFrame.RxFrame_StatusBar.SetStatusText("RxBox Ready")
            self.bpNow_Button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Label.SetLabel("Start")
            self.bpNow_Button.Enable(True)
            self.Call_Button.Enable(False)
            self.Send_Button.Enable(False)
            self.lead12_button.Enable(False)
            self.bp_isCyclic = 0
            self.referflag = 0
            self.panel = 0
            self.timer1.Stop()
            self.timer2.Stop()       
            self.timerEDF.Stop()    
            self.timerSend.Stop()  
            self.timerECG_refresh.Stop()
            self.timerECGNodeCheck.Stop()    
            self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
            self.spo2_infolabel.SetLabel('Pulse Ox Ready')
            self.parentFrame.DAQPanel.RemarkValueDaq.SetValue('')            
            self.SaveQuery()
            self.ClearPatient()
            self.with_patient_info = 0
            CallAfter(self.parentFrame.DestroyReferPanel)

    def SaveQuery(self):
        
        dlg = wx.MessageDialog(self,'Do you want to save data?','', wx.YES_NO | wx.ICON_QUESTION |wx.CANCEL)
        dlg.ShowModal()
        
    def ClearPatient(self):
        
        self.parentFrame.FirstNameValue.SetValue("")
        self.parentFrame.MiddleNameValue.SetValue("")
        self.parentFrame.LastNameValue.SetValue("")
        self.parentFrame.AddressValue.SetValue("") 
        self.parentFrame.PhoneNumberValue.SetValue("")
        self.parentFrame.GenderCombo.SetValue("")
        self.parentFrame.AgeValue.SetValue("")
        self.parentFrame.AgeCombo.SetValue("")
        self.parentFrame.BirthYear.SetValue("")
        self.parentFrame.BirthMonth.SetSelection(0)
        self.parentFrame.BirthDayCombo.SetValue('')
            
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

    def displayECG(self,evt):
        """ Calls the ecg_lead() method of the ecglogfile module to extract
            the 12 leads then passes it to the ecgplotter module for plotting
        """
        self.ECGplotcounter = self.ECGplotcounter + 1
        ecg_plot = []
        ecg_plot2 = []
        self.ecgdata.ecg_list = []
        
        for y in range(0,4):
            for i in range(100,400):
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
                
    def birthday_update(self,evt):
        year_temp = self.parentFrame.BirthYear.GetValue()
        month_temp = self.parentFrame.BirthMonth.GetSelection()
        day_temp = self.parentFrame.BirthDayCombo.GetSelection()

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
            self.parentFrame.AgeValue.SetValue(str(age))

        
    def on_timer1(self,evt):
        
        self.spo2data.get()    
        print 'Spo2 data acquired'
        
    def on_timerbp(self,evt):
        
        self.bpdata.get()
        
    def pressure_update(self, evt):
        press = int(self.file.readline())
        if press != 999:
#            self.bp_slider.SetValue(20-(press/10))
            self.bp_pressure_indicator.SetValue(press)
        else:
            self.file.close()
            self.pressure_timer.Stop()
#            self.bp_slider.Enable(False)
            self.bp_pressure_indicator.Enable(False)
            self.bpNow_Button.Enable(True)
            self.setBPmins_combobox.Enable(True)
#            self.bpdata.get()
        
    def make_edf(self,evt):

        self.Endtime = datetime.datetime.today()
        self.Starttime = self.Endtime + datetime.timedelta(seconds = -15)
        self.strDate = self.Starttime.strftime("%d.%m.%y")
        self.strStarttime = self.Starttime.strftime("%H.%M.%S")
        self.strY2KDate = self.Starttime.strftime("%d-%b-%Y")
        
#        print len(self.spo2data.spo2_list)
#        print len(self.spo2data.bpm_list)
#        print len(self.bpdata.systole_sim_values)
#        print len(self.bpdata.diastole_sim_values)
#        print len(self.ecgdata.ecg_list_scaled)
        
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
        self.on_send = 0
        self.parentFrame.RxFrame_StatusBar.SetStatusText("Requesting connection to triage...")
        if (self.Call_Label.GetLabel() == "Call") and (self.referflag == 0):    
            print "call ba"
            self.Call_Label.SetLabel(">>  ") 
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.referflag = 1
            self.panel = 1
            if self.with_patient_info == 0:
                CreateDialog = CreateRecordDialog2(self.parentFrame,self)
                CreateDialog.ShowModal()
            CallAfter(self.parentFrame.CreateReferPanel)
            self.parentFrame.Layout()             
        elif (self.Call_Label.GetLabel() == "<<  ") and (self.referflag == 1) : 
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquring biomedical readings... Call Panel Shown.")        
            self.parentFrame.ReferPanel.Show()
            self.Call_Label.SetLabel(">>  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 1
            self.parentFrame.Layout()               
        else:
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquring biomedical readings... Call Panel Hidden.")
            self.Call_Button.Enable(False)
            self.Call_Label.Enable(False)
            self.parentFrame.ReferPanel.Hide()
            self.Call_Label.SetLabel("<<  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 0
            self.parentFrame.Layout()
                        
    def onSend(self, event): # wxGlade: DAQPanel.<event_handler>

        self.on_send = 1
        if self.with_patient_info == 0:
            CreateDialog = CreateRecordDialog2(self.parentFrame,self)
            CreateDialog.ShowModal() 
        self.timerSend.Start(5000)
        self.sendcount = self.sendcount + 1
        self.parentFrame.RxFrame_StatusBar.SetStatusText("Sending Data to Server...")
        if (self.sendcount == 2):

            self.parentFrame.RxFrame_StatusBar.SetStatusText("Sending Data to Server...")
            t = triage.Triage('triage/email.cfg')
            t.login()
            headers = {'Subject': 'refer ' + self.parentFrame.topic, 'X-Eccs-Priority': 'emergency',
                            'X-Eccs-Rxboxextension': '2001'}
            body= self.parentFrame.body
            afilename=['triage/Ebido_113056.edf']
            attach={}
            for i in afilename:
                    f = open(i, 'r')
                    attach[i] = f.read()
                    f.close()

            print "sending..\n";
            t.request(headers, body, attach)
            print "sent";


            self.SendStatus(self)

    def onSend2(self): 
        self.timerSend.Start(5000)
        self.sendcount = self.sendcount + 1
        self.parentFrame.RxFrame_StatusBar.SetStatusText("Sending Data to Server...")
        print self.sendcount
        if (self.sendcount == 2):
            self.SendStatus(self)   
            
    
    def SendStatus(self,event):
        if (self.config.getint('triage','connection') == 1): 
            print "Send to Server Successful"
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Send to Server Successful")
            dlg = wx.MessageDialog(self,"Send to Server Successful","Send to Server Successful",wx.OK | wx.ICON_QUESTION )
            dlg.ShowModal()
            self.sendtoggled = 1
        elif (self.config.getint('triage','connection') == 0):  
            print "Send to Server Failed"
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Send to Server Failed")
            self.sendtoggled = 0
            dlg = wx.MessageDialog(self,"Would you like to resend data?","Send to Server Failed",wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.parentFrame.RxFrame_StatusBar.SetStatusText("Resending data to server...")
                self.sendtoggled = 0
                self.timerSend.Stop()    
                self.sendcount = 1               
                self.onSend2()
        self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")            
        self.timerSend.Stop()    
        self.sendcount = 0

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
        CreateDialog2 = Lead12Dialog2(self,self)
        CreateDialog2.ShowModal()
        
    def onECGNodeCheck(self,x): 
        self.timerECGNodeCheck.Start(250)
        self.nodetimer = self.nodetimer + 1
        self.parentFrame.RxFrame_StatusBar.SetStatusText("Checking Node Placement of ECG...")
        if (self.nodetimer == 1):
            self.R_bitmap.SetBitmap(wx.Bitmap("Icons/R_connected.png",wx.BITMAP_TYPE_ANY))
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_unconnected.png",wx.BITMAP_TYPE_ANY))
            self.C1_bitmap.SetBitmap(wx.Bitmap("Icons/C1_connected.png", wx.BITMAP_TYPE_ANY))
            self.C2_bitmap.SetBitmap(wx.Bitmap("Icons/C2_connected.png", wx.BITMAP_TYPE_ANY))
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C4_bitmap.SetBitmap(wx.Bitmap("Icons/C4_connected.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C6_bitmap.SetBitmap(wx.Bitmap("Icons/C6_connected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.F_bitmap.SetBitmap(wx.Bitmap("Icons/F_connected.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 2):
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_initial.png",wx.BITMAP_TYPE_ANY))
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 3):
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_unconnected.png",wx.BITMAP_TYPE_ANY))
            self.C3_bitmap.SetBitmap(wx.Bitmap("Icons/C3_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.C5_bitmap.SetBitmap(wx.Bitmap("Icons/C5_unconnected.png", wx.BITMAP_TYPE_ANY))
            self.N_bitmap.SetBitmap(wx.Bitmap("Icons/N_unconnected.png", wx.BITMAP_TYPE_ANY))
        elif (self.nodetimer == 4):
            self.L_bitmap.SetBitmap(wx.Bitmap("Icons/L_connected.png",wx.BITMAP_TYPE_ANY))
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
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")            
            self.timerECGNodeCheck.Stop()    
            self.nodetimer = 0
            self.ecgdata.get()
            self.timerECG_refresh.Start(125)         

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
        self.PatientAge_TextCtrl.SetValue(self.parentFrame.AgeValue.GetValue())
        self.PatientAgeDMY_Combo.SetValue(self.parentFrame.AgeCombo.GetValue())
        self.RemarkValue.SetValue(self.parentFrame.DAQPanel.RemarkValueDaq.GetValue())
        
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

        self.parentFrame.topic = self.ReferralTopic_TextCtrl.GetValue()
        self.parentFrame.body = self.RemarkValue.GetValue()

        self.parentFrame.FirstNameValue.SetValue(FirstName)
        self.parentFrame.MiddleNameValue.SetValue(MiddleName)
        self.parentFrame.LastNameValue.SetValue(LastName)
        self.parentFrame.AddressValue.SetValue(Address) 
        self.parentFrame.PhoneNumberValue.SetValue(Phone)
        self.parentFrame.GenderCombo.SetValue(Gender)
        self.parentFrame.AgeValue.SetValue(Age)
        self.parentFrame.AgeCombo.SetValue(DMY)
        self.parentFrame.DAQPanel.RemarkValueDaq.SetValue(self.RemarkValue.GetValue())     

        self.Destroy()
        
        self.parentFrame.DAQPanel.with_patient_info = 1
        if self.parentFrame.DAQPanel.on_send == 0:
 #           CallAfter(self.parentFrame.CreateReferPanel)
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquring biomedical readings... Call Panel Initiated.")


        
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
        
        self.plotter_bigII=extendedPlotter(self,bigsizer,self.parent.getlead[1])
        self.leadII_sizer.Add(self.plotter_bigII,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        
            
# end of rxboxGUI classes

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = RxFrame2(None, -1, "")
    app.SetTopWindow(rx_frame)
    rx_frame.Maximize(True)
    rx_frame.Show()
    app.MainLoop()



        


