#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General PubliLicense
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import wx
import types
from base64 import b32encode, b32decode
from schcli.guilib.tools import bitmap_from_href

def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    ):

    def xmlrpc_edit(self, path=None):
        okno=self.GetTopWindow().new_main_page("^standard/editor/editor.html", path, None)
        p = "/schcommander/table/FileManager/open/%s/" % b32encode(path.encode('utf-8')).decode('utf-8')
        ed = okno.Body["EDITOR"]
        ed.load_from_url(p, "py")
        ed.set_save_path(p.replace('/open/','/save/'))
        ed.GotoPos(0)
        self.GetTopWindow().Raise()
        #self.GetTopWindow().RequestUserAttention()
        return "OK"

    app.xmlrpc_edit = types.MethodType(xmlrpc_edit, app)

    def xmlrpc_test(self):
        return "OK"

    app.xmlrpc_test = types.MethodType(xmlrpc_test, app)


    def on_edit3(self):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    mainframe.on_edit = types.MethodType(on_edit, mainframe)

    idn = mainframe._append_command("python", "self.on_edit3()")
    bitmap = bitmap_from_href("client://emblems/emblem-favorite.png")

    page = toolbar.create_page("page2")
    panel = page.create_panel("special")
    panel.append(idn, "test", bitmap)
    toolbar.realize_bar()


