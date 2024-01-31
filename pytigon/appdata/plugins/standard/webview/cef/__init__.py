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

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

import wx
from pytigon_gui.guilib.tools import get_colour

CEF_INITIATED = False
TIMER = None


def init_plugin_cef(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    base_web_browser,
):
    from pytigon_lib.schindent.indent_tools import norm_html
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl

    try:
        pass
    except:
        pass

    from .cefcontrol import CEFControl, cef_shutdown

    class Html2(CEFControl, SchBaseCtrl, base_web_browser):
        logged = False

        def __init__(self, parent, **kwds):
            wx.GetApp().web_ctrl = self
            self.component = False
            if "component" in kwds:
                del kwds["component"]
                self.component = True
            SchBaseCtrl.__init__(self, parent, kwds)
            if "style" in kwds:
                kwds["style"] |= wx.WANTS_CHARS
            else:
                kwds["style"] = wx.WANTS_CHARS

            CEFControl.__init__(self, parent, **kwds)

            href = self.href

            base_web_browser.__init__(self)
            if hasattr(self.GetParent(), "any_parent_command"):
                self.GetParent().any_parent_command("set_handle_info", "browser", self)

            if hasattr(self.GetParent(), "any_parent_command"):
                self.GetParent().any_parent_command("show_info")

            self.edit = False

            # self.browser.GetMainFrame().LoadUrl("about:blank")

            if href != None:
                self.go(href)

            self.afetr_init()

        def html_from_str(self, str_body):
            color = get_colour(wx.SYS_COLOUR_3DFACE)
            return (
                (
                    '<!DOCTYPE html><html><head><base href="%s" target="_blank"></head><body bgcolor=\'%s\'>'
                    % (self._static_prefix(), color)
                )
                + str_body
                + "</body></html>"
            )

        def get_shtml_window(self):
            return self.GetParent()

        def _static_prefix(self):
            rp = wx.GetApp().root_path
            if rp[0] == "/":
                rpp = "file://" + rp.replace("\\", "/") + "/"
            else:
                rpp = "file:///" + rp.replace("\\", "/") + "/"
            return rpp

        def load_str(self, data, base=None):
            if self.browser:
                if base:
                    self.browser.GetMainFrame().LoadUrl(
                        "data:text/html, "
                        + data.replace("<head>", '<head><base href="%s/">' % base)
                    )
                else:
                    self.browser.GetMainFrame().LoadUrl("data:text/html, " + data)
            else:
                wx.CallLater(100, self.load_str, data, base)

        def on_back(self, event):
            if self.browser:
                self.browser.GoBack()

        def on_forward(self, event):
            if self.browser:
                self.browser.GoForward()

        def on_stop(self, event):
            if self.browser:
                self.browser.StopLoad()

        def on_refresh(self, event):
            if self.browser:
                self.browser.Reload()

        def can_go_back(self):
            return self.browser and self.browser.CanGoBack()

        def can_go_forward(self):
            return self.browser and self.browser.CanGoForward()

        def execute_javascript(self, script):
            frame = self.browser.GetMainFrame()
            frame.ExecuteJavascript(script)

        def on_source(self, event):
            okno = self.GetParent().new_main_page(
                "^standard/editor/editor.html",
                self.GetParent().GetTab().title + " - page source",
                None,
            )
            okno.body["EDITOR"].SetValue(norm_html(self.browser.GetPageSource()))
            okno.body["EDITOR"].GotoPos(0)

        def on_edit(self, event):
            self.edit = not self.edit
            self.browser.SetEditable(self.edit)

    pytigon_gui.guictrl.ctrl.HTML2 = Html2

    return cef_shutdown
