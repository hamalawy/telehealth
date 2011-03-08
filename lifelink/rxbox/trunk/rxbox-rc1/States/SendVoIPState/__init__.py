from States.SendState import *

                                  
class SendVoIPState(SendState):
    def __init__(self, engine, *args, **kwds):
        SendState.__init__(self, engine, *args, **kwds)
    
    def __name__(self):
        return 'SendVoIPState'
        
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        self._frame.setGui('lock')
        self._logger.info('Create Record Mode')
        self.panelmode = 'createrecord'
        self._panel['createrecord'] = CreateRecordPanel2(self._frame, -1)
        self._frame._mgr.AddPane(self._panel['createrecord'], wx.aui.AuiPaneInfo().
                      Caption("Create Patient Record").Dockable(False).Name('createrecord').
                      Float().FloatingPosition(wx.Point(25, 25)).DestroyOnClose(True).
                      FloatingSize(wx.Size(460, 628)).CloseButton(True).MaximizeButton(True))
        self._frame._mgr.Update()
            
    def after(self):    
        pane = self._frame._mgr.GetPane(self.panelmode)
        self._frame._mgr.ClosePane(pane)
        self._frame._mgr.Update()
            
        self.sendEmail('VoIP Ticket')
        self._engine.change_state('ReferState')
        
    def stop(self):
        self._frame.setGui('unlock')
        self._logger.info('State Machine: %s Stop'%self.__name__())       
 
    def emailDetails(self):
        """Sends an email containing an attachment of biomedical data to a remote server or an email address"""
        self._logger.info('Sending VoIP Ticket')
        try:
            dlg = wx.ProgressDialog("Sending VoIP Request",
                           "Sending VoIP Ticket... Please Wait...",
                           maximum = 5,
                           parent=self._frame,
                           style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE 
                            )
            dlg.Update(1,"Loading")
            t = Triage('rxbox.cfg')
            dlg.Update(2,"Logging In")
            t.login()
            dlg.Update(3,"Loading Data")
            headers = {'Subject': self.emailmode + ' ' + self.topic, 'X-Eccs-Voip': self._config.get('voip', 'id'),
                            'X-Eccs-Rxboxextension': '2001'}
            body = self.body
            dlg.Update(4,"Sending Ticket")
            t.request(headers, body, {})
            dlg.Update(5,"Sent")
            self._logger.info('Send VoIP Ticket Successful!!!')
        except:
            ERROR(comment='Sending VoIP Ticket Failed!!!',logger=self._logger,frame=self._frame)
            dlg.Destroy()
            raise
