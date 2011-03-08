import wx
import wx.aui
from wx.lib.wordwrap import wordwrap
from Panels import *

ID_TransparentHint = wx.NewId()
ID_VenetianBlindsHint = wx.NewId()
ID_RectangleHint = wx.NewId()
ID_NoHint = wx.NewId()
ID_HintFade = wx.NewId()
ID_NoVenetianFade = wx.NewId()
ID_TransparentDrag = wx.NewId()
ID_AllowActivePane = wx.NewId()
ID_NoGradient = wx.NewId()
ID_VerticalGradient = wx.NewId()
ID_HorizontalGradient = wx.NewId()

ID_AllowFloating = wx.NewId()
ID_FirstPerspective = wx.NewId()
ID_LogFileSend = wx.NewId()
ID_Update = wx.NewId()
ID_About = wx.NewId()
ID_BPcal=wx.NewId()
ID_Conf=wx.NewId()

CAPTION2NAME = {"12 Lead ECG":"lead12", "Create Patient Record":"createrecord","Support":"logfile","Snapshot":"snapshot2"}

class RxboxFrame(wx.Frame):
    def __init__(self, engine, *args, **kwds):
        # begin wxGlade: RxboxFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self._engine = engine
        self._config = self._engine._config
        
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        flags = wx.aui.AUI_MGR_TRANSPARENT_DRAG
        flags &= ~wx.aui.AUI_MGR_TRANSPARENT_HINT
        flags &= ~wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
        flags &= ~wx.aui.AUI_MGR_RECTANGLE_HINT
        self._mgr.SetFlags(flags^wx.aui.AUI_MGR_TRANSPARENT_HINT)
        self._perspectives = []

        # Menu Bar
        self.RxboxFrame_menubar = wx.MenuBar()
        
        self.file_menu = wx.Menu()
        self.file_menu.Append(wx.ID_EXIT, "Exit")
        
        self.options_menu = wx.Menu()
#        self.options_menu.AppendRadioItem(ID_TransparentHint, "Transparent Hint")
#        self.options_menu.AppendRadioItem(ID_VenetianBlindsHint, "Venetian Blinds Hint")
#        self.options_menu.AppendRadioItem(ID_RectangleHint, "Rectangle Hint")
#        self.options_menu.AppendRadioItem(ID_NoHint, "No Hint")
#        self.options_menu.AppendSeparator();
#        self.options_menu.AppendCheckItem(ID_HintFade, "Hint Fade-in")
        self.options_menu.AppendCheckItem(ID_AllowFloating, "Allow Floating")
#        self.options_menu.AppendCheckItem(ID_NoVenetianFade, "Disable Venetian Blinds Hint Fade-in")
#        self.options_menu.AppendCheckItem(ID_TransparentDrag, "Transparent Drag")
#        self.options_menu.AppendCheckItem(ID_AllowActivePane, "Allow Active Pane")
#        self.options_menu.AppendSeparator();
#        self.options_menu.AppendRadioItem(ID_NoGradient, "No Caption Gradient")
#        self.options_menu.AppendRadioItem(ID_VerticalGradient, "Vertical Caption Gradient")
#        self.options_menu.AppendRadioItem(ID_HorizontalGradient, "Horizontal Caption Gradient")
        self.options_menu.AppendSeparator();
        self.options_menu.Append(ID_FirstPerspective + 0, "Default Startup")

        self.tools_menu = wx.Menu()
        self.tools_menu.Append(ID_BPcal, "BP Calibrate")
        self.tools_menu.Append(ID_Conf, "Configuration")


        self.help_menu = wx.Menu()
        self.help_menu.Append(ID_LogFileSend, "Support")
        self.help_menu.Append(ID_Update, "Update")
        self.help_menu.Append(ID_About, "About")

        self.RxboxFrame_menubar.Append(self.file_menu, "File")        
        self.RxboxFrame_menubar.Append(self.options_menu, "Option")
        self.RxboxFrame_menubar.Append(self.tools_menu, "Tools")        
        self.RxboxFrame_menubar.Append(self.help_menu, "Help")
        
        self.SetMenuBar(self.RxboxFrame_menubar)
        # Menu Bar end
        
        self.RxFrame_StatusBar = self.CreateStatusBar(1, 0)

        self._panel = {}
        self._panel['patientinfo'] = PatientInfoPanel2(self, -1)
        self._panel['comm'] = CommPanel2(self, -1)
        self._panel['snapshot'] = Snapshot(self, -1)
        self._panel['steth'] = StethPanel2(self, -1)
        self._panel['bp'] = BP(self, -1)
        self._panel['spo2'] = SPO2(self, -1)
        self._panel['ecg'] = ECG(self, -1)
        self._panel['voip'] = VoIP(self, -1)
        self._panel['im'] = IM(self, -1)
        self._panel['snapshot2'] = SnapshotWindow(self, -1)
        
        self._mgr.AddPane(self._panel['patientinfo'], wx.aui.AuiPaneInfo().
                          Name("patientinfo").Caption("Patient Info").MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['comm'], wx.aui.AuiPaneInfo().
                          Name("comm").Caption("").CaptionVisible(False).MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['snapshot'], wx.aui.AuiPaneInfo().
                          Name("snapshot").Caption("Snapshot").MinSize(wx.Size(25, 25)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['steth'], wx.aui.AuiPaneInfo().
                          Name("steth").Caption("Stethoscope").MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['bp'], wx.aui.AuiPaneInfo().
                          Name("bp").Caption("BP").MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['spo2'], wx.aui.AuiPaneInfo().
                          Name("spo2").Caption("SPO2").MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['ecg'], wx.aui.AuiPaneInfo().
                          Name("ecg").Caption("ECG").MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['voip'], wx.aui.AuiPaneInfo().
                          Name("voip").Caption("VoIP").MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['im'], wx.aui.AuiPaneInfo().
                          Name("im").Caption("Instant Messenger").MinSize(wx.Size(50, 50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['snapshot2'], wx.aui.AuiPaneInfo().
                          Caption("Snapshot").Dockable(False).Name("snapshot2").
                          Float().FloatingPosition(wx.Point(25, 25)).DestroyOnClose(False).
                          FloatingSize(wx.Size(370, 440)).CloseButton(True).MaximizeButton(True))

        self._mgr.GetPane("patientinfo").Show().Left().Layer(1).Row(1).Position(0)
        self._mgr.GetPane("comm").Show().Left().Layer(2).Row(1).Position(4)
        self._mgr.GetPane("snapshot").Show().Left().Layer(1).Row(3).Position(0)
        self._mgr.GetPane("steth").Show().Left().Layer(1).Row(4).Position(0)
        self._mgr.GetPane("bp").Show().Left().Layer(1).Row(1).Position(3)
        self._mgr.GetPane("spo2").Show().Left().Layer(1).Row(4).Position(3)
        self._mgr.GetPane("ecg").Show().Left().Layer(1).Row(1).Position(2)
        self._mgr.GetPane("voip").Show().Left().Layer(1).Row(1).Position(3)
        self._mgr.GetPane("im").Show().Left().Layer(1).Row(1).Position(4)
        self._mgr.GetPane("snapshot2").Hide()
        
        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE, 1)
        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 2)
        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_CAPTION_SIZE, 12)
        self._mgr.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,'blue')
        self._mgr.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR,'#9A9BF8')
        self._mgr.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR,'white')

        self._mgr.Update()

        #Event Handlers
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowFloating)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentHint)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_VenetianBlindsHint)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_RectangleHint)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoHint)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_HintFade)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoVenetianFade)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentDrag)
#        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowActivePane)
#
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentHint)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VenetianBlindsHint)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_RectangleHint)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoHint)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowFloating)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoVenetianFade)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentDrag)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowActivePane)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoGradient)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VerticalGradient)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HorizontalGradient)

        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective)
        self.Bind(wx.EVT_MENU_RANGE, self.OnLogFileSend, id=ID_LogFileSend)
        self.Bind(wx.EVT_MENU_RANGE, self.OnUpdate, id=ID_Update)
        self.Bind(wx.EVT_MENU_RANGE, self.OnAbout, id=ID_About)
        self.Bind(wx.EVT_MENU_RANGE, self.OnBPcal, id=ID_BPcal)
        self.Bind(wx.EVT_MENU_RANGE, self.OnConfig, id=ID_Conf)
        self.SetTitle("Rxbox Frame")
        self.SetMinSize((1200, 700))
        self.RxFrame_StatusBar.SetStatusWidths([-1])
        self.RxFrame_StatusBar.SetStatusText('Rxbox Started')
   
        self.SetIcon(wx.Icon("Icons/RxBox.ico", wx.BITMAP_TYPE_ICO))

    def OnPaneClose(self, event):
        name = CAPTION2NAME[event.GetPane().caption]
        self._panel[name].OnPaneClose()
        
    def OnUpdateUI(self, event):

        flags = self._mgr.GetFlags()
        eid = event.GetId()
        
        if eid == ID_NoGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_NONE)

        elif eid == ID_VerticalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_VERTICAL)

        elif eid == ID_HorizontalGradient:
            event.Check(self._mgr.GetArtProvider().GetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE) == wx.aui.AUI_GRADIENT_HORIZONTAL)

        elif eid == ID_AllowFloating:
            event.Check((flags & wx.aui.AUI_MGR_ALLOW_FLOATING) != 0)

        elif eid == ID_TransparentDrag:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_DRAG) != 0)

        elif eid == ID_TransparentHint:
            event.Check((flags & wx.aui.AUI_MGR_TRANSPARENT_HINT) != 0)

        elif eid == ID_VenetianBlindsHint:
            event.Check((flags & wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT) != 0)

        elif eid == ID_RectangleHint:
            event.Check((flags & wx.aui.AUI_MGR_RECTANGLE_HINT) != 0)

        elif eid == ID_NoHint:
            event.Check(((wx.aui.AUI_MGR_TRANSPARENT_HINT | 
                          wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT | 
                          wx.aui.AUI_MGR_RECTANGLE_HINT) & flags) == 0)

        elif eid == ID_HintFade:
            event.Check((flags & wx.aui.AUI_MGR_HINT_FADE) != 0);

        elif eid == ID_NoVenetianFade:
            event.Check((flags & wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE) != 0);
            
    def OnManagerFlag(self, event):

        flag = 0
        eid = event.GetId()

        if eid in [ ID_TransparentHint, ID_VenetianBlindsHint, ID_RectangleHint, ID_NoHint ]:
            flags = self._mgr.GetFlags()
            flags &= ~wx.aui.AUI_MGR_TRANSPARENT_HINT
            flags &= ~wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
            flags &= ~wx.aui.AUI_MGR_RECTANGLE_HINT
            self._mgr.SetFlags(flags)

        if eid == ID_AllowFloating:
            flag = wx.aui.AUI_MGR_ALLOW_FLOATING
        elif eid == ID_TransparentDrag:
            flag = wx.aui.AUI_MGR_TRANSPARENT_DRAG
        elif eid == ID_HintFade:
            flag = wx.aui.AUI_MGR_HINT_FADE
        elif eid == ID_NoVenetianFade:
            flag = wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        elif eid == ID_AllowActivePane:
            flag = wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE
        elif eid == ID_TransparentHint:
            flag = wx.aui.AUI_MGR_TRANSPARENT_HINT
        elif eid == ID_VenetianBlindsHint:
            flag = wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
        elif eid == ID_RectangleHint:
            flag = wx.aui.AUI_MGR_RECTANGLE_HINT
        
        self._mgr.SetFlags(self._mgr.GetFlags() ^ flag)

    def OnRestorePerspective(self, event):
        if self._engine.state.__name__() == 'ReferState':
            self._mgr.LoadPerspective(self._perspectives[1])
        else:
            self._mgr.LoadPerspective(self._perspectives[0])
      
    def OnLogFileSend(self, event):
        self._engine.change_state('SendLogState')

    def OnUpdate(self, event):
        self._engine.change_state('UpdateState')

    def OnBPcal(self,evt):
        print "BP Calibrations started"
        self._engine.change_state('BPCALState')

    def OnConfig(self,evt):
        print "Configuration started"
        self._engine.change_state('CONFIGState')

    def OnAbout(self, evt):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "Rxbox"
        info.Version = "1.0 Beta"
        info.Copyright = "(C) 2010 National Telehealth Service Program"
        info.Description = wordwrap(
            "A Telemedicine Program.",
            350, wx.ClientDC(self))
        info.WebSite = ("http://www.google.com", "Google")
        info.Developers = [ "Luke Wicent Sy",
                            "Mark Jan Bangoy",
                            "Luther Carangian",
                            "Timothy Ebido" ]

        info.License = wordwrap("Rxbox 1.0 Telemedicine Appliance\nUP Intrumentation, Robotics, and Control Laboratory\nUP Philippine General Hospital\nNational Telehealth Center\nUP Manila\nUP Diliman\n", 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
        
    def setGui(self, mode='unlock'):
        """mode expects lock, unlock"""
        if mode not in ['unlock', 'lock']:
            print 'mode unsupported'
            return
        
        [self._panel[i].setGui(mode) for i in ['ecg','bp','spo2','comm']]
        
    def OnExit(self, event):
        dlg = wx.MessageDialog(self, 'Are you sure you want to Exit?', 'Exit', \
                                wx.YES_NO)
        responce = dlg.ShowModal()
        if responce == wx.ID_YES:
            self._engine.change_state('ExitState')
            dlg.Destroy()
