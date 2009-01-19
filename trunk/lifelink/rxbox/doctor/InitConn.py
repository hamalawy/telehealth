import wx
import threading
#import serial
import socket
import time


RQT_MSSG        = 'TELEMED'
PKY_MSSG        = '1234'
WEL_MSSG        = RQT_MSSG + ' ' + PKY_MSSG

VFY_MSSG        = 'READY TO RECEIVE'
REF_MSSG        = 'CONNECTION REFUSED'
FIN_MSSG        = 'FINISHED TRANSMISSION'

DATA_TIMEOUT 	= 10
BUFSIZ 		= 1024
IM_SOCK_PORT = 50015

class InitConnThread(threading.Thread):
    def __init__(self, threadNum, window):      
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.stopInitConnThr = threading.Event()
        self.stopInitConnThr.clear()
        
        self.window = window
        self.welcome = WEL_MSSG
        self.verify = VFY_MSSG
        self.refuse = REF_MSSG
        self.finished = FIN_MSSG
        
    def stop(self):
        self.stopInitConnThr.set()
       
    def run(self):
        try:
            self.window.data_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.window.data_sock.bind(('',int(self.window.user_config['ip_port'])))
            print 'Waiting for RxBox...'
        except socket.error:
            wx.CallAfter(self.window.raiseMessage, " \nUnable to listen to port " + port_str + ".\nTry changing IP port.")

        self.window.data_sock.setblocking(0)

        while True:
            if self.stopInitConnThr.isSet(): break
            try:
                input, self.addr = self.window.data_sock.recvfrom(BUFSIZ)
                print 'InitConn input:', input
                if (input == self.welcome):
                    self.window.data_sock.sendto(self.verify, self.addr)
                    self.window.user_config['ip_host'] = self.addr[0]
                    self.window.addr = self.addr
                    self.window.start_button.Enable(True)
                    wx.CallAfter(self.window.raiseStatus, 'Connected to RxBox ' + self.addr[0])
                    print 'Data Socket: Connected to RxBox ', self.addr
                    break
                else:
                    self.window.data_sock.sendto(self.refuse, self.addr)
            # nothing is read from socket
            except:
                pass
        
