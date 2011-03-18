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

import commands

wildcard = "Jpeg (*.jpg)|*.jpg|"        \
           "Bitmap (*.bmp)|*.bmp|"        \
           "All files (*.*)|*.*"
           
class Snapshot (Module, SnapshotPanel):
    def __init__(self, *args, **kwds):
        Module.__init__(self, *args, **kwds)
        SnapshotPanel.__init__(self, *args, **kwds)
        
        self.list = wx.ImageList(100,70, True)
        self.image_list.AssignImageList(self.list, wx.IMAGE_LIST_NORMAL)
        self.image_listW = False

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
        self.list.Add(img)
        end = self.list.GetImageCount()-1
        self.image_list.InsertImageItem(end,end)
        self.image_listW.InsertImageItem(end,end)
        self.image_list.EnsureVisible(end)
        self.image_listW.EnsureVisible(end)

    def remove_image(self, index):
        self.pics.pop(index)
        self.image_list.DeleteItem(index)
        self.image_listW.DeleteItem(index)
        self.list.Remove(index)
        for i in xrange(self.list.GetImageCount()):
            self.image_list.SetItemImage(i,i)
            self.image_listW.SetItemImage(i,i)
    
    def device_check(self):
        output=str(commands.getoutput('ls /dev/video*'))
        if output[1:4]=='dev':
            self._logger.info('Webcam Ready')
            return True
        else:
            self._logger.info('Webcam Not Connected')
            return None

    def onSnapshot(self, event): # wxGlade: SnapshotPanel.<event_handler>        
        output=str(commands.getoutput('ls /dev/video*'))
        if output[1:4]!='dev':
            dlg = wx.MessageDialog(self, 'Connect Webcam to the USB Port-->> ', 'Error', wx.OK|wx.ICON_HAND)
            dlg.ShowModal()
            dlg.Destroy()
            return
        
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
        while True:
            itemIndex = self.image_list.GetNextItem(-1,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            if itemIndex == -1: break
            else:
                os.system('rm "%s"'%self.pics[itemIndex])
                self._logger.info("Deleted: %s"%self.pics[itemIndex])
                self.remove_image(itemIndex)
                count = 0
                
    def OnRemove(self, event): # wxGlade: SnapshotPanel.<event_handler>
        itemIndex = -1
        while True:
            itemIndex = self.image_list.GetNextItem(-1,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            if itemIndex == -1: break
            else:
                self._logger.info("Removed: %s"%self.pics[itemIndex])
                self.remove_image(itemIndex)

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
        self._panel['snapshot'].image_listW = self.image_list
        self.image_list.AssignImageList(self._panel['snapshot'].list, wx.IMAGE_LIST_NORMAL)
        self.video_device = self._config.get('webcam','port')
        self.webcam = WebcamControl(self, self.video_device[-1])
        self.ds=dicom_rxbox.RDicom()
        self.dicom_filelist=[]    
        self.patientpanel = self._panel['patientinfo']
        self.dicom_filename = ''
        
        self.load_image = self._panel['snapshot'].load_image
        self.remove_image = self._panel['snapshot'].remove_image

    def __name__(self):
        return 'Snapshot'
        
    def Start(self):
        self.webcam.close_phone()
        self.webcam.init_phone()
        self._logger.info('Start')
       
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
        self.process_config(tnow)
        os.system("python Modules/Snapshot/camera.py")
        self.load_image("Pictures/%s.jpg"%(tnow))
        self.dicom_filelist.append("Pictures/%s.jpg"%(tnow))
        self._logger.info('Picture %s taken'%tnow)
        self.webcam.init_phone()

    def OnDelete(self, event): # wxGlade: SnapshotPanel.<event_handler>
        itemIndex = -1
        while True:
            itemIndex = self.image_list.GetNextItem(-1,
                                         wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
            if itemIndex == -1: break
            else:
                os.system('rm "%s"'%self.pics[itemIndex])
                self._logger.info("Deleted: %s"%self.pics[itemIndex])
                self.remove_image(itemIndex)
                count = 0

    def process_config(self, tnow):
        filename = tnow + '.jpg'
        pathname = '%s/Modules/Snapshot/webcam.cfg'%os.getcwd()
        config = ConfigParser.ConfigParser()
        config.read(pathname)
        config.set('ftp', 'file', filename)
        config.set('ftp', 'dir', '%s/Pictures'%os.getcwd())
        print filename
        print config.get('ftp', 'file')
        
        with open(pathname, 'wb') as configfile:
            config.write(configfile)   

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
            self.dicom_filename = "DICOM/%s.dcm"%(tnow)
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
