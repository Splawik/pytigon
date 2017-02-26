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

import platform
import os
import wx

_ = wx.GetTranslation


SIZE_DEFAULT = -1
SIZE_SMALL = 0
SIZE_MEDIUM = 1
SIZE_LARGE = 2

def norm_colour2(c):
    x = int(c)
    if x > 255:
        return 255
    else:
        return x

def norm_colour(r,g,b,proc):
    if proc > 1:
        y = (255, 255, 255)
        dx = 2 - proc
    else:
        y = (0, 0, 0)
        dx = proc
    dy = 1 - dx
    ret = [int(r * dx + y[0] * dy), int(g * dx + y[1] * dy), int(b * dx + y[1]
            * dy)]
    for i in range(3):
        if ret[i] > 255:
            ret[i] = 255
    return ret

def colour_to_html(colour):
    return wx.Colour(colour.Red(), colour.Green(), colour.Blue()).GetAsString(wx.C2S_HTML_SYNTAX)

def get_colour(wx_id, proc=None):
    c1 = wx.SystemSettings.GetColour(wx_id)
    if not proc:
        return colour_to_html(c1)
    else:
        x = norm_colour(c1.Red(), c1.Green(), c1.Blue(), proc)
        c2 = wx.Colour(x[0], x[1], x[2])
        return colour_to_html(c2)

def standard_tab_colour():
    return (
        ('color_body_0_2', get_colour(wx.SYS_COLOUR_3DFACE, 0.2)),
        ('color_body_0_5', get_colour(wx.SYS_COLOUR_3DFACE, 0.5)),
        ('color_body_0_7', get_colour(wx.SYS_COLOUR_3DFACE, 0.7)),
        ('color_body_0_9', get_colour(wx.SYS_COLOUR_3DFACE, 0.9)),
        ('color_body', get_colour(wx.SYS_COLOUR_3DFACE)),
        ('color_body_1_1', get_colour(wx.SYS_COLOUR_3DFACE, 1.1)),
        ('color_body_1_3', get_colour(wx.SYS_COLOUR_3DFACE, 1.3)),
        ('color_body_1_5', get_colour(wx.SYS_COLOUR_3DFACE, 0)),
        ('color_body_1_8', get_colour(wx.SYS_COLOUR_3DFACE, 1.8)),
        ('color_higlight', get_colour(wx.SYS_COLOUR_3DHIGHLIGHT)),
        ('color_shadow', get_colour(wx.SYS_COLOUR_3DSHADOW)),
        ('color_background_0_5', get_colour(wx.SYS_COLOUR_3DFACE, 0.5)),
        ('color_background_0_8', get_colour(wx.SYS_COLOUR_3DFACE, 0.8)),
        ('color_background_0_9', get_colour(wx.SYS_COLOUR_3DFACE, 0.9)),
        ('color_background', get_colour(wx.SYS_COLOUR_3DFACE)),
        ('color_background_1_1', get_colour(wx.SYS_COLOUR_3DFACE, 1.1)),
        ('color_background_1_2', get_colour(wx.SYS_COLOUR_3DFACE, 1.2)),
        ('color_background_1_5', get_colour(wx.SYS_COLOUR_3DFACE, 1.5)),
        ('color_info', get_colour(wx.SYS_COLOUR_INFOBK, 1.5)),
        )


def get_desktop_folder():
    if platform.system() == "Windows":
        from comtypes.client import CreateObject
        from comtypes.gen import IWshRuntimeLibrary
        ws = CreateObject("WScript.Shell")
        return ws.SpecialFolders("Desktop")
    else:
        with open(os.path.expanduser("~/.config/user-dirs.dirs"), "rt") as f:
            for line in f:
                if 'XDG_DESKTOP_DIR' in line:
                    return os.path.expanduser(line.split('=')[1].split('#')[0].strip().replace('$HOME','~').replace('"',''))
        return os.path.expanduser("~/Desktop")


def get_pytigon_path():
    base_path = __file__.replace("tools.py", "")
    if base_path == "":
        base_path = os.getcwd()
    pytigon_path = os.path.normpath(os.path.join(base_path, "../.."))
    return pytigon_path


DESKTOP_STR = """[Desktop Entry]
Type=Application
Name=%s
Exec=%s/python/bin/python %s/pytigon.py %s
Categories=Other
NoDisplay=true
MimeType=application/pytigon
Terminal=false
X-KeepTerminal=false
Icon=%s/pytigon.svg
"""

def create_desktop_shortcut(app_name, title=None, parameters = ""):
    title2 = title
    parameters2 = parameters
    if parameters2 == "":
        parameters2 = app_name
    if platform.system() == "Windows":
        from comtypes.client import CreateObject
        from comtypes.gen import IWshRuntimeLibrary
        ws = CreateObject("WScript.Shell")
        fname = os.path.join(get_desktop_folder(), app_name+".lnk")
        icon_name = os.path.join(get_pytigon_path(), 'pytigon.ico')
        scut = ws.CreateShortcut(fname).QueryInterface(IWshRuntimeLibrary.IWshShortcut)
        scut.Description = title2
        scut.TargetPath = os.path.join(get_pytigon_path(), "python\pythonw.exe")
        scut.Arguments = os.path.join(get_pytigon_path(), "pytigon.py")  + " " + parameters2
        scut.IconLocation = icon_name
        scut.Save()
    else:
        fname = os.path.join(get_desktop_folder(), app_name+".desktop")
        if not os.path.exists(fname):
            pytigon_path = get_pytigon_path()
            desktop_str2 = DESKTOP_STR % (title2, pytigon_path, pytigon_path, parameters2, pytigon_path)
            with open(fname,"wt") as f:
                f.write(desktop_str2)


LAST_FOCUS_CTRL_IN_FORM = None

def find_focus_in_form():
    global LAST_FOCUS_CTRL_IN_FORM
    win_focus = wx.Window.FindFocus()
    win = win_focus
    while win:
        if win.__class__.__name__ == 'SchForm':
            LAST_FOCUS_CTRL_IN_FORM = win_focus
            return win_focus
        win = win.GetParent()
    if LAST_FOCUS_CTRL_IN_FORM and LAST_FOCUS_CTRL_IN_FORM.IsBeingDeleted():
        LAST_FOCUS_CTRL_IN_FORM
        return None
    else:
        return LAST_FOCUS_CTRL_IN_FORM


