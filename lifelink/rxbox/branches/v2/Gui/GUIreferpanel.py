#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Thu Nov 26 12:35:37 2009

import wx

# begin wxGlade: extracode
# end wxGlade



class ReferPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ReferPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.upperpanel = wx.Panel(self, -1)
        self.Videoconf_Label = wx.StaticText(self, -1, "Video", style=wx.ALIGN_CENTRE)
        self.video_panel = wx.Panel(self, -1)
        self.IM_Label = wx.StaticText(self, -1, "Instant Messaging", style=wx.ALIGN_CENTRE)
        self.IMtexts_Text = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_READONLY)
        self.IMreply_Text = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        self.lowerpanel = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ReferPanel.__set_properties
        self.upperpanel.SetMinSize((320, 160))
        self.Videoconf_Label.SetBackgroundColour(wx.Colour(251, 255, 100))
        self.Videoconf_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.video_panel.SetMinSize((320,240))
        self.IM_Label.SetMinSize((620, 20))
        self.IM_Label.SetBackgroundColour(wx.Colour(253, 255, 191))
        self.IM_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.IMtexts_Text.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.IMreply_Text.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.lowerpanel.SetMinSize((320, 160))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ReferPanel.__do_layout
        refer_panel_sizer = wx.FlexGridSizer(3, 1, 0, 0)
        im_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        video_sizer = wx.BoxSizer(wx.VERTICAL)
        video_holder = wx.FlexGridSizer(2, 1, 0, 0)
        refer_panel_sizer.Add(self.upperpanel, 1, wx.EXPAND, 0)
        video_sizer.Add(self.Videoconf_Label, 0, wx.ALL|wx.EXPAND, 0)
        video_holder.Add(self.video_panel, 0, wx.ALL|wx.EXPAND, 0)
        video_sizer.Add(video_holder, 1, wx.EXPAND, 0)
        refer_panel_sizer.Add(video_sizer, 1, wx.ALL|wx.EXPAND, 0)
        im_sizer.Add(self.IM_Label, 1, wx.RIGHT|wx.EXPAND, 1)
        sizer_18.Add(self.IMtexts_Text, 3, wx.TOP|wx.EXPAND, 1)
        sizer_18.Add(self.IMreply_Text, 0, wx.TOP|wx.EXPAND, 4)
        im_sizer.Add(sizer_18, 8, wx.EXPAND, 0)
        refer_panel_sizer.Add(im_sizer, 1, wx.EXPAND, 0)
        refer_panel_sizer.Add(self.lowerpanel, 1, wx.EXPAND, 0)
        self.SetSizer(refer_panel_sizer)
        refer_panel_sizer.Fit(self)
        # end wxGlade

# end of class ReferPanel


class refer_panel_new(wx.Panel):
    def __init__(self, *args, **kwds):
        # content of this block not found: did you rename this class?
        pass

    def __set_properties(self):
        # content of this block not found: did you rename this class?
        pass

    def __do_layout(self):
        # content of this block not found: did you rename this class?
        pass

# end of class refer_panel_new


