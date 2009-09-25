#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Thu Jul 16 00:47:07 2009

import wx

# begin wxGlade: extracode
# end wxGlade



class RxFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RxFrame.__init__
        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE|wx.MAXIMIZE_BOX|wx.SYSTEM_MENU|wx.RESIZE_BORDER|wx.CLIP_CHILDREN
        wx.Frame.__init__(self, *args, **kwds)
        self.RxFrame_StatusBar = self.CreateStatusBar(1, 0)
        self.PatientInfoHeader_Label = wx.StaticText(self, -1, "Patient Information", style=wx.ALIGN_CENTRE)
        self.PatientInfo_Label = wx.StaticText(self, -1, "No Information")

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
        self.PatientInfo_Label.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.PatientInfo_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RxFrame.__do_layout
        mainvertical_sizer = wx.BoxSizer(wx.VERTICAL)
        mainhorizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        info_daq_sizer = wx.BoxSizer(wx.VERTICAL)
        patient_info_tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        patient_info_sizer = wx.BoxSizer(wx.VERTICAL)
        info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        patient_info_sizer.Add(self.PatientInfoHeader_Label, 1, wx.EXPAND, 0)
        info_sizer.Add(self.PatientInfo_Label, 3, wx.TOP|wx.EXPAND, 1)
        patient_info_sizer.Add(info_sizer, 4, wx.EXPAND, 0)
        patient_info_tab_sizer.Add(patient_info_sizer, 1, wx.EXPAND, 0)
        info_daq_sizer.Add(patient_info_tab_sizer, 0, wx.ALL|wx.EXPAND, 4)
        mainhorizontal_sizer.Add(info_daq_sizer, 1, wx.EXPAND, 0)
        mainvertical_sizer.Add(mainhorizontal_sizer, 1, wx.EXPAND, 0)
        self.SetSizer(mainvertical_sizer)
        self.Layout()
        self.Centre()
        self.SetSize((1288, 778))
        # end wxGlade

# end of class RxFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = RxFrame(None, -1, "")
    app.SetTopWindow(rx_frame)
    rx_frame.Show()
    app.MainLoop()