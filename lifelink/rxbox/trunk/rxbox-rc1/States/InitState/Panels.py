import datetime

from PatientInfoPanel import *
from CommPanel import *
from Modules.All import *

class PatientInfoPanel2 (PatientInfoPanel):
    def __init__(self, *args, **kwds):
        PatientInfoPanel.__init__(self, *args, **kwds)
        self._frame = args[0]
        self._engine = self._frame._engine
        self._panel = self._frame._panel
        self.rxboxDB = self._engine.rxboxDB
        self.dbuuid = self._engine.dbuuid
        
        self.BirthMonth.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.BirthDayCombo.Bind(wx.EVT_COMBOBOX, self.birthday_update)
        self.BirthYear.Bind(wx.EVT_TEXT, self.birthday_update)
            
    def ClearPatient(self):
        """Clear patient information panel"""
        self.FirstNameValue.SetValue("")
        self.MiddleNameValue.SetValue("")
        self.LastNameValue.SetValue("")
        self.AddressValue.SetValue("") 
        self.PhoneNumberValue.SetValue("")
        self.GenderCombo.SetValue("")
        self.AgeValue.SetValue("")
        self.AgeCombo.SetValue("")
        self.BirthYear.SetValue("")
        self.BirthMonth.SetValue("")        
        self.BirthDayCombo.SetValue("")
    
    def setGui(self, mode='unlock'):
        modeb = (mode == 'unlock')
        self.FirstNameValue.Enable(modeb)
        self.MiddleNameValue.Enable(modeb)
        self.LastNameValue.Enable(modeb)
        self.AddressValue.Enable(modeb) 
        self.PhoneNumberValue.Enable(modeb)
        self.GenderCombo.Enable(modeb)
        self.AgeValue.Enable(modeb)
        self.AgeCombo.Enable(modeb)
        self.BirthYear.Enable(modeb)
        self.BirthMonth.Enable(modeb)        
        self.BirthDayCombo.Enable(modeb)
        
    def birthday_update(self, evt):
        """Automatically updates the age of patient and the corresponding birth year"""
        year_temp = int(self.BirthYear.GetValue()) if self.BirthYear.GetValue() else 0 
        month_temp = int(self.BirthMonth.GetSelection())
        day_temp = int(self.BirthDayCombo.GetSelection())

        age = 0
        
        if year_temp != 0:
            date = datetime.datetime.today()
            year_now = date.year
            age = int(year_now) - year_temp
            if int(date.month) < month_temp:
                age = age - 1
            if int(date.month) == month_temp:
                if int(date.day) < dat_temp + 1:
                    age = age - 1
            self.AgeValue.SetValue(str(age))
            self.AgeCombo.SetValue('Years')

class CommPanel2(CommPanel):
    def __init__(self, *args, **kwds):
        CommPanel.__init__(self, *args, **kwds)
        self._frame = args[0]
        self._engine = self._frame._engine
        self._panel = self._frame._panel
        
    def onStartStop(self, event): # wxGlade: CommPanel.<event_handler>
        if self.StartStop_Label.GetLabel() == "Start":
            self._engine.change_state('DAQState')
        else:
            self._engine.change_state('StandbyState')
            
    def onSend(self, event): # wxGlade: CommPanel.<event_handler>
        self._engine.change_state('SendEDFState')

    def onCall(self, event): # wxGlade: CommPanel.<event_handler>
        if self._engine.state.__name__() == 'ReferState':
            self._engine.change_state('StandbyState')
        else:
            self._engine.change_state('SendVoIPState')
        
        
    def setGui(self, mode='unlock'):
        """mode expects lock, unlock, acquire, standby"""
        if mode not in ['acquire', 'standby', 'unlock', 'lock']:
            print 'mode unsupported'
            return
        
        if mode == 'acquire' or mode == 'standby':
            start = (mode == 'standby')
            self.StartStop_Label.SetLabel("Start" if start else "Stop")
            self.StartStop_Button.SetBitmapLabel(wx.Bitmap("Icons/%sButton.png" % ("Play" if start else "Stop"), wx.BITMAP_TYPE_ANY))
            self.StartStop_Button.SetToolTipString("Start data acquisition from the biomedical modules" if start else "Stop RxBox session")
            
        modeb = (mode != 'lock')
        self.StartStop_Button.Enable(modeb)
        self.Send_Button.Enable(modeb)
        self.Call_Button.Enable(modeb)            
