from States.SendState import *
                                  
class SendLogState(SendState):
    def __init__(self, engine, *args, **kwds):
        SendState.__init__(self, engine, *args, **kwds)
    
    def __name__(self):
        return 'SendLogState'
        
    def start(self):
        self._logger.info('State Machine: %s Start'%self.__name__())
        self._frame.setGui('lock')
        self._logger.info('LogFile Mode')
        self.panelmode = 'logfile'
        self._panel['logfile'] = LogFilePanel2(self._frame, -1)
        self._frame._mgr.AddPane(self._panel['logfile'], wx.aui.AuiPaneInfo().
                      Caption("Support").Dockable(False).Name('logfile').
                      Float().FloatingPosition(wx.Point(25, 25)).DestroyOnClose(True).
                      FloatingSize(wx.Size(300, 400)).CloseButton(True).MaximizeButton(True))
        self._frame._mgr.Update()
            
    def after(self):    
        pane = self._frame._mgr.GetPane(self.panelmode)
        self._frame._mgr.ClosePane(pane)
        self._frame._mgr.Update()
            
        self.sendEmail('Log Files')
        self._engine.change_state('StandbyState')
        
    def stop(self):
        self._frame.setGui('unlock')
        self._logger.info('State Machine: %s Stop'%self.__name__())       
 
    def emailDetails(self):
        """Sends an email containing an attachment of biomedical data to a remote server or an email address"""
        self._logger.info('Sending Log')
        try:
            dlg = wx.ProgressDialog("Sending Log Files",
                           "Sending Log Files... Please Wait...",
                           maximum = 5,
                           parent=self._frame,
                           style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE 
                            )
            dlg.Update(1,"Loading")
            t = Triage('rxbox.cfg', target='support')
            dlg.Update(2,"Logging In")
            t.login()
            dlg.Update(3,"Loading Data")
            headers = {'Subject': 'Support: (ID:%s)'%self._config.get('info', 'id'), 'X-Eccs-Priority': 'emergency',
                            'X-Eccs-Rxboxextension': '2001'}
            body = self.body
            
            afilename = ['Logs/%s'%i for i in subprocess.Popen("ls Logs",shell=True,stdout=subprocess.PIPE).stdout.read().strip().split('\n')]

            attach = {}
            for i in afilename:
                f = open(i, 'r')
                attach[i] = f.read()
                f.close()
                
            attach['dmesg'] = subprocess.Popen("dmesg",shell=True,stdout=subprocess.PIPE).stdout.read()
            attach['ifconfig'] = subprocess.Popen("ifconfig",shell=True,stdout=subprocess.PIPE).stdout.read()
            attach['psaux'] = subprocess.Popen("ps aux",shell=True,stdout=subprocess.PIPE).stdout.read()
            
            dlg.Update(4,"Sending Data")
            t.request(headers, body, attach)
            dlg.Update(5,"Sent")
            self._logger.info('Send Log Successful!!!')
        except:
            ERROR(comment='Send Log Failed!!!',logger=self._logger,frame=self._frame)
            dlg.Destroy()
            raise
