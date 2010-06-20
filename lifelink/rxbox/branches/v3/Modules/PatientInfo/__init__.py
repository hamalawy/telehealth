from PatientInfoPanel import *
from CommPanel2 import *
import uuid
import datetime


class PatientInfoPanel2 (PatientInfoPanel):
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

class CommPanel2(CommPanel):
    def __init__(self, *args, **kwds):
        CommPanel.__init__(self, *args, **kwds)
        
        self.frame = args[0]
        
    def onStartStop(self, event): # wxGlade: CommPanel.<event_handler>
        self.frame._panel['ecg'].ecmstat_reset()

        if self.StartStop_Label.GetLabel() == "Start":
            if not self.frame.rxboxinitialized:
                self.frame.dbuuid = str(uuid.uuid1())
                print "uuid = ", self.frame.dbuuid
                self.frame.rxboxDB.dbinsert('sessions', 'uuid', self.frame.dbuuid)
                self.frame.rxboxDB.dbupdate('sessions', 'starttime', str(datetime.datetime.today()), 'uuid', self.frame.dbuuid)
            self.frame.rxboxinitialized = False
            self.setGui('acquire')    
            self.frame._panel    
            
        else:
            self.setGui('standby')
            
            
    def onSend(self, event): # wxGlade: CommPanel.<event_handler>
        print "Event handler `onSend' not implemented!"
        event.Skip()

    def onCall(self, event): # wxGlade: CommPanel.<event_handler>
        print "Event handler `onCall' not implemented!"
        event.Skip()
        
    def setGui(self, mode):
        #yes its not yet optimized, but it may serve a purpose having it this way
        if mode == 'standby':
            self.StartStop_Label.SetLabel("Start")
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/PlayButton.png", wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Start data acquisition from the biomedical modules")
            
            self.frame._panel['ecg'].lead12_button.Enable(False)
            self.frame._panel['bp'].bpNow_Button.Enable(False)
            self.frame._panel['comm'].Send_Button.Enable(False)
            self.frame._panel['comm'].Call_Button.Enable(False)
        elif mode == 'acquire':
            self.StartStop_Label.SetLabel("Stop")
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/StopButton.png", wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Stop RxBox session")
            
            self.frame._panel['ecg'].lead12_button.Enable(True)
            self.frame._panel['bp'].bpNow_Button.Enable(True)
            self.frame._panel['comm'].Send_Button.Enable(True)
            self.frame._panel['comm'].Call_Button.Enable(True)
            