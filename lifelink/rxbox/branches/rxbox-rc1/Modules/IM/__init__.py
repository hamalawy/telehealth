import datetime

from IMPanel import *
from messenger import *
"""
This is the template module
A module is the class which combines the GUI and the DAQ

basic functions include:
    Start
    Stop
    setGui
    OnPaneClose
"""
class IM (IMPanel):
    def __init__(self, *args, **kwds):
        IMPanel.__init__(self, *args, **kwds)
        
        self._frame = args[0]
        self._engine = self._frame._engine
        self._config = self._engine._config
        
        self.rxboxDB = self._engine.rxboxDB
        self.dbuuid = self._engine.dbuuid
        self._panel = self._frame._panel
        self.status = 'stop'
        self.error = ''

        self.usrname = self._config.get('im', 'id')
        self.domain = self._config.get('im', 'domain')
        self.passwd = self._config.get('im', 'passwd')
        self.recepient = self._config.get('im', 'recepient')
        
        self.IMreply_Text.Bind(wx.EVT_TEXT_ENTER, self.sendMessage)        
        
    def Start(self):
        """
        Starts the function of the module
        Includes DAQ and GUI
        """
        self.status = 'start'
        self.m = Messenger('%s@%s'%(self.usrname,self.domain), self.passwd)
        self.m.handler_new_message = self.onMsgRcvd
        self.m.handler_sent_message = self.onMsgSent
        self.m.set_recipient('%s@%s'%(self.recepient,self.domain))

        self.m.connect()
        self.m.start()
        
    def Stop(self):
        """
        Stops the function of the module
        Includes DAQ and GUI
        """
        self.status = 'stop'
        self.m.stop()
        self.m.join()
        
    def setGui(self, mode='unlock'):
        """
        This locks or unlocks the gui elements.
        String is used as an indicator to be more readable.
        Boolean may also be used but who knows, there might be the need of another mode other than lock and unlock.
        """
        if mode not in ['unlock', 'lock']:
            print 'mode unsupported'
            return
        
    def OnPaneClose(self):
        pass
    
    def onMsgRcvd(self, conn, msg):
        """Shows message received in the IM panel"""
        time = self.get_time()
        msgrcvd = 'DE1: ' + msg.getBody()
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self._engine.dbuuid, 'IM', '', msgrcvd)
        self.IMtexts_Text.AppendText('(%s) DE1: %s\n'%(time,msg.getBody()))
       
    def onMsgSent(self, msg):
        """Shows message sent in the IM panel"""
        time = self.get_time()
        msgsent = 'RXBOX: ' + msg
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self._engine.dbuuid, 'IM', '', msgsent)
        self.IMtexts_Text.AppendText('(%s) RXBOX: %s\n'%(time,msg))
        self.IMreply_Text.Clear()
        
    def get_time(self):
        """Get current date and time"""
        time = datetime.datetime.today()
        time = time.strftime("%H:%M:%S")
        return str(time)

    def sendMessage(self, event):
        """Sends the message to a specified destination (address)"""
        msg = self.IMreply_Text.GetValue()
        self.m.set_recipient('1000@one.telehealth.ph')
        self.m.send_message(msg)
