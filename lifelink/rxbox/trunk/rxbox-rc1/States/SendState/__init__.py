import subprocess
import wx

from States.State import *
from SendPanels import *
from Modules.Triage import *

                                  
class SendState(State):
    def __init__(self, engine, *args, **kwds):
        State.__init__(self, engine, *args, **kwds)
        self.dbuuid = self._engine.dbuuid
        self.rxboxDB = self._engine.rxboxDB
        
        self.emailmode = self._config.get('email', 'mode')
        
        self.topic = ''
        self.body = ''
        self.reason = ''
        self.haspatientinfo = False
    
    def __name__(self):
        return 'SendState'
        
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        self._frame.setGui('lock')
        print self.args
            
    def after(self):    
        pane = self._frame._mgr.GetPane(self.panelmode)
        self._frame._mgr.ClosePane(pane)
        self._frame._mgr.Update()
        
        self._engine.change_state('StandbyState')
        
    def stop(self):
        self._frame.setGui('unlock')
        self._logger.info('State Machine: %s Stop'%self.__name__())       
 
    def sendEmail(self,msg='Email'):
        self._frame.RxFrame_StatusBar.SetStatusText("Sending %s to Server..."%msg)
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Sending %s to Server...'%msg)
        tries = 0
        while tries < 3:
            try:
                self.emailDetails()
                self._logger.info('Send Email Successful!!!')
                dlg = wx.MessageDialog(self._frame, "Send %s Successful"%msg, "Send %s Successful"%msg, wx.OK | wx.ICON_QUESTION)
                dlg.ShowModal()
                self._frame.RxFrame_StatusBar.SetStatusText("%s Sent..."%msg)
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', '%s Sent...'%msg)
                break
            except Exception, e:
                print ERROR()
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Send %s Failed'%msg)
            dlg = wx.MessageDialog(self._frame, "Would you like to resend data?", "Send %s Failed"%msg, wx.YES_NO | wx.ICON_QUESTION)
            
            if dlg.ShowModal() == wx.ID_YES:
                self._logger.info('Resending Email')
                self._frame.RxFrame_StatusBar.SetStatusText("Resending %s to server..."%msg)
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Resending %s to server...'%msg)
            else:
                break
            tries += 1
            
    def emailDetails(self):
        print 'SendState emailDetails'
