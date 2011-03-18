from start_gui import MyFrame
import wx
import time
import os
path=os.getcwd()+'/States/TestState/start_box/'
import subprocess
import commands

from Modules.Util import *

class ShowMain(MyFrame):
    def __init__(self, engine, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        self.Center()
        self.SetTitle('Initializing')
        self._engine = engine
        self._app = self._engine._app
        self._config = self._engine._config
        self._panel = self._engine._frame._panel

        self.status="Initializing Processes...."
        #self.stat_txt.SetValue(self.status)
        self.stat_txt.Hide()
        #self.SetSize((557, 200))
        self.Layout()
        #self.Refresh()
        self.SetSize((557, 500))
        self.Refresh()
        self.timer1 = wx.Timer(self, -1)
        self.Bind(wx.EVT_TIMER, self.start_system_check, self.timer1)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.picstat=True
        self.finished=False
        self.test_method={  self.test_ecg:(self.ecgbmp,'ecg_standby.png','ecg_fail.png','ecg_ready.png'),\
                            self.test_spo2:(self.spo2bmp,'spo2_standby.png','spo2_fail.png','spo2_ready.png'),\
                            self.test_bp:(self.bpbmp,'bp_standby.png','bp_fail.png','bp_ready.png'),\
                            self.test_cam:(self.cambmp,'cam_standby.png','cam_fail.png','cam_ready.png'),\
                            self.test_dicom:(self.dcmbmp,'dcm_standby.png','dcm_fail.png','dcm_ready.png'),\
                            self.test_edf:(self.edfbmp,'edf_standby.png','edf_fail.png','edf_ready.png'),\
                            self.test_net:(self.netbmp,'net_standby.png','net_fail.png','net_ready.png')}

        self.ports=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2']

        self.Show()
        wx.Yield()
        self.start_system_check()

    def start_system_check(self):
        self.statlabel.SetLabel('Starting')
        
        try:
            comm = subprocess.Popen("dmesg%s"%self._config.get('SPO2', 'dynamic'), shell=True, stdout=subprocess.PIPE)
            self.spoport=comm.stdout.read().split('ttyUSB')[-1].strip()
            self._config.set('SPO2', 'port', '/dev/ttyUSB%s'%self.spoport[0])
            self.spoport='/dev/ttyUSB'+self.spoport[0]
            statmsg='Dmesg SPO2 device passed...Setting Priority SPO2 port to '+self.spoport
            self.status=self.status+'\n'+statmsg
            self.stat_txt.SetValue(self.status)
        except:
            self.spoport='/dev/ttyUSB1'
            statmsg='Dmesg SPO2 device failed...Setting Default SPO2 port to '+self.spoport
            self.status=self.status+'\n'+statmsg
            self.stat_txt.SetValue(self.status)
            #self._logger.error(ERROR('SPO2 Dynamic Port Allocation Failed'))   

        try:
            comm = subprocess.Popen("dmesg%s"%self._config.get('BP', 'dynamic'), shell=True, stdout=subprocess.PIPE)
            self.bpport=comm.stdout.read().split('ttyUSB')[-1].strip()
            self._config.set('BP', 'port', '/dev/ttyUSB%s'%self.bpport[0])
            self.bpport='/dev/ttyUSB'+self.bpport[0]
            self.bpport='/dev/ttyUSB2'
            statmsg='Dmesg BP device passed...Setting Priority BP port to '+self.bpport
            self.status=self.status+'\n'+statmsg
            self.stat_txt.SetValue(self.status)
        except:
            self.bpport='/dev/ttyUSB2'
            statmsg='Dmesg BP device failed...Setting Default BP port to '+self.spoport
            self.status=self.status+'\n'+statmsg
            self.stat_txt.SetValue(self.status)
            #self._logger.error(ERROR('BP Dynamic Port Allocation Failed'))   

        self._config.write(open('rxbox.cfg', 'w'))
        self._config.read('rxbox.cfg')

        #print 'test begins'        
        for test in self.test_method.keys():
            self.key=test
            test()
            self.Refresh()
        self.statlabel.SetLabel('Testing Finished.....')    
        wx.Yield()       
        time.sleep(5)
        self.backstate()

    def on_Details(self, event): # wxGlade: MyFrame.<event_handler>
        self.stat_txt.Show()
        self.stat_txt.SetValue(self.status)
       # self.stat_txt.Show() 
        #self.SetSize((557, 200))
        self.Layout()
        #self.Refresh()
        #self.SetSize((557, 500))
        self.Refresh()
        self.finished=True        
        #self.backstate()
       

    def test_ecg(self):
        self.statlabel.SetLabel('Testing ECG.....')
        self.bmppanel=self.test_method[self.key][0]
        self.guipic=self.test_method[self.key]
        ecgport = self._panel['ecg'].get_port()
        try:
            if ecgport:
                self._config.set('ECG', 'port', '%s'%ecgport)
                self._config.write(open('rxbox.cfg', 'w'))
                self._config.read('rxbox.cfg')
                self._panel['ecg'].load_config()
                status=True 
                statmsg='ECG Ready...Connected to '+ecgport
            else: 
                status=False
                statmsg='ECG device Failed Initialization....No ECG device connected'
        except:
            self._config.set('ECG', 'port', '%s'%ecgport)
            self._config.write(open('rxbox.cfg', 'w'))
            statmsg='ECG device failed...Setting Default ECG port to '+ecgport 
       
        self.status=self.status+'\n'+statmsg
        self.stat_txt.SetValue(self.status)
        self.update_result(status)

    def delay(self):
        pass

    def test_spo2(self):
        self.statlabel.SetLabel('Testing SPO2 device.....')
        self.bmppanel=self.test_method[self.key][0]
        self.guipic=self.test_method[self.key]
        
        port2check=self.port_priority(self.spoport,self.ports)
        #print port2check
        spo2_port=self._panel['spo2'].find_port(port2check)
        
        if spo2_port!=None:
            self._config.set('SPO2', 'port', spo2_port)
            self._config.write(open('rxbox.cfg', 'w'))
            self.ports.remove(spo2_port)
            self._panel['spo2'].minor_check()
            status=True 
            statmsg='SPO2 Ready...Connected to '+spo2_port
        else:
            status=False
            statmsg='SPO2 device Failed Initialization....No SPO2 device connected'
        
        self.status=self.status+'\n'+statmsg
        self.stat_txt.SetValue(self.status)
        self.update_result(status)

    def test_bp(self):
        self.statlabel.SetLabel('Testing Blood Pressure device.....')
        self.bmppanel=self.test_method[self.key][0]
        self.guipic=self.test_method[self.key]
        
        port2check=self.port_priority(self.bpport,self.ports)
        #print port2check
        bp_port=self._panel['bp'].find_port(port2check)
        if bp_port!=None:
            self._config.set('BP', 'port', bp_port)
            self._config.write(open('rxbox.cfg', 'w'))        
            self._panel['bp'].minor_check()
            status=True 
            statmsg='BP Ready...Connected to '+bp_port
        else:
            status=False
            statmsg='BP device Failed Initialization....No BP device connected'
            
        #self.timer2.Stop()
        self.status=self.status+'\n'+statmsg
        self.stat_txt.SetValue(self.status)
        self.update_result(status)

    def test_cam(self):
        self.statlabel.SetLabel('Testing Webcam device.....')
        self.bmppanel=self.test_method[self.key][0]
        self.guipic=self.test_method[self.key]
        
        ready=self._panel['snapshot'].device_check()
        if ready==True:
            status=True
            statmsg='Webcam Ready.....'
        else:
            statmsg='Webcam device not found.....'
            status=False
        
        statmsg='CAM Ready'
        self.status=self.status+'\n'+statmsg
        self.stat_txt.SetValue(self.status)
        self.update_result(status)

    def test_dicom(self):
        #self.timer2.Start(500)
        self.statlabel.SetLabel('Checking DICOM template.....')
        self.bmppanel=self.test_method[self.key][0]
        self.guipic=self.test_method[self.key]
        file_path=os.getcwd()+'/DICOM/dcmtemplate.dcm'
        if os.path.exists(file_path):        
            status=True
            statmsg='DICOM Ready.....'
        else:
            statmsg='DICOM template not found.....'
            status=False
        self.status=self.status+'\n'+statmsg
        self.stat_txt.SetValue(self.status)
        self.update_result(status)

    def test_edf(self):
        self.statlabel.SetLabel('Testing EDF template.....')
        self.bmppanel=self.test_method[self.key][0]
        self.guipic=self.test_method[self.key]
        
        status=True
        statmsg='European Data Format Ready.....'
        self.status=self.status+'\n'+statmsg
        self.stat_txt.SetValue(self.status)        
        self.update_result(status)

    def test_net(self):
        #self.timer2.Start(500)
        self.statlabel.SetLabel('Testing Internet Connection.....')
        self.bmppanel=self.test_method[self.key][0]
        self.guipic=self.test_method[self.key]
        ready=check_internet()
        if ready:
            status=True
            statmsg='Internet Connection Establish.....'
        else:
            status=False
            statmsg='Internet Connection Unavailable.....'

        self.status=self.status+'\n'+statmsg
        self.stat_txt.SetValue(self.status)
        self.update_result(status)

    def port_priority(self,mainport,portlist):
        try:
            portlist.remove(mainport)
            portlist.insert(0,mainport)
            return portlist
        except ValueError:
            return portlist

    def onflicker(self,event):
        #print self.picstat
        if self.picstat==True:
            self.bmppanel.SetBitmap(wx.Bitmap(path+"none.png"))
            self.picstat=False
            
        else:
            self.bmppanel.SetBitmap(wx.Bitmap(path+self.guipic[1]))
            self.picstat=True

    def update_result(self,status):
        if status==True:
            self.bmppanel.SetBitmap(wx.Bitmap(path+self.guipic[3]))
        else:
            self.bmppanel.SetBitmap(wx.Bitmap(path+self.guipic[2]))
        wx.Yield()
    
    def OnExit(self,event):
        self.backstate()
    
    def backstate(self):
        self._engine.change_state('StandbyState') 
        self.Destroy()

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    rx_frame = ShowMain(None, -1, "")
    app.SetTopWindow(rx_frame)
    #rx_frame.Maximize(True)
    #rx_frame.Show()
    app.MainLoop()
