#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Jan 14 15:49:01 2010

import wx
# begin wxGlade: extracode
# end wxGlade



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.ECG_Demo_statusbar = self.CreateStatusBar(1, 0)
        self.play_button = wx.BitmapButton(self, -1, wx.Bitmap("Icons/PlayButton.png", wx.BITMAP_TYPE_ANY))
        self.R_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/R_initial.png", wx.BITMAP_TYPE_ANY))
        self.L_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/L_initial.png", wx.BITMAP_TYPE_ANY))
        self.C1_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C1_initial.png", wx.BITMAP_TYPE_ANY))
        self.C2_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C2_initial.png", wx.BITMAP_TYPE_ANY))
        self.C3_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C3_initial.png", wx.BITMAP_TYPE_ANY))
        self.C4_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C4_initial.png", wx.BITMAP_TYPE_ANY))
        self.C5_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C5_initial.png", wx.BITMAP_TYPE_ANY))
        self.C6_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/C6_initial.png", wx.BITMAP_TYPE_ANY))
        self.ECM_panel_1 = wx.Panel(self, -1)
        self.N_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/N_initial.png", wx.BITMAP_TYPE_ANY))
        self.F_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/F_initial.png", wx.BITMAP_TYPE_ANY))
        self.lead12_button = wx.Button(self, -1, "12 Lead")
        self.ECM_panel_2 = wx.Panel(self, -1)
        self.ecglabel_leftpanel = wx.Panel(self, -1)
        self.ecglabel = wx.StaticBitmap(self, -1, wx.Bitmap("Icons/ecglabel.png", wx.BITMAP_TYPE_ANY))
        self.ecglabel_rightpanel = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.play_button_clicked, self.play_button)
        self.Bind(wx.EVT_BUTTON, self.lead12_button_clicked, self.lead12_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("ECG Demo Program")
        self.ECG_Demo_statusbar.SetStatusWidths([-1])
        # statusbar fields
        ECG_Demo_statusbar_fields = ["Ready"]
        for i in range(len(ECG_Demo_statusbar_fields)):
            self.ECG_Demo_statusbar.SetStatusText(ECG_Demo_statusbar_fields[i], i)
        self.play_button.SetSize(self.play_button.GetBestSize())
        self.ECM_panel_1.SetMinSize((10, 15))
        self.lead12_button.SetMinSize((175, 50))
        self.ecglabel_leftpanel.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.ecglabel_rightpanel.SetBackgroundColour(wx.Colour(0, 0, 255))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        ECG_Demo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        plot_sizer = wx.BoxSizer(wx.VERTICAL)
        plotgraph_sizer = wx.BoxSizer(wx.HORIZONTAL)
        plotlabel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sidebar_sizer = wx.BoxSizer(wx.VERTICAL)
        ECM_sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        ECM_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        ECM_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        play_sizer = wx.BoxSizer(wx.HORIZONTAL)
        play_sizer.Add(self.play_button, 0, 0, 0)
        play_label = wx.StaticText(self, -1, "START")
        play_label.SetFont(wx.Font(17, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        play_sizer.Add(play_label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sidebar_sizer.Add(play_sizer, 0, wx.EXPAND, 0)
        ECM_sizer_1.Add(self.R_bitmap, 0, 0, 0)
        ECM_sizer_1.Add(self.L_bitmap, 0, 0, 0)
        sidebar_sizer.Add(ECM_sizer_1, 0, 0, 0)
        ECM_sizer_2.Add(self.C1_bitmap, 0, 0, 0)
        ECM_sizer_2.Add(self.C2_bitmap, 0, 0, 0)
        ECM_sizer_2.Add(self.C3_bitmap, 0, 0, 0)
        ECM_sizer_2.Add(self.C4_bitmap, 0, 0, 0)
        ECM_sizer_2.Add(self.C5_bitmap, 0, 0, 0)
        ECM_sizer_2.Add(self.C6_bitmap, 0, 0, 0)
        sidebar_sizer.Add(ECM_sizer_2, 0, wx.EXPAND, 0)
        sidebar_sizer.Add(self.ECM_panel_1, 0, 0, 0)
        ECM_sizer_3.Add(self.N_bitmap, 0, 0, 0)
        ECM_sizer_3.Add(self.F_bitmap, 0, 0, 0)
        sidebar_sizer.Add(ECM_sizer_3, 0, 0, 0)
        sidebar_sizer.Add(self.lead12_button, 0, 0, 0)
        sidebar_sizer.Add(self.ECM_panel_2, 1, wx.EXPAND, 0)
        ECG_Demo_sizer.Add(sidebar_sizer, 0, wx.EXPAND, 0)
        plotlabel_sizer.Add(self.ecglabel_leftpanel, 1, wx.EXPAND, 0)
        plotlabel_sizer.Add(self.ecglabel, 0, 0, 0)
        plotlabel_sizer.Add(self.ecglabel_rightpanel, 1, wx.EXPAND, 0)
        plot_sizer.Add(plotlabel_sizer, 0, wx.EXPAND, 0)
        plot_sizer.Add(plotgraph_sizer, 1, wx.EXPAND, 0)
        ECG_Demo_sizer.Add(plot_sizer, 1, wx.EXPAND, 0)
        self.SetSizer(ECG_Demo_sizer)
        ECG_Demo_sizer.Fit(self)
        self.plotgraph_sizer = plotgraph_sizer
        self.Layout()
        # end wxGlade

    def play_button_clicked(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `play_button_clicked' not implemented"
        event.Skip()

    def lead12_button_clicked(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `lead12_button_clicked' not implemented"
        event.Skip()

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    ECG_Demo = MyFrame(None, -1, "")
    app.SetTopWindow(ECG_Demo)
    ECG_Demo.Show()
    app.MainLoop()