#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Aug 30 10:18:04 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class IM_config_frame(wx.Frame):
    def __init__(self,parent, *args, **kwds):
        # begin wxGlade: IM_config_frame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self,parent, *args, **kwds)
        self.panel_1 = wx.Panel(parent, -1)
        self.panel_3 = wx.Panel(self.panel_1, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.static_line_2 = wx.StaticLine(self.panel_1, -1)
        self.label_8_copy_copy = wx.StaticText(self.panel_1, -1, "Simulated                   ")
        self.imsim_checkbox = wx.CheckBox(self.panel_1, -1, "")
        self.static_line_2_copy = wx.StaticLine(self.panel_1, -1)
        self.label_8_copy = wx.StaticText(self.panel_1, -1, "Domain                ")
        self.im_domaintxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_2_copy_1 = wx.StaticLine(self.panel_1, -1)
        self.label_8_copy_1 = wx.StaticText(self.panel_1, -1, "Recepient                ")
        self.im_recepienttxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_2_copy_2 = wx.StaticLine(self.panel_1, -1)
        self.label_8_copy_2 = wx.StaticText(self.panel_1, -1, "Password                 ")
        self.im_passwordtxt = wx.TextCtrl(self.panel_1, -1, "", style=wx.TE_PASSWORD)
        self.static_line_2_copy_3 = wx.StaticLine(self.panel_1, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: IM_config_frame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((420, 520))
        self.panel_3.SetMinSize((420, 20))
        self.panel_2.SetMinSize((40, 500))
        self.label_8_copy_copy.SetMinSize((142, 25))
        self.label_8_copy.SetMinSize((142, 25))
        self.im_domaintxt.SetMinSize((200, 27))
        self.label_8_copy_1.SetMinSize((142, 25))
        self.im_recepienttxt.SetMinSize((200, 27))
        self.label_8_copy_2.SetMinSize((142, 25))
        self.im_passwordtxt.SetMinSize((200, 27))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: IM_config_frame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_15_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_14.Add(self.static_line_2, 0, wx.EXPAND, 0)
        sizer_15.Add(self.label_8_copy_copy, 0, 0, 0)
        sizer_15.Add(self.imsim_checkbox, 0, 0, 0)
        sizer_14.Add(sizer_15, 0, wx.EXPAND, 0)
        sizer_14.Add(self.static_line_2_copy, 0, wx.EXPAND, 0)
        sizer_15_copy.Add(self.label_8_copy, 0, 0, 0)
        sizer_15_copy.Add(self.im_domaintxt, 0, 0, 0)
        sizer_14.Add(sizer_15_copy, 0, wx.EXPAND, 0)
        sizer_14.Add(self.static_line_2_copy_1, 0, wx.EXPAND, 0)
        sizer_15_copy_1.Add(self.label_8_copy_1, 0, 0, 0)
        sizer_15_copy_1.Add(self.im_recepienttxt, 0, 0, 0)
        sizer_14.Add(sizer_15_copy_1, 0, wx.EXPAND, 0)
        sizer_14.Add(self.static_line_2_copy_2, 0, wx.EXPAND, 0)
        sizer_15_copy_2.Add(self.label_8_copy_2, 0, 0, 0)
        sizer_15_copy_2.Add(self.im_passwordtxt, 0, 0, 0)
        sizer_14.Add(sizer_15_copy_2, 0, wx.EXPAND, 0)
        sizer_14.Add(self.static_line_2_copy_3, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_2_copy, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class IM_config_frame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = IM_config_frame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
