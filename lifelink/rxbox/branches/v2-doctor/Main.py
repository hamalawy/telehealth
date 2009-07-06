"""

v4

integrated rxpanel
integrated icon
integrated authentication window
integrated Patient Information Tab

"""

import wx
import rxpanel
import referpanel
import subprocess, time

class MyDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.parentFrame = parent
        self.Referral_Label = wx.StaticText(self, -1, "REFERRAL", style=wx.ALIGN_CENTRE)
        self.ReferralTitle_Label = wx.StaticText(self, -1, "Session Title:")
        self.ReferralTitle_TextCtrl = wx.TextCtrl(self, -1, "session title")
        self.ReferralTopic_Label = wx.StaticText(self, -1, "Topic of Referral:")
        self.ReferralTopic_TextCtrl = wx.TextCtrl(self, -1, "topic of referral")
        self.ReferralReason_Label = wx.StaticText(self, -1, "Reason of Referral:")
        self.ReferralReason_Combo = wx.ComboBox(self, -1, choices=["Case", "Incident", "Request"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.static_line_3 = wx.StaticLine(self, -1)
        self.PatientInfo_Label = wx.StaticText(self, -1, "PATIENT INFORMATION", style=wx.ALIGN_CENTRE)
        self.PatientFirstName_Label = wx.StaticText(self, -1, "First Name:")
        self.PatientFirstName_TextCtrl = wx.TextCtrl(self, -1, "first name")
        self.PatientMiddleName_Label = wx.StaticText(self, -1, "Middle Name:")
        self.PatientMiddleName_TextCtrl = wx.TextCtrl(self, -1, "middle name")
        self.PatientLastName_Label = wx.StaticText(self, -1, "Last Name:")
        self.PatientLastName_TextCtrl = wx.TextCtrl(self, -1, "last name")
        self.PatientGender_Label = wx.StaticText(self, -1, "Gender:")
        self.PatientGender_Combo = wx.ComboBox(self, -1, choices=["Female", "Male"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.PatientAge_Label = wx.StaticText(self, -1, "Age:")
        self.PatientAge_TextCtrl = wx.TextCtrl(self, -1, "age")
        self.PatientAgeDMY_Combo = wx.ComboBox(self, -1, choices=["Days", "Months", "Years"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.PatientAgeValidity_Combo = wx.ComboBox(self, -1, choices=["Known", "Unknown", "Estimated"], style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        self.PatientAddress_Label = wx.StaticText(self, -1, "Address:")
        self.PatientAddress_TextCtrl = wx.TextCtrl(self, -1, "address", style=wx.TE_MULTILINE)
        self.PatientPhoneNumber_Label = wx.StaticText(self, -1, "Phone Number:")
        self.PatientPhoneNumber_TextCtrl = wx.TextCtrl(self, -1, "phone number")
        self.static_line_4 = wx.StaticLine(self, -1)
        self.CreatePatient_Button = wx.Button(self, -1, "CREATE RECORD")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnCreateRecord, self.CreatePatient_Button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("Create Patient Record")
        self.ReferralReason_Combo.SetSelection(-1)
        self.PatientGender_Combo.SetSelection(-1)
        self.PatientAgeDMY_Combo.SetSelection(0)
        self.PatientAgeValidity_Combo.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_24 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_13 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_10 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_9 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_8 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_5 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_4 = wx.FlexGridSizer(1, 4, 0, 0)
        sizer_3.Add(self.Referral_Label, 0, wx.ALL|wx.EXPAND, 4)
        sizer_4.Add(self.ReferralTitle_Label, 0, wx.ALL, 4)
        sizer_4.Add((50, 20), 0, 0, 0)
        sizer_4.Add(self.ReferralTitle_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_4.Add((20, 20), 0, 0, 0)
        sizer_4.AddGrowableCol(2)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_5.Add(self.ReferralTopic_Label, 0, wx.ALL, 4)
        sizer_5.Add((30, 20), 0, 0, 0)
        sizer_5.Add(self.ReferralTopic_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_5.Add((20, 20), 0, 0, 0)
        sizer_5.AddGrowableCol(2)
        sizer_3.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_6.Add(self.ReferralReason_Label, 0, wx.ALL, 4)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_6.Add(self.ReferralReason_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_6.AddGrowableCol(2)
        sizer_3.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_3, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_7.Add(self.PatientInfo_Label, 0, wx.ALL|wx.EXPAND, 4)
        sizer_8.Add(self.PatientFirstName_Label, 0, wx.ALL, 4)
        sizer_8.Add((60, 20), 0, 0, 0)
        sizer_8.Add(self.PatientFirstName_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_8.Add((20, 20), 0, 0, 0)
        sizer_8.AddGrowableCol(2)
        sizer_7.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_9.Add(self.PatientMiddleName_Label, 0, wx.ALL, 4)
        sizer_9.Add((51, 20), 0, 0, 0)
        sizer_9.Add(self.PatientMiddleName_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_9.Add((120, 20), 0, 0, 0)
        sizer_9.AddGrowableCol(2)
        sizer_7.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_10.Add(self.PatientLastName_Label, 0, wx.ALL, 4)
        sizer_10.Add((61, 20), 0, 0, 0)
        sizer_10.Add(self.PatientLastName_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_10.Add((120, 20), 0, 0, 0)
        sizer_10.AddGrowableCol(2)
        sizer_7.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_11.Add(self.PatientGender_Label, 0, wx.ALL, 4)
        sizer_11.Add((76, 20), 0, 0, 0)
        sizer_11.Add(self.PatientGender_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        sizer_11.Add((20, 20), 0, 0, 0)
        sizer_11.AddGrowableCol(2)
        sizer_7.Add(sizer_11, 0, wx.EXPAND, 0)
        sizer_12.Add(self.PatientAge_Label, 0, wx.ALL, 4)
        sizer_12.Add((92, 20), 0, 0, 0)
        sizer_12.Add(self.PatientAge_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        sizer_12.Add(self.PatientAgeDMY_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        sizer_12.Add(self.PatientAgeValidity_Combo, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        sizer_12.Add((20, 20), 0, 0, 0)
        sizer_7.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_13.Add(self.PatientAddress_Label, 0, wx.ALL, 4)
        sizer_13.Add((72, 20), 0, 0, 0)
        sizer_13.Add(self.PatientAddress_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 4)
        sizer_13.Add((20, 20), 0, 0, 0)
        sizer_13.AddGrowableCol(2)
        sizer_7.Add(sizer_13, 0, wx.EXPAND, 0)
        sizer_14.Add(self.PatientPhoneNumber_Label, 0, wx.ALL, 4)
        sizer_14.Add((41, 20), 0, 0, 0)
        sizer_14.Add(self.PatientPhoneNumber_TextCtrl, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 4)
        sizer_14.Add((20, 20), 0, 0, 0)
        sizer_14.AddGrowableCol(2)
        sizer_7.Add(sizer_14, 0, wx.EXPAND, 0)
        sizer_7.Add(self.static_line_4, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_24.Add((150, 20), 0, 0, 0)
        sizer_24.Add((160, 20), 0, 0, 0)
        sizer_24.Add(self.CreatePatient_Button, 0, wx.ALL|wx.EXPAND, 4)
        sizer_24.Add((20, 20), 0, 0, 0)
        sizer_2.Add(sizer_24, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def OnCreateRecord(self, event): # wxGlade: MyDialog.<event_handler>

        FirstName = self.TextCtrl_PatientFirstName.GetValue()
        MiddleName = self.TextCtrl_PatientMiddleName.GetValue()
        LastName = self.TextCtrl_PatientLastName.GetValue()
        Gender = self.Combo_PatientGender.GetValue()
        Age = self.TextCtrl_PatientAge.GetValue()
        DMY = self.Combo_PatientAgeDMY.GetValue()
        Validity = self.Combo_PatientAgeValidity.GetValue()
        Address = self.TextCtrl_PatientAddress.GetValue()
        Phone = self.TextCtrl_PatientPhoneNumber.GetValue()
        
        PatientName = FirstName + ' ' + MiddleName + ' ' + LastName
        
        self.parent.PatientInfo_Label.SetLabel(PatientName+'\n'+ 'Gender: ' + Gender + '\nAge: ' + Age + ' ' + DMY + ' ' + Validity +\
                                               '\nAddress: ' + Address + '\nPhone: ' + Phone)


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.PatientInfoHeader_Label = wx.StaticText(self, -1, "Patient Information", style=wx.ALIGN_CENTRE)
        self.PatientInfo_Label = wx.StaticText(self, -1, "No Information")

        self.static_line_6 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.frame_StatusBar = self.CreateStatusBar(1, 0)

        self.RxPanel = rxpanel.MyPanel(self, self, -1)        

        self.__set_properties()
        self.__do_layout()

        
	self.Bind(wx.EVT_SHOW, self.CreateReferPanel)
	self.Bind(wx.EVT_CLOSE, self.DestroyReferPanel)

        
	# call the Modal Window
        self.TextEntry("Please enter username:", "username")
        
        
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("RxBox - Philippine General Hospital")
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(wx.Colour(245, 255, 207))
        self.PatientInfoHeader_Label.SetMinSize((620, 20))
        #size = self.RxPanel.GetSize()
        #print "PanelSize: ", size
        #self.RxPanel.SetMinSize((1335,500))
        self.PatientInfoHeader_Label.SetBackgroundColour(wx.Colour(219, 219, 112))
        self.PatientInfoHeader_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.PatientInfo_Label.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.PatientInfo_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, ""))
        self.frame_StatusBar.SetStatusWidths([-1])
        # statusbar fields
        frame_StatusBar_fields = ["RxBox ready..."]
        for i in range(len(frame_StatusBar_fields)):
            self.frame_StatusBar.SetStatusText(frame_StatusBar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_19 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_5.Add(self.PatientInfoHeader_Label, 1, wx.EXPAND, 0)
        sizer_5.Add(self.PatientInfo_Label, 3, wx.TOP|wx.BOTTOM|wx.EXPAND, 1)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 1, wx.ALL|wx.EXPAND, 4)
        # add RxPanel
        sizer_3.Add(self.RxPanel, 5, wx.ALL|wx.EXPAND, 4)
        self.sizer_2.Add(sizer_3, 1, wx.ALL|wx.EXPAND, 4)
        self.sizer_2.Add(self.static_line_6, 0, wx.EXPAND, 0)
        # add ReferPanel
        # self.sizer_2.Add(self.ReferPanel, 1, wx.ALL|wx.EXPAND, 4)

        sizer_1.Add(self.sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
	

    def CreateReferPanel(self, event): # wxGlade: MyFrame.<event_handler>

        self.ReferPanel = referpanel.MyPanel(self, -1)
        self.sizer_2.Add(self.ReferPanel, 1, wx.ALL|wx.EXPAND, 4)
        # refresh the GUI
        self.Layout()
	
	#Messenger start
	#TODO: Check if connect()is succesful before starting messenger
	self.ReferPanel.phone.spawn()
	self.ReferPanel.phone.start()
	if self.ReferPanel.messenger.connect() is True:
		self.ReferPanel.messenger.start()
		
	self.ReferPanel.phone.setFrame(self)
	self.Bind(self.ReferPanel.phone.EVT_CALL_INCOMING, self.onCallIncoming)
        self.Bind(self.ReferPanel.phone.EVT_CALL_TERMINATED, self.onCallTerminated)
        self.Bind(self.ReferPanel.phone.EVT_CALL_FAILED, self.onCallFailed)
        self.Bind(self.ReferPanel.phone.EVT_CALL_ANSWERED, self.onCallAnswered)
	#handle Service Unavailable

	
    def DestroyReferPanel(self, event):
	# TODO: Destroy Main window cleanly
        try:
	    self.ReferPanel.phone.terminateCall()
            self.ReferPanel.messenger.stop() 	#Messenger stop
	    self.ReferPanel.phone.stop()
	    #time.sleep(3)
            self.ReferPanel.Destroy()

        except AttributeError:
            pass


    def onCallIncoming(self, event):
	print "received"
	self.RxPanel.StartStop_Button.Enable(True)
	    
    def onCallTerminated(self, event):
        self.RxPanel.onStartStop(event)
	    
    def onCallFailed(self, event):
	    print "failed"
	  
    def onCallAnswered(self, event):
	    print "answered"

    def TextEntry(self, message, text):
        self.username = "lifelink"
        dlg = wx.TextEntryDialog(self, message, "RxBox - Philippine General Hospital: User Authentication", defaultValue = text)
        dlg.CenterOnScreen()
        #dlg.SetValue("username")
        

        if dlg.ShowModal() == wx.ID_OK:
            if dlg.GetValue() == self.username:
                print "User Authenticated"
                self.SetTitle("RxBox - Philippine General Hospital" + ' - ' + self.username)
                dlg.Destroy()
            else:
                print "Invalid"
                self.TextEntry("Invalid!\nPlease enter username:", "")
        else:
        # when cancel is clicked
            print 'Main Window closed'
            dlg.Destroy()
            self.Close()

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame = MyFrame(None, -1, "")
    app.SetTopWindow(frame)
   
    frame.Show()
    frame.Maximize(True)
    app.MainLoop()
