#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Aug 26 20:51:54 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class VoIPPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: VoIPPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.video_panel = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: VoIPPanel.__set_properties
        self.SetBackgroundColour(wx.Colour(226, 255, 180))
        self.video_panel.SetMinSize((320,240))
        self.video_panel.SetBackgroundColour(wx.Colour(226, 255, 180))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: VoIPPanel.__do_layout
        video_sizer = wx.BoxSizer(wx.VERTICAL)
        video_holder = wx.FlexGridSizer(2, 1, 0, 0)
        video_holder.Add(self.video_panel, 0, wx.ALL|wx.EXPAND, 0)
        video_sizer.Add(video_holder, 1, wx.EXPAND, 0)
        self.SetSizer(video_sizer)
        video_sizer.Fit(self)
        # end wxGlade

# end of class VoIPPanel


