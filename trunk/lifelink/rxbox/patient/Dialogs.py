import wx
import serial
import os

class ConfigDialog(wx.Dialog):
    def __init__(self, window):
        wx.Dialog.__init__(self, window, -1, 'Configuration Options')
        
        self.dict = window.user_config
        self.id_dict = {1: 'Serial Port', 2: 'USB Port', 3: 'Saved File'}
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        serial_sizer = self.__set_SerialPortOptions()
        usb_sizer = self.__set_USBInputOptions()
        file_sizer = self.__set_FileInputOptions()
        reply_sizer = self.__set_ReplyButtons()
        
        self.OnRadioSelect(None)
        
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, self.serialradio)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, self.fileradio)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, self.netradio)
        self.Bind(wx.EVT_CHOICE, self.OnChoiceSelect, self.baudrate)
        self.Bind(wx.EVT_BUTTON, self.OnBrowseSelect, self.browsebutton)
        
        main_sizer.Add(serial_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(usb_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(reply_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
    
    def __set_SerialPortOptions(self):
        serial_sizer = wx.BoxSizer(wx.VERTICAL)
        column_sizer = wx.FlexGridSizer(cols=2, hgap=5)
        content_sizer = wx.FlexGridSizer(cols=2, rows=2, hgap=5, vgap=5)
        
        self.serialradio = wx.RadioButton(self, 1, 'Acquire input from Serial Port', style=wx.RB_GROUP)
        serialport_text = wx.StaticText(self, -1, 'Serial Port')
        self.serialport = wx.TextCtrl(self, -1, self.dict['serial_port'], size=(150,-1))
        baudlist = ['9600', '14400', '19200', '38400', '57600', '115200']
        baudrate_text = wx.StaticText(self, -1, 'Baud Rate')
        self.baudrate = wx.Choice(self, -1, choices=baudlist)
        baudrate_dict = {'9600':0, '14400':1, '19200':2, '38400':3, '57600':4, '115200':5}
        self.baudrate.SetSelection(baudrate_dict[self.dict['baud_rate']])
        
        content_sizer.Add(serialport_text, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        content_sizer.Add(self.serialport, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        content_sizer.Add(baudrate_text, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        content_sizer.Add(self.baudrate, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        column_sizer.Add(wx.BoxSizer(), 0, wx.EXPAND | wx.ALL, 3)
        column_sizer.Add(content_sizer, 0, wx.EXPAND | wx.ALL, 3)
        serial_sizer.Add(self.serialradio, 0, wx.EXPAND | wx.ALL, 3)
        serial_sizer.Add(column_sizer, 0, wx.EXPAND | wx.ALL, 3)
        return serial_sizer
    
    def __set_USBInputOptions(self):
        usb_sizer = wx.BoxSizer(wx.VERTICAL)
        column_sizer = wx.FlexGridSizer(cols=2, hgap=5)
        port_sizer = wx.FlexGridSizer(cols=2, hgap=5)
        
        self.netradio = wx.RadioButton(self, 2, 'Acquire input from USB Port')
        listenport_text = wx.StaticText(self, -1, 'Sampling Rate')
        self.samplerate = wx.TextCtrl(self, -1, '0.5', size=(150,-1))
        
        port_sizer.Add(listenport_text, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        port_sizer.Add(self.samplerate, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        column_sizer.Add(wx.BoxSizer(), 0, wx.EXPAND | wx.ALL, 3)
        column_sizer.Add(port_sizer, 0, wx.EXPAND | wx.ALL, 3)
        usb_sizer.Add(self.netradio, 0, wx.EXPAND | wx.ALL, 3)
        usb_sizer.Add(column_sizer, 0, wx.EXPAND | wx.ALL, 3)
        return usb_sizer
    
    def __set_FileInputOptions(self):
        file_sizer = wx.BoxSizer(wx.VERTICAL)
        column_sizer = wx.FlexGridSizer(cols=2, hgap=5)
        path_sizer = wx.FlexGridSizer(cols=2, hgap=5)
        
        self.fileradio = wx.RadioButton(self, 3, 'Acquire Input from Saved File')
        self.filepath = wx.TextCtrl(self, -1, self.dict['file_input'], size=(150,-1))
        self.browsebutton = wx.Button(self, -1, 'Browse')
        
        path_sizer.Add(self.filepath, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        path_sizer.Add(self.browsebutton, 0, wx.ALIGN_CENTER_VERTICAL, 3)
        column_sizer.Add(wx.BoxSizer(), 0, wx.EXPAND | wx.ALL, 3)
        column_sizer.Add(path_sizer, 0, wx.EXPAND | wx.ALL, 3)
        file_sizer.Add(self.fileradio, 0, wx.EXPAND | wx.ALL, 3)
        file_sizer.Add(column_sizer, 0, wx.EXPAND | wx.ALL, 3)
        return file_sizer
    
    def __set_ReplyButtons(self):
        reply_sizer = wx.StdDialogButtonSizer()
        
        okbutton = wx.Button(self, wx.ID_OK, size=(85,32))
        cancelbutton = wx.Button(self, wx.ID_CANCEL, size=(85,32))
        okbutton.SetDefault()
        
        reply_sizer.AddButton(okbutton)
        reply_sizer.AddButton(cancelbutton)
        reply_sizer.Realize()
        return reply_sizer
    
    def OnRadioSelect(self, event):
        if event is not None:
            sel_input = event.GetEventObject().GetId()
            sel_input = self.id_dict[sel_input]
            self.dict['input_method'] = sel_input
        if self.dict['input_method'] == 'Serial Port':
            self.serialradio.SetValue(True)
            self.serialport.Enable(True)
            self.baudrate.Enable(True)
            self.filepath.Enable(False)
            self.browsebutton.Enable(False)
            self.samplerate.Enable(False)
        elif self.dict['input_method'] == 'USB Port':
            self.netradio.SetValue(True)
            self.serialport.Enable(False)
            self.baudrate.Enable(False)
            self.filepath.Enable(False)
            self.browsebutton.Enable(False)
            self.samplerate.Enable(True)
        elif self.dict['input_method'] == 'Saved File':
            self.fileradio.SetValue(True)
            self.serialport.Enable(False)
            self.baudrate.Enable(False)
            self.filepath.Enable(True)
            self.browsebutton.Enable(True)
            self.samplerate.Enable(False)
        else:
            print 'input not recognized'
        
    def OnBrowseSelect(self, event):
        wildcard = "Textfile (*.txt)|*.txt"
        dialog = wx.FileDialog(self, 'Select input file', os.getcwd(), '', wildcard, wx.OPEN)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            mypath = dialog.GetPath()
        dialog.Destroy()
        
        if result == wx.ID_CANCEL:
            return
        
        self.filepath.SetValue(mypath)
        
    def OnChoiceSelect(self, event):
        sel_baudrate = self.baudrate.GetStringSelection()
        self.dict['baud_rate'] = sel_baudrate

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

class TransmitDialog(wx.Dialog):
    def __init__(self, window):
        wx.Dialog.__init__(self, window, -1, 'Connection Options')
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
        ipadd_sizer = wx.BoxSizer(wx.VERTICAL)
        ipport_sizer = wx.BoxSizer(wx.VERTICAL)
        
        ipadd_text = wx.StaticText(self, -1, 'IP Address')
        self.ippath = wx.TextCtrl(self, -1, self.dict['ip_host'], size=(150,-1))
        ipport_text = wx.StaticText(self, -1, 'Listen Port')
        self.ipport = wx.SpinCtrl(self, -1, self.dict['ip_port'], style=wx.SP_ARROW_KEYS, min=0, max=65535)
        
        ipadd_sizer.Add(ipadd_text, 0, wx.EXPAND | wx.ALL, 3)
        ipadd_sizer.Add(self.ippath, 0, wx.EXPAND | wx.ALL, 3)
        ipport_sizer.Add(ipport_text, 0, wx.EXPAND | wx.ALL, 3)
        ipport_sizer.Add(self.ipport, 0, wx.EXPAND | wx.ALL, 3)
        network_sizer.Add(ipadd_sizer, 0, wx.EXPAND | wx.ALL, 3)
        network_sizer.Add(ipport_sizer, 0, wx.EXPAND | wx.ALL, 3)
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


