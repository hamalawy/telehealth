#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Nov 16 23:36:16 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.main = wx.Panel(self, -1)
        self.panel_8 = wx.Panel(self.main, -1)
        self.panel_7 = wx.Panel(self.main, -1)
        self.panel_6 = wx.Panel(self.main, -1)
        self.panel_5 = wx.Panel(self.main, -1)
        self.panel_1 = wx.Panel(self.main, -1)
        self.panel_2 = wx.Panel(self.main, -1)
        self.panel_4 = wx.Panel(self.main, -1)
        self.panel_4_copy = wx.Panel(self.panel_4, -1)
        self.panel_15 = wx.Panel(self.main, -1)
        self.label_14 = wx.StaticText(self.panel_15, -1, "BP Calibration")
        self.label_15 = wx.StaticText(self.panel_15, -1, "Beta")
        self.panel_14_copy = wx.Panel(self.main, -1)
        self.panel_13 = wx.Panel(self.main, -1)
        self.panel_14 = wx.Panel(self.main, -1)
        self.panel_3_copy = wx.Panel(self.main, -1)
        self.label_3 = wx.StaticText(self.panel_4_copy, -1, "STEP 1")
        self.label_4 = wx.StaticText(self.panel_4, -1, "BP Mercurial Reading:\n")
        self.label_5 = wx.StaticText(self.panel_4, -1, "Systolic / Dastolic")
        self.Sys_Merc_txt = wx.TextCtrl(self.panel_4, -1, "")
        self.label_6 = wx.StaticText(self.panel_4, -1, "/")
        self.Dias_Merc_txt = wx.TextCtrl(self.panel_4, -1, "")
        self.panel_3 = wx.Panel(self.main, -1)
        self.label_2 = wx.StaticText(self.panel_2, -1, "STEP 2")
        self.bpNow_Button = wx.Button(self.panel_1, -1, "BP NOW")
        self.setBPmaxpressure_combobox = wx.ComboBox(self.panel_1, -1, choices=["140 mmHg", "160 mmHg", "180 mmHg", "200 mmHg", "220 mmHg", "240 mmHg"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.bpbarpanel = wx.Panel(self.panel_1, -1)
        self.bp_label = wx.StaticText(self.panel_1, -1, "Blood Pressure", style=wx.ALIGN_CENTRE)
        self.bpvalue_label = wx.StaticText(self.panel_1, -1, "-- / --", style=wx.ALIGN_CENTRE)
        self.bpunit_label = wx.StaticText(self.panel_1, -1, "mmHg", style=wx.ALIGN_RIGHT)
        self.static_line_1 = wx.StaticLine(self.panel_1, -1)
        self.label_1 = wx.StaticText(self.panel_1, -1, "Status: ")
        self.bp_infolabel = wx.StaticText(self.panel_1, -1, "--")
        self.panel_9 = wx.Panel(self.main, -1)
        self.panel_12 = wx.Panel(self.main, -1)
        self.label_7 = wx.StaticText(self.panel_5, -1, "STEP 3")
        self.label_8 = wx.StaticText(self.panel_6, -1, "Record Data: ")
        self.button_1 = wx.Button(self.panel_6, -1, "RECORD")
        self.static_line_2 = wx.StaticLine(self.main, -1)
        self.label_9 = wx.StaticText(self.panel_7, -1, "Note: After recording, you can add more samples by repeating the process from step 1")
        self.panel_11 = wx.Panel(self.main, -1)
        self.panel_10 = wx.Panel(self.main, -1)
        self.panel_11_copy = wx.Panel(self.main, -1)
        self.label_12 = wx.StaticText(self.panel_8, -1, "Rxbox 1.0")
        self.version_label = wx.StaticText(self.panel_8, -1, "version: Adam")
        self.static_line_3 = wx.StaticLine(self.panel_8, -1)
        self.label_10 = wx.StaticText(self.panel_8, -1, "Number of Samples: ")
        self.Samples_label = wx.StaticText(self.panel_8, -1, "0")
        self.label_11 = wx.StaticText(self.panel_8, -1, "\n\n\nIf samples are adequate, \n            Press \"Calibrate\"")
        self.Calibrate_button = wx.Button(self.panel_8, -1, "Calibrate")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onBPNow, self.bpNow_Button)
        self.Bind(wx.EVT_BUTTON, self.onRecord, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.onCalibrate, self.Calibrate_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((935, 350))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_14.SetMinSize((214, 32))
        self.label_14.SetForegroundColour(wx.Colour(35, 35, 142))
        self.label_14.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_14_copy.SetMinSize((1000, 10))
        self.panel_14_copy.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.panel_13.SetMinSize((700,3))
        self.panel_13.SetBackgroundColour(wx.Colour(66, 111, 66))
        self.panel_14.SetMinSize((1000, 10))
        self.panel_14.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.panel_3_copy.SetMinSize((10, 150))
        self.panel_3_copy.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_3.SetMinSize((180, 17))
        self.label_3.SetBackgroundColour(wx.Colour(35, 35, 142))
        self.label_3.SetForegroundColour(wx.Colour(255, 255, 255))
        self.label_3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_4_copy.SetMinSize((200, 17))
        self.panel_4_copy.SetBackgroundColour(wx.Colour(35, 35, 142))
        self.label_4.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_5.SetFont(wx.Font(10, wx.ROMAN, wx.ITALIC, wx.NORMAL, 0, ""))
        self.Sys_Merc_txt.SetMinSize((80, 50))
        self.Sys_Merc_txt.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
        self.label_6.SetFont(wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.Dias_Merc_txt.SetMinSize((80, 50))
        self.Dias_Merc_txt.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
        self.panel_4.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.panel_3.SetMinSize((10, 150))
        self.panel_3.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_2.SetForegroundColour(wx.Colour(255, 255, 255))
        self.label_2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_2.SetBackgroundColour(wx.Colour(35, 35, 142))
        self.bpNow_Button.SetMinSize((109, 75))
        self.bpNow_Button.SetBackgroundColour(wx.Colour(196, 209, 255))
        self.bpNow_Button.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        self.bpNow_Button.SetToolTipString("Acquire One-Shot BP Reading")
        self.setBPmaxpressure_combobox.SetMinSize((109, 38))
        self.setBPmaxpressure_combobox.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.setBPmaxpressure_combobox.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))
        self.setBPmaxpressure_combobox.SetToolTipString("Set BP Acquisition Interval")
        self.setBPmaxpressure_combobox.SetSelection(2)
        self.bpbarpanel.SetMinSize((20,150))
        self.bpbarpanel.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bp_label.SetMinSize((151, 15))
        self.bp_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bp_label.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.bpvalue_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpvalue_label.SetFont(wx.Font(30, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.bpunit_label.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.bpunit_label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.label_1.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.label_1.SetForegroundColour(wx.Colour(0, 0, 0))
        self.label_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
        self.bp_infolabel.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.bp_infolabel.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.panel_1.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.panel_9.SetMinSize((500, 10))
        self.panel_9.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.panel_12.SetMinSize((10, 78))
        self.panel_12.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_7.SetForegroundColour(wx.Colour(255, 255, 255))
        self.label_7.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_5.SetBackgroundColour(wx.Colour(35, 35, 142))
        self.label_8.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_1.SetBackgroundColour(wx.Colour(196, 209, 255))
        self.button_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_6.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.panel_7.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.panel_11.SetMinSize((10, 255))
        self.panel_11.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.panel_10.SetMinSize((3, 255))
        self.panel_10.SetBackgroundColour(wx.Colour(66, 111, 66))
        self.panel_11_copy.SetMinSize((10, 255))
        self.panel_11_copy.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_12.SetFont(wx.Font(25, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.static_line_3.SetMinSize((200, 2))
        self.label_10.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.LIGHT, 0, ""))
        self.Samples_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.Calibrate_button.SetMinSize((130, 180))
        self.Calibrate_button.SetBackgroundColour(wx.Colour(196, 209, 255))
        self.panel_8.SetMinSize((300, 265))
        self.panel_8.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.main.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_20 = wx.BoxSizer(wx.VERTICAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        bpnow_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bp_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_4_copy = wx.BoxSizer(wx.HORIZONTAL)
        bplabelsizer = wx.BoxSizer(wx.HORIZONTAL)
        bp_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        nowButton_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_21 = wx.BoxSizer(wx.VERTICAL)
        sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_22.Add((50, 50), 0, 0, 0)
        sizer_22.Add(self.label_14, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_22.Add(self.label_15, 0, wx.ALIGN_BOTTOM, 0)
        self.panel_15.SetSizer(sizer_22)
        sizer_2.Add(self.panel_15, 0, wx.EXPAND, 0)
        sizer_21.Add(self.panel_14_copy, 0, wx.EXPAND, 0)
        sizer_21.Add(self.panel_13, 0, wx.EXPAND, 0)
        sizer_21.Add(self.panel_14, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_21, 0, wx.EXPAND, 0)
        sizer_3.Add(self.panel_3_copy, 0, wx.EXPAND, 0)
        sizer_8.Add(self.label_3, 0, 0, 0)
        self.panel_4_copy.SetSizer(sizer_8)
        sizer_7.Add(self.panel_4_copy, 0, wx.EXPAND, 0)
        sizer_7.Add(self.label_4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(self.label_5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_9.Add((10, 20), 0, 0, 0)
        sizer_9.Add(self.Sys_Merc_txt, 0, 0, 0)
        sizer_9.Add(self.label_6, 0, 0, 0)
        sizer_9.Add(self.Dias_Merc_txt, 0, 0, 0)
        sizer_7.Add(sizer_9, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        self.panel_4.SetSizer(sizer_7)
        sizer_3.Add(self.panel_4, 1, wx.EXPAND, 0)
        sizer_3.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_5_copy.Add(self.label_2, 0, 0, 0)
        self.panel_2.SetSizer(sizer_5_copy)
        sizer_4.Add(self.panel_2, 0, wx.EXPAND, 0)
        nowButton_vertical_sizer.Add(self.bpNow_Button, 1, wx.EXPAND, 0)
        nowButton_vertical_sizer.Add(self.setBPmaxpressure_combobox, 0, wx.EXPAND, 0)
        bpnow_horizontal_sizer.Add(nowButton_vertical_sizer, 0, wx.ALL|wx.EXPAND, 1)
        bpnow_horizontal_sizer.Add(self.bpbarpanel, 0, wx.ALL|wx.EXPAND, 0)
        bp_label_sizer.Add(self.bp_label, 2, wx.BOTTOM, 1)
        bp_label_sizer.Add((100, 20), 0, 0, 0)
        bp_sizer.Add(bp_label_sizer, 0, wx.EXPAND, 0)
        bplabelsizer.Add(self.bpvalue_label, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        bp_sizer.Add(bplabelsizer, 1, wx.ALL|wx.EXPAND, 0)
        bp_sizer.Add(self.bpunit_label, 0, wx.ALIGN_RIGHT, 0)
        bp_sizer.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_4_copy.Add(self.label_1, 0, 0, 0)
        sizer_4_copy.Add(self.bp_infolabel, 1, wx.BOTTOM|wx.EXPAND, 1)
        bp_sizer.Add(sizer_4_copy, 0, wx.EXPAND, 0)
        bpnow_horizontal_sizer.Add(bp_sizer, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(bpnow_horizontal_sizer)
        sizer_4.Add(self.panel_1, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_6.Add(sizer_3, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(self.panel_9, 0, wx.EXPAND, 0)
        sizer_10.Add(self.panel_12, 0, wx.EXPAND, 0)
        sizer_12.Add(self.label_7, 0, 0, 0)
        self.panel_5.SetSizer(sizer_12)
        sizer_11.Add(self.panel_5, 0, wx.EXPAND, 0)
        sizer_13.Add((100, 20), 0, 0, 0)
        sizer_13.Add(self.label_8, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        self.panel_6.SetSizer(sizer_13)
        sizer_11.Add(self.panel_6, 1, wx.EXPAND, 0)
        sizer_14.Add(self.static_line_2, 0, wx.EXPAND, 0)
        sizer_15.Add(self.label_9, 0, 0, 0)
        self.panel_7.SetSizer(sizer_15)
        sizer_14.Add(self.panel_7, 0, wx.EXPAND, 0)
        sizer_11.Add(sizer_14, 0, wx.EXPAND, 0)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_18.Add(self.panel_11, 0, wx.EXPAND, 0)
        sizer_18.Add(self.panel_10, 0, wx.EXPAND, 0)
        sizer_18.Add(self.panel_11_copy, 0, wx.EXPAND, 0)
        sizer_5.Add(sizer_18, 0, wx.EXPAND, 0)
        sizer_16.Add(self.label_12, 0, 0, 0)
        sizer_16.Add(self.version_label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_20.Add(self.static_line_3, 0, wx.EXPAND, 0)
        sizer_17.Add(self.label_10, 0, 0, 0)
        sizer_17.Add(self.Samples_label, 0, 0, 0)
        sizer_20_copy.Add(sizer_17, 0, wx.EXPAND, 0)
        sizer_20_copy.Add(self.label_11, 0, 0, 0)
        sizer_19.Add(sizer_20_copy, 0, wx.EXPAND, 0)
        sizer_19.Add(self.Calibrate_button, 0, 0, 0)
        sizer_20.Add(sizer_19, 0, wx.EXPAND, 0)
        sizer_16.Add(sizer_20, 0, wx.EXPAND, 0)
        self.panel_8.SetSizer(sizer_16)
        sizer_5.Add(self.panel_8, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(sizer_5, 0, wx.EXPAND, 0)
        self.main.SetSizer(sizer_2)
        sizer_1.Add(self.main, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def onBPNow(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `onBPNow' not implemented!"
        event.Skip()

    def onRecord(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `onRecord' not implemented!"
        event.Skip()

    def onCalibrate(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `onCalibrate' not implemented!"
        event.Skip()

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
