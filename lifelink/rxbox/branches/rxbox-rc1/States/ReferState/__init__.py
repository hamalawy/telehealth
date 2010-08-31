from Modules.VoIP import *
from Modules.IM import *
import wx

class ReferState:
    def __init__(self, engine, *args, **kwds):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        
        self._frame = self._engine._frame
        self._mgr = self._frame._mgr
        self._panel = self._frame._panel
    
    def __name__(self):
        return 'ReferState'
    
    def start(self):
        print 'State Machine: ReferState Start'
        #load refer perspective
        self._mgr.LoadPerspective(self._config.get('Perspective', 'refer'))
        self._mgr.Update()
        self._panel['comm'].Call_Label.SetLabel('Wait')
        wx.Yield()
        
        #initialize voip and im
        self._panel['voip'].Start()
        self._panel['im'].Start()
        self._panel['comm'].Call_Label.SetLabel('Drop')
        
    def stop(self):
        print 'State Machine: ReferState Stop'
        try:
            dlg = wx.ProgressDialog("Stopping Refer Session",
                           "Stopping Refer Session... Please Wait...",
                           maximum = 6,
                           parent=self._frame,
                           style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
                            )
            dlg.Update(1,"Fixing Panels")
            #save current perspective
            current_perspective = self._frame._mgr.SavePerspective()
            self._config.set('Perspective', 'refer', current_perspective)
            #return perspective
            self._mgr.LoadPerspective(self._config.get('Perspective', 'onoff'))
            self._mgr.Update()
            self._panel['comm'].Call_Label.SetLabel('Call')
            wx.Yield()
            #stop voip and im
            dlg.Update(2,"Stopping VoIP")
            self._panel['voip'].Stop()
            dlg.Update(4,"Stopping IM")
            self._panel['im'].Stop()
            dlg.Update(6,"Stopping IM")
        except:
            dlg.Destroy()
