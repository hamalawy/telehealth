import wx
import threading
import socket

IM_SOCK_PORT       = 50015

class IMReceiveThread(threading.Thread):
    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.stopIMThr = threading.Event()
        self.stopIMThr.clear()
        self.window = window
                 
    def stop(self):
        self.stopIMThr.set()
        
    def run(self):
        print 'Starting IM\n'
        while True:
            if self.stopIMThr.isSet(): break
            if (self.window.addr != None):
                self.window.im_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.window.im_sock.bind(('', IM_SOCK_PORT))
                self.window.im_sock.listen(5)
                self.sock = self.window.im_sock
                print 'IM Socket Ready'
                break
            else: pass

        # loop waiting for connections
        # terminate with Ctrl-Break on Win32, Ctrl-C on Unix
        while True:
            if self.stopIMThr.isSet(): break
            if (self.sock != None):
                print 'Waiting again...'
                newSocket, address = self.sock.accept( )
                self.window.newsock = newSocket
                self.window.statusbar.SetStatusText("Connected to RxBox " + address[0])
                print "IM Socket: Connected to RxBox ", address
                self.window.reply_button.Enable(True)
                break

        while True:
            if self.stopIMThr.isSet(): break
            response = newSocket.recv(8192)
            if response:
                print 'Received:',response
                self.text = self.Text_Wrap(response)
                self.window.text_list.append('Rx: ' + self.text + '\n')
                self.window.text_count += 1
                self.SetIMText()
                wx.CallAfter(self.window.UpdateIMRcvText)

            if not response: break

    def Text_Wrap(self, string):
        count = 1
        width = 45                  #the width of your matrix
        final=""                   #output string
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
