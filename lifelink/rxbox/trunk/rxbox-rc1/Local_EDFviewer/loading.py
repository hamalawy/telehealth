import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(300, 125))
        self.SetTitle("Processing")
        self.timer = wx.Timer(self, 1)
        self.count = 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.gauge = wx.Gauge(panel, -1, 70, size=(250, 25))
        self.text = wx.StaticText(panel, -1, 'Loading EDF.....')

        hbox1.Add(self.gauge, 1, wx.ALIGN_CENTRE)
        hbox3.Add(self.text, 1)
        vbox.Add((0, 30), 0)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 30), 0)
        vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)
        panel.SetSizer(vbox)
        self.Centre()

    def OnOk(self):
        self.timer.Start(100)

    def OnTimer(self, event):
        self.count = self.count +1
        self.gauge.SetValue(self.count)
        if self.count == 70:
            self.timer.Stop()
            self.Close()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'gauge.py')
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
