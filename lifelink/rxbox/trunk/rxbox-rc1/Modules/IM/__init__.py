import datetime

from IMPanel import *
from messenger import *
from Modules.Module import *

"""
This is the template module
A module is the class which combines the GUI and the DAQ

basic functions include:
    Start
    Stop
    setGui
    OnPaneClose
"""
class IM (Module, IMPanel):
    def __init__(self, *args, **kwds):
        Module.__init__(self, *args, **kwds)
        IMPanel.__init__(self, *args, **kwds)

        self.usrname = self._config.get('im', 'id')
        self.domain = self._config.get('im', 'domain')
        self.passwd = self._config.get('im', 'passwd')
        self.recepient = self._config.get('im', 'recepient')
        
        self.IMreply_Text.Bind(wx.EVT_TEXT_ENTER, self.sendMessage)        
    
    def __name__(self):
        return 'IM'
        
    def Start(self):
        """
        Starts the function of the module
        Includes DAQ and GUI
        """
        self.m = Messenger('%s@%s'%(self.usrname,self.domain), self.passwd)
        self.m.handler_new_message = self.onMsgRcvd
        self.m.handler_sent_message = self.onMsgSent
        self.m.set_recipient('%s@%s'%(self.recepient,self.domain))

        self.m.connect()
        self.m.start()
        
        self._logger.info('Start')
        self.status = 'start'
        
    def Stop(self):
        """
        Stops the function of the module
        Includes DAQ and GUI
        """
        self.m.stop()
        self.m.join()
        self.status = 'stop'
        self._logger.info('Stop')
        
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
        msgrcvd = '(%s) DE1: %s\n'%(time,msg.getBody())
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self._engine.dbuuid, 'IM', '', msgrcvd)
        self.IMtexts_Text.AppendText(msgrcvd)
        self._logger.debug(msgrcvd.strip())
       
    def onMsgSent(self, msg):
        """Shows message sent in the IM panel"""
        time = self.get_time()
        msgsent = '(%s) RXBOX: %s\n'%(time,msg)
        self.rxboxDB.dbbiosignalsinsert('biosignals', 'uuid', 'type', 'filename', 'content', self._engine.dbuuid, 'IM', '', msgsent)
        self.IMtexts_Text.AppendText(msgsent)
        self._logger.debug(msgsent.strip())
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
