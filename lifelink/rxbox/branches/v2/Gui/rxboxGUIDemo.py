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
from lead12dialog import Lead12Dialog
import wx.lib.plot as plot
from ecglogfile import ECG
from ecgplotter import Plotter
#from ecgplot import Plotter
from ecgplot import extendedPlotter

class RxFrame2(RxFrame):
    def __init__(self, *args, **kwds):
        RxFrame.__init__(self, *args, **kwds)
        self.DAQPanel=DAQPanel2(self,self,-1)
        self.info_daq_sizer.Add(self.DAQPanel, 1, wx.ALL|wx.EXPAND,4)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def __set_properties(self):
        RxFrame.__set_properties(self)
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        
    def CreateReferPanel(self):
        self.ReferPanel=ReferPanel(self,-1)
        self.mainhorizontal_sizer.Add(self.ReferPanel, 1, wx.ALL|wx.EXPAND,4)
        self.Layout()
        
    def onClose(self,evt):
        dlg = wx.MessageDialog(self,'Do you want to save data?','', wx.YES_NO | wx.ICON_QUESTION |wx.CANCEL)
        dlg.ShowModal()        
        
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

        self.sizersize = self.ecg_vertical_sizer.GetSize()
        self.plotter = Plotter(self,(1120,380))
        self.ecg_vertical_sizer.Add(self.plotter.plotpanel,1,\
                                    wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)

        self.timer1 = wx.Timer(self)
        self.timer2 = wx.Timer(self)
        self.timerEDF = wx.Timer(self)
        self.pressure_timer = wx.Timer(self)
        self.timerUpload = wx.Timer(self)
        self.timerECG_refresh = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer1, self.timer1)
        self.Bind(wx.EVT_TIMER, self.on_timerbp, self.timer2)
        self.Bind(wx.EVT_TIMER, self.make_edf, self.timerEDF)
        self.Bind(wx.EVT_TIMER, self.pressure_update, self.pressure_timer)
        self.Bind(wx.EVT_TIMER, self.onUpload, self.timerUpload)
        self.Bind(wx.EVT_TIMER, self.displayECG, self.timerECG_refresh)
        self.parentFrame.isEstimated.Bind(wx.EVT_CHECKBOX, self.onEstimate)
        
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
        self.on_check = 0
        self.getlead = ECG().ecg_lead()  
        
        self.parentFrame.AgeValue.Enable(False)
        self.parentFrame.AgeCombo.Enable(False)

    def onStartStop(self, event):

        self.referflag = 0
        self.panel = 0
        self.uploadcount=0
        self.uploadtoggled=0
        
        if self.StartStop_Label.GetLabel() == "Start":
            
            self.Call_Label.SetLabel("Call")
            self.bpvalue_label.Enable(True)
            self.bpmvalue_label.Enable(True)
            self.spo2value_label.Enable(True)
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.bpNow_Button.Enable(True)
            self.Upload_Button.Enable(True)
            self.Upload_Label.Enable(True)
            self.lead12_button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/StopButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Stop RxBox session")
            self.StartStop_Label.SetLabel("Stop")
            self.bp_isCyclic = 1
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings...")

            self.spo2data.get()
            self.bpdata.get()
            self.ecgdata.get()
#            self.displayECG()            
            self.timer1.Start(1000)
            self.timerEDF.Start(15000)
            self.timerECG_refresh.Start(125)
            
        else:
            self.bpNow_Button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Label.SetLabel("Start")
            self.bpNow_Button.Enable(True)
            self.Call_Button.Enable(False)
            self.Upload_Button.Enable(False)
            self.lead12_button.Enable(False)
            self.bp_isCyclic = 0

            self.timer1.Stop()
            self.timer2.Stop()       
            self.timerEDF.Stop()    
            self.timerUpload.Stop()  
            self.timerECG_refresh.Stop()
            self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
            self.spo2_infolabel.SetLabel('Pulse Ox Ready')
            
            self.SaveQuery()
            
            CallAfter(self.parentFrame.DestroyReferPanel)

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

    def displayECG(self,evt):
        """ Calls the ecg_lead() method of the ecglogfile module to extract
            the 12 leads then passes it to the ecgplotter module for plotting
        """
        
        ecg_plot = []
        ecg_plot2 = []
        
        
        
        if (self.ecg_counter < 1500):
            for x in range(0,self.ecg_counter):
                ecg_plot.append(self.ecgdata.ecg_list[x])
            
            if (self.ecg_first == 0):
                for x in range(0,(1500-self.ecg_counter)):
                    ecg_plot.append(0)
            if (self.ecg_first == 1):
                for x in range(self.ecg_counter,1500):
                    ecg_plot.append(self.ecgdata.ecg_list[x+1500])
            
            self.plotter.plot(ecg_plot)
            self.ecg_counter += 125

        if (self.ecg_counter >= 1500):
            for x in range(0,(self.ecg_counter-1500)):
                ecg_plot.append(self.ecgdata.ecg_list[x+1500])
                
            for x in range((self.ecg_counter-1500),1500):
                ecg_plot.append(self.ecgdata.ecg_list[x])
            self.plotter.plot(ecg_plot)
            self.ecg_counter += 125
            if (self.ecg_counter == 3000):
                self.ecg_counter = 0
                self.ecg_first = 1

        
    def on_timer1(self,evt):
        
        self.spo2data.get()    
        print 'Spo2 data acquired'
        
    def on_timerbp(self,evt):
        
        self.bpdata.get()
        
    def pressure_update(self, evt):
        press = int(self.file.readline())
        if press != 999:
            self.bp_slider.SetValue(20-(press/10))
            self.bp_pressure_indicator.SetValue(press)
        else:
            self.file.close()
            self.pressure_timer.Stop()
            self.bp_slider.Enable(False)
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
            CreateDialog = CreateRecordDialog2(self.parentFrame,self)
            CreateDialog.ShowModal()
            CallAfter(self.parentFrame.CreateReferPanel)
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Requesting connection to triage...")
            self.Call_Label.SetLabel(">>  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.referflag = 1
            self.panel = 1
            
        elif (self.Call_Label.GetLabel() == "<<  ") and (self.referflag == 1):   
#            CallAfter(self.parentFrame.CreateReferPanel)
            self.Call_Label.SetLabel(">>  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 1
               
        else:
            self.Call_Button.Enable(False)
            self.Call_Label.Enable(False)
#            CallAfter(self.parentFrame.DestroyReferPanel)
            self.Call_Label.SetLabel("<<  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 0

    def onUpload(self, event): # wxGlade: DAQPanel.<event_handler>
        self.timerUpload.Start(5000)
        self.uploadcount = self.uploadcount + 1
        print self.uploadcount
        if (self.uploadcount == 2):
            self.UploadStatus(self)
         
    
    def UploadStatus(self,event):
        if (self.uploadtoggled == 0): 
#            RxFrame_StatusBar_fields = ["success"]
#            for i in range(len(RxFrame_StatusBar_fields)):
#                self.RxFrame_StatusBar.SetStatusText(RxFrame_StatusBar_fields[i], i)        
            print "Upload to Server Successful"
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Upload to Server Successful")
            self.uploadtoggled = 1
        elif (self.uploadtoggled == 1):  
            print "Upload to Server Failed"
            self.parentFrame.RxFrame_StatusBar.SetStatusText("Upload to Server Failed")
            self.uploadtoggled = 0     
        self.timerUpload.Stop()    
        self.uploadcount = 0

    def onBPNow(self, event): # wxGlade: MyPanel1.<event_handler>
#        self.bpNow_Button.Enable(False)
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



        

