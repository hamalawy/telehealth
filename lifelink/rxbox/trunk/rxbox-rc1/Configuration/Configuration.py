"""

Configuration Parser Rxbox 1.0

Developers:
Mark Jan C. Bangoy
Luke Wicent Sy

Adviser:
Luis G. Sison

"""
import wx
import sys
from gui_conf import MyFrame_conf
from errorlog_config import ERRORLOG_Configurationmain
from db_config import DB_Configurationmain
from gen_config import Geninfo_Configurationmain

import os
path=os.getcwd()
if path[len(path)-13:]=='Configuration':
    path='../Modules'
else:
    path=os.getcwd()+'/Modules'

sys.path.append( path+'/BP' )
from bp_config  import BP_Configurationmain
sys.path.append( path + '/SPO2' )
from spo2_config  import SPO2_Configurationmain
sys.path.append( path + '/VoIP' )
from voip_config import VOIP_Configurationmain
sys.path.append( path + '/IM' )
from im_config import IM_Configurationmain
sys.path.append( path + '/ECG' )
from ecg_config import ECG_Configurationmain
sys.path.append( path + '/Triage' )
from email_config import EMAIL_Configurationmain


class Configurationmain(MyFrame_conf):
    def __init__(self, *args, **kwds):
        MyFrame_conf.__init__(self, *args, **kwds)
        self.SetTitle('System Settings')
        root = self.tree.AddRoot('Modules')
        geninfo = self.tree.AppendItem(root, 'General Information')
        ecg = self.tree.AppendItem(root, 'ECG')
        bp = self.tree.AppendItem(root, 'Blood Pressure')
        spo2 = self.tree.AppendItem(root, 'Pulse Oximeter')
        steth = self.tree.AppendItem(root, 'Stethoscope')
        email = self.tree.AppendItem(root, 'Email')
        voip = self.tree.AppendItem(root, 'VOIP')
        im = self.tree.AppendItem(root, 'Instant Messaging')
        snapshot = self.tree.AppendItem(root, 'Snapshot')
        db = self.tree.AppendItem(root, 'Database')
        errorlog = self.tree.AppendItem(root, 'Error Log')
        perspective = self.tree.AppendItem(root, 'Perspective')

        self.module_method={'General Information':self.m_geninfo,'ECG':self.m_ecg,'Blood Pressure':self.m_bp,\
                            'Pulse Oximeter':self.m_spo2,\
                            'Stethoscope':self.m_steth,'Email':self.m_email, \
                            'VOIP':self.m_voip,'Instant Messaging':self.m_im,'Snapshot':self.m_snapshot,\
                            'Database':self.m_db, 'Error Log':self.m_errorlog, 'Perspective':self.m_perspective}
        

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.gen=Geninfo_Configurationmain(self.module)
        self.ecg=ECG_Configurationmain(self.module)
        self.bp=BP_Configurationmain(self.module)
        self.spo2=SPO2_Configurationmain(self.module)
        self.email=EMAIL_Configurationmain(self.module)
        self.voip=VOIP_Configurationmain(self.module)
        self.im=IM_Configurationmain(self.module)
        self.db=DB_Configurationmain(self.module)
        self.errorlog=ERRORLOG_Configurationmain(self.module)

        self.instances=(self.gen,self.ecg,self.bp,self.spo2,self.email,self.voip,self.im,self.db,self.errorlog)
        self.display = wx.StaticText(self.module, -1, '',(10,10), style=wx.ALIGN_LEFT)

        self.m_geninfo()
  #      self.bp()
   #     self.bp.Hide()
    #    self.ecg.Hide()
     #   self.gen.Show()
        self.Centre()
        

    def OnSelect(self, event):
        item =  event.GetItem()
        self.module_method[self.tree.GetItemText(item)]()

    def m_geninfo(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.gen.panel_1.Show()
    
    def m_ecg(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.ecg.panel_1.Show()

    def m_bp(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.bp.panel_1.Show()

    def m_spo2(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.spo2.panel_1.Show()

    def m_steth(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.display.SetLabel("Under Development: \nTrivia\n Did you know that the medical term for the sound\n of a heartbeat is 'Lab-dub'")

    def m_email(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.email.panel_1.Show()

    def m_voip(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.voip.panel_1.Show()
    def m_im(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.im.panel_1.Show()
    def m_snapshot(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.display.SetLabel("Under Development: Ensure Camera Connected\n \nDid you know that : \n As of July 2005, the smallest country in\n terms of population was Pitcairn Islands with \n 45 inhabitants!  ")

    def m_db(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.db.panel_1.Show()

    def m_errorlog(self):
        for var in self.instances:
            var.panel_1.Hide()
        self.errorlog.panel_1.Show()

    def m_perspective(self):
        for var in self.instances:
            var.panel_1.Hide()
        
        self.display.SetLabel("Critical Data: Only Admin allowed")
    
    def onClose(self,event):
        self.Destroy()

    def onCancel(self, event): # wxGlade: MyFrame_conf.<event_handler>
        self.Destroy()

    def onDone(self, event): # wxGlade: MyFrame_conf.<event_handler>
        self.gen.set_data()
        rxboxid=self.gen.rxboxid
        self.email.rxboxid,self.voip.rxboxid,self.im.rxboxid = [rxboxid]*3
        self.db.set_data()
        self.errorlog.set_data()
        self.ecg.set_data()
        self.bp.set_data()
        self.spo2.set_data()
        self.email.set_data()
        self.voip.set_data()
        self.im.set_data()
        dlg = wx.MessageDialog(self, 'Settings Saved', 'Information', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def onDefault(self, event): # wxGlade: MyFrame_conf.<event_handler>
        dlg = wx.MessageDialog(self, 'This will revert system to Factory Settings', 'Alert', wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_OK:
            for var in self.instances:
                var.default_data()
        dlg.Destroy()
        


class MyApp(wx.App):
    def OnInit(self):
        frame = Configurationmain(None, -1, 'treectrl.py')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()

