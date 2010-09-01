"""Config Layout for Rxbox

Initializes the layout and GUI Elements for Configuration Generator

Classes: MyApp

Author: RxBox Development Team
        IRC, EEEI, UP Diliman

"""

import wx
from wx import xrc

class MyApp(wx.App):
    """Main class for application
    
    - Initializes OnInit() on start-up
    
    Methods:
    OnInit
    init_frame
    """

    def OnInit(self):
        """Instantiates the xml file"""
        
        self.res = xrc.XmlResource('layout.xrc')
        self.init_frame()
        return True

    def init_frame(self):
        """Creates GUI elements
        
        - Binds necessary methods for checkbox and combobox
        
        """
        
        self.frame = self.res.LoadFrame(None, 'frame_1')
        self.smtp_val = xrc.XRCCTRL(self.frame, 'smtp_val')
        self.smtp_user_val = xrc.XRCCTRL(self.frame, 'smtp_user_val')
        self.smtp_pass_val = xrc.XRCCTRL(self.frame, 'smtp_pass_val')
        self.imap_val = xrc.XRCCTRL(self.frame, 'imap_val')
        self.imap_user_val = xrc.XRCCTRL(self.frame, 'imap_user_val')
        self.imap_pass_val = xrc.XRCCTRL(self.frame, 'imap_pass_val')
        self.ecg_com_value = xrc.XRCCTRL(self.frame, 'ecg_com_value')
        self.ecg_lead_value = xrc.XRCCTRL(self.frame, 'ecg_lead_value')
        self.ecg_baud_value = xrc.XRCCTRL(self.frame, 'ecg_baud_value')
        self.ecg_sim_type_val = xrc.XRCCTRL(self.frame, 'ecg_sim_type_val')
        self.bp_com_value = xrc.XRCCTRL(self.frame, 'bp_com_value')
        self.bp_sim_type_val = xrc.XRCCTRL(self.frame, 'bp_sim_type_val')
        self.spo2_com_value = xrc.XRCCTRL(self.frame, 'spo2_com_value')
        self.heartrate_sim_type_val = xrc.XRCCTRL(self.frame, 'heartrate_sim_type_val')
        self.spo2_sim_type_val = xrc.XRCCTRL(self.frame, 'spo2_sim_type_val')
        
        self.ecg_sim = xrc.XRCCTRL(self.frame, 'ecg_sim')
        self.email_sim = xrc.XRCCTRL(self.frame, 'email_sim')
        self.im_sim = xrc.XRCCTRL(self.frame, 'im_sim')
        self.voip_sim = xrc.XRCCTRL(self.frame, 'voip_sim')
        self.bp_sim = xrc.XRCCTRL(self.frame, 'bp_sim')
        self.spo2_sim = xrc.XRCCTRL(self.frame, 'spo2_sim')
        self.email_mode = xrc.XRCCTRL(self.frame, 'email_mode')
        self.email_sim_connection_val = xrc.XRCCTRL(self.frame, 'email_sim_connection_val')
        
        self.database_pass_val = xrc.XRCCTRL(self.frame, 'database_pass_val')
        self.voip_rxboxid_val = xrc.XRCCTRL(self.frame, 'voip_rxboxid_val')

        self.Bind(wx.EVT_MENU, self.onLoad, id=1)
        self.Bind(wx.EVT_MENU, self.onAbout, id=3)
        self.Bind(wx.EVT_MENU, self.onExit, id=2)
        self.Bind(wx.EVT_BUTTON, self.onGenerate, id=xrc.XRCID('Generate'))
        self.Bind(wx.EVT_CHECKBOX, self.onCheckECG, id=xrc.XRCID('ecg_sim'))
        self.Bind(wx.EVT_CHECKBOX, self.onCheckBP, id=xrc.XRCID('bp_sim'))
        self.Bind(wx.EVT_CHECKBOX, self.onCheckSpo2, id=xrc.XRCID('spo2_sim'))
        self.Bind(wx.EVT_CHECKBOX, self.onCheckEmail, id=xrc.XRCID('email_sim'))
        self.Bind(wx.EVT_CHECKBOX, self.onCheckIM, id=xrc.XRCID('im_sim'))        
        self.Bind(wx.EVT_CHECKBOX, self.onCheckVoip, id=xrc.XRCID('voip_sim'))
        self.Bind(wx.EVT_COMBOBOX, self.onECGSimSensorVal, id=xrc.XRCID('ecg_sim_type_val'))
        self.Bind(wx.EVT_COMBOBOX, self.onBPSimSensorVal, id=xrc.XRCID('bp_sim_type_val'))
        self.Bind(wx.EVT_COMBOBOX, self.onHeartRateSimSensorVal, id=xrc.XRCID('heartrate_sim_type_val'))
        self.Bind(wx.EVT_COMBOBOX, self.onSpo2SimSensorVal, id=xrc.XRCID('spo2_sim_type_val'))

"""        
    def onGenerate(self, event):
        self.file = open('rxbox.cfg','w')
        self.file.write('This is a test\n')
        self.file.close()
        
    def onExit(self, event):
        print 'Exit'
        self.frame.Destroy()
"""
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
