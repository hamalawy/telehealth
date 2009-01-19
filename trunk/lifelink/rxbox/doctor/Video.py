import wx
import threading
import os

VLC_DIR = "/usr/bin"

class VideoconfServThr(threading.Thread):
    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.stopVideoconfServThr = threading.Event()
        self.stopVideoconfServThr.clear()
        
        self.window = window
        self.user_config = self.window.user_config
        
        self.host = self.user_config['ip_host']
        self.port = self.user_config['video_ip_port']
        
        self.vlc_run = './vlc v4l:// :v4l-vdev="/dev/video0" :v4l-adev="/dev/dsp" :v4l-channel=1 :v4l-norm=pal :v4l-size=320x240 --sout \'#duplicate{dst="transcode{vcodec=DIV3,acodec=mpga,vb=96,ab=16,deinterlace}:standard{access=udp,mux=ts,dst=' + self.host + ':' + self.port + '}"}\''
        
    def stop(self):
        self.stopVideoconfServThr.set()
        
    def run(self):
        os.chdir(VLC_DIR)
        os.system(self.vlc_run)
        
        self.window.video_count -= 1
        wx.CallAfter(self.window.onClickStopVideo)


class VideoconfClientThr(threading.Thread):
    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.stopVideoconfClientThr = threading.Event()
        self.stopVideoconfClientThr.clear()
        
        self.window = window
        self.user_config = self.window.user_config
        
        self.vlc_wait = "./vlc -vvv udp:"
        
    def stop(self):
        self.stopVideoconfClientThr.set()
        
    def run(self):
        os.chdir(VLC_DIR)
        os.system(self.vlc_wait)
        
        self.window.video_count -= 1
        wx.CallAfter(self.window.onClickStopVideo)

