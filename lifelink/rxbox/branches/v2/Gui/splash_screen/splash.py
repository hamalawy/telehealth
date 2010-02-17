#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2010 Tim Ebido <tim@jachin-desktop>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from multiprocessing import Process
import time

import wx
from wx import xrc

class SplashApp(wx.App):

    def OnInit(self):
        """Instantiates the xml file"""
        self.res = xrc.XmlResource('splash.xrc')
        self.init_frame()
        return True
        
    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'frame_1')
        
        self.gauge = xrc.XRCCTRL(self.frame, 'gauge')
        
        self.frame.Bind(wx.EVT_BUTTON, self.on_close, id=xrc.XRCID('Skip'))
        
        self.init_loadingbar()
        self.frame.Show()
        
    def init_loadingbar(self):
        self.bar = wx.Gauge(self.gauge, -1, 100, size=(525,30), style=wx.GA_HORIZONTAL)
        self.bar_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.inc_bar, self.bar_timer)
        self.value = 0
        self.bar_timer.Start(50)
        
    def inc_bar(self, event):
        
        if (self.value != 100):
            self.bar.SetValue(self.value)
            self.value += 1
            
        else:
            self.bar_timer.Stop()
            
    def on_close(self, event):
        self.frame.Destroy()

if __name__ == '__main__':
    app = SplashApp(False)
    app.MainLoop()
