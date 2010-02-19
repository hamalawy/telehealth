# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Thu Jan  7 14:11:50 2010

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class CreateRecordDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CreateRecordDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.Referral_Label = wx.StaticText(self, -1, "REFERRAL", style=wx.ALIGN_CENTRE)
        self.ReferralTopic_Label = wx.StaticText(self, -1, "Topic of Referral:    ")
        self.ReferralTopic_TextCtrl = wx.TextCtrl(self, -1, "topic of referral")
        self.ReferralReason_Label = wx.StaticText(self, -1, "Reason of Referral:")
        self.ReferralReason_Combo = wx.ComboBox(self, -1, choices=["Case", "Incident", "Request"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.infolabel_lineseparator = wx.StaticLine(self, -1)
        self.PatientInfo_Label = wx.StaticText(self, -1, "PATIENT INFORMATION", style=wx.ALIGN_CENTRE)
        self.PatientFirstName_Label = wx.StaticText(self, -1, "First Name:            ")
        self.PatientFirstName_TextCtrl = wx.TextCtrl(self, -1, "first name")
        self.PatientMiddleName_Label = wx.StaticText(self, -1, "Middle Name:        ")
        self.PatientMiddleName_TextCtrl = wx.TextCtrl(self, -1, "middle name")
        self.PatientLastName_Label = wx.StaticText(self, -1, "Last Name:            ")
        self.PatientLastName_TextCtrl = wx.TextCtrl(self, -1, "last name")
        self.PatientGender_Label = wx.StaticText(self, -1, "Gender:                  ")
        self.PatientGender_Combo = wx.ComboBox(self, -1, choices=["Male", "Female"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.PatientAge_Label = wx.StaticText(self, -1, "Age:                       ")
        self.PatientAge_TextCtrl = wx.TextCtrl(self, -1, "age")
        self.PatientBirth_Combo = wx.ComboBox(self, -1, choices=["Days", "Months", "Years"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.PatientAgeValidity_Combo = wx.ComboBox(self, -1, choices=["Known", "Unknown", "Estimated"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.PatientAddress_Label = wx.StaticText(self, -1, "Address:                ")
        self.PatientAddress_TextCtrl = wx.TextCtrl(self, -1, "address", style=wx.TE_MULTILINE)
        self.PatientPhoneNumber_Label = wx.StaticText(self, -1, "Phone Number:     ")
        self.PatientPhoneNumber_TextCtrl = wx.TextCtrl(self, -1, "phone number")
        self.createrecordline = wx.StaticLine(self, -1)
        self.PatientRemarks = wx.StaticText(self, -1, "Remarks:               ")
        self.RemarkValue = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.CreatePatient_Button = wx.Button(self, -1, "CREATE RECORD")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnCreateRecord, self.CreatePatient_Button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CreateRecordDialog.__set_properties
        self.SetTitle("Create Patient Record")
        self.ReferralTopic_TextCtrl.SetMinSize((300, 27))
        self.ReferralReason_Combo.SetMinSize((200, 27))
        self.ReferralReason_Combo.SetSelection(-1)
        self.PatientFirstName_TextCtrl.SetMinSize((300, 27))
        self.PatientMiddleName_TextCtrl.SetMinSize((300, 27))
        self.PatientLastName_TextCtrl.SetMinSize((300, 27))
        self.PatientGender_Combo.SetMinSize((150, 27))
        self.PatientGender_Combo.SetSelection(-1)
        self.PatientAge_TextCtrl.SetMinSize((62, 27))
        self.PatientBirth_Combo.SetMinSize((110, 27))
        self.PatientBirth_Combo.SetSelection(0)
        self.PatientAgeValidity_Combo.SetMinSize((110, 27))
        self.PatientAgeValidity_Combo.SetSelection(0)
        self.PatientAddress_TextCtrl.SetMinSize((300, 86))
        self.PatientPhoneNumber_TextCtrl.SetMinSize((150, 27))
        self.RemarkValue.SetMinSize((300, 86))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CreateRecordDialog.__do_layout
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainhorizontal_sizer = wx.BoxSizer(wx.VERTICAL)
        createrecordsizer = wx.BoxSizer(wx.HORIZONTAL)
        patientaddress_sizer_copy = wx.FlexGridSizer(1, 4, 0, 0)
        infolabel_sizer = wx.BoxSizer(wx.VERTICAL)
        phonenumber_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        patientaddress_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        patientage_sizer = wx.BoxSizer(wx.HORIZONTAL)
        patientgender_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        lastname_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        middlename_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        firstname_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        referral_sizer = wx.BoxSizer(wx.VERTICAL)
        referralreason_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        referraltopic_sizer = wx.FlexGridSizer(1, 4, 0, 0)
        referral_sizer.Add(self.Referral_Label, 0, wx.ALL|wx.EXPAND, 4)
        referraltopic_sizer.Add(self.ReferralTopic_Label, 0, wx.ALL, 4)
        referraltopic_sizer.Add(self.ReferralTopic_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        referraltopic_sizer.AddGrowableCol(2)
        referral_sizer.Add(referraltopic_sizer, 1, wx.EXPAND, 0)
        referralreason_sizer.Add(self.ReferralReason_Label, 0, wx.ALL, 4)
        referralreason_sizer.Add(self.ReferralReason_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        referralreason_sizer.AddGrowableCol(2)
        referral_sizer.Add(referralreason_sizer, 1, wx.EXPAND, 0)
        referral_sizer.Add(self.infolabel_lineseparator, 0, wx.EXPAND, 0)
        mainhorizontal_sizer.Add(referral_sizer, 0, wx.EXPAND, 0)
        infolabel_sizer.Add(self.PatientInfo_Label, 0, wx.ALL|wx.EXPAND, 4)
        firstname_sizer.Add(self.PatientFirstName_Label, 0, wx.ALL, 4)
        firstname_sizer.Add(self.PatientFirstName_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        firstname_sizer.AddGrowableCol(2)
        infolabel_sizer.Add(firstname_sizer, 0, wx.EXPAND, 0)
        middlename_sizer.Add(self.PatientMiddleName_Label, 0, wx.ALL, 4)
        middlename_sizer.Add(self.PatientMiddleName_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        middlename_sizer.AddGrowableCol(2)
        infolabel_sizer.Add(middlename_sizer, 1, wx.EXPAND, 0)
        lastname_sizer.Add(self.PatientLastName_Label, 0, wx.ALL, 4)
        lastname_sizer.Add(self.PatientLastName_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        lastname_sizer.AddGrowableCol(2)
        infolabel_sizer.Add(lastname_sizer, 0, wx.EXPAND, 0)
        patientgender_sizer.Add(self.PatientGender_Label, 0, wx.ALL, 4)
        patientgender_sizer.Add(self.PatientGender_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        patientgender_sizer.AddGrowableCol(2)
        infolabel_sizer.Add(patientgender_sizer, 0, wx.EXPAND, 0)
        patientage_sizer.Add(self.PatientAge_Label, 0, wx.ALL, 4)
        patientage_sizer.Add(self.PatientAge_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        patientage_sizer.Add(self.PatientBirth_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        patientage_sizer.Add(self.PatientAgeValidity_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        infolabel_sizer.Add(patientage_sizer, 1, wx.EXPAND, 0)
        patientaddress_sizer.Add(self.PatientAddress_Label, 0, wx.ALL, 4)
        patientaddress_sizer.Add(self.PatientAddress_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        patientaddress_sizer.AddGrowableCol(2)
        infolabel_sizer.Add(patientaddress_sizer, 0, wx.EXPAND, 0)
        phonenumber_sizer.Add(self.PatientPhoneNumber_Label, 0, wx.ALL, 4)
        phonenumber_sizer.Add(self.PatientPhoneNumber_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        phonenumber_sizer.AddGrowableCol(2)
        infolabel_sizer.Add(phonenumber_sizer, 0, wx.EXPAND, 0)
        infolabel_sizer.Add(self.createrecordline, 0, wx.EXPAND, 0)
        mainhorizontal_sizer.Add(infolabel_sizer, 0, wx.EXPAND, 0)
        patientaddress_sizer_copy.Add(self.PatientRemarks, 0, wx.ALL, 4)
        patientaddress_sizer_copy.Add(self.RemarkValue, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        patientaddress_sizer_copy.AddGrowableCol(2)
        mainhorizontal_sizer.Add(patientaddress_sizer_copy, 0, wx.EXPAND, 0)
        createrecordsizer.Add((150, 20), 0, 0, 0)
        createrecordsizer.Add((160, 20), 0, 0, 0)
        createrecordsizer.Add(self.CreatePatient_Button, 0, wx.ALL|wx.EXPAND, 4)
        createrecordsizer.Add((20, 20), 0, 0, 0)
        mainhorizontal_sizer.Add(createrecordsizer, 1, wx.EXPAND, 0)
        mainsizer.Add(mainhorizontal_sizer, 0, wx.EXPAND, 0)
        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
        self.Layout()
        # end wxGlade

    def OnCreateRecord(self, event): # wxGlade: CreateRecordDialog.<event_handler>
        print "Event handler `OnCreateRecord' not implemented!"
        event.Skip()

# end of class CreateRecordDialog


