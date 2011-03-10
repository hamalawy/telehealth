import wx
from email_cgui import EMAIL_config_frame
import ConfigParser
import os
path=os.getcwd()
if path[len(path)-13:]=='Configuration':
    path='../'
else:
    path=os.getcwd()+'/'

class EMAIL_Configurationmain(EMAIL_config_frame):
    def __init__(self, parent,*args, **kwds):
        EMAIL_config_frame.__init__(self, parent,*args, **kwds)
        #self.path=path+'/Triage/'
        self.config=ConfigParser.ConfigParser()
        self.config.read(path+'rxbox.cfg')
        self.get_data()

    def get_data(self):
        if self.config.get('email','simulated') == 'false':
            self.emailsim_checkbox.SetValue(False)
        else:
            self.emailsim_checkbox.SetValue(True)

        self.email_imapusertxt.SetValue(self.config.get('email','imapuser'))
        self.email_imapservertxt.SetValue(self.config.get('email','imapserver'))
        self.email_imappasswordtxt.SetValue(self.config.get('email','imappasswd'))
        self.email_smtpusertxt.SetValue(self.config.get('email','smtpuser'))
        self.email_smtpservertxt.SetValue(self.config.get('email','smtpserver'))
        self.email_smtppasswordtxt.SetValue(self.config.get('email','smtppasswd'))
        self.email_modetxt.SetValue(self.config.get('email','mode'))
        self.email_sleeptxt.SetValue(self.config.get('email','sleep'))
        self.email_msghandlertxt.SetValue(self.config.get('email','msghandler'))


    def set_data(self):
        self.config.read(path+'rxbox.cfg')
        if self.emailsim_checkbox.GetValue() == True:
            self.config.set('email','simulated','true')
        else:
            self.config.set('email','simulated','false')

        self.config.set('email','imapuser',self.email_imapusertxt.GetValue())
        self.config.set('email','imapserver',self.email_imapservertxt.GetValue())
        self.config.set('email','imappasswd',self.email_imappasswordtxt.GetValue())
        self.config.set('email','smtpuser',self.email_smtpusertxt.GetValue())
        self.config.set('email','smtpserver',self.email_smtpservertxt.GetValue())
        self.config.set('email','smtppasswd',self.email_smtppasswordtxt.GetValue())
        self.config.set('email','mode',self.email_modetxt.GetValue())
        self.config.set('email','sleep',self.email_sleeptxt.GetValue())
        self.config.set('email','msghandler',self.email_msghandlertxt.GetValue())
        self.config.set('email','rxboxid',self.rxboxid)
        configfile = open(path+'rxbox.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(path+'rxbox_backup.cfg')
        if self.config.get('email','simulated') == 'false':
            self.emailsim_checkbox.SetValue(False)
        else:
            self.emailsim_checkbox.SetValue(True)

        self.email_imapusertxt.SetValue(self.config.get('email','imapuser'))
        self.email_imapservertxt.SetValue(self.config.get('email','imapserver'))
        self.email_imappasswordtxt.SetValue(self.config.get('email','imappasswd'))
        self.email_smtpusertxt.SetValue(self.config.get('email','smtpuser'))
        self.email_smtpservertxt.SetValue(self.config.get('email','smtpserver'))
        self.email_smtppasswordtxt.SetValue(self.config.get('email','smtppasswd'))
        self.email_modetxt.SetValue(self.config.get('email','mode'))
        self.email_sleeptxt.SetValue(self.config.get('email','sleep'))
        self.email_msghandlertxt.SetValue(self.config.get('email','msghandler'))
        self.config.read(path+'rxbox.cfg')

