#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Aug 30 10:53:55 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class ECG_config_frame(wx.Frame):
    def __init__(self, parent,*args, **kwds):
        # begin wxGlade: ECG_config_frame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self,parent, *args, **kwds)
        self.panel_1 = wx.Panel(parent, -1)
        self.panel_3 = wx.Panel(self.panel_1, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.static_line_1 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_copy = wx.StaticText(self.panel_1, -1, "Simulated              ")
        self.ecgsim_checkbox = wx.CheckBox(self.panel_1, -1, "")
        self.static_line_1_copy = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy = wx.StaticText(self.panel_1, -1, "Simulation File      ")
        self.ecg_cbox = wx.ComboBox(self.panel_1, -1, choices=["Normal", "Others"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.static_line_1_copy_1 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_1 = wx.StaticText(self.panel_1, -1, "Port                        ")
        self.ecg_porttxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_2 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_2 = wx.StaticText(self.panel_1, -1, "Baud Rate             ")
        self.ecg_baudtxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_3 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_3 = wx.StaticText(self.panel_1, -1, "Timeout                 ")
        self.ecg_timeouttxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_4 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_4 = wx.StaticText(self.panel_1, -1, "DAQ Duration        ")
        self.ecg_daqdurtxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_5 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_5 = wx.StaticText(self.panel_1, -1, "ECM Check            ")
        self.ecg_ecmtxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_6 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_6 = wx.StaticText(self.panel_1, -1, "Filter                      ")
        self.ecgfilter_checkbox = wx.CheckBox(self.panel_1, -1, "")
        self.static_line_1_copy_7 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_7 = wx.StaticText(self.panel_1, -1, "Debug                    ")
        self.ecgdebug_checkbox = wx.CheckBox(self.panel_1, -1, "")
        self.static_line_1_copy_8 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_8 = wx.StaticText(self.panel_1, -1, "Frequency             ")
        self.ecg_freqtxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_9 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_9 = wx.StaticText(self.panel_1, -1, "Mode                     ")
        self.ecg_modecbox = wx.ComboBox(self.panel_1, -1, choices=["3 Lead", "12 Lead"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.static_line_1_copy_10 = wx.StaticLine(self.panel_1, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.onBrowse, self.ecg_cbox)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ECG_config_frame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((420, 520))
        self.panel_3.SetMinSize((420, 20))
        self.panel_2.SetMinSize((40, 500))
        self.static_line_1.SetMinSize((380, 2))
        self.label_1_copy_copy.SetMinSize((122, 25))
        self.static_line_1_copy.SetMinSize((380, 2))
        self.label_1_copy.SetMinSize((122, 25))
        self.ecg_cbox.SetMinSize((150, 29))
        self.ecg_cbox.SetSelection(0)
        self.static_line_1_copy_1.SetMinSize((380, 2))
        self.label_1_copy_1.SetMinSize((122, 25))
        self.ecg_porttxt.SetMinSize((200, 27))
        self.static_line_1_copy_2.SetMinSize((380, 2))
        self.label_1_copy_2.SetMinSize((122, 25))
        self.ecg_baudtxt.SetMinSize((150, 27))
        self.static_line_1_copy_3.SetMinSize((380, 2))
        self.label_1_copy_3.SetMinSize((122, 25))
        self.ecg_timeouttxt.SetMinSize((150, 27))
        self.static_line_1_copy_4.SetMinSize((380, 2))
        self.label_1_copy_4.SetMinSize((122, 25))
        self.ecg_daqdurtxt.SetMinSize((150, 27))
        self.static_line_1_copy_5.SetMinSize((380, 2))
        self.label_1_copy_5.SetMinSize((122, 25))
        self.ecg_ecmtxt.SetMinSize((150, 27))
        self.static_line_1_copy_6.SetMinSize((380, 2))
        self.label_1_copy_6.SetMinSize((122, 25))
        self.static_line_1_copy_7.SetMinSize((380, 2))
        self.label_1_copy_7.SetMinSize((122, 25))
        self.static_line_1_copy_8.SetMinSize((380, 2))
        self.label_1_copy_8.SetMinSize((122, 25))
        self.ecg_freqtxt.SetMinSize((150, 27))
        self.static_line_1_copy_9.SetMinSize((380, 2))
        self.label_1_copy_9.SetMinSize((122, 25))
        self.ecg_modecbox.SetMinSize((150, 29))
        self.ecg_modecbox.SetSelection(1)
        self.static_line_1_copy_10.SetMinSize((380, 2))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ECG_config_frame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4_copy_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_4.Add(self.label_1_copy_copy, 0, 0, 0)
        sizer_4.Add(self.ecgsim_checkbox, 0, 0, 0)
        sizer_3.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy, 0, wx.EXPAND, 0)
        sizer_4_copy.Add(self.label_1_copy, 0, 0, 0)
        sizer_4_copy.Add(self.ecg_cbox, 0, 0, 0)
        sizer_3.Add(sizer_4_copy, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_1, 0, wx.EXPAND, 0)
        sizer_4_copy_1.Add(self.label_1_copy_1, 0, 0, 0)
        sizer_4_copy_1.Add(self.ecg_porttxt, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_1, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_2, 0, wx.EXPAND, 0)
        sizer_4_copy_2.Add(self.label_1_copy_2, 0, 0, 0)
        sizer_4_copy_2.Add(self.ecg_baudtxt, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_2, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_3, 0, wx.EXPAND, 0)
        sizer_4_copy_3.Add(self.label_1_copy_3, 0, 0, 0)
        sizer_4_copy_3.Add(self.ecg_timeouttxt, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_3, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_4, 0, wx.EXPAND, 0)
        sizer_4_copy_4.Add(self.label_1_copy_4, 0, 0, 0)
        sizer_4_copy_4.Add(self.ecg_daqdurtxt, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_4, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_5, 0, wx.EXPAND, 0)
        sizer_4_copy_5.Add(self.label_1_copy_5, 0, 0, 0)
        sizer_4_copy_5.Add(self.ecg_ecmtxt, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_5, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_6, 0, wx.EXPAND, 0)
        sizer_4_copy_6.Add(self.label_1_copy_6, 0, 0, 0)
        sizer_4_copy_6.Add(self.ecgfilter_checkbox, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_6, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_7, 0, wx.EXPAND, 0)
        sizer_4_copy_7.Add(self.label_1_copy_7, 0, 0, 0)
        sizer_4_copy_7.Add(self.ecgdebug_checkbox, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_7, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_8, 0, wx.EXPAND, 0)
        sizer_4_copy_8.Add(self.label_1_copy_8, 0, 0, 0)
        sizer_4_copy_8.Add(self.ecg_freqtxt, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_8, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_9, 0, wx.EXPAND, 0)
        sizer_4_copy_9.Add(self.label_1_copy_9, 0, 0, 0)
        sizer_4_copy_9.Add(self.ecg_modecbox, 0, 0, 0)
        sizer_3.Add(sizer_4_copy_9, 0, wx.EXPAND, 0)
        sizer_3.Add(self.static_line_1_copy_10, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_2_copy, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def onBrowse(self, event): # wxGlade: ECG_config_frame.<event_handler>
        print "Event handler `onBrowse' not implemented!"
        event.Skip()

# end of class ECG_config_frame


