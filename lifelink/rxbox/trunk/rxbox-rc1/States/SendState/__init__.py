from SendPanels import *
from Modules.Triage import *

import subprocess
import wx
                                  
class SendState:
    def __init__(self, engine, *args):
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        
        self._frame = self._engine._frame
        self._panel = self._frame._panel
        self.dbuuid = self._engine.dbuuid
        self.rxboxDB = self._engine.rxboxDB
        
        self.emailmode = self._config.get('email', 'mode')
        
        self.topic = ''
        self.body = ''
        self.reason = ''
        self.haspatientinfo = False
        
        if(len(args) == 0): self.args = ''
        else: self.args = args[0]
    
    def __name__(self):
        return 'SendState'
        
    def start(self):
        print 'State Machine: SendState Start'
        self._frame.setGui('lock')
        if (self.args == 'LogFileSend'):
            self.panelmode = 'logfile'
            self._panel['logfile'] = LogFilePanel2(self._frame, -1)
            self._frame._mgr.AddPane(self._panel['logfile'], wx.aui.AuiPaneInfo().
                          Caption("Support").Dockable(False).Name('logfile').
                          Float().FloatingPosition(wx.Point(25, 25)).DestroyOnClose(True).
                          FloatingSize(wx.Size(300, 400)).CloseButton(True).MaximizeButton(True))
        else:
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
            
        if(self.args == 'ReferState'):
            self.sendEmail('requestVoip','VoIP Ticket')
            self._engine.change_state('ReferState')
        elif (self.args == 'LogFileSend'):
            self.sendEmail('sendLog','Log Files')
            self._engine.change_state('StandbyState')            
        else:
            self.sendEmail('sendEDF','EDF')
            self._engine.change_state('StandbyState')
        
    def stop(self):
        print 'State Machine: SendState Stop'
        self._frame.setGui('unlock')
        
    def sendEmail(self,mode='sendEDF',msg='EDF'):
        self._frame.RxFrame_StatusBar.SetStatusText("Sending %s to Server..."%msg)
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Sending %s to Server...'%msg)
        tries = 0
        while tries < 2:
            try:
                getattr(self, mode)()
                dlg = wx.MessageDialog(self._frame, "Send %s Successful"%msg, "Send %s Successful"%msg, wx.OK | wx.ICON_QUESTION)
                dlg.ShowModal()
                self._frame.RxFrame_StatusBar.SetStatusText("%s Sent..."%msg)
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', '%s Sent...'%msg)
                break
            except Exception, e:
                print 'Sending Error: ',e
                self._frame.RxFrame_StatusBar.SetStatusText("Sending %s Failed: %s"%(msg,e))
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Send %s Failed'%msg)
            dlg = wx.MessageDialog(self._frame, "Would you like to resend data?", "Send %s Failed"%msg, wx.YES_NO | wx.ICON_QUESTION)
            
            if dlg.ShowModal() == wx.ID_YES:
                self._frame.RxFrame_StatusBar.SetStatusText("Resending %s to server..."%msg)
                self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self.dbuuid, 'status message', '', 'Resending %s to server...'%msg)
            else:
                break
            tries += 1
            
            
    def requestVoip(self):
        """Sends an email containing an attachment of biomedical data to a remote server or an email address"""
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
        except:
            dlg.Destroy()
            raise

    def sendEDF(self):
        """Sends an email containing an attachment of biomedical data to a remote server or an email address"""
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
            afilename = [self._engine._myedf.edfilename]+self._panel['snapshot'].pics
            attach = {}
            for i in afilename:
                    f = open(i, 'r')
                    attach[i] = f.read()
                    f.close()
            dlg.Update(4,"Sending Data")
            t.request(headers, body, attach)
            dlg.Update(5,"Sent")
        except:
            dlg.Destroy()
            raise

    def sendLog(self):
        """Sends an email containing an attachment of biomedical data to a remote server or an email address"""
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
            headers = {'Subject': 'Support: %s'%self._config.get('info', 'id'), 'X-Eccs-Priority': 'emergency',
                            'X-Eccs-Rxboxextension': '2001'}
            body = self.body
            
            afilename = ['rxboxlog']

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
        except:
            dlg.Destroy()
            raise
