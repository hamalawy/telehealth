import threading

from CreateRecordPanel import *
from LogFilePanel import *


class CreateRecordPanel2(CreateRecordPanel):
    """ Class for Create Record Dialog instance and methods
    
    Methods:
        __init__(CreateRecordDialog) 
        OnCreateRecord        
         
    """
    def __init__(self, *args, **kwds):
        """Patient data from Information Panel is copied to their respective fields in the Patient Record Dialog
        - Sets necessary variables
        
        Arguments: __init__(CreateRecordDialog)
        
        """
        CreateRecordPanel.__init__(self, *args, **kwds)
        self._frame = args[0]
        self._engine = self._frame._engine
        self._panel = self._frame._panel
        self.rxboxDB = self._engine.rxboxDB
        self.dbuuid = self._engine.dbuuid
        self.state = self._engine.state
        
        
        self.patientinfo = self._panel['patientinfo']
        self.PatientFirstName_TextCtrl.SetValue(self.patientinfo.FirstNameValue.GetValue())
        self.PatientMiddleName_TextCtrl.SetValue(self.patientinfo.MiddleNameValue.GetValue())
        self.PatientLastName_TextCtrl.SetValue(self.patientinfo.LastNameValue.GetValue())
        self.PatientAddress_TextCtrl.SetValue(self.patientinfo.AddressValue.GetValue())
        self.PatientPhoneNumber_TextCtrl.SetValue(self.patientinfo.PhoneNumberValue.GetValue())
        self.PatientGender_Combo.SetValue(self.patientinfo.GenderCombo.GetValue())
        self.PatientAge_TextCtrl.SetValue(self.patientinfo.AgeValue.GetValue())
        self.PatientBirth_Combo.SetValue(self.patientinfo.AgeCombo.GetValue())
        self.RemarkValue.SetValue(self._panel['comm'].RemarkValueDaq.GetValue())
        
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

        self.patientinfo.FirstNameValue.SetValue(FirstName)
        self.patientinfo.MiddleNameValue.SetValue(MiddleName)
        self.patientinfo.LastNameValue.SetValue(LastName)
        self.patientinfo.AddressValue.SetValue(Address) 
        self.patientinfo.PhoneNumberValue.SetValue(Phone)
        self.patientinfo.GenderCombo.SetValue(Gender)
        self.patientinfo.AgeValue.SetValue(Age)
        self.patientinfo.AgeCombo.SetValue(Birth)
        self._panel['comm'].RemarkValueDaq.SetValue(self.RemarkValue.GetValue())  
           
        self.state.topic = self.ReferralTopic_TextCtrl.GetValue()
        self.state.body = self.RemarkValue.GetValue()
        self.state.reason = self.ReferralReason_Combo.GetValue()
                
        check_valid = self.check_patient_valid(FirstName, MiddleName, LastName, Gender, Age,\
                                            Birth, Validity, self.state.topic, self.state.reason)
        
        if (check_valid == 1):
            self.rxboxDB.dbpatientinsert('patients', 'lastname', 'firstname', \
                'middlename', 'address', 'phonenumber', 'age', 'birth', 'gender', 'uuid', \
                LastName, FirstName, MiddleName, Address, Phone, Age, Birth, Gender, self.dbuuid)
            wx.CallAfter(self.state.after)
            
#            if self.RxFrame.DAQPanel.on_send == 0:
#                self.RxFrame.RxFrame_StatusBar.SetStatusText("Acquiring biomedical readings... Call Panel Initiated.")
#                self.RxFrame.DAQPanel.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.RxFrame.DAQPanel.dbuuid, 'status message', '', 'Acquiring biomedical readings... Call Panel Initiated.')
            
    def check_patient_valid(self, firstname, middlename, lastname, gender, age, birth, validity, topic, reason):
        """Checks if the required fields in the create patient record are filled-up
        """
        if ((firstname == '')|(middlename == '')|(lastname == '')|(gender == '')|(age == '')|(birth == '')|(validity == '')|(topic == '')|(reason == '')):
            return 0
        else:
            return 1
        
    def OnPaneClose(self):
        del self._panel['createrecord']
        self._engine.change_state('StandbyState')
#        self._panel['ecg'].setGui('unlock')

class LogFilePanel2(LogFilePanel):
    def __init__(self, *args, **kwds):
        LogFilePanel.__init__(self, *args, **kwds)
        self._frame = args[0]
        self._engine = self._frame._engine
        self._panel = self._frame._panel
        self._config = self._engine._config
        self.state = self._engine.state

        self.label_id.SetLabel(self._config.get('info', 'id'))
    
    def sendlogfile(self, event): # wxGlade: LogFilePanel.<event_handler>
        self.state.body = self.text_ctrl_1.GetValue()
        wx.CallAfter(self.state.after)

    def OnPaneClose(self):
        del self._panel['logfile']
        self._engine.change_state('StandbyState')
