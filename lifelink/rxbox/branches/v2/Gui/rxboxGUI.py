#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sat Jul 04 23:04:52 2009

import wx

# begin wxGlade: extracode
# end wxGlade



class RxFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RxFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.RxFrame_StatusBar = self.CreateStatusBar(1, 0)
        self.PatientInfoHeader_Label = wx.StaticText(self, -1, "Patient Information", style=wx.ALIGN_CENTRE)
        self.LastName = wx.StaticText(self, -1, "Last Name:   ")
        self.LastNameValue = wx.TextCtrl(self, -1, "")
        self.FirstName = wx.StaticText(self, -1, "First Name:   ")
        self.FirstNameValue = wx.TextCtrl(self, -1, "")
        self.MiddleName = wx.StaticText(self, -1, "Middle Name:   ")
        self.MiddleNameValue = wx.TextCtrl(self, -1, "")
        self.Gender = wx.StaticText(self, -1, "Gender:   ")
        self.GenderCombo = wx.ComboBox(self, -1, choices=["", "Male", "Female"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Address = wx.StaticText(self, -1, "Address:   ")
        self.AddressValue = wx.TextCtrl(self, -1, "")
        self.PhoneNumber = wx.StaticText(self, -1, "Phone Number:   ")
        self.PhoneNumberValue = wx.TextCtrl(self, -1, "")
        self.Birthdate = wx.StaticText(self, -1, "Birthdate:")
        self.isEstimated = wx.CheckBox(self, -1, "Estimated")
        self.BirthMonth = wx.ComboBox(self, -1, choices=["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], style=wx.CB_DROPDOWN|wx.CB_SIMPLE|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.BirthDayCombo = wx.ComboBox(self, -1, choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.BirthYear = wx.TextCtrl(self, -1, "")
        self.Age = wx.StaticText(self, -1, "Age:   ")
        self.AgeValue = wx.TextCtrl(self, -1, "")
        self.AgeCombo = wx.ComboBox(self, -1, choices=["Years", "Months", "Days"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.panel_1 = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RxFrame.__set_properties
        self.SetTitle("RxBox - Philippine General Hospital")
        self.SetSize((1288, 778))
        self.SetBackgroundColour(wx.Colour(245, 255, 207))
        self.RxFrame_StatusBar.SetStatusWidths([-1])
        # statusbar fields
        RxFrame_StatusBar_fields = ["RxBox ready..."]
        for i in range(len(RxFrame_StatusBar_fields)):
            self.RxFrame_StatusBar.SetStatusText(RxFrame_StatusBar_fields[i], i)
        self.PatientInfoHeader_Label.SetBackgroundColour(wx.Colour(219, 219, 112))
        self.PatientInfoHeader_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.GenderCombo.SetMinSize((85, 29))
        self.GenderCombo.SetSelection(0)
        self.AddressValue.SetMinSize((220, 27))
        self.PhoneNumberValue.SetMinSize((75, 27))
        self.BirthMonth.SetMinSize((120, 29))
        self.BirthMonth.SetSelection(0)
        self.BirthDayCombo.SetMinSize((60, 29))
        self.BirthDayCombo.SetSelection(-1)
        self.BirthYear.SetMinSize((70, 27))
        self.AgeValue.SetMinSize((60, 27))
        self.AgeCombo.SetMinSize((120, 29))
        self.AgeCombo.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RxFrame.__do_layout
        mainvertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.mainhorizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.info_daq_sizer = wx.BoxSizer(wx.VERTICAL)
        patient_info_tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        patient_info_sizer = wx.BoxSizer(wx.VERTICAL)
        info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        patient_info_sizer.Add(self.PatientInfoHeader_Label, 1, wx.EXPAND, 0)
        sizer_6.Add(self.LastName, 0, 0, 0)
        sizer_6.Add(self.LastNameValue, 0, 0, 0)
        sizer_6.Add((20, 27), 0, 0, 0)
        sizer_6.Add(self.FirstName, 0, 0, 0)
        sizer_6.Add(self.FirstNameValue, 0, 0, 0)
        sizer_6.Add((20, 27), 0, 0, 0)
        sizer_6.Add(self.MiddleName, 0, 0, 0)
        sizer_6.Add(self.MiddleNameValue, 0, 0, 0)
        sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_8.Add(self.Gender, 0, 0, 0)
        sizer_8.Add(self.GenderCombo, 0, 0, 0)
        sizer_8.Add(self.Address, 0, 0, 0)
        sizer_8.Add(self.AddressValue, 0, 0, 0)
        sizer_8.Add(self.PhoneNumber, 0, 0, 0)
        sizer_8.Add(self.PhoneNumberValue, 0, 0, 0)
        sizer_1.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_9.Add(self.Birthdate, 0, 0, 0)
        sizer_9.Add(self.isEstimated, 0, 0, 0)
        sizer_9.Add(self.BirthMonth, 0, 0, 0)
        sizer_9.Add(self.BirthDayCombo, 0, 0, 0)
        sizer_9.Add(self.BirthYear, 0, 0, 0)
        sizer_9.Add(self.Age, 0, 0, 0)
        sizer_9.Add(self.AgeValue, 0, 0, 0)
        sizer_9.Add(self.AgeCombo, 0, 0, 0)
        sizer_1.Add(sizer_9, 1, wx.EXPAND, 0)
        info_sizer.Add(sizer_1, 1, wx.EXPAND, 0)
        patient_info_sizer.Add(info_sizer, 0, wx.EXPAND, 0)
        patient_info_tab_sizer.Add(patient_info_sizer, 2, wx.EXPAND, 0)
        patient_info_tab_sizer.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.info_daq_sizer.Add(patient_info_tab_sizer, 0, wx.ALL|wx.EXPAND, 4)
        self.mainhorizontal_sizer.Add(self.info_daq_sizer, 3, wx.EXPAND, 0)
        mainvertical_sizer.Add(self.mainhorizontal_sizer, 1, wx.EXPAND, 0)
        self.SetSizer(mainvertical_sizer)
        self.Layout()
        self.Centre()
        # end wxGlade

# end of class RxFrame


class DAQPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: DAQPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.button_window_separator = wx.StaticLine(self, -1)
        self.StartStop_Button = wx.BitmapButton(self, -1, wx.Bitmap("Icons/PlayButton.png", wx.BITMAP_TYPE_ANY))
        self.StartStop_Label = wx.StaticText(self, -1, "Start")
        self.Send_Button = wx.BitmapButton(self, -1, wx.Bitmap("Icons/Send.png", wx.BITMAP_TYPE_ANY))
        self.Send_Label = wx.StaticText(self, -1, "Send")
        self.Call_Button = wx.BitmapButton(self, -1, wx.Bitmap("Icons/Refer.png", wx.BITMAP_TYPE_ANY))
        self.Call_Label = wx.StaticText(self, -1, "Call")
        self.button_display_separator = wx.StaticLine(self, -1)
        self.nodeplacement_Bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/NodePlacement.png", wx.BITMAP_TYPE_ANY), style=wx.SIMPLE_BORDER)
        self.calibsignal_Bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/CalibrationSignal.png", wx.BITMAP_TYPE_ANY), style=wx.SIMPLE_BORDER)
        self.lead12_button = wx.Button(self, -1, "12 Lead")
        self.ecg_label = wx.StaticText(self, -1, "ECG WAVEFORM", style=wx.ALIGN_CENTRE)
        self.ecg_lowerdata_separator = wx.StaticLine(self, -1)
        self.bpNow_Button = wx.Button(self, -1, "NOW")
        self.setBPmins_combobox = wx.ComboBox(self, -1, choices=["5 min", "15 min", "30 min", "60 min"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.bpbarpanel = wx.Panel(self, -1)
        self.bp_label = wx.StaticText(self, -1, "Blood Pressure", style=wx.ALIGN_CENTRE)
        self.bp_infolabel = wx.StaticText(self, -1, "--")
        self.bpvalue_label = wx.StaticText(self, -1, "-- / --", style=wx.ALIGN_CENTRE)
        self.bprightpanel = wx.Panel(self, -1)
        self.bpunit_label = wx.StaticText(self, -1, "mmHg", style=wx.ALIGN_RIGHT)
        self.heartrate_label = wx.StaticText(self, -1, "Heart Rate", style=wx.ALIGN_CENTRE)
        self.heartrate_infolabel = wx.StaticText(self, -1, "--")
        self.bpmvalue_label = wx.StaticText(self, -1, "--", style=wx.ALIGN_CENTRE)
        self.bpmrightpanel = wx.Panel(self, -1)
        self.bpmunit_label = wx.StaticText(self, -1, "bpm", style=wx.ALIGN_RIGHT)
        self.spo2_label = wx.StaticText(self, -1, "Blood Oxygen\nSaturation", style=wx.ALIGN_CENTRE)
        self.spo2_infolabel = wx.StaticText(self, -1, "--")
        self.spo2value_label = wx.StaticText(self, -1, "--", style=wx.ALIGN_CENTRE)
        self.spo2rightpanel = wx.Panel(self, -1)
        self.spo2unit_label = wx.StaticText(self, -1, "%SpO2", style=wx.ALIGN_RIGHT)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onStartStop, self.StartStop_Button)
        self.Bind(wx.EVT_BUTTON, self.onSend, self.Send_Button)
        self.Bind(wx.EVT_BUTTON, self.onCall, self.Call_Button)
        self.Bind(wx.EVT_BUTTON, self.on12Lead, self.lead12_button)
        self.Bind(wx.EVT_BUTTON, self.onBPNow, self.bpNow_Button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: DAQPanel.__set_properties
        self.StartStop_Button.SetBackgroundColour(wx.Colour(50, 50, 204))
        self.StartStop_Button.SetToolTipString("Start data acquisition from the biomedical modules")
        self.StartStop_Button.SetSize(self.StartStop_Button.GetBestSize())
        self.StartStop_Label.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
        self.Send_Button.SetToolTipString("Stop data acquisition from the biomedical modules")
        self.Send_Button.Enable(False)
        self.Send_Button.SetSize(self.Send_Button.GetBestSize())
        self.Send_Label.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
        self.Call_Button.SetToolTipString("Stop data acquisition from the biomedical modules")
        self.Call_Button.Enable(False)
        self.Call_Button.SetSize(self.Call_Button.GetBestSize())
        self.Call_Label.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
        self.button_display_separator.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.lead12_button.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        self.lead12_button.Enable(False)
        self.ecg_label.SetMinSize((306, 20))
        self.ecg_label.SetBackgroundColour(wx.Colour(241, 123, 241))
        self.ecg_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bpNow_Button.SetMinSize((323, 66))
        self.bpNow_Button.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bpNow_Button.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        self.setBPmins_combobox.SetMinSize((323, 21))
        self.setBPmins_combobox.SetForegroundColour(wx.Colour(255, 217, 222))
        self.setBPmins_combobox.SetSelection(0)
        self.bpbarpanel.SetMinSize((45, 95))
        self.bpbarpanel.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bp_label.SetMinSize((60, 30))
        self.bp_label.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bp_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.bp_infolabel.SetMinSize((145, 30))
        self.bp_infolabel.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bp_infolabel.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.bpvalue_label.SetMinSize((60, 40))
        self.bpvalue_label.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bpvalue_label.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bprightpanel.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bpunit_label.SetMinSize((60, 30))
        self.bpunit_label.SetBackgroundColour(wx.Colour(255, 217, 222))
        self.bpunit_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.heartrate_label.SetMinSize((60, 30))
        self.heartrate_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.heartrate_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.heartrate_infolabel.SetMinSize((145, 30))
        self.heartrate_infolabel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.heartrate_infolabel.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.bpmvalue_label.SetMinSize((60, 40))
        self.bpmvalue_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpmvalue_label.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bpmrightpanel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpmunit_label.SetMinSize((60, 30))
        self.bpmunit_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpmunit_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.spo2_label.SetMinSize((60, 30))
        self.spo2_label.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.spo2_infolabel.SetMinSize((145, 30))
        self.spo2_infolabel.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2_infolabel.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.spo2value_label.SetMinSize((60, 40))
        self.spo2value_label.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2value_label.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.spo2rightpanel.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2unit_label.SetMinSize((60, 30))
        self.spo2unit_label.SetBackgroundColour(wx.Colour(201, 248, 255))
        self.spo2unit_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DAQPanel.__do_layout
        main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        lowerdata_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        spo2_sizer = wx.BoxSizer(wx.VERTICAL)
        spo2labelsizer = wx.BoxSizer(wx.HORIZONTAL)
        spo2_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        heartrate_sizer = wx.BoxSizer(wx.VERTICAL)
        bpmlabelsizer = wx.BoxSizer(wx.HORIZONTAL)
        heartrate_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bp_sizer = wx.BoxSizer(wx.VERTICAL)
        bplabelsizer = wx.BoxSizer(wx.HORIZONTAL)
        bp_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        nowButton_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bpbarsizer = wx.BoxSizer(wx.HORIZONTAL)
        nowButton_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        ecg_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ecg_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        image_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        lead12_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_vertical_sizer.Add(self.button_window_separator, 0, wx.EXPAND, 0)
        buttons_sizer.Add(self.StartStop_Button, 0, wx.ALL, 4)
        buttons_sizer.Add(self.StartStop_Label, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 4)
        buttons_sizer.Add((20, 20), 1, wx.ALL|wx.EXPAND, 4)
        buttons_sizer.Add(self.Send_Button, 0, wx.ALL, 4)
        buttons_sizer.Add(self.Send_Label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        buttons_sizer.Add(self.Call_Button, 0, wx.ALL, 4)
        buttons_sizer.Add(self.Call_Label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        main_vertical_sizer.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 0)
        main_vertical_sizer.Add(self.button_display_separator, 0, wx.ALL|wx.EXPAND, 2)
        image_vertical_sizer.Add(self.nodeplacement_Bitmap, 0, wx.ALL|wx.EXPAND, 4)
        image_vertical_sizer.Add(self.calibsignal_Bitmap, 1, wx.ALL|wx.EXPAND, 4)
        lead12_vertical_sizer.Add(self.lead12_button, 1, wx.EXPAND, 0)
        lead12_vertical_sizer.Add((20, 50), 0, wx.EXPAND, 0)
        lead12_vertical_sizer.Add((20, 50), 0, wx.EXPAND, 0)
        image_vertical_sizer.Add(lead12_vertical_sizer, 1, wx.EXPAND, 0)
        ecg_horizontal_sizer.Add(image_vertical_sizer, 0, 0, 0)
        self.ecg_vertical_sizer.Add(self.ecg_label, 0, wx.ALL|wx.EXPAND, 4)
        ecg_horizontal_sizer.Add(self.ecg_vertical_sizer, 5, wx.EXPAND, 0)
        main_vertical_sizer.Add(ecg_horizontal_sizer, 1, wx.EXPAND, 0)
        main_vertical_sizer.Add(self.ecg_lowerdata_separator, 0, wx.EXPAND, 0)
        nowButton_vertical_sizer.Add(self.bpNow_Button, 2, wx.EXPAND, 0)
        nowButton_vertical_sizer.Add(self.setBPmins_combobox, 1, wx.EXPAND, 0)
        nowButton_horizontal_sizer.Add(nowButton_vertical_sizer, 1, wx.BOTTOM|wx.EXPAND, 4)
        bpbarsizer.Add(self.bpbarpanel, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 4)
        nowButton_horizontal_sizer.Add(bpbarsizer, 1, wx.EXPAND, 0)
        lowerdata_horizontal_sizer.Add(nowButton_horizontal_sizer, 2, wx.TOP|wx.BOTTOM|wx.EXPAND, 0)
        bp_label_sizer.Add(self.bp_label, 1, wx.BOTTOM, 1)
        bp_label_sizer.Add(self.bp_infolabel, 1, wx.BOTTOM|wx.EXPAND, 1)
        bp_sizer.Add(bp_label_sizer, 0, wx.EXPAND, 0)
        bplabelsizer.Add(self.bpvalue_label, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        bplabelsizer.Add(self.bprightpanel, 1, wx.EXPAND, 0)
        bp_sizer.Add(bplabelsizer, 1, wx.EXPAND, 0)
        bp_sizer.Add(self.bpunit_label, 0, wx.EXPAND, 0)
        lowerdata_horizontal_sizer.Add(bp_sizer, 3, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 4)
        heartrate_label_sizer.Add(self.heartrate_label, 1, wx.BOTTOM|wx.EXPAND, 1)
        heartrate_label_sizer.Add(self.heartrate_infolabel, 1, wx.BOTTOM|wx.EXPAND, 1)
        heartrate_sizer.Add(heartrate_label_sizer, 0, wx.EXPAND, 0)
        bpmlabelsizer.Add(self.bpmvalue_label, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        bpmlabelsizer.Add(self.bpmrightpanel, 1, wx.EXPAND|wx.ALIGN_RIGHT, 0)
        heartrate_sizer.Add(bpmlabelsizer, 1, wx.EXPAND, 0)
        heartrate_sizer.Add(self.bpmunit_label, 0, wx.EXPAND, 0)
        lowerdata_horizontal_sizer.Add(heartrate_sizer, 3, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 4)
        spo2_label_sizer.Add(self.spo2_label, 1, wx.BOTTOM|wx.EXPAND, 1)
        spo2_label_sizer.Add(self.spo2_infolabel, 1, wx.BOTTOM|wx.EXPAND, 1)
        spo2_sizer.Add(spo2_label_sizer, 0, wx.EXPAND, 0)
        spo2labelsizer.Add(self.spo2value_label, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        spo2labelsizer.Add(self.spo2rightpanel, 1, wx.EXPAND|wx.ALIGN_RIGHT, 0)
        spo2_sizer.Add(spo2labelsizer, 1, wx.EXPAND, 0)
        spo2_sizer.Add(self.spo2unit_label, 0, wx.EXPAND, 0)
        lowerdata_horizontal_sizer.Add(spo2_sizer, 3, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 4)
        main_vertical_sizer.Add(lowerdata_horizontal_sizer, 0, wx.EXPAND, 0)
        self.SetSizer(main_vertical_sizer)
        main_vertical_sizer.Fit(self)
        # end wxGlade

    def onStartStop(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `onStartStop' not implemented!"
        event.Skip()

    def onUpload(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `onUpload' not implemented!"
        event.Skip()

    def onCall(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `onCall' not implemented!"
        event.Skip()

    def on12Lead(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `on12Lead' not implemented!"
        event.Skip()

    def onBPNow(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `onBPNow' not implemented!"
        event.Skip()

    def onSend(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `onSend' not implemented"
        event.Skip()

# end of class DAQPanel



class ReferPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: refer_panel_new.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.Videoconf_Label = wx.StaticText(self, -1, "Video", style=wx.ALIGN_CENTRE)
        self.video_panel = wx.Panel(self, -1)
        self.snap_prev = wx.Button(self, -1, "Snapshot")
        self.Photosnap_label = wx.StaticText(self, -1, "Snapshot", style=wx.ALIGN_CENTRE)
        self.photo_panel = wx.Panel(self, -1)
        self.prev_snapshot = wx.Button(self, -1, "<<  Prev")
        self.next_snapshot = wx.Button(self, -1, "Next >>")
        self.IM_Label = wx.StaticText(self, -1, "Instant Messaging", style=wx.ALIGN_CENTRE)
        self.IMtexts_Text = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_READONLY)
        self.IMreply_Text = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onSnapshot, self.snap_prev)
        self.Bind(wx.EVT_BUTTON, self.onPrevSnapshot, self.prev_snapshot)
        self.Bind(wx.EVT_BUTTON, self.onNextSnapshot, self.next_snapshot)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: refer_panel_new.__set_properties
        self.Videoconf_Label.SetBackgroundColour(wx.Colour(251, 255, 100))
        self.Videoconf_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.video_panel.SetMinSize((320,240))
        self.snap_prev.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.Photosnap_label.SetBackgroundColour(wx.Colour(251, 255, 100))
        self.Photosnap_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.photo_panel.SetMinSize((320,240))
        self.prev_snapshot.SetBackgroundColour(wx.Colour(255, 127, 0))
        self.next_snapshot.SetBackgroundColour(wx.Colour(255, 127, 0))
        self.IM_Label.SetMinSize((620, 20))
        self.IM_Label.SetBackgroundColour(wx.Colour(253, 255, 191))
        self.IM_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.IMtexts_Text.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.IMreply_Text.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: refer_panel_new.__do_layout
        refer_panel_sizer = wx.FlexGridSizer(3, 1, 0, 0)
        im_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        photosnap_sizer = wx.BoxSizer(wx.VERTICAL)
        photo_holder = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_2 = wx.GridSizer(1, 2, 0, 0)
        video_sizer = wx.BoxSizer(wx.VERTICAL)
        video_holder = wx.FlexGridSizer(2, 1, 0, 0)
        video_sizer.Add(self.Videoconf_Label, 0, wx.ALL|wx.EXPAND, 0)
        video_holder.Add(self.video_panel, 0, wx.ALL|wx.EXPAND, 0)
        video_holder.Add(self.snap_prev, 0, wx.ALL|wx.EXPAND, 0)
        video_sizer.Add(video_holder, 1, wx.EXPAND, 0)
        refer_panel_sizer.Add(video_sizer, 1, wx.ALL|wx.EXPAND, 0)
        photosnap_sizer.Add(self.Photosnap_label, 0, wx.ALL|wx.EXPAND, 0)
        photo_holder.Add(self.photo_panel, 0, wx.ALL|wx.EXPAND, 0)
        grid_sizer_2.Add(self.prev_snapshot, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.next_snapshot, 0, wx.EXPAND, 0)
        photo_holder.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        photosnap_sizer.Add(photo_holder, 1, wx.EXPAND, 0)
        refer_panel_sizer.Add(photosnap_sizer, 1, wx.EXPAND, 0)
        im_sizer.Add(self.IM_Label, 1, wx.RIGHT|wx.EXPAND, 1)
        sizer_18.Add(self.IMtexts_Text, 3, wx.TOP|wx.EXPAND, 1)
        sizer_18.Add(self.IMreply_Text, 0, wx.TOP|wx.EXPAND, 4)
        im_sizer.Add(sizer_18, 8, wx.EXPAND, 0)
        refer_panel_sizer.Add(im_sizer, 1, wx.EXPAND, 0)
        self.SetSizer(refer_panel_sizer)
        refer_panel_sizer.Fit(self)
        # end wxGlade

    def onSnapshot(self, event): # wxGlade: refer_panel_new.<event_handler>
        print "Event handler `onSnapshot' not implemented!"
        event.Skip()

    def onPrevSnapshot(self, event): # wxGlade: refer_panel_new.<event_handler>
        print "Event handler `onPrevSnapshot' not implemented!"
        event.Skip()

    def onNextSnapshot(self, event): # wxGlade: refer_panel_new.<event_handler>
        print "Event handler `onNextSnapshot' not implemented!"
        event.Skip()


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = RxFrame(None, -1, "")
    app.SetTopWindow(rx_frame)
    rx_frame.Show()
    app.MainLoop()
