import wx

class VideoOptionDialog(wx.Dialog):
    def __init__(self, window):
        wx.Dialog.__init__(self, window, -1, 'Video Options')
        
        self.dict = window.user_config
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        network_sizer = self.__set_NetworkInputOptions()
        reply_sizer = self.__set_ReplyButtons()
        
        main_sizer.Add(network_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(reply_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
    
    def __set_NetworkInputOptions(self):
        network_sizer = wx.FlexGridSizer(cols=2, hgap=5)
        videoipadd_sizer = wx.BoxSizer(wx.VERTICAL)
        videoipport_sizer = wx.BoxSizer(wx.VERTICAL)
        
        videoipadd_text = wx.StaticText(self, -1, 'Client IP Address')
        self.videoippath = wx.TextCtrl(self, -1, self.dict['ip_host'], size=(150,-1))
        videoipport_text = wx.StaticText(self, -1, 'Port')
        self.videoipport = wx.SpinCtrl(self, -1, self.dict['video_ip_port'], style=wx.SP_ARROW_KEYS, min=0, max=65535)
        
        videoipadd_sizer.Add(videoipadd_text, 0, wx.EXPAND | wx.ALL, 3)
        videoipadd_sizer.Add(self.videoippath, 0, wx.EXPAND | wx.ALL, 3)
        videoipport_sizer.Add(videoipport_text, 0, wx.EXPAND | wx.ALL, 3)
        videoipport_sizer.Add(self.videoipport, 0, wx.EXPAND | wx.ALL, 3)
        network_sizer.Add(videoipadd_sizer, 0, wx.EXPAND | wx.ALL, 3)
        network_sizer.Add(videoipport_sizer, 0, wx.EXPAND | wx.ALL, 3)
        return network_sizer
    
    def __set_ReplyButtons(self):
        reply_sizer = wx.StdDialogButtonSizer()
        
        okbutton = wx.Button(self, wx.ID_OK, size=(85,32))
        cancelbutton = wx.Button(self, wx.ID_CANCEL, size=(85,32))
        okbutton.SetDefault()
        
        reply_sizer.AddButton(okbutton)
        reply_sizer.AddButton(cancelbutton)
        reply_sizer.Realize()
        return reply_sizer
