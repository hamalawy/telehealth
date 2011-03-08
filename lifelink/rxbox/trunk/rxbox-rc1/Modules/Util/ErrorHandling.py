import traceback
import wx

def ERROR(comment='', logger=False, frame=False):
    error_message = '%s\n%s'%(comment,traceback.format_exc())
    if logger: logger.error(error_message)
    if frame:
        frame.RxFrame_StatusBar.SetStatusText(comment)
        dlg = wx.MessageDialog(frame, comment, 'Error', wx.OK|wx.ICON_HAND)
        dlg.ShowModal()
        dlg.Destroy()
    return error_message
