import subprocess
import os
import wx
from datetime import datetime

from SnapshotPanel import *
from SnapshotPanel2 import *
from camera_control import WebcamControl

wildcard = "Jpeg (*.jpg)|*.jpg|"        \
           "Bitmap (*.bmp)|*.bmp|"        \
           "All files (*.*)|*.*"
           
class Snapshot (SnapshotPanel):
    def __init__(self, *args, **kwds):
        SnapshotPanel.__init__(self, *args, **kwds)

        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        self._panel = self._frame._panel
        
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
    def load_image(self, name):
        img = wx.Bitmap(name, wx.BITMAP_TYPE_ANY)
        size = img.GetSize() 
        image = wx.ImageFromBitmap(img)
        image = image.Rescale(size[0]*70/size[1], 70, wx.IMAGE_QUALITY_HIGH)
        img = wx.BitmapFromImage(image)
        
        self.pics.append(name)
        il_max = self.list.Add(img)
        il_max2 = self.list2.Add(img)
        self.image_list.InsertImageStringItem(len(self.pics)-1,'', len(self.pics)-1)
        self.image_list2.InsertImageStringItem(len(self.pics)-1,'', len(self.pics)-1)

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
                self.image_list.DeleteItem(itemIndex)
                self.image_list2.DeleteItem(itemIndex)
                del self.pics[itemIndex]
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
                self.image_list.DeleteItem(itemIndex)
                self.image_list2.DeleteItem(itemIndex)
                del self.pics[itemIndex]
                count = 0

    def OnRemoveAll(self, event): # wxGlade: SnapshotPanel.<event_handler>
        for i in self.pics:
            self.image_list.DeleteItem(0)
            self.image_list2.DeleteItem(0)
        self.pics = []
        
    def setGui(self, mode='unlock'):
        """
        This locks or unlocks the gui elements.
        String is used as an indicator to be more readable.
        Boolean may also be used but who knows, there might be the need of another mode other than lock and unlock.
        """
        if mode not in ['unlock', 'lock']:
            print 'mode unsupported'
            return

        self.snapshot.Enable(mode=='unlock')
            
class SnapshotWindow(SnapshotPanel2):
    def __init__(self, *args, **kwds):
        SnapshotPanel2.__init__(self, *args, **kwds)
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        self._panel = self._frame._panel
        
        self.pics = self._panel['snapshot'].pics
        self.list = wx.ImageList(100,70, True)
        self.image_list.AssignImageList(self.list, wx.IMAGE_LIST_NORMAL)
        self._panel['snapshot'].list2 = self.list
        self._panel['snapshot'].image_list2 = self.image_list
        self.list2 = self._panel['snapshot'].list
        self.image_list2 = self._panel['snapshot'].image_list
        self.video_device = '/dev/video0'
        self.webcam = WebcamControl(self, self.video_device[-1])

    def Start(self):
        self.webcam.close_phone()
        self.webcam.init_phone()   
        
    def load_image(self, name):
        img = wx.Bitmap(name, wx.BITMAP_TYPE_ANY)
        size = img.GetSize() 
        image = wx.ImageFromBitmap(img)
        image = image.Rescale(size[0]*70/size[1], 70, wx.IMAGE_QUALITY_HIGH)
        img = wx.BitmapFromImage(image)
        
        self.pics.append(name)
        il_max = self.list.Add(img)
        il_max2 = self.list2.Add(img)
        self.image_list.InsertImageStringItem(len(self.pics)-1,'', len(self.pics)-1)
        self.image_list2.InsertImageStringItem(len(self.pics)-1,'', len(self.pics)-1)
        
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
        os.system("v4lctl -c %s snap jpeg 176x144 Pictures/%s.jpg"%(self.video_device,tnow))
        self.load_image("Pictures/%s.jpg"%(tnow))
        self.webcam.init_phone()

    def OnDelete(self, event): # wxGlade: SnapshotPanel2.<event_handler>
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
                self.image_list.DeleteItem(itemIndex)
                self.image_list2.DeleteItem(itemIndex)
                del self.pics[itemIndex]
                count = 0
        
    def OnPaneClose(self):
        """Main function for closing the program
            - Closes Linphone
            - Destroys current frame
        """
        self.webcam.close_phone()
