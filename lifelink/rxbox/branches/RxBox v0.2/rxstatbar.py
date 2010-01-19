import wx

class RxStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent)

        self.SetFieldsCount(2)  
        self.SetStatusWidths([-10, -1])
        #self.SetStatusText("\t Average:",1)
        #self.SetStatusText("Connecting...",2)
        self.neticon = wx.StaticBitmap(self,-1,wx.Bitmap("Icons/unconnected_net.png",wx.BITMAP_TYPE_ANY))
        self.mailicon = wx.StaticBitmap(self,-1,wx.Bitmap("Icons/mail_web.png",wx.BITMAP_TYPE_ANY))
        #self.SetToolTipString("Network Status")
        
        #print self.GetToolTip()
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.PlaceIcon()

    def PlaceIcon(self):
        rect = self.GetFieldRect(1)
        self.neticon.SetPosition((rect.x+3,rect.y))
        self.mailicon.SetPosition((rect.x+22,rect.y))

    def OnSize(self, evet):
        self.PlaceIcon()
        
