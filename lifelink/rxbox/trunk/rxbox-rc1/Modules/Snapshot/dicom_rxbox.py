import dicom
import scipy.misc
import Image
from scipy.misc import fromimage
import datetime

class RDicom:
    def __init__(self):
        self.Columns=320
        self.Rows=240
        
    def test_dicom(self):
        if (dicom.read_file("DICOM/dcmtemplate.dcm")):
            self.df = dicom.read_file("DICOM/dcmtemplate.dcm")
            self.df.PixelData = ''
            self.df.pixel_array = []
            self.df.NumberofFrames = 0
            self.df.Columns = self.Columns
            self.df.Rows = self.Rows
            self.df.PixelData = ''
            self.pic = []
            return True
        else:
            return False
        
    def add_picture(self, filename):
        self.df.NumberofFrames += 1
        temp=fromimage(Image.open(filename))
        self.pic.append(temp)
        self.df.pixel_array = self.pic
        self.df.PixelData =self.df.PixelData + temp.tostring()
        
    def save_picture(self,filename,lastname,firstname,middlename,birthday,sex,address):
        name=lastname.strip()+'^'+firstname.strip()+'^'+middlename.strip()
        print name
        print birthday
        sex=sex.upper()
        print sex
        print address
        self.df.AddNew((0x10,0x10),'PN',name) #add patient's name to the dicom file
        self.df.AddNew((0x10,0x40),'CS',sex)
        if address!='':
            self.df.AddNew((0x10,0x1040),'LO',address)
        if birthday!='':
            self.df.AddNew((0x10,0x30),'DA',birthday)
        now=datetime.datetime.now()
        year=str(now.year)
        month=str(now.month).zfill(2)
        day=str(now.day).zfill(2)
        self.df[0x08,0x22].value=year+month+day
        self.df.save_as(filename)
        self.test_dicom()
