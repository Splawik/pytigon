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

import wx
import os
import tempfile
import platform

init_script = """
window.addEventListener("click", mod_click, false);

function mod_click(e) {
    e = e ||  window.event;
    var element = e.target || e.srcElement;

    if (e.ctrlKey && element.tagName == 'A') {
        var old_target = element.getAttribute("target");
        element.setAttribute("target", "_blank");
        setTimeout(function() {
                if (old_target) element.setAttribute("target", old_target);
                else element.removeAttribute("target");
            },
            0
        );
    }
}
"""

import wx.html2

class WebViewMemoryHandler(wx.html2.WebViewHandler):

    def __init__(self, browser):
        wx.html2.WebViewHandler.__init__(self, "http")
        self.browser = browser
        self.fs = wx.FileSystem()

    def GetFile(self, uri):
        print(uri)
        if uri.startswith('http://127.0.0.2/?:'):
            if uri != "http://127.0.0.2/?:":
                self.browser.run_command_from_js(uri[19:])
            return None
        elif uri.startswith('http://127.0.0.2'):
            s, file_name = self.browser._get_http_file(uri)
            if not file_name:
                p = uri.replace('http://127.0.0.2', '').split('?')[0].split('#')[0]
                file_name = os.path.join(tempfile.gettempdir(), p.replace('/', '_').replace('\\','_').replace(':','_'))
                f = open(file_name, "wb")
                f.write(s)
                f.close()
            return self.fs.OpenFile(file_name)
        else:
            return None

    def GetName(self):
        return "http"



def init_plugin_web_view(app, mainframe, desktop, mgr, menubar, toolbar, accel, base_web_browser):
    import wx.html2
    from pytigon_lib.schindent.indent_tools import norm_html
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl
    try:
        from urllib.parse import quote as escape
    except:
        from urllib import quote as escape

    class BaseBrowser(SchBaseCtrl, base_web_browser):
        logged = False

        def Init(self, parent, **kwds):
            kwds['style'] = wx.TRANSPARENT_WINDOW| wx.WANTS_CHARS
            SchBaseCtrl.__init__(self, parent, kwds)
            base_web_browser.__init__(self)

            self.loaded = True
            self.next_in_new_win = False
            self.page_loaded = False

            self.redirect_to_html = [None, None]
            self.redirect_to_local = True
            self.last_status_txt = ''
            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('set_handle_info', 'browser', self)

            self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)
            self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.on_web_view_loaded, self)
            self.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, self.on_new_window, self)
            self.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, self.on_title_changed, self)
            self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_navigating, self)
            self.Bind(wx.html2.EVT_WEBVIEW_ERROR, self.on_error, self)
            self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)
            self.Bind(wx.EVT_SET_FOCUS, self.on_setfocus)
            self.Bind(wx.EVT_KILL_FOCUS, self.on_killfocus)

            self.edit = False
            self.local = False

            if 'url' in kwds and kwds['url'].startswith('http://127.0.0.2'):
                self.RegisterHandler(WebViewMemoryHandler(self))
                self.local = True

            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('show_info')
            self.afetr_init()

        def on_setfocus(self, event):
            event.Skip()

        def on_killfocus(self, event):
            print("on_killfocus", event.GetWindow())
            event.Skip()

        def on_destroy(self, event):
            self.loaded=False
            event.Skip()

        def on_navigating(self, event):
            url = event.GetURL()
            if url.startswith('http://127.0.0.2/?:'):
                event.Veto()
                self.run_command_from_js(url[21:])
            else:
                if self.next_in_new_win and wx.GetKeyState(wx.WXK_CONTROL):
                    self.next_in_new_win = False
                    event.Veto()
                    self.new_win(event.GetURL())
                else:
                    self.next_in_new_win = False
                    self.page_loaded = False
                    event.Skip()

        def on_error(self, event):
            message = "%s\n, %s" % ( event.GetURL(),event.GetString())
            self.show_error("WebView error", message+"\n"+event.GetString())
            event.Skip()

        def on_web_view_loaded(self, event):
            self.page_loaded = True

            ev = wx.CommandEvent()
            try:
                ev.SetString(event.GetURL().decode('utf-8'))
            except:
                ev.SetString(event.GetURL())
            self.on_address_changed(ev)
            self.on_load_end(ev)
            event.Skip()

            self.execute_javascript(init_script)
            self.SetFocus()

        def on_web_view_error(self, event):
            print("on_web_view_error:", event.GetURL())
            event.Skip()

        def on_new_window(self, event):
            url = event.GetURL()
            if url.startswith('http://127.0.0.2/?:'):
                event.Veto()
                if url != "http://127.0.0.2/?:":
                    self.run_command_from_js(url[19:])
            else:
                self.new_win(event.GetURL())
                event.Skip()

        def progress_change(self, progress, max_progress):
            if max_progress == 0:
                max_progress = 100
            if progress >= 0:
                progress2 = int((progress * 100) / max_progress)
            else:
                progress2 = 100
            return self.progress_changed(progress2)

        def load_url(self, url, cookies=None):
            if not self.local and url.startswith('http://127.0.0.2'):
                self.local = True
                self.RegisterHandler(WebViewMemoryHandler(self))
            self.LoadURL(url)

        def _static_prefix(self):
            if wx.Platform == '__WXMSW__':
                p = '/' + wx.GetApp().root_path.replace('\\','/')
            else:
                p = wx.GetApp().root_path.replace('\\','/')
            return "static://" + p + "/static/"

        def load_str(self, data, base=None):
            self.LoadURL("about:blank")
            self.SetPage(data, "")

        def on_back(self, event):
            self.GoBack()

        def on_forward(self, event):
            self.GoForward()

        def on_stop(self, event):
            self.Stop()

        def on_refresh(self, event):
            self.Reload()
            
        def execute_javascript(self, script):
            self.RunScript(script)

        def on_source(self, event):
            okno = self.GetParent().new_main_page('^standard/editor/editor.html',
                    self.GetParent().GetTab().title + ' - page source', None)
            okno.body['EDITOR'].SetValue(norm_html(self.GetPageSource()))
            okno.body['EDITOR'].GotoPos(0)

        def on_edit(self, event):
            self.edit = not self.edit
            self.SetEditable(self.edit)

        def can_go_back(self):
            ret = self.CanGoBack()
            return ret

        def can_go_forward(self):
            return self.CanGoForward()

        def clear_history(self):
            self.ClearHistory()

    def Html2(parent, **kwds):
        kwds2 = {}
        kwds2['name'] = kwds['name']
        kwds2['size'] = kwds['size']
        kwds2['style'] = wx.BORDER_NONE
        if 'backend' in kwds:
            kwds2['backend'] = kwds['backend']
        else:
            if platform.system() == "Windows":
                kwds2['backend'] = "wxWebViewChromium"

        if 'url' in kwds:
            kwds2['url'] = kwds['url']
        wb = wx.html2.WebView.New(parent, **kwds2)
        wb.__class__ = type('BrowserCtrl',(wb.__class__,BaseBrowser),{})
        wb.Init(parent, **kwds)

        return wb

    pytigon_gui.guictrl.ctrl.HTML2 = Html2

