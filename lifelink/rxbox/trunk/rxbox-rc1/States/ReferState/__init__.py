import wx

from States.State import *
from Modules.VoIP import *
from Modules.IM import *

class ReferState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        self._mgr = self._frame._mgr
    
    def __name__(self):
        return 'ReferState'
    
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
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
            self._logger.error(ERROR('Failed to stop refer session properly'))
        self._logger.info('State Machine: %s Stop'%self.__name__())
