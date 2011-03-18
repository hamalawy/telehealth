import logging
import traceback
import wx
import subprocess
import urllib2

def ERROR(comment='', logger=False, frame=False):
    error_message = '%s\n%s'%(comment,traceback.format_exc())
    if logger: logger.error(error_message)
    if frame:
        frame.RxFrame_StatusBar.SetStatusText(comment)
        dlg = wx.MessageDialog(frame, error_message, 'Error', wx.OK|wx.ICON_HAND)
        dlg.ShowModal()
        dlg.Destroy()
    return error_message

def TERMINAL(command='', logger=False):
    comm = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    if logger: logger.debug(comm.stdout.read())

def check_internet():
    try:
        con = urllib2.urlopen("http://www.google.com/")
        data = con.read()
        if data:
            return True
    except:
        return False  
