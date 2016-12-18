#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

"""Module contains helper classes for button widgets"""

import wx
from wx.lib.agw.ribbon import art
import wx.lib.agw.ribbon as RB
from wx.lib import imageutils


class BitmapTextButton(wx.lib.buttons.GenBitmapButton):
    """Button for toolbars"""

    def __init__(self,parent,id=-1,bitmap=wx.NullBitmap,label='',pos=wx.DefaultPosition,size=wx.DefaultSize,style=0,
            validator=wx.DefaultValidator,name='bitmaptextbutton'):
        """Constructor"""

        self._art = RB.RibbonMSWArtProvider()
        #self._art = RB.RibbonArtProvider()
        wx.lib.buttons.GenBitmapButton.__init__(self,parent,id,bitmap,pos,size,style | wx.BU_EXACTFIT,
            validator,name)
        self.SetLabel(label)
        self.enter_state = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        image = self.bmpLabel.ConvertToImage()
        imageutils.grayOut(image)
        self.bmpLabel2 = wx.Bitmap(image)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))

    def _GetLabelSize(self):
        s = (self.bmpLabel.GetWidth(), self.bmpLabel.GetHeight())
        ret = self._art.GetButtonBarButtonSize(self,self,art.RIBBON_BUTTON_NORMAL,art.RIBBON_BUTTONBAR_BUTTON_LARGE,
            self.GetLabel(),s,s)
        size_ret = ret[1]
        return (size_ret.GetWidth(), size_ret.GetHeight() - 1, True)

    def DrawLabel(self,dc,width,height,dx=0,dy=0):
        label = self.GetLabel()
        state = art.RIBBON_BUTTONBAR_BUTTON_LARGE
        if self.IsEnabled() and self.GetParent().IsEnabled():
            if self.enter_state:
                state |= art.RIBBON_BUTTONBAR_BUTTON_NORMAL_HOVERED
                if not self.up:
                    state |= art.RIBBON_BUTTONBAR_BUTTON_NORMAL_ACTIVE
            bmp = self.bmpLabel
        else:
            state |= art.RIBBON_BUTTONBAR_BUTTON_DISABLED
            bmp = self.bmpLabel2
        self._art.DrawButtonBarButton(dc,self,wx.Rect(0, 0, width, height),art.RIBBON_BUTTON_NORMAL,
            state,label,bmp,bmp)

    def on_enter(self, event):
        if not self.enter_state:
            self.enter_state = True
            wx.CallAfter(self.Refresh)
        event.Skip()

    def on_leave(self, event):
        if self.enter_state:
            self.enter_state = False
            wx.CallAfter(self.Refresh)
        event.Skip()
