
from edf_gui_base import MyFrame
import wx
import os
import edfviewer
from edf_plotter import Plotter
import wx.lib.plot as plot

class EDFmain(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self, *args, **kwds)
        self.SetTitle("Local EDF Browser")
        self.bo = plot.PlotCanvas(self.bloodox_panel)
        self.hr = plot.PlotCanvas(self.heartrate_panel)
        self.sys = plot.PlotCanvas(self.systolic_panel)
        self.dias = plot.PlotCanvas(self.diastolic_panel)
        self.ecg = plot.PlotCanvas(self.ecg_panel)
        self.ecg.SetXSpec(type='none')
        self.ecg.SetYSpec(type='none')
        self.photo_list=['no_photo.bmp','no_photo2.bmp']
        self.photo_num=1
#        self.plotter_bo = Plotter(self, (700, 100))
#        self.plotter_hr = Plotter(self, (726, 119))
#        self.plotter_sys = Plotter(self, (726, 119))
#        self.plotter_dias = Plotter(self, (700, 100))
#        self.plotter_ecg = Plotter(self, (726, 119))

       # self.heartrate_sizer.Add(self.plotter_hr.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        #self.systolic_sizer.Add(self.plotter_sys.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
     #   self.diastolic_sizer.Add(self.plotter_dias.plotpanel, 0,wx.EXPAND | wx.ALL, 20)
        #self.ecg_sizer.Add(self.plotter_ecg.plotpanel, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 4)
        
        
    def parse_edf(self):
        self.edf_inst=edfviewer.EDF_File(self.path)
        self.data=self.edf_inst.parseDataRecords()
        patient_info=self.edf_inst.LocalPatientID
        self.patientid=patient_info[:5].rstrip()
        self.firstname=patient_info[5:25].rstrip()
        self.middlename=patient_info[25:37].rstrip()
        self.lastname=patient_info[37:49].rstrip()
        self.sex=patient_info[61:67].rstrip()
        self.age=patient_info[77:79].rstrip()
        self.birthdate=patient_info[67:75].rstrip()
        self.date=self.edf_inst.StartDate 
        self.time=self.edf_inst.StartTime[0:5].replace('.',':')
        self.bpsysnum,self.bpdiasnum,self.ecgnum,self.bonum,self.hrnum=99,99,99,99,99
        for i in range(len(self.edf_inst.BioSignals)):
            label=self.edf_inst.BioSignals[i].TechInfolist[0]
            if label.rstrip() == "bpsystole":
                self.bpsysnum=i
            if label.rstrip() == "bpdiastole":
                self.bpdiasnum=i
            if label.rstrip() == "II":
                self.ecgnum=i   
            if label.rstrip() == "SpO2 finger":
                unit=self.edf_inst.BioSignals[i].TechInfolist[2]
                if unit.rstrip()== "%":
                    self.bonum=i
                elif unit.rstrip()=="bpm":
                    self.hrnum=i
        self.update_Screen_info()
            

    def onFileopen(self, event): # wxGlade: MyFrame.<event_handler>
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.edf*", wx.OPEN)
        dlg.SetDirectory(os.getenv('HOME')+'/.Rxbox/EDF')
        if dlg.ShowModal() == wx.ID_OK:
            self.path = dlg.GetPath() 
            self.parse_edf()
        dlg.Destroy()   
        
    def update_Screen_info(self):
        self.patientid_text.SetLabel(self.patientid)
        self.firstname_text.SetLabel(self.firstname)
        self.middlename_text.SetLabel(self.middlename)
        self.lastname_text.SetLabel(self.lastname)
        self.age_text.SetLabel(self.age)
        self.sex_text.SetLabel(self.sex)
        self.birthdate_text.SetLabel(self.birthdate.replace('.','/') + ' ' + 'mm/dd/yy')
        self.date_text.SetLabel(self.date[3:5]+'/'+self.date[0:2]+'/'+self.date[6:]+' ' + 'mm/dd/yy')
        self.time_text.SetLabel(self.time+' ' + 'hh/min')
        self.update_plot()
    
    def update_plot(self):
        
        self.bo.Clear()
        self.hr.Clear()
        self.sys.Clear()
        self.dias.Clear()
        self.ecg.Clear()
        
        #for blood oxygen plot, bo==blood oxygen
        if self.bonum != 99:
            y=self.data[self.bonum]
            x=range(1,len(self.data[self.bonum])+1)
            self.bo.SetInitialSize(size=(740,135))
            bo_line = plot.PolyLine(zip(x,y), colour='red', width=1)
            bo_gc = plot.PlotGraphics([bo_line])
            self.bo.Draw(bo_gc,xAxis= (1,len(self.data[self.bonum])), yAxis= (min(self.data[self.bonum])-2,max(self.data[self.bonum])+2))
        
        #for heart rate plot
        if self.hrnum != 99:
            y=self.data[self.hrnum]
            x=range(1,len(self.data[self.hrnum])+1)
            self.hr.SetInitialSize(size=(740,135))
            hr_line = plot.PolyLine(zip(x,y), colour='red', width=1)
            hr_gc = plot.PlotGraphics([hr_line])
            self.hr.Draw(hr_gc,xAxis= (1,len(self.data[self.hrnum])), yAxis= (min(self.data[self.hrnum])-2,max(self.data[self.hrnum])+2))
        
        #for systolic plot
        if self.bpsysnum != 99:
            y=self.data[self.bpsysnum]
            x=range(1,len(self.data[self.bpsysnum])+1)
            self.sys.SetInitialSize(size=(740,135))
            sys_line = plot.PolyLine(zip(x,y), colour='red', width=1)
            sys_gc = plot.PlotGraphics([sys_line])
            self.sys.Draw(sys_gc,xAxis= (1,len(self.data[self.bpsysnum])), yAxis= (min(self.data[self.bpsysnum])-2,max(self.data[self.bpsysnum])+2))
        
        #for diastolic plot
        if self.bpdiasnum !=99:
            y=self.data[self.bpdiasnum]
            x=range(1,len(self.data[self.bpdiasnum])+1)
            self.dias.SetInitialSize(size=(740,135))
            dias_line = plot.PolyLine(zip(x,y), colour='red', width=1)
            dias_gc = plot.PlotGraphics([dias_line])
            self.dias.Draw(dias_gc,xAxis= (1,len(self.data[self.bpdiasnum])), yAxis= (min(self.data[self.bpdiasnum])-2,max(self.data[self.bpdiasnum])+2))
        
        #for ecg plot
        if self.ecgnum != 99:
            y=self.data[self.ecgnum]
            x=range(1,len(self.data[self.ecgnum])+1)
            self.ecg.SetInitialSize(size=(740,135))
            ecg_line = plot.PolyLine(zip(x,y), colour='red', width=1)
            ecg_gc = plot.PlotGraphics([ecg_line])
            self.ecg.Draw(ecg_gc,xAxis=(1,len(self.data[self.ecgnum])),yAxis= (min(self.data[self.ecgnum])-2,max(self.data[self.ecgnum])+2))
        
    def onPicprevious(self, event): # wxGlade: MyFrame.<event_handler>
        self.bitmap_1.SetBitmap(wx.Bitmap('no_photo.bmp'))

    def onPicnext(self, event): # wxGlade: MyFrame.<event_handler>
        self.bitmap_1.SetBitmap(wx.Bitmap('no_photo2.bmp'))
                    
class Loading_screen(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(300, 125))
        self.SetTitle("Processing")
        self.timer = wx.Timer(self, 1)
        self.count = 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.gauge = wx.Gauge(panel, -1, 50, size=(250, 25))
        self.text = wx.StaticText(panel, -1, 'Loading EDF.....')

        hbox1.Add(self.gauge, 1, wx.ALIGN_CENTRE)
        hbox3.Add(self.text, 1)
        vbox.Add((0, 30), 0)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 30), 0)
        vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)
        panel.SetSizer(vbox)
        self.Centre()

    def OnOk(self):
        self.timer.Start(100)

    def OnTimer(self, event):
        self.count = self.count +1
        self.gauge.SetValue(self.count)
        if self.count == 50:
            self.timer.Stop()
            self.Close()
    

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    edf_frame = EDFmain(None, -1, "")
    app.SetTopWindow(edf_frame)
    #rx_frame.Maximize(True)
    edf_frame.Show()
    app.MainLoop()
