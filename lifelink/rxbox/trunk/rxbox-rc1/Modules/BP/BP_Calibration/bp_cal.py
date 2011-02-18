
import wx
from bpcal_gui import MyFrame
import time
import threading
import ConfigParser
config = ConfigParser.ConfigParser()
import os
path=os.getcwd()
print path[len(path)-14:]
if path[len(path)-14:]=='BP_Calibration':
    config.read('../../../rxbox.cfg')
else:
    config.read('rxbox.cfg')
print config.get('BP','port')
from BPDAQLive import BPDAQ
from least_squares import Ls
import datetime
import csv
import bp_portcheck

class Calibration_main(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        #self.bp = BPDAQ(self,port =config.get('BP','port'),coeff= (1,0,0,0,1,0))
        self.SetTitle("BP Calibration")
        self.bp_pressure_indicator = wx.Gauge(self.bpbarpanel,-1, 250, size=(50, 130),style=wx.GA_VERTICAL)
        self.bp_pressure_indicator.Enable(False)
        self.alive=False       
        self.updatealive=False
        self.bp_infolabel.SetLabel('Not Ready')
        self.bpNow_Button.Enable(True)
        self.Calibrate_button.Enable(False)
        self.button_1.Enable(False)
        self.button_1.SetLabel("RECORD NOW")
        self.Calibrate_button.SetLabel("CALIBRATE NOW")
        self.Sys_Merc_txt.SetValue("0")
        self.Dias_Merc_txt.SetValue("0")
        self.Sys_Comm_txt.SetValue("0")
        self.Dias_Comm_txt.SetValue("0")
        self.version_label.SetLabel('version: '+str(config.get('GENINFO','model')))
        #self.minor_check()
        now = datetime.datetime.now()     
        path=os.getcwd()
        if path[len(path)-14:]=='BP_Calibration':
            self.fileopen=open("Data/"+now.strftime("%m-%d-%y_%H-%M")+".csv","ab")
        else:
           self.fileopen=open(path+'/Modules/BP/BP_Calibration/Data/'+now.strftime("%m-%d-%y_%H-%M")+".csv","ab")  
        self.csvfile=csv.writer(self.fileopen)
        data=["Mercurial Systolic","Mercurial Diastolic","Commercial Systolic","Commercial Diastolic","Uncalibrated Rxbox Systolic","Uncalibrated Rxbox Diastolic","Calibrated Rxbox Systolic","Calibrated Rxbox Diastolic"]
        self.ls=Ls()
        self.csv_writer(data)
        self.n_samples=0

    def csv_writer(self,data):
        self.csvfile.writerow(data)

    def minor_check(self):
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(0.981,0,-6.59,0,0.38741,38.45))

        status=self.bp.init_status_check()
        if status== False:
            print 'initialization failed'
            self.bp_infolabel.SetLabel('Not Ready')
            return
        print 'bp init part 1 done'

        status=self.bp.init_firmware_version()
        if status== False:
            print 'initialization failed'
            self.bp_infolabel.SetLabel('Not Ready')
            return
        print 'bp init part 2 done'

        self.bpNow_Button.Enable(True)
        self.bp_infolabel.SetLabel('BP Ready')

    def onBPNow(self, event): # wxGlade: MyFrame.<event_handler>
        self.bpNow_Button.Enable(False)
        self.Calibrate_button.Enable(False)
        self.button_1.Enable(False)
        self.start()

    def start(self):
        print 'BP START'
        port2check=[config.get('BP','port')]
        c=bp_portcheck.Bp_check(port2check)
        port=c.check()
        if port == None:
            self.bp_infolabel.SetLabel('Cannot Proceed:BP Unavailable')
            return
        self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(float(config.get('BP','sys_coeff_a')),0,float(config.get('BP','sys_coeff_b')),0,float(config.get('BP','dias_coeff_a')),float(config.get('BP','dias_coeff_b'))))
        #self.bp = BPDAQ(self,port =config.get('BP','port'),coeff=(0.74212,0,19.00353,0,0.36265,45.688))
        self.bp.OpenSerial()
        self.bp.send_request(self.setBPmaxpressure_combobox.GetValue()[:3])
        self.setBPmaxpressure_combobox.Enable(False)
        self.bpNow_Button.SetToolTipString("Acquiring BP")
        self.bpdaq_thread = threading.Thread(target=self.Get_bp)
        self.bpdaq_thread.start()
        return True

    def onRecord(self, event): # wxGlade: MyFrame.<event_handler>
        
        
        print self.Sys_Merc_txt.GetValue()
        print self.Dias_Merc_txt.GetValue()
        sys_real=int(self.Sys_Merc_txt.GetValue())
        dias_real=int(self.Dias_Merc_txt.GetValue())
        sys_comm=int(self.Sys_Comm_txt.GetValue())
        dias_comm=int(self.Dias_Comm_txt.GetValue())
        if (sys_real == 0 and dias_real == 0) or (sys_comm == 0 and dias_comm == 0):
            dlg = wx.MessageDialog(self, 'Please fill up the required fields', 'Error', wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        sys_actual=int(self.bp.bp_systolic)
        dias_actual=int(self.bp.bp_diastolic)
        rawsys=int(self.bp.rawsys)
        rawdias=int(self.bp.rawdias)
        print "Data"
        print sys_real,sys_actual,dias_real,dias_actual
        self.ls.add(sys_real,rawsys,dias_real,rawdias)
        self.Sys_Merc_txt.SetValue("0")
        self.Dias_Merc_txt.SetValue("0")
        self.Sys_Comm_txt.SetValue("0")
        self.Dias_Comm_txt.SetValue("0")
        self.bpvalue_label.SetLabel("--/--")
        data=[sys_real,dias_real,sys_comm,dias_comm,rawsys,rawdias,sys_actual,dias_actual]
        self.csv_writer(data)
        self.button_1.Enable(False)
        print "add record"
        self.n_samples+=1
        self.Samples_txt.SetLabel(str(self.n_samples))
        if self.n_samples>2:
            self.Calibrate_button.Enable(True)

    def onCalibrate(self, event): # wxGlade: MyFrame.<event_handler>
        a_sys,b_sys,a_dias,b_dias=self.ls.get_coeffecients()
        self.n_samples=0
        self.Samples_label.SetLabel(str(self.n_samples))
        self.Sys_Merc_txt.SetValue("0")
        self.Dias_Merc_txt.SetValue("0")
        self.bpvalue_label.SetLabel("--/--")
        self.Calibrate_button.Enable(False)
        config.set('BP','sys_coeff_a',a_sys)
        config.set('BP','sys_coeff_b',b_sys)
        config.set('BP','dias_coeff_a',a_dias)
        config.set('BP','dias_coeff_b',b_dias)
        path=os.getcwd()
        if path[len(path)-14:]=='BP_Calibration':
            configfile = open('../../../rxbox.cfg', 'wb')
        else:
            configfile = open('rxbox.cfg', 'wb')
        config.write(configfile)
        configfile.close()
        dlg = wx.MessageDialog(self, 'Calibration Successful', 'Confirmation', wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

        

    def Get_bp(self):
        self.alive=True 
        none_count=0
        while self.alive:
            time.sleep(0.1)
            press = self.bp.get_reply()
            if press == 'S5':
                press =''
                continue
            if press == None or press == '':
                print 'none type returned'
                none_count+=1
                if none_count<1:
                    continue
                else:
                    press='09990'
            try:
                self.press = int(press[1:4])
            except:
                print 'bp error'
                print press
                self.press=999
            if self.press== 999:
                self.alive=False
                self.bp.get()
                self.updatealive=False
                self.bp.stop()                
                self.bp.CloseSerial()
            wx.CallAfter(self.pressure_update)
        self.bp.CloseSerial()
                
    def pressure_update(self):
        if self.press != 999:
            self.bpNow_Button.Enable(False)
            self.bp_pressure_indicator.SetValue(self.press)
            self.bp_infolabel.SetLabel(str(self.press)+' mmHg')
        else:
            self.updatealive=False
            self.alive=False
            self.bp_pressure_indicator.SetValue(0)
            self.bp_infolabel.SetLabel(self.bp.bpstatus)
            self.bp_pressure_indicator.Enable(False)
            self.bpNow_Button.Enable(True)
            self.setBPmaxpressure_combobox.Enable(True)
            self.button_1.Enable(True)
            self.bpNow_Button.SetToolTipString("Acquire BP Reading")
            self.bpvalue_label.SetLabel(' Cal    UnCal \n'+str(self.bp.bp_systolic)+'/'+str(self.bp.bp_diastolic)+' '+str(self.bp.rawsys)+'/'+str(self.bp.rawdias))

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = Calibration_main(None, -1, "")
    app.SetTopWindow(rx_frame)
    #rx_frame.Maximize(True)
    rx_frame.Show()
    app.MainLoop()
