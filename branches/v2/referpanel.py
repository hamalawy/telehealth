import wx, os
from wxMessenger import wxMessenger
from Linphone import Linphone
# added for photosnapshot
import opencv
from opencv import highgui
# added for photosnapshot

PGH_EXTENSION	= '2001'
PGH_JID		= '2001@openfire'
RXBOX_EXTENSION	= '2002'
RXBOX_JID	= '2002@openfire'
RXBOX_PWD	= '12345'

class MyPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
	self.messenger = wxMessenger(RXBOX_JID, RXBOX_PWD, self, -1,)
	self.phone = Linphone(self)
        self.Videoconf_Label = wx.StaticText(self, -1, "Video Conference", style=wx.ALIGN_CENTRE)
        self.Videoconf_Panel = wx.Panel(self, -1)
        self.Photoshot_Label = wx.StaticText(self, -1, "Photo Snapshot", style=wx.ALIGN_CENTRE)
        self.Photoshot_Panel = wx.Panel(self, -1)
        # added for photosnapshot
        self.Capture_Button = wx.Button(self, -1, "CAPTURE!")
        self.camera = highgui.cvCreateCameraCapture(1)
        self.image_counter = 0
        # added for photosnapshot
        
        self.static_line_5 = wx.StaticLine(self, -1)
        self.IM_Label = wx.StaticText(self, -1, "Instant Messaging", style=wx.ALIGN_CENTRE)
        self.Remarks_Label = wx.StaticText(self, -1, "Remarks", style=wx.ALIGN_CENTRE)
        self.Remarks_Text = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()

        # added for photosnapshot
        self.Bind(wx.EVT_BUTTON, self.onCapture, self.Capture_Button)
        # end wxGlade
	
	os.environ['SDL_VIDEODRIVER']='x11'
	os.environ['SDL_VIDEO_YUV_HWACCEL']='0'
        os.environ['SDL_WINDOWID']=str(self.Videoconf_Panel.GetHandle())
	

    def __set_properties(self):
        # begin wxGlade: MyPanel.__set_properties
        self.Videoconf_Label.SetMinSize((620, 20))
        self.Videoconf_Label.SetBackgroundColour(wx.Colour(251, 255, 100))
        self.Videoconf_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.Videoconf_Panel.SetBackgroundColour(wx.Colour(244, 244, 244))
        self.Photoshot_Label.SetMinSize((620, 20))
        self.Photoshot_Label.SetBackgroundColour(wx.Colour(251, 255, 100))
        self.Photoshot_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.Photoshot_Panel.SetBackgroundColour(wx.Colour(244, 244, 244))
        self.IM_Label.SetMinSize((620, 20))
        self.IM_Label.SetBackgroundColour(wx.Colour(253, 255, 191))
        self.IM_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.Remarks_Label.SetMinSize((620, 20))
        self.Remarks_Label.SetBackgroundColour(wx.Colour(253, 255, 191))
        self.Remarks_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.Remarks_Text.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_19 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_11.Add(self.Videoconf_Label, 1, wx.RIGHT|wx.EXPAND, 1)
        sizer_11.Add(self.Videoconf_Panel, 8, wx.RIGHT|wx.TOP|wx.EXPAND, 1)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_12.Add(self.Photoshot_Label, 1, wx.LEFT|wx.EXPAND, 1)
        sizer_12.Add(self.Photoshot_Panel, 8, wx.LEFT|wx.TOP|wx.EXPAND, 1)
        # added for photosnapshot
        sizer_12.Add(self.Capture_Button, 1, wx.EXPAND, 0)
        sizer_10.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_10, 5, wx.ALL|wx.EXPAND, 4)
        sizer_6.Add(self.static_line_5, 0, wx.EXPAND, 0)
        sizer_14.Add(self.IM_Label, 1, wx.RIGHT|wx.EXPAND, 1)
        sizer_14.Add(self.messenger, 8, wx.EXPAND, 0)
        sizer_13.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_19.Add(self.Remarks_Label, 1, wx.LEFT|wx.EXPAND, 1)
        sizer_19.Add(self.Remarks_Text, 8, wx.TOP|wx.EXPAND, 1)
        sizer_13.Add(sizer_19, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_13, 5, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(sizer_6)
        sizer_6.Fit(self)
        # end wxGlade

	
    def onCapture(self, event):

        self.buffer = highgui.cvQueryFrame(self.camera)
        self.im = highgui.cvQueryFrame(self.camera)
        self.im = opencv.cvGetMat(self.im)
        self.im = opencv.adaptors.Ipl2PIL(self.im)
        filename = 'img' + str(self.image_counter) + '.jpg'
        self.im.save('Photos/'+filename)
        raw = wx.Image('Photos/'+filename)
        # (308, 267) is the size of the picture after getting the
        # size of the panel
        bmp = raw.Rescale(308,267)
        bmp = bmp.ConvertToBitmap()
        wx.StaticBitmap(self.Photoshot_Panel, -1, bmp)
        self.image_counter += 1
        
        

# end of class MyPanel


class MyDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        #wx.Dialog.__init__(self)
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


