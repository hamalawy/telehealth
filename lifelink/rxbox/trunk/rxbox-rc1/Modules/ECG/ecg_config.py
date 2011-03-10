import wx
from ecg_cgui import ECG_config_frame
import ConfigParser
import os

path=os.getcwd()
if path[len(path)-13:]=='Configuration':
    path='../'
else:
    path=os.getcwd()+'/'

class ECG_Configurationmain(ECG_config_frame):
    def __init__(self, parent,*args, **kwds):
        ECG_config_frame.__init__(self, parent,*args, **kwds)
        self.config=ConfigParser.ConfigParser()
        self.config.read(path+'rxbox.cfg')
        self.get_data()
        self.Bind(wx.EVT_COMBOBOX, self.onBrowse)
        self.newpath = ''

    def get_data(self):
        if self.config.get('ECG','simulated') == 'false':
            self.ecgsim_checkbox.SetValue(False)
        else:
            self.ecgsim_checkbox.SetValue(True)
        if self.config.get('ECG','simfile') == 'data':
            self.ecg_cbox.SetSelection(0)
        else:  
            self.ecg_cbox.SetSelection(1)
        #ADD here an option for the sim type combobox
        self.ecg_porttxt.SetValue(self.config.get('ECG','port'))
        self.ecg_baudtxt.SetValue(self.config.get('ECG','baud'))
        self.ecg_timeouttxt.SetValue(self.config.get('ECG','timeout'))
        self.ecg_daqdurtxt.SetValue(self.config.get('ECG','daqdur'))
        self.ecg_ecmtxt.SetValue(self.config.get('ECG','ecmcheck'))
        if self.config.get('ECG','filter') == 'false':
            self.ecgfilter_checkbox.SetValue(False)
        else:
            self.ecgfilter_checkbox.SetValue(True)
        if self.config.get('ECG','debug') == 'false':
            self.ecgdebug_checkbox.SetValue(False)
        else:
            self.ecgdebug_checkbox.SetValue(True)
        self.ecg_freqtxt.SetValue(self.config.get('ECG','freq'))
        if self.config.get('ECG','mode') == '3 Lead':
            self.ecg_modecbox.SetSelection(0)
        else:  
            self.ecg_modecbox.SetSelection(1)        
        
    def onBrowse(self, event):
        if event.GetSelection() == 'Others':
            dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                    path = dlg.GetPath()
                    self.newpath = os.path.basename(path)
            dlg.Destroy()


    def set_data(self):
        self.config.read(path+'rxbox.cfg')
        if self.ecgsim_checkbox.GetValue() == True:
            self.config.set('ECG','simulated','true')
        else:
            self.config.set('ECG','simulated','false')
        # Add file here
        if self.ecg_cbox.GetValue == 'Others':
            if self.newpath != '':
                self.config.set('ECG','simfile',self.newpath)
            else:
                self.config.set('ECG','simfile','data')
        else:
            self.config.set('ECG','simfile','data')
        self.config.set('ECG','port',self.ecg_porttxt.GetValue())
        self.config.set('ECG','baud',self.ecg_baudtxt.GetValue())
        self.config.set('ECG','timeout',self.ecg_timeouttxt.GetValue())
        self.config.set('ECG','daqdur',self.ecg_daqdurtxt.GetValue())
        self.config.set('ECG','ecmcheck',self.ecg_ecmtxt.GetValue())

        if self.ecgfilter_checkbox.GetValue() == True:
            self.config.set('ECG','filter','true')
        else:
            self.config.set('ECG','filter','false')

        if self.ecgdebug_checkbox.GetValue() == True:
            self.config.set('ECG','debug','true')
        else:
            self.config.set('ECG','debug','false')

        self.config.set('ECG','freq',self.ecg_freqtxt.GetValue())

        if self.ecg_modecbox.GetValue() == '3 Lead':
            self.config.set('ECG','mode','3 Lead')
        else:
            self.config.set('ECG','mode','12 Lead')
        self.config.set('ECG','ecmcheck',self.ecg_ecmtxt.GetValue())

        configfile = open(path+'ecg.cfg', 'wb')
        self.config.write(configfile)

    def default_data(self):
        self.config.read(path+'rxbox_backup.cfg')
        if self.config.get('ECG','simulated') == 'false':
            self.ecgsim_checkbox.SetValue(False)
        else:
            self.ecgsim_checkbox.SetValue(True)
        if self.config.get('ECG','simfile') == 'data':
            self.ecg_cbox.SetSelection(0)
        else:  
            self.ecg_cbox.SetSelection(1)
        #ADD here an option for the sim type combobox
        self.ecg_porttxt.SetValue(self.config.get('ECG','port'))
        self.ecg_baudtxt.SetValue(self.config.get('ECG','baud'))
        self.ecg_timeouttxt.SetValue(self.config.get('ECG','timeout'))
        self.ecg_daqdurtxt.SetValue(self.config.get('ECG','daqdur'))
        self.ecg_ecmtxt.SetValue(self.config.get('ECG','ecmcheck'))
        if self.config.get('ECG','filter') == 'false':
            self.ecgfilter_checkbox.SetValue(False)
        else:
            self.ecgfilter_checkbox.SetValue(True)
        if self.config.get('ECG','debug') == 'false':
            self.ecgdebug_checkbox.SetValue(False)
        else:
            self.ecgdebug_checkbox.SetValue(True)
        self.ecg_freqtxt.SetValue(self.config.get('ECG','freq'))
        if self.config.get('ECG','mode') == '3 Lead':
            self.ecg_modecbox.SetSelection(0)
        else:  
            self.ecg_modecbox.SetSelection(1)
        self.config.read(path+'rxbox.cfg')



