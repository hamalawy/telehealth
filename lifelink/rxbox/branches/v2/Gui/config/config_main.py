"""Config Maker for Rxbox

An application that creates a configuration file to be used by Rxbox

Author: Timothy John Ebido

"""

import ConfigParser

import wx
from wx import xrc

import config_layout
from config_layout import MyApp


class ConfigMain(MyApp):
    
    def __init__(self, *args, **kwds):
        MyApp.__init__(self, *args, **kwds)
        
        self.ecg_simulated = 0
        self.bp_simulated = 0
        self.spo2_simulated = 0
        self.email_simulated = 0
        self.im_simulated = 0
        self.voip_simulated = 0
        
        self.frame.Show()
        
    def onGenerate(self, event):
        """Method for generating configuration file"""

        self.config = ConfigParser.ConfigParser()       
        self.createTriageConfig()
        self.createSensorsConfig()
        self.createEDFConfig()
        
        configfile = open('../rxbox.cfg', 'w')
        self.config.write(configfile)
        
        dlg = wx.MessageDialog(self.frame, \
                'Rxbox Configuration File Generation Successful', 'Generate', wx.OK)
        dlg.ShowModal()
        
        print 'Generation Finished'
        
    def onCheckECG(self, event):
        """Event when checkbox value is changed when clicked"""
        self.ecg_simulated ^= 1
        
        if self.ecg_simulated == 0:
            self.ecg_com_value.Enable()
            self.ecg_baud_value.Enable()
            self.ecg_lead_value.Enable()
            self.ecg_sim_type_val.Disable()
        else:
            self.ecg_com_value.Disable()
            self.ecg_baud_value.Disable()
            self.ecg_lead_value.Disable()
            self.ecg_sim_type_val.Enable()
        
    def onCheckBP(self, event):
        print 'BP Check'
        self.bp_simulated ^= 1
        if self.bp_simulated == 0:
            self.bp_com_value.Enable()
            self.bp_sim_type_val.Disable()
        else:
            self.bp_com_value.Disable()
            self.bp_sim_type_val.Enable()

    def onCheckSpo2(self, event):
        print 'Spo2 Check'
        self.spo2_simulated ^= 1
        if self.spo2_simulated == 0:
            self.spo2_com_value.Enable()
            self.heartrate_sim_type_val.Disable()
            self.spo2_sim_type_val.Disable()
        else:
            self.spo2_com_value.Disable()
            self.heartrate_sim_type_val.Enable()
            self.spo2_sim_type_val.Enable()
    
    def onECGSimSensorVal(self, event):
        """Checks if sensor sim type value is 'others'. If yes, display file
            dialog box
        """
        self.ecg_path = ''
        
        if self.ecg_sim_type_val.GetValue() == 'Others':
            self.ecg_path = self.display_file_dialog()

    def onBPSimSensorVal(self, event):
        
        if self.bp_sim_type_val.GetValue() == 'Others':
            self.display_file_dialog()
            
    def onHeartRateSimSensorVal(self, event):
        
        if self.heartrate_sim_type_val.GetValue() == 'Others':
            self.display_file_dialog()
            
    def onSpo2SimSensorVal(self, event):
        
        if self.spo2_sim_type_val.GetValue() == 'Others':
            self.display_file_dialog()
            
    def display_file_dialog(self):
        file_dialog = wx.FileDialog(self.frame)
        file_dialog.ShowModal()
        temp_list = file_dialog.GetPath().split('/')
        return 'simulators/' + temp_list[-1]
        
    def onCheckEmail(self, event):
        print 'email check'
        self.email_simulated ^= 1
        if self.email_simulated == 0:
            self.enableEmailFields()
            self.email_sim_connection_val.Disable()
            
        else:            
            self.disableEmailFields()
            self.email_sim_connection_val.Enable()

    def enableEmailFields(self):
        self.smtp_val.Enable()
        self.smtp_user_val.Enable()
        self.smtp_pass_val.Enable()
        self.imap_val.Enable()
        self.imap_user_val.Enable()
        self.imap_pass_val.Enable()
        self.email_mode.Enable()
        
    def disableEmailFields(self):
        self.smtp_val.Disable()
        self.smtp_user_val.Disable()
        self.smtp_pass_val.Disable()
        self.imap_val.Disable()
        self.imap_user_val.Disable()
        self.imap_pass_val.Disable()
        self.email_mode.Disable()

    def onCheckIM(self, event):
        print 'im check'
        self.im_simulated ^= 1
        
    def onCheckVoip(self, event):
        print 'voip check'
        self.voip_simulated ^= 1

    def createTriageConfig(self):
        """Method for creating sections related to triage"""
        
        self.config.add_section('email')
        self.config.add_section('im')
        self.config.add_section('voip')
        
        self.config.set('email', 'simulated', self.email_simulated)
        
        if self.email_simulated == 0:
            self.config.set('email', 'smtpserver', self.smtp_val.GetValue())
            self.config.set('email', 'smtpuser', self.smtp_user_val.GetValue())
            self.config.set('email', 'smtppasswd', self.smtp_pass_val.GetValue())
            self.config.set('email', 'imapserver', self.imap_val.GetValue())
            self.config.set('email', 'imapuser', self.imap_user_val.GetValue())
            self.config.set('email', 'imappasswd', self.imap_pass_val.GetValue())
            self.config.set('email', 'mode', self.email_mode.GetValue())
            
        if self.email_simulated == 1:
            if self.email_sim_connection_val.GetValue() == 'Connected':
                self.config.set('email', 'connection', '1')
            else:
                self.config.set('email', 'connection', '0')
        
        self.config.set('im', 'simulated', self.im_simulated)
        self.config.set('voip', 'simulated', self.voip_simulated)
        
    def createSensorsConfig(self):
        """Method for creating sections related to biomedical sensors"""
        
        self.config.add_section('ecg')
        self.config.add_section('bp')
        self.config.add_section('spo2')
        
        self.config.set('ecg', 'simulated', self.ecg_simulated)
        self.config.set('bp', 'simulated', self.bp_simulated)
        self.config.set('spo2', 'simulated', self.spo2_simulated)
        
        if self.ecg_simulated == 0:
            self.config.set('ecg', 'port', self.ecg_com_value.GetValue())
            self.config.set('ecg', 'lead', self.ecg_lead_value.GetValue())
            self.config.set('ecg', 'baud', self.ecg_baud_value.GetValue())
        else:
            if self.ecg_sim_type_val.GetValue() == 'Others':
                self.config.set('ecg', 'sim_type', self.ecg_path)
            else:
                self.config.set('ecg', 'sim_type', self.ecg_sim_type_val.GetValue())
        if self.bp_simulated == 0:
            self.config.set('bp', 'port', self.bp_com_value.GetValue())
        else:
            self.config.set('bp', 'sim_type', self.bp_sim_type_val.GetValue())
        if self.spo2_simulated == 0:
            self.config.set('spo2', 'port', self.spo2_com_value.GetValue()) 
        else:
            self.config.set('spo2', 'hr_sim_type', self.heartrate_sim_type_val.GetValue())
            self.config.set('spo2', 'spo2_sim_type', self.spo2_sim_type_val.GetValue())
            
    def createEDFConfig(self):
        
        spo2_label = 'SpO2 finger'
        spo2_transducer_type = 'IR-Red sensor'
        spo2_phy_dim = '%'
        spo2_phy_min = 0
        spo2_phy_max = 100
        spo2_dig_min = 0
        spo2_dig_max = 100
        spo2_prefiltering = 'None'
        spo2_samples = 15
        
        hr_phy_min = 0
        hr_phy_max = 300
        hr_dig_min = 0
        hr_dig_max = 300
        hr_prefiltering = 'None'
        hr_samples = 15
        
        bp_label = 'bpsystole'
        bp_transducer_type = 'NIBP2010'
        bp_phy_dim = 'mmHg'
        bp_phy_min = 0
        bp_phy_max = 300
        bp_dig_min = 0
        bp_dig_max = 300
        bp_prefiltering = 'None'
        bp_samples = 1
        
        ecg_label = 'ecgII'
        ecg_transducer_type = 'CM'
        ecg_phy_dim = 'mV'
        ecg_phy_min = -43
        ecg_phy_max = 43
        ecg_dig_min = 0
        ecg_dig_max = 32767
        ecg_prefiltering = 'None'
        ecg_samples = 7500
        
        
        self.config.add_section('edf')
        
        self.config.set('edf', 'ecg_label', ecg_label)
        self.config.set('edf', 'ecg_transducer_type', ecg_transducer_type)
        self.config.set('edf', 'ecg_phy_dim', ecg_phy_dim)
        self.config.set('edf', 'ecg_phy_max', ecg_phy_max)
        self.config.set('edf', 'ecg_dig_min', ecg_dig_min)
        self.config.set('edf', 'ecg_dig_max', ecg_dig_max)
        self.config.set('edf', 'ecg_prefiltering', ecg_prefiltering)
        self.config.set('edf', 'ecg_samples', ecg_samples)
        
        self.config.set('edf', 'bp_label', bp_label)
        self.config.set('edf', 'bp_transducer_type', bp_transducer_type)
        self.config.set('edf', 'bp_phy_dim', bp_phy_dim)
        self.config.set('edf', 'bp_phy_max', bp_phy_max)
        self.config.set('edf', 'bp_phy_min', bp_phy_min)
        self.config.set('edf', 'bp_dig_min', bp_dig_min)
        self.config.set('edf', 'bp_dig_max', bp_dig_max)
        self.config.set('edf', 'bp_prefiltering', bp_prefiltering)
        self.config.set('edf', 'bp_samples', bp_samples)
        
        self.config.set('edf', 'spo2_label', spo2_label)
        self.config.set('edf', 'spo2_transducer_type', spo2_transducer_type)
        self.config.set('edf', 'spo2_phy_dim', spo2_phy_dim)
        self.config.set('edf', 'spo2_phy_min', spo2_phy_min)
        self.config.set('edf', 'spo2_phy_max', spo2_phy_max)
        self.config.set('edf', 'hr_phy_min', hr_phy_min)
        self.config.set('edf', 'hr_phy_max', hr_phy_max)
        self.config.set('edf', 'spo2_dig_min', spo2_dig_min)
        self.config.set('edf', 'spo2_dig_max', spo2_dig_max)
        self.config.set('edf', 'hr_dig_min', hr_dig_min)
        self.config.set('edf', 'hr_dig_max', hr_dig_max)
        self.config.set('edf', 'spo2_prefiltering', spo2_prefiltering)
        self.config.set('edf', 'hr_prefiltering', hr_prefiltering)
        self.config.set('edf', 'spo2_samples', spo2_samples)
        self.config.set('edf', 'hr_samples', hr_samples)

    def onLoad(self, event):
        """Method for loading and displaying the contents of configuration file"""
        print 'Load'
        self.config_load = ConfigParser.ConfigParser()
        self.config_load.read('../rxbox.cfg')

        if self.config_load.get('email', 'simulated') == '0':
            self.email_simulated = 0
            self.email_sim.SetValue(False)
            self.enableEmailFields()
            self.email_sim_connection_val.Disable()
            self.smtp_val.SetValue(self.config_load.get('email', 'smtpserver'))
            self.smtp_user_val.SetValue(self.config_load.get('email', 'smtpuser'))
            self.smtp_pass_val.SetValue(self.config_load.get('email', 'smtppasswd'))
            self.imap_val.SetValue(self.config_load.get('email', 'imapserver'))
            self.imap_user_val.SetValue(self.config_load.get('email', 'imapuser'))
            self.imap_pass_val.SetValue(self.config_load.get('email', 'imappasswd'))
            self.email_mode.SetValue(self.config_load.get('email', 'mode'))
            
        if self.config_load.get('email', 'simulated') == '1':
            self.email_simulated = 1
            self.disableEmailFields()
            self.email_sim_connection_val.Enable()
            if self.config_load.get('email', 'connection') == '0':
                self.email_sim_connection_val.SetValue('Not Connected')
            else:
                self.email_sim_connection_val.SetValue('Connected')
                
            self.email_sim.SetValue(True)
            
        if self.config_load.get('im', 'simulated') == '0':
            self.im_simulated = 0
            self.im_sim.SetValue(False)
        
        if self.config_load.get('im', 'simulated') == '1':
            self.im_simulated = 1
            self.im_sim.SetValue(True)
            
        if self.config_load.get('voip', 'simulated') == '0':
            self.voip_simulated = 0
            self.voip_sim.SetValue(False)
            
        if self.config_load.get('voip', 'simulated') == '1':
            self.voip_simulated = 1
            self.voip_sim.SetValue(True)
            
        if self.config_load.get('ecg', 'simulated') == '0':
            self.ecg_simulated = 0
            self.ecg_sim.SetValue(False)
            self.ecg_com_value.SetValue(self.config_load.get('ecg', 'port'))
            self.ecg_lead_value.SetValue(self.config_load.get('ecg', 'lead'))
            self.ecg_sim_type_val.Disable()
            
        if self.config_load.get('ecg', 'simulated') == '1':
            self.ecg_simulated = 1
            self.ecg_sim.SetValue(True)
            self.ecg_com_value.Disable()
            self.ecg_lead_value.Disable()
            self.ecg_sim_type_val.SetValue(self.config_load.get('ecg', 'sim_type'))
            self.ecg_sim_type_val.Enable()
            
        if self.config_load.get('bp', 'simulated') == '0':
            self.bp_simulated = 0
            self.bp_sim.SetValue(False)
            self.bp_com_value.SetValue(self.config_load.get('bp', 'port'))
            self.bp_sim_type_val.Disable()

        if self.config_load.get('bp', 'simulated') == '1':
            self.bp_simulated = 1
            self.bp_sim.SetValue(True)
            self.bp_sim_type_val.Enable()
            self.bp_sim_type_val.SetValue(self.config_load.get('bp', 'sim_type'))
            self.bp_com_value.Disable()
            
        if self.config_load.get('spo2', 'simulated') == '0':
            self.spo2_simulated = 0
            self.spo2_sim.SetValue(False)
            self.spo2_com_value.SetValue(self.config_load.get('spo2', 'port'))
            self.spo2_sim_type_val.Disable()

        if self.config_load.get('spo2', 'simulated') == '1':
            self.spo2_simulated = 1
            self.spo2_sim.SetValue(True)
            self.spo2_sim_type_val.SetValue(self.config_load.get('spo2', 'spo2_sim_type'))
            self.heartrate_sim_type_val.SetValue(self.config_load.get('spo2', 'hr_sim_type'))
            self.heartrate_sim_type_val.Enable()
            self.spo2_sim_type_val.Enable()
            self.spo2_com_value.Disable()        
    
    def onAbout(self, event):
        """Method that shows an "About" box"""
        
        dlg = wx.MessageDialog(self.frame, \
                'RxBox Configuration Maker\n\n\Version 0.1\n\nAuthor: Tim Ebido', \
                'About', wx.OK)
        dlg.ShowModal()
        
    def onExit(self, event):

        self.frame.Destroy()

if __name__ == '__main__':
    app = ConfigMain(False)
    app.MainLoop()


