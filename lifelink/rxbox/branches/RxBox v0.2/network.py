import subprocess
import datetime
from subprocess import Popen
#from subprocess import call
import os
from signal import SIGTERM
import threading
import smtplib
import socket
import wx

class ping(threading.Thread):
    def __init__(self,ip,parent):
        self.parent = parent
        threading.Thread.__init__(self)
        self.ip = ip
        self.average = 0
        self.info = ""        

    def run(self): 
        command = "ping %s"%self.ip

        #process = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.readlines()
        data = output[len(output)-1]
        end = data.find('\r')
        self.info = data[:end]
        index = self.info.find('Average =')
        print '\nTelehealth Server Status'
        if index == -1:
            self.average = 0
        else:        
            b=self.info[index+9:len(self.info)-2]
            self.average=int(b)

        if self.average == 0:
            print "%s: did not respond\n" % self.ip
            print "%s\n" % self.info
            self.parent.RxFrame_StatusBar.neticon.SetBitmap(wx.Bitmap("Icons/telehealth_down.png",wx.BITMAP_TYPE_ANY))
             
        else:
            print "%s: is alive\n" % self.ip
            print 'Approximate round trip times in milli-seconds:'
            print "%s\n" % self.info
            self.parent.RxFrame_StatusBar.neticon.SetBitmap(wx.Bitmap("Icons/telehealth_up.png",wx.BITMAP_TYPE_ANY))

        return self.average


class mailcheck(threading.Thread):
    def __init__(self,parent):
        self.parent = parent
        threading.Thread.__init__(self)
        

    def run(self):
        print '\nSMTP Gmail Server Status'
        try:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("dmcornillez@gmail.com", "simone78455")
            #server.login("dttb.rxbox@gmail.com", "telehealth")
            server.sendmail("rxbox","dmcornillez@gmail.com","rxbox test message")
            

        except smtplib.SMTPException:
            print 'Error while sending email'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPServerDisconnected:
            print 'Server unexpectedly disconnected'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPResponseException:
            print 'Server returned an error code'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPSenderRefused:
            print 'Sender address refused'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPRecipientsRefused:
            print 'All recipient addresses refused'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPDataError:
            print 'SMTP sever refused to accept the message data'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPConnectError:
            print 'Cannot connect to server'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPHeloError:
            print 'Server refused our HELO message'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        except smtplib.SMTPAuthenticationError:
            print 'SMTP Authentication Error'
            print 'Username and password did not match'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False   
        except socket.error:
            #err_log.error('Unable to connect to SMTP server...')
            #err_log.error(e)
            print 'Unable to connect to SMTP server'
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_down.png",wx.BITMAP_TYPE_ANY))
            return False
        else:
            print 'Message Sent Successfully'
            server.quit()
            self.parent.RxFrame_StatusBar.mailicon.SetBitmap(wx.Bitmap("Icons/email_up.png",wx.BITMAP_TYPE_ANY))
            return True
