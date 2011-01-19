import subprocess
import os
import wx
from datetime import datetime
import ConfigParser

from SnapshotPanel import *
from SnapshotPanel2 import *
from camera_control import WebcamControl
import dicom_rxbox

from Modules.Module import *

wildcard = "Jpeg (*.jpg)|*.jpg|"        \
           "Bitmap (*.bmp)|*.bmp|"        \
           "All files (*.*)|*.*"
           
class Snapshot (Module, SnapshotPanel):
    def __init__(self, *args, **kwds):
        Module.__init__(self, *args, **kwds)
        SnapshotPanel.__init__(self, *args, **kwds)
        
        self.list = wx.ImageList(100,70, True)
        self.image_list.AssignImageList(self.list, wx.IMAGE_LIST_NORMAL)
        self.list2 = False
        self.image_list2 = False

        self.pics = []
        """
        modules = subprocess.Popen("ls Pictures/",shell=True,stdout=subprocess.PIPE).stdout.read().strip().split('\n')        
        for i in modules:
            self.load_image('Pictures/%s'%i)
        """
        
    def __name__(self):
        return 'SnapshotControl'
        
    def load_image(self, name):
        img = wx.Bitmap(name, wx.BITMAP_TYPE_ANY)
        size = img.GetSize() 
        image = wx.ImageFromBitmap(img)
        image = image.Rescale(size[0]*70/size[1], 70, wx.IMAGE_QUALITY_HIGH)
        img = wx.BitmapFromImage(image)
        
        self.pics.append(name)
        il_max = self.list.Add(img)
        il_max2 = self.list2.Add(img)
        self.image_list.InsertImageStringItem(0,'', len(self.pics)-1)
        self.image_list2.InsertImageStringItem(0,'', len(self.pics)-1)

    def remove_image(self, index=0):
        self.list.Remove(index)
        self.list2.Remove(index)
        self.image_list.DeleteItem(index)
        self.image_list2.DeleteItem(index)
        self.pics.pop(index)

    def onSnapshot(self, event): # wxGlade: SnapshotPanel.<event_handler>
        self._frame._mgr.GetPane("snapshot2").Float().Show()
        self._frame._mgr.Update()
        wx.Yield()
        self._panel['snapshot2'].Start()

    def OnLoad(self, event): # wxGlade: SnapshotPanel.<event_handler>
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir="%s/Pictures"%os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE
            )

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for i in paths:
                if i not in self.pics:
                    self.load_image(i)
        dlg.Destroy()

    def OnDelete(self, event): # wxGlade: SnapshotPanel.<event_handler>
        itemIndex = -1
        count = 0
        while True:
            itemIndex = self.image_list.GetNextItem(itemIndex,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            if itemIndex == -1:
                count += 1
                if count == 2:
                    break
            else:
                print "Deleted: %s"%self.pics[itemIndex]
                os.system('rm "%s"'%self.pics[itemIndex])
                self.remove_image(itemIndex)
                count = 0
                
    def OnRemove(self, event): # wxGlade: SnapshotPanel.<event_handler>
        itemIndex = -1
        count = 0
        while True:
            itemIndex = self.image_list.GetNextItem(itemIndex,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            if itemIndex == -1:
                count += 1
                if count == 2:
                    break
            else:
                print "Removed: %s"%self.pics[itemIndex]
                self.remove_image(itemIndex)
                count = 0

    def OnRemoveAll(self, event): # wxGlade: SnapshotPanel.<event_handler>
        for i in xrange(len(self.pics)):
            self.remove_image(0)
        
    def setGui(self, mode='unlock'):
        """
        This locks or unlocks the gui elements.
        String is used as an indicator to be more readable.
        Boolean may also be used but who knows, there might be the need of another mode other than lock and unlock.
        """
        if mode not in ['unlock', 'lock']:
            self._logger.info('setGui mode unsupported')
            return

        self.snapshot.Enable(mode=='unlock')
            
class SnapshotWindow(Module, SnapshotPanel2):
    def __init__(self, *args, **kwds):
        Module.__init__(self, *args, **kwds)
        SnapshotPanel2.__init__(self, *args, **kwds)
        
        self.pics = self._panel['snapshot'].pics
        self.list = wx.ImageList(100,70, True)
        self.image_list.AssignImageList(self.list, wx.IMAGE_LIST_NORMAL)
        self._panel['snapshot'].list2 = self.list
        self._panel['snapshot'].image_list2 = self.image_list
        self.list2 = self._panel['snapshot'].list
        self.image_list2 = self._panel['snapshot'].image_list
        self.video_device = '/dev/video0'
        self.webcam = WebcamControl(self, self.video_device[-1])
        self.ds=dicom_rxbox.RDicom()
        self.dicom_filelist=[]    
        self.patientpanel = self._panel['patientinfo']   
        

    def __name__(self):
        return 'Snapshot'
        
    def Start(self):
        self.webcam.close_phone()
        self.webcam.init_phone()
        self._logger.info('Start')
        
    def load_image(self, name):
        img = wx.Bitmap(name, wx.BITMAP_TYPE_ANY)
        size = img.GetSize() 
        image = wx.ImageFromBitmap(img)
        image = image.Rescale(size[0]*70/size[1], 70, wx.IMAGE_QUALITY_HIGH)
        img = wx.BitmapFromImage(image)
        
        self.pics.append(name)
        il_max = self.list.Add(img)
        il_max2 = self.list2.Add(img)
        self.image_list.InsertImageStringItem(0,'', len(self.pics)-1)
        self.image_list2.InsertImageStringItem(0,'', len(self.pics)-1)

    def remove_image(self, index=0):
        self.list.Remove(index)
        self.list2.Remove(index)
        self.image_list.DeleteItem(index)
        self.image_list2.DeleteItem(index)
        self.pics.pop(index)
       
    def OnSnapshot(self, event): # wxGlade: SnapshotPanel2.<event_handler>
        """Main function for taking images
            - Closes linphone to access device
            - Takes image using v4lctl module
            - Converts jpeg file to bitmap
            - Displays bmp to wx panel
        """ 
        self.webcam.close_phone()
        tnow = datetime.now()
        tnow = tnow.strftime("%Y_%m_%d_%H_%M_%S")+("_%s"%tnow.microsecond.__str__().replace('.',''))
        print tnow
        self.process_config(tnow)
        os.system("python Modules/Snapshot/camera.py")
        self.load_image("Pictures/%s.jpg"%(tnow))
        self.dicom_filelist.append("Pictures/%s.jpg"%(tnow))
        self._logger.info('Picture %s taken'%tnow)
        self.webcam.init_phone()

    def process_config(self, tnow):
        
        filename = tnow + '.jpg'
        pathname = '%s/Modules/Snapshot/webcam.cfg'%os.getcwd()
        print pathname
        config = ConfigParser.ConfigParser()
        config.read(pathname)
        config.set('ftp', 'file', filename)
        config.set('ftp', 'dir', '%s/Pictures'%os.getcwd())
        print filename
        print config.get('ftp', 'file')
        
        with open(pathname, 'wb') as configfile:
            config.write(configfile)   

    def OnDelete(self, event): # wxGlade: SnapshotPanel2.<event_handler>
        itemIndex = 0
        count = 0
        while True:
            itemIndex = self.image_list.GetNextItem(itemIndex,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            print itemIndex
            if itemIndex == -1:
                count += 1
                if count == 2:
                    break
            else:
                print "Deleted: %s"%self.pics[itemIndex]
                os.system('rm "%s"'%self.pics[itemIndex])
                self.remove_image(itemIndex)
                count = 0

    def generate_dicom(self,files):
        self._logger.info('DICOM Generate')
        if self.ds.test_dicom():
            self._logger.info('DICOM Test Passed!!!')
            for x in files:
                self.ds.add_picture(x)
            tnow = datetime.now()
            tnow = tnow.strftime("%Y_%m_%d_%H_%M_%S")+("_%s"%tnow.microsecond.__str__().replace('.',''))
            #bday = '.'.join([str(self.patientpanel.BirthMonth.GetSelection() + 1), str(self.patientpanel.BirthDayCombo.GetSelection() + 1),) 
            bday=str(self. patientpanel.BirthYear.GetValue())+str(self.patientpanel.BirthMonth.GetSelection() + 1).zfill(2)+str(self.patientpanel.BirthDayCombo.GetSelection() + 1).zfill(2)
            print bday
            self.ds.save_picture("DICOM/%s.dcm"%(tnow),str(self.patientpanel.LastNameValue.GetValue()),str(self.patientpanel.FirstNameValue.GetValue()),\
                                str(self.patientpanel.MiddleNameValue.GetValue()),bday,str(self.patientpanel.GenderCombo.GetValue()),\
                                str(self.patientpanel.AddressValue.GetValue()))
        
    def OnPaneClose(self):
        """Main function for closing the program
            - Closes Linphone
            - Destroys current frame
        """
        if self.dicom_filelist!=[]:
            self.generate_dicom(self.dicom_filelist)

        self.webcam.close_phone()
        self._logger.info('Stop')
