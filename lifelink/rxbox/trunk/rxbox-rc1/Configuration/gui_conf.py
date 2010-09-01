#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun Aug 29 21:40:00 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class MyFrame_conf(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame_conf.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_1 = wx.Panel(self, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.panel_10 = wx.Panel(self, -1)
        self.panel_9 = wx.Panel(self, -1)
        self.bitmap_1 = wx.StaticBitmap(self, -1, wx.Bitmap("/home/rxboxpilot04/Rxbox 1.0/Configuration/index.jpeg", wx.BITMAP_TYPE_ANY))
        self.label_1 = wx.StaticText(self.panel_10, -1, "   RxBox Configuration", style=wx.ALIGN_CENTRE)
        self.tree = wx.TreeCtrl(self.panel_1, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE|wx.DOUBLE_BORDER|wx.SUNKEN_BORDER)
        self.module = wx.Panel(self.panel_2, -1)
        self.static_line_2 = wx.StaticLine(self.panel_1, -1)
        self.panel_7 = wx.Panel(self.panel_1, -1)
        self.default_button = wx.Button(self.panel_1, -1, "Default")
        self.panel_8 = wx.Panel(self.panel_1, -1)
        self.done_button = wx.Button(self.panel_1, -1, "Save")
        self.cancel_button = wx.Button(self.panel_1, -1, "Cancel")
        self.panel_7_copy = wx.Panel(self.panel_1, -1)
        self.static_line_3 = wx.StaticLine(self.panel_1, -1)
        self.panel_3 = wx.Panel(self.panel_1, -1)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, self.tree)
        self.Bind(wx.EVT_BUTTON, self.onDefault, self.default_button)
        self.Bind(wx.EVT_BUTTON, self.onDone, self.done_button)
        self.Bind(wx.EVT_BUTTON, self.onCancel, self.cancel_button)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame_conf.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((600, 650))
        self.panel_9.SetMinSize((40, 48))
        self.panel_9.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.label_1.SetMinSize((620, 48))
        self.label_1.SetFont(wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL, 0, ""))
        self.panel_10.SetMinSize((630, 48))
        self.panel_10.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.tree.SetMinSize((180, 600))
        self.module.SetMinSize((420,520))
        self.panel_7.SetMinSize((20, 20))
        self.panel_8.SetMinSize((126, 29))
        self.panel_7_copy.SetMinSize((20, 20))
        self.panel_1.SetMinSize((600, 600))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame_conf.__do_layout
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8_copy = wx.BoxSizer(wx.HORIZONTAL)
        module_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9.Add(self.panel_9, 0, wx.EXPAND, 0)
        sizer_9.Add(self.bitmap_1, 0, 0, 0)
        sizer_10.Add(self.label_1, 0, wx.RIGHT|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        self.panel_10.SetSizer(sizer_10)
        sizer_9.Add(self.panel_10, 0, wx.EXPAND, 0)
        sizer_8.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_2.Add(self.tree, 0, wx.EXPAND, 0)
        module_sizer.Add(self.module, 0, wx.EXPAND, 0)
        self.panel_2.SetSizer(module_sizer)
        sizer_7.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_7.Add(self.static_line_2, 0, wx.EXPAND, 0)
        sizer_8_copy.Add(self.panel_7, 0, wx.EXPAND, 0)
        sizer_8_copy.Add(self.default_button, 0, 0, 0)
        sizer_8_copy.Add(self.panel_8, 0, wx.EXPAND, 0)
        sizer_8_copy.Add(self.done_button, 0, 0, 0)
        sizer_8_copy.Add(self.cancel_button, 0, 0, 0)
        sizer_8_copy.Add(self.panel_7_copy, 0, wx.EXPAND, 0)
        sizer_7.Add(sizer_8_copy, 0, wx.EXPAND, 0)
        sizer_7.Add(self.static_line_3, 0, wx.EXPAND, 0)
        sizer_6.Add(self.panel_3, 1, wx.EXPAND, 0)
        sizer_7.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_7, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        sizer_8.Add(sizer_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_8)
        self.Layout()
        # end wxGlade

    def OnSelect(self, event): # wxGlade: MyFrame_conf.<event_handler>
        print "Event handler `OnSelect' not implemented"
        event.Skip()

    def onDefault(self, event): # wxGlade: MyFrame_conf.<event_handler>
        print "Event handler `onDefault' not implemented"
        event.Skip()

    def onDone(self, event): # wxGlade: MyFrame_conf.<event_handler>
        print "Event handler `onDone' not implemented"
        event.Skip()

    def onCancel(self, event): # wxGlade: MyFrame_conf.<event_handler>
        print "Event handler `onCancel' not implemented"
        event.Skip()

# end of class MyFrame_conf


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame_conf(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
