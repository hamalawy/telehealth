#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon May 31 14:54:48 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.panel_6 = wx.Panel(self.panel_1, -1)
        self.bitmap_2 = wx.StaticBitmap(self.panel_1, -1, wx.Bitmap("logo.bmp", wx.BITMAP_TYPE_ANY))
        self.label_1 = wx.StaticText(self.panel_1, -1, "Telehealth", style=wx.ALIGN_RIGHT)
        self.panel_3 = wx.Panel(self.panel_1, -1)
        self.panel_3_copy = wx.Panel(self.panel_1, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.bitmap_1 = wx.StaticBitmap(self.panel_1, -1, wx.Bitmap("no_photo.bmp", wx.BITMAP_TYPE_ANY))
        self.panel_2_copy = wx.Panel(self.panel_1, -1)
        self.pic_previous = wx.Button(self.panel_1, -1, "<<")
        self.pic_next = wx.Button(self.panel_1, -1, ">>")
        self.label_2 = wx.StaticText(self.panel_1, -1, "Patient Information:")
        self.panel_4 = wx.Panel(self.panel_1, -1)
        self.label_3 = wx.StaticText(self.panel_1, -1, "Patient ID :")
        self.patientid_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_3_copy = wx.StaticText(self.panel_1, -1, "First Name:")
        self.firstname_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_3_copy_1 = wx.StaticText(self.panel_1, -1, "Middle Name :")
        self.middlename_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_3_copy_2 = wx.StaticText(self.panel_1, -1, "Last Name :")
        self.lastname_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_3_copy_3 = wx.StaticText(self.panel_1, -1, "Sex :")
        self.sex_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_3_copy_3_copy = wx.StaticText(self.panel_1, -1, "Age :")
        self.age_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_3_copy_4_copy = wx.StaticText(self.panel_1, -1, "Birthdate :")
        self.birthdate_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_2_copy = wx.StaticText(self.panel_1, -1, "Session :")
        self.panel_4_copy = wx.Panel(self.panel_1, -1)
        self.label_3_copy_5 = wx.StaticText(self.panel_1, -1, "Date Taken :")
        self.date_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_3_copy_copy = wx.StaticText(self.panel_1, -1, "Time Taken :")
        self.time_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.remarks1_text = wx.StaticText(self.panel_1, -1, "Remarks :")
        self.remarks_text = wx.StaticText(self.panel_1, -1, "--------------------------")
        self.label_2_copy_copy = wx.StaticText(self.panel_1, -1, "Load EDF :")
        self.load_file_button = wx.Button(self.panel_1, -1, "FILE")
        self.load_database_button = wx.Button(self.panel_1, -1, "DATABASE")
        self.panel_5 = wx.Panel(self.panel_1, -1)
        self.label_4 = wx.StaticText(self.panel_6, -1, "\n\n\nBlood\nOxygen")
        self.panel_6_copy = wx.Panel(self.panel_6, -1)
        self.bloodox_panel = wx.Panel(self.panel_6, -1)
        self.label_4_copy = wx.StaticText(self.panel_6, -1, "\n\n\nHeart\nRate")
        self.panel_6_copy_1 = wx.Panel(self.panel_6, -1)
        self.heartrate_panel = wx.Panel(self.panel_6, -1)
        self.label_4_copy_1 = wx.StaticText(self.panel_6, -1, "\n\n\nSystolic")
        self.panel_6_copy_2 = wx.Panel(self.panel_6, -1)
        self.systolic_panel = wx.Panel(self.panel_6, -1)
        self.label_4_copy_2 = wx.StaticText(self.panel_6, -1, "\n\n\nDiastolic")
        self.panel_6_copy_3 = wx.Panel(self.panel_6, -1)
        self.diastolic_panel = wx.Panel(self.panel_6, -1)
        self.label_4_copy_3 = wx.StaticText(self.panel_6, -1, "\n\n\nECG")
        self.panel_6_copy_2_copy = wx.Panel(self.panel_6, -1)
        self.ecg_panel = wx.Panel(self.panel_6, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onPicprevious, self.pic_previous)
        self.Bind(wx.EVT_BUTTON, self.onPicnext, self.pic_next)
        self.Bind(wx.EVT_BUTTON, self.onFileopen, self.load_file_button)
        self.Bind(wx.EVT_BUTTON, self.onDBopen, self.load_database_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((1150, 720))
        self.label_1.SetFont(wx.Font(30, wx.ROMAN, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_3.SetMinSize((350,2))
        self.panel_3.SetBackgroundColour(wx.Colour(21, 255, 30))
        self.panel_3_copy.SetMinSize((350, 2))
        self.panel_3_copy.SetBackgroundColour(wx.Colour(21, 255, 30))
        self.panel_2.SetMinSize((2, 200))
        self.panel_2.SetBackgroundColour(wx.Colour(21, 255, 30))
        self.bitmap_1.SetMinSize((250, 200))
        self.panel_2_copy.SetMinSize((2, 200))
        self.panel_2_copy.SetBackgroundColour(wx.Colour(21, 255, 30))
        self.pic_previous.SetMinSize((40, 30))
        self.pic_next.SetMinSize((40, 30))
        self.label_2.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
        self.panel_4.SetMinSize((50, 180))
        self.panel_4.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_2_copy.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
        self.panel_4_copy.SetMinSize((50, 50))
        self.panel_4_copy.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_2_copy_copy.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Sans"))
        self.load_file_button.SetMinSize((80, 30))
        self.load_database_button.SetMinSize((90, 30))
        self.panel_5.SetMinSize((10, 720))
        self.label_4.SetMinSize((60, 144))
        self.label_4.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.label_4.SetForegroundColour(wx.Colour(0, 0, 0))
        self.label_4.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_6_copy.SetMinSize((720, 10))
        self.panel_6_copy.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.bloodox_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_4_copy.SetMinSize((60, 144))
        self.label_4_copy.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.label_4_copy.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_6_copy_1.SetMinSize((720, 10))
        self.panel_6_copy_1.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.heartrate_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_4_copy_1.SetMinSize((60, 144))
        self.label_4_copy_1.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.label_4_copy_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_6_copy_2.SetMinSize((720, 10))
        self.panel_6_copy_2.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.systolic_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_4_copy_2.SetMinSize((60, 144))
        self.label_4_copy_2.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.label_4_copy_2.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_6_copy_3.SetMinSize((720, 10))
        self.panel_6_copy_3.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.diastolic_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_4_copy_3.SetMinSize((60, 144))
        self.label_4_copy_3.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.label_4_copy_3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.panel_6_copy_2_copy.SetMinSize((720, 10))
        self.panel_6_copy_2_copy.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.ecg_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.panel_6.SetBackgroundColour(wx.Colour(230, 221, 213))
        self.panel_1.SetBackgroundColour(wx.Colour(255, 255, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_17_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18_copy_1_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_19_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18_copy_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_17_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18_copy_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18_copy = wx.BoxSizer(wx.VERTICAL)
        heart_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        bo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_6_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_13_copy_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13_copy_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13_copy_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20 = wx.BoxSizer(wx.VERTICAL)
        sizer_13_copy_4_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_13_copy_3_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_13_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8.Add(self.bitmap_2, 0, 0, 0)
        sizer_8.Add(self.label_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_7.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_7.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_9.Add((350, 10), 0, 0, 0)
        sizer_9.Add(self.panel_3_copy, 0, wx.EXPAND, 0)
        sizer_9.Add((350, 10), 0, 0, 0)
        sizer_3.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_5.Add((40, 200), 0, 0, 0)
        sizer_5.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_4.Add(self.bitmap_1, 0, 0, 0)
        sizer_5_copy.Add(self.panel_2_copy, 0, wx.EXPAND, 0)
        sizer_5_copy.Add((40, 200), 0, 0, 0)
        sizer_4.Add(sizer_5_copy, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_3.Add((350, 10), 0, 0, 0)
        sizer_6.Add((90, 30), 0, 0, 0)
        sizer_6.Add(self.pic_previous, 0, 0, 0)
        sizer_6.Add((90, 30), 0, 0, 0)
        sizer_6.Add(self.pic_next, 0, 0, 0)
        sizer_6.Add((86, 30), 0, 0, 0)
        sizer_3.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_3.Add((350, 20), 0, 0, 0)
        sizer_3.Add(self.label_2, 0, 0, 0)
        sizer_11.Add(self.panel_4, 0, wx.EXPAND, 0)
        sizer_13.Add(self.label_3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13.Add(self.patientid_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_13_copy.Add(self.label_3_copy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy.Add(self.firstname_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12.Add(sizer_13_copy, 1, wx.EXPAND, 0)
        sizer_13_copy_1.Add(self.label_3_copy_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_1.Add(self.middlename_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12.Add(sizer_13_copy_1, 1, wx.EXPAND, 0)
        sizer_13_copy_2.Add(self.label_3_copy_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_2.Add(self.lastname_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12.Add(sizer_13_copy_2, 1, wx.EXPAND, 0)
        sizer_13_copy_3.Add(self.label_3_copy_3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_3.Add(self.sex_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_20_copy.Add(sizer_13_copy_3, 1, wx.EXPAND, 0)
        sizer_12.Add(sizer_20_copy, 1, wx.EXPAND, 0)
        sizer_13_copy_3_copy.Add(self.label_3_copy_3_copy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_3_copy.Add(self.age_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12.Add(sizer_13_copy_3_copy, 1, wx.EXPAND, 0)
        sizer_20.Add(sizer_12, 0, wx.EXPAND, 0)
        sizer_13_copy_4_copy.Add(self.label_3_copy_4_copy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_4_copy.Add(self.birthdate_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_20.Add(sizer_13_copy_4_copy, 0, wx.EXPAND, 0)
        sizer_11.Add(sizer_20, 1, wx.EXPAND, 0)
        sizer_10.Add(sizer_11, 0, wx.EXPAND, 0)
        sizer_10.Add(self.label_2_copy, 0, 0, 0)
        sizer_11_copy.Add(self.panel_4_copy, 0, wx.EXPAND, 0)
        sizer_13_copy_5.Add(self.label_3_copy_5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_5.Add(self.date_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12_copy.Add(sizer_13_copy_5, 1, wx.EXPAND, 0)
        sizer_13_copy_copy.Add(self.label_3_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_copy.Add(self.time_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12_copy.Add(sizer_13_copy_copy, 1, wx.EXPAND, 0)
        sizer_13_copy_copy_1.Add(self.remarks1_text, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13_copy_copy_1.Add(self.remarks_text, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_12_copy.Add(sizer_13_copy_copy_1, 1, wx.EXPAND, 0)
        sizer_11_copy.Add(sizer_12_copy, 1, wx.EXPAND, 0)
        sizer_10.Add(sizer_11_copy, 0, wx.EXPAND, 0)
        sizer_10.Add((350, 20), 0, 0, 0)
        sizer_10.Add(self.label_2_copy_copy, 0, 0, 0)
        sizer_6_copy.Add((78, 30), 0, 0, 0)
        sizer_6_copy.Add(self.load_file_button, 0, 0, 0)
        sizer_6_copy.Add((20, 30), 0, 0, 0)
        sizer_6_copy.Add(self.load_database_button, 0, 0, 0)
        sizer_6_copy.Add((78, 30), 0, 0, 0)
        sizer_10.Add(sizer_6_copy, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 2)
        sizer_2.Add(self.panel_5, 0, wx.EXPAND, 0)
        sizer_17.Add(self.label_4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_18.Add(self.panel_6_copy, 0, wx.EXPAND, 0)
        bo_sizer.Add(self.bloodox_panel, 1, wx.EXPAND, 0)
        sizer_18.Add(bo_sizer, 1, wx.EXPAND, 0)
        sizer_17.Add(sizer_18, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_17, 0, wx.EXPAND, 0)
        sizer_17_copy.Add(self.label_4_copy, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_18_copy.Add(self.panel_6_copy_1, 0, wx.EXPAND, 0)
        heart_sizer.Add(self.heartrate_panel, 1, wx.EXPAND, 0)
        sizer_18_copy.Add(heart_sizer, 1, wx.EXPAND, 0)
        sizer_17_copy.Add(sizer_18_copy, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_17_copy, 0, wx.EXPAND, 0)
        sizer_17_copy_1.Add(self.label_4_copy_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_18_copy_1.Add(self.panel_6_copy_2, 0, wx.EXPAND, 0)
        sizer_19.Add(self.systolic_panel, 1, wx.EXPAND, 0)
        sizer_18_copy_1.Add(sizer_19, 1, wx.EXPAND, 0)
        sizer_17_copy_1.Add(sizer_18_copy_1, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_17_copy_1, 0, wx.EXPAND, 0)
        sizer_17_copy_2.Add(self.label_4_copy_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_18_copy_2.Add(self.panel_6_copy_3, 0, wx.EXPAND, 0)
        sizer_18_copy_2.Add(self.diastolic_panel, 1, wx.EXPAND, 0)
        sizer_17_copy_2.Add(sizer_18_copy_2, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_17_copy_2, 0, wx.EXPAND, 0)
        sizer_17_copy_3.Add(self.label_4_copy_3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_18_copy_1_copy.Add(self.panel_6_copy_2_copy, 0, wx.EXPAND, 0)
        sizer_19_copy.Add(self.ecg_panel, 1, wx.EXPAND, 0)
        sizer_18_copy_1_copy.Add(sizer_19_copy, 1, wx.EXPAND, 0)
        sizer_17_copy_3.Add(sizer_18_copy_1_copy, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_17_copy_3, 0, wx.EXPAND, 0)
        self.panel_6.SetSizer(sizer_16)
        sizer_2.Add(self.panel_6, 1, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def onPicprevious(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `onPicprevious' not implemented!"
        event.Skip()

    def onPicnext(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `onPicnext' not implemented!"
        event.Skip()

    def onFileopen(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `onFileopen' not implemented"
        event.Skip()

    def onDBopen(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `onDBopen' not implemented"
        event.Skip()

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    localedf = MyFrame(None, -1, "")
    app.SetTopWindow(localedf)
    localedf.Show()
    app.MainLoop()
