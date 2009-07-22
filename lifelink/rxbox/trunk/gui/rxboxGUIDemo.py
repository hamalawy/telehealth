import wx
from rxboxGUI import RxFrame
from rxboxGUI import DAQPanel
from rxboxGUI import ReferPanel
from createrecord import CreateRecordDialog
from wx import CallAfter
import time
import simsensors
import ecggrid

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
##
    def __init__(self, parent,*args, **kwds):
        DAQPanel.__init__(self, *args, **kwds)
        self.parentFrame = parent

        self.ecgplotter = ecggrid.ecggrid(self)
        self.ecgplotter.canvas.SetSize((520, 350))
        self.ecg_vertical_sizer.Add(self.ecgplotter.canvas,1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        
        #dagdag Tim
        self.Bind (wx.EVT_IDLE, self.OnIdle)
        self.working=0
        self.spo2data=simsensors.spo2_sim(self)
        
    def OnIdle(self,event):
        
        if self.working:
            if self.need_abort:
                print "Computation aborted"
            else:
                self.count = self.count + 1
                time.sleep(1)
                if True:
                    self.spo2data.get() #place sensor get here :D
                    event.RequestMore()
                    return
                else:
                    print "Computation completed"
            
            self.working = 0
    #end dagdag
            
    def onStartStop(self, event):

        if self.StartStop_Label.GetLabel() == "Start":

            self.bpvalue_label.Enable(True)
            self.bpmvalue_label.Enable(True)
            self.spo2value_label.Enable(True)
            self.Refer_Button.Enable(True)
            self.Refer_Label.Enable(True)
            self.bpNow_Button.Enable(True)
            
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/StopButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Stop RxBox session")
            self.StartStop_Label.SetLabel("Stop")
            
            #dagdag Tim
            if not self.working:

                self.count = 0
                self.working = 1
                self.need_abort = 0
            #end dagdag
            
        else:
            self.bpNow_Button.Enable(True)
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png",wx.BITMAP_TYPE_ANY))
            self.StartStop_Label.SetLabel("Start")
            self.bpNow_Button.Enable(True)
            self.Refer_Button.Enable(False)

            CallAfter(self.parentFrame.DestroyReferPanel)

            #dagdag Tim
            if self.working:
                self.need_abort = 1
            #end dagdag

    def onRefer(self, event): # wxGlade: DAQPanel_Parent.<event_handler>
        self.Refer_Button.Enable(False)
        self.Refer_Label.Enable(False)

        CreateDialog = CreateRecordDialog2(self.parentFrame,self)
        CreateDialog.ShowModal()

        CallAfter(self.parentFrame.CreateReferPanel)

    def onBPNow(self, event): # wxGlade: MyPanel1.<event_handler>
        self.bpNow_Button.Enable(False)
##        self.myBP.getnow()
        
##
    def updateSPO2Display(self, data):
        self.spo2value_label.SetLabel(data)
        

    def updateBPMDisplay(self, data):
        self.bpmvalue_label.SetLabel(data)
        
        
    def updateBPDisplay(self, data):
        self.bpvalue_label.SetLabel(data)
        
        
    def startSaveThread (self):
##        """ calls makeEDF.SaveThread.run() """
        event.Skip()

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
# end of rxboxGUI classes

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = RxFrame2(None, -1, "")
    app.SetTopWindow(rx_frame)
    rx_frame.Maximize(True)
    rx_frame.Show()
    app.MainLoop()
    



        

