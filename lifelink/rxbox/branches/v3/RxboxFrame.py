import wx
import wx.aui

import ConfigParser

import uuid
import datetime

from Modules import *

ID_TransparentHint = wx.NewId()
ID_VenetianBlindsHint = wx.NewId()
ID_RectangleHint = wx.NewId()
ID_NoHint = wx.NewId()
ID_HintFade = wx.NewId()
ID_AllowFloating = wx.NewId()
ID_NoVenetianFade = wx.NewId()
ID_TransparentDrag = wx.NewId()
ID_AllowActivePane = wx.NewId()
ID_NoGradient = wx.NewId()
ID_VerticalGradient = wx.NewId()
ID_HorizontalGradient = wx.NewId()

ID_FirstPerspective = wx.NewId()

class RxboxFrame(wx.Frame):
    def __init__(self, config, *args, **kwds):
        # begin wxGlade: RxboxFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.config = config
        
        self.rxboxDB = rxboxdb.rxboxDB()
        self.rxboxDB.dbconnect()
        self.rxboxDB.dbcreatetables()

        self.dbuuid = str(uuid.uuid1())
        print "uuid = ", self.dbuuid
        self.rxboxDB.dbinsert('sessions', 'uuid', self.dbuuid)
        self.rxboxDB.dbupdate('sessions', 'starttime', str(datetime.datetime.today()), 'uuid', self.dbuuid)
        self.rxboxinitialized = True
        
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self._mgr.SetFlags(self._mgr.GetFlags() ^ ID_AllowFloating)
        self._perspectives = []

        # Menu Bar
        self.RxboxFrame_menubar = wx.MenuBar()
        
        self.file_menu = wx.Menu()
        self.file_menu.Append(wx.ID_EXIT, "Exit")
        
        self.options_menu = wx.Menu()
        self.options_menu.AppendRadioItem(ID_TransparentHint, "Transparent Hint")
        self.options_menu.AppendRadioItem(ID_VenetianBlindsHint, "Venetian Blinds Hint")
        self.options_menu.AppendRadioItem(ID_RectangleHint, "Rectangle Hint")
        self.options_menu.AppendRadioItem(ID_NoHint, "No Hint")
        self.options_menu.AppendSeparator();
        self.options_menu.AppendCheckItem(ID_HintFade, "Hint Fade-in")
        self.options_menu.AppendCheckItem(ID_AllowFloating, "Allow Floating")
        self.options_menu.AppendCheckItem(ID_NoVenetianFade, "Disable Venetian Blinds Hint Fade-in")
        self.options_menu.AppendCheckItem(ID_TransparentDrag, "Transparent Drag")
        self.options_menu.AppendCheckItem(ID_AllowActivePane, "Allow Active Pane")
        self.options_menu.AppendSeparator();
        self.options_menu.AppendRadioItem(ID_NoGradient, "No Caption Gradient")
        self.options_menu.AppendRadioItem(ID_VerticalGradient, "Vertical Caption Gradient")
        self.options_menu.AppendRadioItem(ID_HorizontalGradient, "Horizontal Caption Gradient")
        self.options_menu.AppendSeparator();
        self.options_menu.Append(ID_FirstPerspective+0, "Default Startup")

        self.RxboxFrame_menubar.Append(self.file_menu, "File")        
        self.RxboxFrame_menubar.Append(self.options_menu, "Option")
        self.SetMenuBar(self.RxboxFrame_menubar)
        # Menu Bar end
        
        self.RxboxFrame_statusbar = self.CreateStatusBar(1, 0)

        self._panel = {}
        self._panel['patientinfo'] = PatientInfoPanel2(self, -1)
        self._panel['comm'] = CommPanel2(self, -1)
        self._panel['video'] = wx.Panel(self, -1)
        self._panel['snapshot'] = SnapshotPanel2(self, -1)
        self._panel['steth'] = StethPanel2(self, -1)
        self._panel['bp'] = BPPanel2(self, -1)
        self._panel['spo2'] = SPO2Panel2(self, -1)
        self._panel['ecg'] = ECGPanel2(self, -1)
        
        self._mgr.AddPane(self._panel['patientinfo'], wx.aui.AuiPaneInfo().
                          Name("patientinfopanel").Caption("Patient Info").MinSize(wx.Size(50,50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['comm'], wx.aui.AuiPaneInfo().
                          Name("commpanel").Caption("").CaptionVisible(False).MinSize(wx.Size(50,50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['video'], wx.aui.AuiPaneInfo().MinSize(wx.Size(50,50)).
                          Name("videopanel").Caption("Video").
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['snapshot'], wx.aui.AuiPaneInfo().
                          Name("snapshotpanel").Caption("Snapshot").MinSize(wx.Size(50,50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['steth'], wx.aui.AuiPaneInfo().
                          Name("stethpanel").Caption("Stethoscope").MinSize(wx.Size(50,50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['bp'], wx.aui.AuiPaneInfo().
                          Name("bppanel").Caption("BP").MinSize(wx.Size(50,50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['spo2'], wx.aui.AuiPaneInfo().
                          Name("spo2panel").Caption("SPO2").MinSize(wx.Size(50,50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
        self._mgr.AddPane(self._panel['ecg'], wx.aui.AuiPaneInfo().
                          Name("ecgpanel").Caption("ECG").MinSize(wx.Size(50,50)).
                          Bottom().Layer(1).Position(0).CloseButton(False).MaximizeButton(False))
                          
        self._mgr.GetPane("patientinfopanel").Show().Left().Layer(1).Row(1).Position(0)
        self._mgr.GetPane("commpanel").Show().Left().Layer(2).Row(1).Position(4)
        self._mgr.GetPane("videopanel").Show().Left().Layer(1).Row(2).Position(0)
        self._mgr.GetPane("snapshotpanel").Show().Left().Layer(1).Row(3).Position(0)
        self._mgr.GetPane("stethpanel").Show().Left().Layer(1).Row(4).Position(0)
        self._mgr.GetPane("bppanel").Show().Left().Layer(1).Row(1).Position(3)
        self._mgr.GetPane("spo2panel").Show().Left().Layer(1).Row(4).Position(3)
        self._mgr.GetPane("ecgpanel").Show().Left().Layer(1).Row(1).Position(2)
        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_PANE_BORDER_SIZE,1)
        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE,2)
        self._mgr.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_CAPTION_SIZE,12)
#        self._mgr.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,'green')
#        self._mgr.GetArtProvider().SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR,'green')
        self._mgr.Update()

        #Event Handlers
        
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowFloating)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_RectangleHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoHint)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_HintFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_TransparentDrag)
        self.Bind(wx.EVT_MENU, self.OnManagerFlag, id=ID_AllowActivePane)

        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VenetianBlindsHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_RectangleHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoHint)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HintFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowFloating)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoVenetianFade)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_TransparentDrag)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_AllowActivePane)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_NoGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_VerticalGradient)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI, id=ID_HorizontalGradient)

        self.Bind(wx.EVT_MENU_RANGE, self.OnRestorePerspective, id=ID_FirstPerspective)
        
        self.SetTitle("Rxbox Frame")
        self.SetMinSize((1200, 700))
        self.RxboxFrame_statusbar.SetStatusWidths([-1])
        self.RxboxFrame_statusbar.SetStatusText('Hello')

        self._perspectives.append(self.config.get('Perspective','default'))
        self._perspectives.append(self.config.get('Perspective','onoff'))
        try:
            self._mgr.LoadPerspective(self._perspectives[1])
        except:
            print 'No Default SetUp'
        
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
        self._mgr.LoadPerspective(self._perspectives[event.GetId() - ID_FirstPerspective])
        
    def OnExit(self, event):
        dlg = wx.MessageDialog(self, 'Do you want to save data?', 'Exit', \
                                wx.YES_NO | wx.ICON_QUESTION | wx.CANCEL)
        response = dlg.ShowModal()
        if response == wx.ID_CANCEL:
            dlg.Destroy()
        elif response == wx.ID_YES:
            current_perspective = self._mgr.SavePerspective()
            self.config.set('Perspective','onoff',current_perspective)
            self.config.write(open('rxbox.cfg', 'w'))
            dlg.Destroy()
            self.Destroy()   