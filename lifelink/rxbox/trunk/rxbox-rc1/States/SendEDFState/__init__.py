from States.SendState import *

                                  
class SendEDFState(SendState):
    def __init__(self, engine, *args, **kwds):
        SendState.__init__(self, engine, *args, **kwds)
    
    def __name__(self):
        return 'SendEDFState'
        
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
            
        self.sendEmail('EDF')
        self._engine.change_state('StandbyState')
        
    def stop(self):
        self._frame.setGui('unlock')
        self._logger.info('State Machine: %s Stop'%self.__name__())       
 
    def emailDetails(self):
        """Sends an email containing an attachment of biomedical data to a remote server or an email address"""
        self._logger.info('Sending EDF')
        try:
            dlg = wx.ProgressDialog("Sending EDF",
                           "Sending EDF... Please Wait...",
                           maximum = 5,
                           parent=self._frame,
                           style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE 
                            )
            dlg.Update(1,"Loading")
            t = Triage('rxbox.cfg')
            dlg.Update(2,"Logging In")
            t.login()
            dlg.Update(3,"Loading Data")
            headers = {'Subject': self.emailmode + ' ' + self.topic, 'X-Eccs-Priority': 'emergency',
                            'X-Eccs-Rxboxextension': '2001'}
            body = self.body
            afilename = [self._engine._myedf.edfilename]+self._panel['snapshot'].pics+[self._panel['snapshot2'].dicom_filename]
            attach = {}
            for i in afilename:
                try:
                    f = open(i, 'r')
                    attach[i] = f.read()
                    f.close()
                except:
                    continue
            dlg.Update(4,"Sending Data")
            t.request(headers, body, attach)
            dlg.Update(5,"Sent")
            self._logger.info('Send EDF Successful!!!')
        except:
            ERROR(comment='Send EDF Failed!!!',logger=self._logger,frame=self._frame)
            dlg.Destroy()
            raise
