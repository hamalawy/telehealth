"""
Project LifeLink: Main module

Main script of the RxBox software

Authors: Julius Miguel J. Broma
         Arlan Roie A. Santos
         Luis G. Sison, PhD
         ------------------------------------------------
         Instrumentation, Robotics and Control Laboratory
         University of the Philippines - Diliman
         ------------------------------------------------
         March 2009
"""

import sys
sys.path.append('../modules')

import wx
import rxpanel
import referpanel
import subprocess

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.PatientInfoHeader_Label = wx.StaticText(self, -1, "Patient Information", style=wx.ALIGN_CENTRE)
        self.PatientInfo_Label = wx.StaticText(self, -1, "No Information")

        self.static_line_6 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.frame_StatusBar = self.CreateStatusBar(1, 0)

        # create rxpanel window
        self.RxPanel = rxpanel.MyPanel(self, self, -1)
        
        self.__set_properties()
        self.__do_layout()

        # call the User Authentication Window
        self.TextEntry("Please enter username:", "username")
        
        # call the recordmyDesktop subprocess (for LINUX only)
        #self.recorder = subprocess.Popen('gtk-recordMyDesktop')
        
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("RxBox - Philippine General Hospital")
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(wx.Colour(245, 255, 207))
        self.PatientInfoHeader_Label.SetMinSize((620, 20))
        self.PatientInfoHeader_Label.SetBackgroundColour(wx.Colour(219, 219, 112))
        self.PatientInfoHeader_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Arial"))
        self.PatientInfo_Label.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.PatientInfo_Label.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, ""))
        self.frame_StatusBar.SetStatusWidths([-1])
        # statusbar fields
        frame_StatusBar_fields = ["RxBox ready..."]
        for i in range(len(frame_StatusBar_fields)):
            self.frame_StatusBar.SetStatusText(frame_StatusBar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_19 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_5.Add(self.PatientInfoHeader_Label, 1, wx.EXPAND, 0)
        sizer_5.Add(self.PatientInfo_Label, 3, wx.TOP|wx.BOTTOM|wx.EXPAND, 1)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_4, 1, wx.ALL|wx.EXPAND, 4)
        # add RxPanel
        sizer_3.Add(self.RxPanel, 5, wx.ALL|wx.EXPAND, 4)
        self.sizer_2.Add(sizer_3, 1, wx.ALL|wx.EXPAND, 4)
        self.sizer_2.Add(self.static_line_6, 0, wx.EXPAND, 0)
        sizer_1.Add(self.sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def CreateReferPanel(self): # wxGlade: MyFrame.<event_handler>
        """ creates the panel for patient-doctor interaction """
        self.ReferPanel = referpanel.MyPanel(self, -1)
        self.sizer_2.Add(self.ReferPanel, 1, wx.ALL|wx.EXPAND, 4)
        # refresh the GUI
        self.Layout()

    def DestroyReferPanel(self):
        """ destroys the panel for patient-doctor interaction.
            retain rxpanel only. """
        
        try:
            self.ReferPanel.Destroy()
            self.Layout()

        except AttributeError:
            pass

    def TextEntry(self, message, text):
        """ pops the User Authentication window """
        
        self.username = "lifelink"
        
        dlg = wx.TextEntryDialog(self, message, "RxBox - Philippine General Hospital: User Authentication", defaultValue = text)
        dlg.CenterOnScreen()

        # when OK is clicked
        if dlg.ShowModal() == wx.ID_OK:
            if dlg.GetValue() == self.username:
                print "User Authenticated"
                self.SetTitle("RxBox - Philippine General Hospital" + ' - ' + self.username)
                dlg.Destroy()

            else:
                print "Invalid"
                self.TextEntry("Invalid!\nPlease enter username:", "")
                
        # when Cancel is clicked
        else:
            print 'Main Window closed'
            dlg.Destroy()
            self.Close()

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame = MyFrame(None, -1, "")
    app.SetTopWindow(frame)
   
    frame.Show()
    frame.Maximize(True)
    app.MainLoop()
