import wx
import threading
import socket
import time

IM_SOCK_PORT   = 50015
BUFSIZ      = 1024

class IMSendThread(threading.Thread):
    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.stopIMThr = threading.Event()
        self.stopIMThr.clear()
        self.window = window
                             
    def stop(self):
        self.stopIMThr.set()
        
    def run(self):
        self.window.im_sock.sendall(self.window.data)
        print "Sent:", self.window.data
        self.text = self.Text_Wrap(self.window.data)
        self.window.text_list.append('Rx: ' + self.text + '\n')
        self.window.text_count += 1
        self.SetIMText()
        wx.CallAfter(self.window.UpdateIMText)

    def Text_Wrap(self, string):
        count = 1
        width = 45                  
        final=""                   
        for character in string:
            if count == width :
                final = "%s%s\n    " % (final,character)
                count = 1
            else:
                final = "%s%s" % (final,character)
                count += 1
        return final

    def SetIMText(self):
        self.window.text = ''
        if (self.window.text_count >= 10):
            self.window.text_list.remove(self.window.text_list[0])
        for item in self.window.text_list:
            self.window.text = self.window.text + item


