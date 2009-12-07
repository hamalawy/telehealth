#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Mon Nov 23 14:26:55 2009

import wx

# begin wxGlade: extracode
# end wxGlade



class DAQPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: DAQPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.spo2_panel1 = wx.Panel(self, -1)
        self.heartrate_panel1 = wx.Panel(self, -1)
        self.bp_panel1 = wx.Panel(self, -1)
        self.panel_3 = wx.Panel(self, -1)
        self.button_window_separator = wx.StaticLine(self, -1)
        self.StartStop_Button = wx.BitmapButton(self, -1, wx.Bitmap("Icons/PlayButton.png", wx.BITMAP_TYPE_ANY))
        self.StartStop_Label = wx.StaticText(self, -1, "Start")
        self.static_line_1 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.Remark_Daq = wx.StaticText(self, -1, "       Remarks: ")
        self.RemarkValueDaq = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.Send_Button = wx.BitmapButton(self, -1, wx.Bitmap("Icons/Send.png", wx.BITMAP_TYPE_ANY))
        self.Send_Label = wx.StaticText(self, -1, "Send")
        self.Call_Button = wx.BitmapButton(self, -1, wx.Bitmap("Icons/Refer.png", wx.BITMAP_TYPE_ANY))
        self.Call_Label = wx.StaticText(self, -1, "Call")
        self.button_display_separator = wx.StaticLine(self, -1)
        self.calibrationtext = wx.StaticText(self, -1, "Calibration Signal", style=wx.ALIGN_CENTRE)
        self.calibrationsignal = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/CalibrationSignal.png", wx.BITMAP_TYPE_ANY))
        self.R_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/R_initial.png", wx.BITMAP_TYPE_ANY))
        self.L_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/L_initial.png", wx.BITMAP_TYPE_ANY))
        self.C1_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C1_initial.png", wx.BITMAP_TYPE_ANY))
        self.C2_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C2_initial.png", wx.BITMAP_TYPE_ANY))
        self.C3_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
        self.C4_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C4_initial.png", wx.BITMAP_TYPE_ANY))
        self.C5_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
        self.C6_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C6_initial.png", wx.BITMAP_TYPE_ANY))
        self.N_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        self.F_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/F_initial.png", wx.BITMAP_TYPE_ANY))
        self.lead12_button = wx.Button(self, -1, "12 Lead")
        self.ecg_label = wx.StaticText(self, -1, "ECG WAVEFORM", style=wx.ALIGN_CENTRE)
        self.ecg_lowerdata_separator = wx.StaticLine(self, -1)
        self.static_line_6 = wx.StaticLine(self.panel_3, -1, style=wx.LI_VERTICAL)
        self.bpNow_Button = wx.Button(self.panel_3, -1, "NOW")
        self.setBPmins_combobox = wx.ComboBox(self.panel_3, -1, choices=["5 min", "15 min", "30 min", "60 min"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.static_line_4 = wx.StaticLine(self.panel_3, -1, style=wx.LI_VERTICAL)
        self.bpbarpanel = wx.Panel(self.panel_3, -1)
        self.static_line_5 = wx.StaticLine(self.panel_3, -1, style=wx.LI_VERTICAL)
        self.bp_label = wx.StaticText(self.bp_panel1, -1, "Blood Pressure", style=wx.ALIGN_CENTRE)
        self.bp_infolabel = wx.StaticText(self.bp_panel1, -1, "--")
        self.bpvalue_label = wx.StaticText(self.bp_panel1, -1, "-- / --", style=wx.ALIGN_CENTRE)
        self.bprightpanel = wx.Panel(self.bp_panel1, -1)
        self.bpunit_label = wx.StaticText(self.bp_panel1, -1, "mmHg", style=wx.ALIGN_RIGHT)
        self.static_line_2 = wx.StaticLine(self.bp_panel1, -1, style=wx.LI_VERTICAL)
        self.heartrate_label = wx.StaticText(self.heartrate_panel1, -1, "Heart Rate", style=wx.ALIGN_CENTRE)
        self.heartrate_infolabel = wx.StaticText(self.heartrate_panel1, -1, "--")
        self.bpmvalue_label = wx.StaticText(self.heartrate_panel1, -1, "--", style=wx.ALIGN_CENTRE)
        self.bpmrightpanel = wx.Panel(self.heartrate_panel1, -1)
        self.bpmunit_label = wx.StaticText(self.heartrate_panel1, -1, "bpm", style=wx.ALIGN_RIGHT)
        self.static_line_3 = wx.StaticLine(self.heartrate_panel1, -1, style=wx.LI_VERTICAL)
        self.spo2_label = wx.StaticText(self.spo2_panel1, -1, "Blood Oxygen Saturation", style=wx.ALIGN_CENTRE)
        self.spo2_infolabel = wx.StaticText(self.spo2_panel1, -1, "--")
        self.spo2value_label = wx.StaticText(self.spo2_panel1, -1, "--", style=wx.ALIGN_CENTRE)
        self.spo2rightpanel = wx.Panel(self.spo2_panel1, -1)
        self.spo2unit_label = wx.StaticText(self.spo2_panel1, -1, "%SpO2", style=wx.ALIGN_RIGHT)
        self.daq_lowerdata_separator = wx.StaticLine(self, -1)

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
        self.Remark_Daq.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
        self.RemarkValueDaq.SetMinSize((250, 54))
        self.Send_Button.SetToolTipString("Stop data acquisition from the biomedical modules")
        self.Send_Button.Enable(False)
        self.Send_Button.SetSize(self.Send_Button.GetBestSize())
        self.Send_Label.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
        self.Call_Button.SetToolTipString("Stop data acquisition from the biomedical modules")
        self.Call_Button.Enable(False)
        self.Call_Button.SetSize(self.Call_Button.GetBestSize())
        self.Call_Label.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
        self.button_display_separator.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.calibrationtext.SetMinSize((93, 20))
        self.calibrationtext.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.calibrationtext.SetForegroundColour(wx.Colour(255, 255, 255))
        self.calibrationtext.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.lead12_button.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        self.lead12_button.Enable(False)
        self.ecg_label.SetMinSize((306, 20))
        self.ecg_label.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.ecg_label.SetForegroundColour(wx.Colour(255, 255, 255))
        self.ecg_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.bpNow_Button.SetMinSize((172,85))
        self.bpNow_Button.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpNow_Button.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        self.setBPmins_combobox.SetMinSize((172, 35))
        self.setBPmins_combobox.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.setBPmins_combobox.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.setBPmins_combobox.SetSelection(0)
        self.bpbarpanel.SetMinSize((20, 120))
        self.bpbarpanel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.panel_3.SetMinSize((148, 120))
        self.panel_3.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bp_label.SetMinSize((94, 30))
        self.bp_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bp_label.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.bp_infolabel.SetMinSize((145, 30))
        self.bp_infolabel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bp_infolabel.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.bpvalue_label.SetMinSize((142, 60))
        self.bpvalue_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpvalue_label.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bprightpanel.SetMinSize((142, 60))
        self.bprightpanel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpunit_label.SetMinSize((289, 20))
        self.bpunit_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpunit_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bp_panel1.SetMinSize((303, 84))
        self.bp_panel1.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.heartrate_label.SetMinSize((94, 30))
        self.heartrate_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.heartrate_label.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.heartrate_infolabel.SetMinSize((189, 30))
        self.heartrate_infolabel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.heartrate_infolabel.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.bpmvalue_label.SetMinSize((26, 60))
        self.bpmvalue_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpmvalue_label.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bpmrightpanel.SetMinSize((258, 60))
        self.bpmrightpanel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpmunit_label.SetMinSize((289, 20))
        self.bpmunit_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpmunit_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.heartrate_panel1.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.spo2_label.SetMinSize((160, 30))
        self.spo2_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.spo2_label.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.spo2_infolabel.SetMinSize((320, 30))
        self.spo2_infolabel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.spo2_infolabel.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.spo2value_label.SetMinSize((26, 60))
        self.spo2value_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.spo2value_label.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.spo2rightpanel.SetMinSize((454, 60))
        self.spo2rightpanel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.spo2unit_label.SetMinSize((485, 20))
        self.spo2unit_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.spo2unit_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.spo2_panel1.SetBackgroundColour(wx.Colour(226, 255, 180))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DAQPanel.__do_layout
        main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        daq_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        daq_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        ecg_biomodule_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ecg_vertical_sizer3 = wx.BoxSizer(wx.VERTICAL)
        biomodule_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        biomodule_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        spo2_sizer = wx.BoxSizer(wx.VERTICAL)
        spo2labelsizer = wx.BoxSizer(wx.HORIZONTAL)
        spo2_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        heartrate_sizer = wx.BoxSizer(wx.VERTICAL)
        bpmlabelsizer = wx.BoxSizer(wx.HORIZONTAL)
        heartrate_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        bp_sizer = wx.BoxSizer(wx.VERTICAL)
        bplabelsizer = wx.BoxSizer(wx.HORIZONTAL)
        bp_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        nowButton_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bpbarsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        nowButton_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        ecg_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ecg_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        image_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        lead12_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        ecm_lower_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ecm_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        ecm_horizontal_ltorso_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ecm_horizontal_utorso_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_vertical_sizer.Add(self.button_window_separator, 0, wx.EXPAND, 0)
        buttons_sizer.Add(self.StartStop_Button, 0, wx.ALL, 4)
        buttons_sizer.Add(self.StartStop_Label, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 4)
        buttons_sizer.Add(self.static_line_1, 0, wx.EXPAND, 0)
        buttons_sizer.Add(self.Remark_Daq, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        buttons_sizer.Add(self.RemarkValueDaq, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        buttons_sizer.Add((20, 20), 1, wx.ALL|wx.EXPAND, 0)
        buttons_sizer.Add(self.Send_Button, 0, wx.ALL, 4)
        buttons_sizer.Add(self.Send_Label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        buttons_sizer.Add(self.Call_Button, 0, wx.ALL, 4)
        buttons_sizer.Add(self.Call_Label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        main_vertical_sizer.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 0)
        main_vertical_sizer.Add(self.button_display_separator, 0, wx.ALL|wx.EXPAND, 2)
        image_vertical_sizer.Add(self.calibrationtext, 0, wx.ALL|wx.EXPAND, 4)
        image_vertical_sizer.Add(self.calibrationsignal, 0, 0, 0)
        image_vertical_sizer.Add((20, 20), 0, wx.EXPAND, 0)
        ecm_horizontal_utorso_sizer.Add(self.R_bitmap, 0, 0, 0)
        ecm_horizontal_utorso_sizer.Add(self.L_bitmap, 0, 0, 0)
        ecm_vertical_sizer.Add(ecm_horizontal_utorso_sizer, 1, 0, 0)
        ecm_horizontal_ltorso_sizer.Add(self.C1_bitmap, 0, 0, 0)
        ecm_horizontal_ltorso_sizer.Add(self.C2_bitmap, 0, 0, 0)
        ecm_horizontal_ltorso_sizer.Add(self.C3_bitmap, 0, 0, 0)
        ecm_horizontal_ltorso_sizer.Add(self.C4_bitmap, 0, 0, 0)
        ecm_horizontal_ltorso_sizer.Add(self.C5_bitmap, 0, 0, 0)
        ecm_horizontal_ltorso_sizer.Add(self.C6_bitmap, 0, 0, 0)
        ecm_vertical_sizer.Add(ecm_horizontal_ltorso_sizer, 2, wx.SHAPED, 0)
        image_vertical_sizer.Add(ecm_vertical_sizer, 0, 0, 1)
        ecm_lower_horizontal_sizer.Add(self.N_bitmap, 0, 0, 0)
        ecm_lower_horizontal_sizer.Add(self.F_bitmap, 0, 0, 0)
        image_vertical_sizer.Add(ecm_lower_horizontal_sizer, 1, wx.EXPAND, 0)
        lead12_vertical_sizer.Add(self.lead12_button, 1, wx.EXPAND, 0)
        lead12_vertical_sizer.Add((20, 50), 0, wx.EXPAND, 0)
        lead12_vertical_sizer.Add((20, 50), 0, wx.EXPAND, 0)
        image_vertical_sizer.Add(lead12_vertical_sizer, 1, wx.EXPAND, 0)
        daq_horizontal_sizer.Add(image_vertical_sizer, 0, 0, 0)
        daq_vertical_sizer.Add(self.ecg_label, 0, wx.ALL|wx.EXPAND, 4)
        ecg_horizontal_sizer.Add(ecg_vertical_sizer, 1, wx.EXPAND, 0)
        ecg_vertical_sizer3.Add(ecg_horizontal_sizer, 4, wx.EXPAND, 0)
        ecg_vertical_sizer3.Add(self.ecg_lowerdata_separator, 0, wx.EXPAND, 0)
        sizer_6.Add(self.static_line_6, 0, wx.EXPAND, 0)
        nowButton_vertical_sizer.Add(self.bpNow_Button, 2, wx.EXPAND, 0)
        nowButton_vertical_sizer.Add(self.setBPmins_combobox, 1, wx.EXPAND, 0)
        nowButton_horizontal_sizer.Add(nowButton_vertical_sizer, 3, wx.BOTTOM|wx.EXPAND, 4)
        sizer_5.Add(self.static_line_4, 0, wx.EXPAND, 0)
        sizer_5.Add(self.bpbarpanel, 1, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_5, 0, wx.EXPAND, 0)
        bpbarsizer.Add(sizer_5, 1, wx.EXPAND, 0)
        nowButton_horizontal_sizer.Add(bpbarsizer, 1, wx.EXPAND, 0)
        sizer_6.Add(nowButton_horizontal_sizer, 1, wx.EXPAND, 0)
        self.panel_3.SetSizer(sizer_6)
        biomodule_horizontal_sizer.Add(self.panel_3, 1, wx.EXPAND, 0)
        bp_label_sizer.Add(self.bp_label, 2, wx.BOTTOM, 1)
        bp_label_sizer.Add(self.bp_infolabel, 3, wx.BOTTOM|wx.EXPAND, 1)
        bp_sizer.Add(bp_label_sizer, 0, wx.EXPAND, 0)
        bplabelsizer.Add(self.bpvalue_label, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        bplabelsizer.Add(self.bprightpanel, 1, wx.EXPAND, 0)
        bp_sizer.Add(bplabelsizer, 1, wx.EXPAND, 0)
        bp_sizer.Add(self.bpunit_label, 0, wx.EXPAND, 0)
        sizer_1.Add(bp_sizer, 1, wx.EXPAND, 0)
        sizer_1.Add(self.static_line_2, 0, wx.EXPAND, 0)
        self.bp_panel1.SetSizer(sizer_1)
        biomodule_horizontal_sizer.Add(self.bp_panel1, 2, wx.EXPAND, 0)
        heartrate_label_sizer.Add(self.heartrate_label, 2, wx.BOTTOM|wx.EXPAND, 1)
        heartrate_label_sizer.Add(self.heartrate_infolabel, 3, wx.BOTTOM|wx.EXPAND, 1)
        heartrate_sizer.Add(heartrate_label_sizer, 0, wx.EXPAND, 0)
        bpmlabelsizer.Add(self.bpmvalue_label, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        bpmlabelsizer.Add(self.bpmrightpanel, 1, wx.EXPAND|wx.ALIGN_RIGHT, 0)
        heartrate_sizer.Add(bpmlabelsizer, 1, wx.EXPAND, 0)
        heartrate_sizer.Add(self.bpmunit_label, 0, wx.EXPAND, 0)
        sizer_4.Add(heartrate_sizer, 1, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_3, 0, wx.EXPAND, 0)
        self.heartrate_panel1.SetSizer(sizer_4)
        biomodule_horizontal_sizer.Add(self.heartrate_panel1, 2, wx.EXPAND, 0)
        spo2_label_sizer.Add(self.spo2_label, 2, wx.BOTTOM|wx.EXPAND, 1)
        spo2_label_sizer.Add(self.spo2_infolabel, 3, wx.BOTTOM|wx.EXPAND, 1)
        spo2_sizer.Add(spo2_label_sizer, 0, wx.EXPAND, 0)
        spo2labelsizer.Add(self.spo2value_label, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        spo2labelsizer.Add(self.spo2rightpanel, 1, wx.EXPAND|wx.ALIGN_RIGHT, 0)
        spo2_sizer.Add(spo2labelsizer, 1, wx.EXPAND, 0)
        spo2_sizer.Add(self.spo2unit_label, 0, wx.EXPAND, 0)
        self.spo2_panel1.SetSizer(spo2_sizer)
        biomodule_horizontal_sizer.Add(self.spo2_panel1, 2, wx.EXPAND, 0)
        biomodule_vertical_sizer.Add(biomodule_horizontal_sizer, 1, wx.EXPAND, 0)
        ecg_vertical_sizer3.Add(biomodule_vertical_sizer, 1, wx.EXPAND, 0)
        ecg_biomodule_horizontal_sizer.Add(ecg_vertical_sizer3, 1, wx.EXPAND, 0)
        daq_vertical_sizer.Add(ecg_biomodule_horizontal_sizer, 1, wx.EXPAND, 0)
        daq_horizontal_sizer.Add(daq_vertical_sizer, 5, wx.EXPAND, 0)
        main_vertical_sizer.Add(daq_horizontal_sizer, 1, wx.EXPAND, 0)
        main_vertical_sizer.Add(self.daq_lowerdata_separator, 0, wx.EXPAND, 0)
        self.SetSizer(main_vertical_sizer)
        main_vertical_sizer.Fit(self)
        # end wxGlade

    def onStartStop(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `onStartStop' not implemented!"
        event.Skip()

    def onSend(self, event): # wxGlade: DAQPanel.<event_handler>
        print "Event handler `onSend' not implemented!"
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

# end of class DAQPanel


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_3 = (None, -1, "")
    app.SetTopWindow(frame_3)
    frame_3.Show()
    app.MainLoop()
