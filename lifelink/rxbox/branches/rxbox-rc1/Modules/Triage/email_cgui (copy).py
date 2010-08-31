#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Aug 30 11:22:58 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class EMAIL_config_frame(wx.Frame):
    def __init__(self, parent,*args, **kwds):
        # begin wxGlade: EMAIL_config_frame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, parent,*args, **kwds)
        self.panel_1 = wx.Panel(parent, -1)
        self.panel_3 = wx.Panel(self.panel_1, -1)
        self.panel_2 = wx.Panel(self.panel_1, -1)
        self.static_line_1 = wx.StaticLine(self.panel_1, -1)
        self.label_1 = wx.StaticText(self.panel_1, -1, "Simulated              ")
        self.emailsim_checkbox = wx.CheckBox(self.panel_1, -1, "")
        self.static_line_1_copy = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy = wx.StaticText(self.panel_1, -1, "IMAP User             ")
        self.email_imapusertxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_1 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_2 = wx.StaticText(self.panel_1, -1, "IMAP Server        ")
        self.email_imapservertxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_2 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_1 = wx.StaticText(self.panel_1, -1, "IMAP Password      ")
        self.email_imappasswordtxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_3 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_3 = wx.StaticText(self.panel_1, -1, "SMTP User             ")
        self.email_smtpusertxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_4 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_4 = wx.StaticText(self.panel_1, -1, "SMTP Server          ")
        self.email_smtpservertxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_5 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_5 = wx.StaticText(self.panel_1, -1, "SMTP Password     ")
        self.email_smtppasswordtxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_6 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_6 = wx.StaticText(self.panel_1, -1, "Mode                     ")
        self.emai_modetxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_7 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_7 = wx.StaticText(self.panel_1, -1, "Sleep                     ")
        self.emai_sleeptxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_8 = wx.StaticLine(self.panel_1, -1)
        self.label_1_copy_8 = wx.StaticText(self.panel_1, -1, "Message Handler  ")
        self.email_msghandlertxt = wx.TextCtrl(self.panel_1, -1, "")
        self.static_line_1_copy_9 = wx.StaticLine(self.panel_1, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: EMAIL_config_frame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((420, 520))
        self.panel_3.SetMinSize((420, 20))
        self.panel_2.SetMinSize((40, 500))
        self.static_line_1.SetMinSize((380, 2))
        self.label_1.SetMinSize((122, 25))
        self.static_line_1_copy.SetMinSize((380, 2))
        self.label_1_copy.SetMinSize((122, 25))
        self.email_imapusertxt.SetMinSize((150, 27))
        self.static_line_1_copy_1.SetMinSize((380, 2))
        self.label_1_copy_2.SetMinSize((122, 25))
        self.email_imapservertxt.SetMinSize((150, 27))
        self.static_line_1_copy_2.SetMinSize((380, 2))
        self.label_1_copy_1.SetMinSize((122, 25))
        self.email_imappasswordtxt.SetMinSize((150, 27))
        self.static_line_1_copy_3.SetMinSize((380, 2))
        self.label_1_copy_3.SetMinSize((122, 25))
        self.email_smtpusertxt.SetMinSize((150, 27))
        self.static_line_1_copy_4.SetMinSize((380, 2))
        self.label_1_copy_4.SetMinSize((122, 25))
        self.email_smtpservertxt.SetMinSize((150, 27))
        self.static_line_1_copy_5.SetMinSize((380, 2))
        self.label_1_copy_5.SetMinSize((122, 25))
        self.email_smtppasswordtxt.SetMinSize((150, 27))
        self.static_line_1_copy_6.SetMinSize((380, 2))
        self.label_1_copy_6.SetMinSize((122, 25))
        self.emai_modetxt.SetMinSize((150, 27))
        self.static_line_1_copy_7.SetMinSize((380, 2))
        self.label_1_copy_7.SetMinSize((122, 25))
        self.emai_sleeptxt.SetMinSize((150, 27))
        self.static_line_1_copy_8.SetMinSize((380, 2))
        self.label_1_copy_8.SetMinSize((122, 25))
        self.email_msghandlertxt.SetMinSize((150, 27))
        self.static_line_1_copy_9.SetMinSize((380, 2))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: EMAIL_config_frame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_5.Add(self.label_1, 0, 0, 0)
        sizer_5.Add(self.emailsim_checkbox, 0, 0, 0)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy, 0, wx.EXPAND, 0)
        sizer_5_copy.Add(self.label_1_copy, 0, 0, 0)
        sizer_5_copy.Add(self.email_imapusertxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_1, 0, wx.EXPAND, 0)
        sizer_5_copy_2.Add(self.label_1_copy_2, 0, 0, 0)
        sizer_5_copy_2.Add(self.email_imapservertxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_2, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_2, 0, wx.EXPAND, 0)
        sizer_5_copy_1.Add(self.label_1_copy_1, 0, 0, 0)
        sizer_5_copy_1.Add(self.email_imappasswordtxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_1, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_3, 0, wx.EXPAND, 0)
        sizer_5_copy_3.Add(self.label_1_copy_3, 0, 0, 0)
        sizer_5_copy_3.Add(self.email_smtpusertxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_3, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_4, 0, wx.EXPAND, 0)
        sizer_5_copy_4.Add(self.label_1_copy_4, 0, 0, 0)
        sizer_5_copy_4.Add(self.email_smtpservertxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_4, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_5, 0, wx.EXPAND, 0)
        sizer_5_copy_5.Add(self.label_1_copy_5, 0, 0, 0)
        sizer_5_copy_5.Add(self.email_smtppasswordtxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_5, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_6, 0, wx.EXPAND, 0)
        sizer_5_copy_6.Add(self.label_1_copy_6, 0, 0, 0)
        sizer_5_copy_6.Add(self.emai_modetxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_6, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_7, 0, wx.EXPAND, 0)
        sizer_5_copy_7.Add(self.label_1_copy_7, 0, 0, 0)
        sizer_5_copy_7.Add(self.emai_sleeptxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_7, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_8, 0, wx.EXPAND, 0)
        sizer_5_copy_8.Add(self.label_1_copy_8, 0, 0, 0)
        sizer_5_copy_8.Add(self.email_msghandlertxt, 0, 0, 0)
        sizer_4.Add(sizer_5_copy_8, 0, wx.EXPAND, 0)
        sizer_4.Add(self.static_line_1_copy_9, 0, wx.EXPAND, 0)
        sizer_2_copy.Add(sizer_4, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_2_copy, 0, wx.EXPAND, 0)
        self.panel_1.SetSizer(sizer_2)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class EMAIL_config_frame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = EMAIL_config_frame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()