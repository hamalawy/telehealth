"""
pylinphone - Linphonec wrapper for Python, based on Darwin Bautista's
pyMplayer module of the Ma3x Team - Computer Networks Laboratory
"""

import sys, os
from subprocess import Popen, PIPE
import thread, threading
import  wx
import  wx.lib.newevent



class Linphone(threading.Thread):
    """
    Linphonec wrapper for Python.
    Provides the basic interface for sending commands and receiving responses
    to and from Linphone, such as starting and stopping the phone, initiating
    and terminating a call, etc. 
    This module also emits proper signal to handle phone events from a WxPython
    program. Initially, the following events are available for use in a wxPython
    code: EVT_CALL_INCOMING, EVT_CALL_TERMINATED, EVT_CALL_FAILED and
    EVT_CALL_ANSWERED.
    Note that this does not implement the embedding of the video window into
    the GUI. You may have to use this hack to embed Linphone video:
    os.environ['SDL_VIDEODRIVER']='x11'
    os.environ['SDL_WINDOWID']=str(self.frame_1.video_panel.GetHandle())
    where getHandle() returns the window id of the frame where to put the video.
    """
    def __init__(self, wxFrame, args=()):
	threading.Thread.__init__(self)
	self.stopEvent = threading.Event()
        self.stopEvent.clear()
        self.set_args(args)
        self.__subprocess = None
        self.onCall = False;

	self.frame = wxFrame
	#Phone events
        self.CallIncomingEvent, self.EVT_CALL_INCOMING = wx.lib.newevent.NewEvent()
        self.CallTerminatedEvent, self.EVT_CALL_TERMINATED = wx.lib.newevent.NewEvent()
        self.CallFailedEvent, self.EVT_CALL_FAILED = wx.lib.newevent.NewEvent()
        self.CallAnsweredEvent, self.EVT_CALL_ANSWERED = wx.lib.newevent.NewEvent()

    def __del__(self):
	pass
    
    def spawn(self):
	"""
	Checks first whether the instance is already running. If not running,
	Linphonec will be started. Connection to the sip proxy server will then
	be initialized. Currently, there are no diagnostic messages outputted
	whenever there is a failed connection.
	Note: Before starting, the wx element that will receive the phone events
	should be set.
	"""
        if not self.isrunning():
            self.__subprocess = Popen(self._command, stdin=PIPE, stdout=PIPE)

    def stop(self):
	"""
	Stops the instance of Linphonec. This should be called before closing the
	application.
	"""

        if self.isrunning():
	    #In Python2.6, subprocess has terminate() and send signal function
	    #Those should be used in the future
	    cmd = 'kill -15 ' + str(self.__subprocess.pid)
	    os.system(cmd)
            return self.__subprocess.poll()
        else:
            return None

    def setFrame(self, frame):
	"""
	Sets the Wx element that will receive the phone signals such as call incoming,
	terminated, etc.
	"""
        self.frame = frame

    def execute(self, cmd):
	"""
	Sends a command to Linphonec. Ideally this should not be used unless
	the command is not yet supported by this module.
	"""
        if not isinstance(cmd, basestring):
            raise TypeError("command must be a string")
        if not cmd:
            raise ValueError("zero-length command")
        if self.isrunning():
            self.__subprocess.stdin.write("".join([cmd, '\n']))

    def isrunning(self):
	"""
	Checks if an instance of the linphonec is running.
	Returns True if running, False othewise.
	"""
        try:
            return True if self.__subprocess.poll() is None else False
        except AttributeError:
            return False

    def set_args(self, args):
	"""
	Sets additional options to the linphonec call. Refer to the linphonec
	usage to know the available options.
	"""
        # args must either be a tuple or a list
        if not isinstance(args, (list, tuple)):
            raise TypeError("args should either be a tuple or list of strings")
        if args:
            for arg in args:
                if not isinstance(arg, basestring):
                    raise TypeError("args should either be a tuple or list of\
                                     strings")
        self._command = ["linphonec", "-V"]
        self._command.extend(args)


    def call(self, extension):
	"""
	Initiates a call. To handle a failed call, EVT_CALL_FAILED event should
	be handled; to handle an answered call, EVT_CALL_ANSWERED event should
	be handled; to handle a terminated call, EVT_CALL_TERMINATED event should
	be handled.
	The only parameter is the extension number, in string, of the phone 
	to be called.
	"""
        self.execute('call ' + extension)
	
    def answer(self):
	"""
	Answers an incoming call. To handle an incoming call, EVT_CALL_INCOMING
	should be handled; to handle a terminated call, EVT_CALL_TERMINATED event should
	be handled.
	"""
        self.execute('answer')

    def terminateCall(self):
	"""
	Terminates a call. To handle a terminated call, EVT_CALL_ANSWERED event should
	be handled.
	"""
        self.execute('terminate')

    def isOnCall(self):
        """
	Checks whether a call is going.
	Returns True if a call is on going, and False otherwise.
	"""
        return self.onCall

    def run(self):
        while self.isrunning():
            line = self.__subprocess.stdout.readline() 
            print line
            if (line.find("Service Unavailable") != -1 or  line.find("Could not reach destination.") != -1):
                evt = self.CallFailedEvent()
                wx.PostEvent(self.frame, evt)
                self.onCall = True
            elif (line.find("Call terminated.") != -1 or line.find("Call ended") != -1):
                evt = self.CallTerminatedEvent()
                wx.PostEvent(self.frame, evt)
                self.onCall = False
            elif (line.find("Connected") != -1):
                evt = self.CallAnsweredEvent(attr1="hello", attr2=654)
                wx.PostEvent(self.frame, evt)
                self.onCall = True
            #not 'incoming'
            elif (line.find("is contacting you") != -1):
		#Assumes four-digit extension
		idx = line.find("sip:")
		     
                evt = self.CallIncomingEvent(caller=line[idx+4:idx+8], attr2=654)
                wx.PostEvent(self.frame, evt)
            elif (line.find("No active call.") != -1):
                if (self.onCall):
                    self.onCall = False




