#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Aug 30 23:25:43 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class BP_config_frame(wx.Frame):
    def __init__(self, parent,*args, **kwds):
        # begin wxGlade: ECG_config_frame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self,parent, *args, **kwds)
        self.panel_1 = wx.Panel(parent, -1)
        self.panel_3 = wx.Panel(self.panel_1, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.static_line_1 = wx.StaticLine(self.panel_1, -1)
        self.label_7 = wx.StaticText(self.panel_1, -1, "Simulated                   ")
        self.bpsim_checkbox = wx.CheckBox(self.panel_1, -1, "")
        self.static_line_1_copy = wx.StaticLine(self.panel_1, -1)
        self.label_7_copy = wx.StaticText(self.panel_1, -1, "Sim Type  ")
        self.bp_simtypecbox = wx.ComboBox(self.panel_1, -1, choices=["Low", "Normal", "High"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN|wx.CB_READONLY)
        self.static_line_1_copy_1 = wx.StaticLine(self.panel_1, -1)
        self.label_7_copy_1 = wx.StaticText(self.panel_1, -1, "Port")
        self.bp_porttxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_2 = wx.StaticLine(self.panel_1, -1)
        self.label_7_copy_2 = wx.StaticText(self.panel_1, -1, "Debug                    ")
        self.bpdebug_checkbox = wx.CheckBox(self.panel_1, -1, "")
        self.static_line_1_copy_3 = wx.StaticLine(self.panel_1, -1)
        self.panel_4 = wx.Panel(self.panel_1, -1)
        self.static_line_1_copy_4 = wx.StaticLine(self.panel_1, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.onSPO2cbox, self.bpsim_checkbox)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: BP_config_frame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((420, 520))
        self.panel_3.SetMinSize((420, 20))
        self.panel_2.SetMinSize((40, 500))
        self.static_line_1.SetMinSize((380, 2))
        self.label_7.SetMinSize((142, 25))
        self.static_line_1_copy.SetMinSize((380, 2))
        self.label_7_copy.SetMinSize((142, 25))
        self.bp_simtypecbox.SetMinSize((150, 29))
        self.bp_simtypecbox.SetSelection(1)
        self.static_line_1_copy_1.SetMinSize((380, 2))
        self.label_7_copy_1.SetMinSize((142, 25))
        self.bp_porttxt.SetMinSize((150, 27))
        self.static_line_1_copy_2.SetMinSize((380, 2))
        self.label_7_copy_2.SetMinSize((142, 25))
        self.static_line_1_copy_3.SetMinSize((380, 2))
        self.static_line_1_copy_4.SetMinSize((380, 2))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: BP_config_frame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_6_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_6.Add(self.label_7, 0, 0, 0)
        sizer_6.Add(self.bpsim_checkbox, 0, 0, 0)
        sizer_5.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1_copy, 0, wx.EXPAND, 0)
        sizer_6_copy.Add(self.label_7_copy, 0, 0, 0)
        sizer_6_copy.Add(self.bp_simtypecbox, 0, 0, 0)
        sizer_5.Add(sizer_6_copy, 0, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1_copy_1, 0, wx.EXPAND, 0)
        sizer_6_copy_1.Add(self.label_7_copy_1, 0, 0, 0)
        sizer_6_copy_1.Add(self.bp_porttxt, 0, 0, 0)
        sizer_5.Add(sizer_6_copy_1, 0, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1_copy_2, 0, wx.EXPAND, 0)
        sizer_6_copy_2.Add(self.label_7_copy_2, 0, 0, 0)
        sizer_6_copy_2.Add(self.bpdebug_checkbox, 0, 0, 0)
        sizer_5.Add(sizer_6_copy_2, 0, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1_copy_3, 0, wx.EXPAND, 0)
        sizer_5.Add(self.panel_4, 1, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1_copy_4, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_2_copy, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def onSPO2cbox(self, event): # wxGlade: BP_config_frame.<event_handler>
        print "Event handler `onSPO2cbox' not implemented!"
        event.Skip()

# end of class BP_config_frame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = BP_config_frame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()