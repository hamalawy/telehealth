import sys
sys.path.append('../')

import wx
from wx import xrc

import messenger
import ConfigParser

class ImApp(wx.App):

    def OnInit(self):
        self.res = xrc.XmlResource('resources/im.xrc')
        self.init_frame()
        return True

    def init_frame(self):
        # Get the gui objects from xrc
        self.im_frame = self.res.LoadFrame(None, 'frame_im')
        self.conv_text = xrc.XRCCTRL(self.im_frame, 'text_ctrl_conv')
	self.msg_text = xrc.XRCCTRL(self.im_frame, 'text_ctrl_mesg')

	self.im_frame.Bind(wx.EVT_CLOSE, self.OnClose)
	self.im_frame.Bind(wx.EVT_TEXT_ENTER, self.send_message, self.msg_text)

        # Show frame first before initializing the phone
        self.im_frame.Show()

	self.init_config('im.cfg')
	self.init_im()

    def init_config(self, configfile):
	self.config = ConfigParser.SafeConfigParser()
	self.config.read(configfile)

	self.jid = self.config.get('im', 'jid')
	self.passwd = self.config.get('im', 'passwd')
	

    def init_im(self):
	self.m = messenger.Messenger(self.jid, self.passwd)

	self.m.handler_new_message = self.OnMsgRcvd
	self.m.handler_sent_message = self.OnMsgSent
	self.m.set_recipient('de1@triage.telehealth.ph')

	self.m.connect()
	self.m.start()

    def send_message(self, event):
	msg = self.msg_text.GetValue()
	self.m.send_message(msg)
	

    def OnClose(self, event):
        self.m.stop()

        self.m.join()

        self.im_frame.Destroy()

    def OnMsgRcvd(self, conn, msg):
        self.conv_text.AppendText('DE1: ' + msg.getBody() + '\n')

    def OnMsgSent(self, msg):
	self.conv_text.AppendText('RXBOX: ' + msg + '\n')
	self.msg_text.Clear()



if __name__ == '__main__':
    app = ImApp(False)
    app.MainLoop()

