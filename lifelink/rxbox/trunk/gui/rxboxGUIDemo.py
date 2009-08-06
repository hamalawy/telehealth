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

    def __set_properties(self):
        RxFrame.__set_properties(self)
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        
    def CreateReferPanel(self):
        self.ReferPanel=ReferPanel(self,-1)
        self.mainhorizontal_sizer.Add(self.ReferPanel, 1, wx.ALL|wx.EXPAND,4)
        self.Layout()

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
        self.ecg_vertical_sizer.Add(self.plotter.plotpanel,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        
        self.timer1 = wx.Timer(self)
        self.timer2 = wx.Timer(self)
        self.timerEDF = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer1, self.timer1)
        self.Bind(wx.EVT_TIMER, self.on_timer2, self.timer2)
        self.Bind(wx.EVT_TIMER, self.make_edf, self.timerEDF)

        self.Biosignals = []
        
        self.spo2data = simsensors.Spo2sim(self)
        self.bpdata = simsensors.BpSim(self)
        
        self.patient1 = edf.Patient('1','Timothy','Cena','Ebido','Servan',\
                                    'Male','09.27.89','19')
                                    
        self.bp_infolabel.SetLabel('BP ready')
        self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
        self.spo2_infolabel.SetLabel('Pulse Ox ready')
        self.count = 0      #no use as of now
        
    def onStartStop(self, event):

        self.referflag = 0
        self.panel = 0
        self.parentFrame.PatientInfo_Label.SetLabel('Patient Name:'+'\n'+ 'Gender: ' + ' ' + '\nAge: ' + ' ' + ' '  + ' ' + 'Validity:' +\
                                               '\nAddress: ' + ' ' + '\nPhone: ' + ' ')

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
            self.displayECG()
            self.spo2data.get()         
            
            self.onBPCyclic()
            self.bpdata.get()
            
            self.timer1.Start(1000)
            self.timerEDF.Start(15000)
            
        else:
            self.bpNow_Button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Label.SetLabel("Start")
            self.bpNow_Button.Enable(True)
            self.Call_Button.Enable(False)
            self.Upload_Button.Enable(False)
            self.lead12_button.Enable(False)

            self.timer1.Stop()
            self.timer2.Stop()       
            self.timerEDF.Stop()    

            self.heartrate_infolabel.SetLabel('Pulse Ox Ready')
            self.spo2_infolabel.SetLabel('Pulse Ox Ready')

            CallAfter(self.parentFrame.DestroyReferPanel)

    def displayECG(self):
        """ Calls the ecg_lead() method of the ecglogfile module to extract
            the 12 leads then passes it to the ecgplotter module for plotting
        """

        self.getlead = ECG().ecg_lead()    
        self.plotter.plot(self.getlead[1]) 

    def on_timer1(self,evt):
        
        self.spo2data.get()    
        print 'Spo2 data acquired'

    def on_timer2(self,evt):
        
        print 'BP ready'
        self.bp_infolabel.SetLabel('BP ready')
        self.onBPCyclic()
        self.bpdata.get()
        
    def make_edf(self,evt):

        self.Endtime = datetime.datetime.today()
        self.Starttime = self.Endtime + datetime.timedelta(seconds = -15)
        self.strDate = self.Starttime.strftime("%d.%m.%y")
        self.strStarttime = self.Starttime.strftime("%H.%M.%S")
        self.strY2KDate = self.Starttime.strftime("%d-%b-%Y")
        
        Biosignal_SPO2 = BioSignal('SpO2 finger','IR-Red sensor',\
                                '%',0,100,0,100,'None',15,self.spo2data.spo2_list)
        Biosignal_BPM = BioSignal('SpO2 finger','IR-Red sensor',\
                                'bpm',0,300,0,300,'None',15,self.spo2data.bpm_list)
        Biosignal_pSys = BioSignal('bpsystole', 'NIBP2010','mmHg',\
                                        0,300,0,300,'None',1,self.bpdata.systole_sim_values)
        Biosignal_pDias = BioSignal('bpdiastole','NIBP2010','mmHg',\
                                        0,300,0,300,'None',1,self.bpdata.diastole_sim_values)
        
        self.Biosignals.append(Biosignal_SPO2)
        self.Biosignals.append(Biosignal_BPM)
        self.Biosignals.append(Biosignal_pSys)
        self.Biosignals.append(Biosignal_pDias)     
        
        myedf = edf.EDF(self.patient1,self.Biosignals,self.strDate,self.strStarttime,self.strY2KDate + \
                        ': LifeLink 15 second data of CorScience modules', \
                        4, 15)
        myedf.get(self.patient1)
        print 'EDF creation finished'

        self.Biosignals = []


    def onCall(self, event): # wxGlade: DAQPanel_Parent.<event_handler>

        if (self.Call_Label.GetLabel() == "Call") and (self.referflag == 0):   
            CreateDialog = CreateRecordDialog2(self.parentFrame,self)
            CreateDialog.ShowModal()
            CallAfter(self.parentFrame.CreateReferPanel)
            self.Call_Label.SetLabel(">>  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.referflag = 1
            self.panel = 1
            
        elif (self.Call_Label.GetLabel() == "<<  ") and (self.referflag == 1):   
            CallAfter(self.parentFrame.CreateReferPanel)
            self.Call_Label.SetLabel(">>  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 1
               
        else:
            self.Call_Button.Enable(False)
            self.Call_Label.Enable(False)
            CallAfter(self.parentFrame.DestroyReferPanel)
            self.Call_Label.SetLabel("<<  ")       
            self.Call_Button.Enable(True)
            self.Call_Label.Enable(True)
            self.panel = 0

    def onBPNow(self, event): # wxGlade: MyPanel1.<event_handler>
        
        reload_bp_str = self.setBPmins_combobox.GetValue()
        reload_bp = int(reload_bp_str[0:2])*1000
        self.bpNow_Button.Enable(False)
        self.bpdata.get()
        
    def onBPCyclic(self):

        reload_bp_str = self.setBPmins_combobox.GetValue()
        reload_bp = int(reload_bp_str[0:2])*1000
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
    



        

