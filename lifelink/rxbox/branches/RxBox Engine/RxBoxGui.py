#!/bin/env python

"""
Demo program for RxBox architecture

The contents of a file are displayed one character per second.
To run, enter the filename of the file to be read in the top text 
input then press the Run button. To stop, press the Run button again.
To exit, press the exit button or close the window.
"""

import time
import threading
import wx
from wx import xrc

import ECG

class MainState:
	"""State with file init and read"""
	def __init__(self, engine):
		self._engine = engine
		self._app = self._engine.app
		self._acquiring = False
		self.port = '/dev/ttyUSB0'
		self.daqdur = 3
		self._reader = ECG.ECG(port=self.port,daqdur=self.daqdur) 
		self._acquire_thread = None

	def start(self):
		"""Start state"""
		self._app.frame = self._app.res.LoadFrame(None, 'main_frame')
		self.fname_input = xrc.XRCCTRL(self._app.frame, 'filename')
		self.output = xrc.XRCCTRL(self._app.frame, 'output')
		self.run_btn = xrc.XRCCTRL(self._app.frame, 'run_btn')
		self._app.Bind(wx.EVT_TOGGLEBUTTON, self.OnRun, id=xrc.XRCID('run_btn'))
		self._app.Bind(wx.EVT_BUTTON, self.OnExit, id=xrc.XRCID('exit_btn'))
		self._app.frame.Show()

	def start_acquire(self):
		"""Start ECG data acquisition"""
		self._reader = ECG.ECG(port=self.port,daqdur=self.daqdur)
		if self._reader.serialstatus:
			self._reader.Init_ECG()
			self._acquiring = True
			self._acquire_thread = threading.Thread(target=self.acquire)
			self._acquire_thread.start()
	
	def acquire(self, wait=0.1):
		"""Run acquire loop, sleeping wait seconds per iteration"""
		while self._acquiring:
			self._reader.get_ecg()
			self._reader.ecg_lead()
			wx.CallAfter(self.output.SetValue, str(self._reader.ecg_leadII))
			self._reader.Pop(end=len(self._reader.ecg_leadII))
			time.sleep(wait)
		self._reader.stop()

	def stop_acquire(self):
		"""Stop ECG data acquisition"""
		if self._acquiring:
			self._acquiring = False
			self._acquire_thread.join()
			self._acquire_thread = None

	def stop(self):
		"""Stop state"""
		self.stop_acquire()

	def OnRun(self, event):
		"""Called when run button is pressed"""
		if self.run_btn.GetValue():
			self.start_acquire()
		else:
			self.stop_acquire()

	def OnExit(self, event):
		"""Called when exit button is pressed"""
		self._engine.change_state(None)

class DemoEngine:
	"""Engine/controller class for demo"""
	def run(self):
		"""Run engine (and program)"""
		self.app = DemoApp(False)
		self.state = MainState(self)
		self.change_state(self.state)
		self.app.MainLoop()

	def change_state(self, state):
		"""Change state to state"""
		if self.state is not None:
			self.state.stop()
		self.state = state
		if self.state is None:
			self.app.Exit()
		else:
			self.state.start()

class DemoApp(wx.App):
	"""wxPython app for demo"""
	def __init__(self, *args, **kwargs):
		wx.App.__init__(self, *args, **kwargs)
		self.res = xrc.XmlResource('demo.xrc')
		self.engine = None

if __name__ == "__main__":
	engine = DemoEngine()
	engine.run()
