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
import ctypes
#import base64
from schcli.guilib.tools import get_colour
import io
import datetime
import tempfile
import platform

html_head = """
<script type="text/javascript">
<script type="text/javascript">
window.onerror = function (msg, url, line) {
   alert("Message : " + msg );
   alert("url : " + url );
   alert("Line number : " + line );
}
</script>"""


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


class WebViewMemoryHandler(wx.html2.WebViewHandler):
    def __init__(self):
        wx.html2.WebViewHandler.__init__(self, "static")
        fs = wx.FileSystem()
        fs.AddHandler(wx.MemoryFSHandler())
        self.fs = fs

    def GetFile(self, uri):
        if wx.Platform == '__WXMSW__':
            uri1 = uri.replace('static://', '')
        else:
            uri1 = uri.replace('static://', '')
            uri1 = uri.replace('static:/', '')
        if uri1[0]=='/':
            uri2 = os.path.join(wx.GetApp().root_path, uri1[1:])
        else:
            uri2 = os.path.join(wx.GetApp().root_path, uri1)
        uri3 = uri2.split('?')[0].replace('//','/')
        ret = self.fs.OpenFile(uri3)
        if not ret:
            print("Resource error:", uri3, uri)
        return ret

    def GetName(self):
        return "static"


class WebViewMemoryHandler2(wx.html2.WebViewHandler):
    def __init__(self, browser):
        wx.html2.WebViewHandler.__init__(self, "intercept")
        self.browser = browser
        self.fs = wx.FileSystem()

    def GetFile(self, uri):
        if '/fonts/glyphicons' in uri:
            uri2='/static/bootstrap/fonts/glyphicons' + uri.split('/fonts/glyphicons')[1].split('#')[0]
        else:
            uri2 = uri

        if '/images/ui' in uri2:
            uri2='/static/themes/bootstrap/images/ui' + uri2.split('/images/ui')[1].split('#')[0]

        s = self.browser.get_local(uri2)
        p = uri.replace('intercept://127.0.0.2', '').split('?')[0].split('#')[0]
        fname = os.path.join(tempfile.gettempdir(), p.replace('/', '_').replace('\\','_'))
        f = open(fname, "wb")
        f.write(s)
        f.close()
        return self.fs.OpenFile(fname)


    def GetName(self):
        return "intercept"


class WebViewMemoryHandler3(wx.html2.WebViewHandler):
    def __init__(self):
        wx.html2.WebViewHandler.__init__(self, "http")
        self.fs = wx.FileSystem()
        self.mfs = wx.MemoryFSHandler()
        self.fs.AddHandler(self.mfs)


    def GetFile(self, uri):
        uri1 = uri.replace('http:/', '')
        if uri1[0]=='/':
            uri2 = wx.GetApp().root_path + uri1
        else:
            uri2 = os.path.join(wx.GetApp().root_path, uri1)
        uri3 = uri2.split('?')[0].replace('//','/')
        ret = self.fs.OpenFile(uri3)
        if not ret:
            print("Resource error:", uri3, uri)
        return ret


    def GetName(self):
        return "http"


def init_plugin_web_view(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    base_web_browser,
    ):
    import wx.html2
    from schlib.schindent.indent_tools import norm_html
    from schcli.guictrl.schctrl import SchBaseCtrl
    import schcli.guictrl.schctrl
    from schcli.guilib import schevent
    try:
        from urllib.parse import quote as escape
    except:
        from urllib import quote as escape
    from tempfile import NamedTemporaryFile


    class BaseBrowser(SchBaseCtrl, base_web_browser):

        logged = False

        def Init(self, *args, **kwds):
            kwds['style'] = wx.TRANSPARENT_WINDOW| wx.WANTS_CHARS
            SchBaseCtrl.__init__(self, args, kwds)
            base_web_browser.__init__(self)

            self.loaded = True
            self.next_in_new_win = False
            self.page_loaded = False

            self.redirect_to_html = [None, None]
            self.redirect_to_local = True
            self.last_status_txt = ''
            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('set_handle_info', 'browser', self)

            self.Bind(schevent.EVT_REFRPARM, self._redirect_to_local)

            self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)

            try:
                self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.on_web_view_loaded,
                      self)
            except:
                self.Bind(wx.html2.EVT_WEB_VIEW_LOADED, self.on_web_view_loaded,
                      self)

            try:
                self.Bind(wx.html2.EVT_WEBVIEW_ERROR, self.on_web_view_error,
                      self)
            except:
                self.Bind(wx.html2.EVT_WEB_VIEW_ERROR, self.on_web_view_error,
                      self)

            try:
                self.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, self.on_new_window, self)
            except:
                self.Bind(wx.html2.EVT_WEB_VIEW_NEWWINDOW, self.on_new_window, self)

            try: 
                self.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, self.on_title_changed, self)
            except:
                self.Bind(wx.html2.EVT_WEB_VIEW_TITLE_CHANGED, self.on_title_changed, self)


            try:
                self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_navigating, self)
            except:
                self.Bind(wx.html2.EVT_WEB_VIEW_NAVIGATING, self.on_navigating, self)


            try:
                self.Bind(wx.html2.EVT_WEBVIEW_ERROR, self.on_error, self)
            except:
                self.Bind(wx.html2.EVT_WEB_VIEW_ERROR, self.on_error, self)


            self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

            self.Bind(wx.EVT_SET_FOCUS, self.on_setfocus)
            self.Bind(wx.EVT_KILL_FOCUS, self.on_killfocus)

            self.edit = False

            self.RegisterHandler(WebViewMemoryHandler())
            self.RegisterHandler(WebViewMemoryHandler2(self))

            if self.href != None and self.href != "":
                self.go(self.href)
            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('show_info')

            self.afetr_init()


        def on_setfocus(self, event):
            print("on_setfocus")
            event.Skip()

        def on_killfocus(self, event):
            print("on_killfocus", event.GetWindow())
            event.Skip()

        def on_destroy(self, event):
            if platform.system() == "Windows":
                if self.IsBusy():
                    self.Stop()
                while self.IsBusy():
                    wx.html2.WebView.New("messageloop")
            self.loaded=False
            event.Skip()


        def html_from_str(self, str_body):
            color = get_colour(wx.SYS_COLOUR_3DFACE)
            return ("<!DOCTYPE html><html><head>%s<base href=\"%s\" target=\"_blank\" /></head><body bgcolor='%s'>" % (html_head, self._static_prefix(), color) ) + str_body+"</body></html>"

        def on_navigating(self, event):
            url = event.GetURL()
            if self.next_in_new_win and wx.GetKeyState(wx.WXK_CONTROL):
                print("on_navigating", url)
                self.next_in_new_win = False
                event.Veto()
                self.new_win(event.GetURL())
            else:
                self.next_in_new_win = False
                self.page_loaded = False
                event.Skip()

        def on_error(self, event):
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERROR!")

        def on_web_view_loaded(self, event):            
            #print("on_web_view_loaded:", event.GetURL())
            #if self.data:
            #    data, base = self.data
            #    self.data = None
            #    self.wb.SetPage(data, base if base else self._static_prefix())
            #    event.Skip()
            #else:

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
            print("on_new_window:", event.GetURL())
            self.new_win(event.GetURL())
            event.Skip()

#         def before_navigate2(
#             self,
#             this,
#             p_disp,
#             url,
#             flags,
#             target_frame_name,
#             post_data,
#             headers,
#             cancel,
#             ):
#             print "Before_navigate_1", url
#             if self.accept_page(url[0]):
#                 if self.redirect_to_local and '127.0.0.2' in url[0]:
#                     cancel[0] = True
#                     self.url = url[0]
#                     evt = schevent.RefrParmEvent(schevent.userEVT_REFRPARM,
#                             self.GetId())
#                     self.GetEventHandler().AddPendingEvent(evt)
#                     return True
#                 else:
#                     return False
#             else:
#                 cancel[0] = True
#                 return True
# 
#         def document_complete(
#             self,
#             this,
#             p_disp,
#             url,
#             ):
#             pass

        def progress_change(self, progress, max_progress):
            if max_progress == 0:
                max_progress = 100
            if progress >= 0:
                progress2 = int((progress * 100) / max_progress)
            else:
                progress2 = 100
            return self.progress_changed(progress2)

#         def status_text_change(self, txt):
#             self.status_text(txt)
#             self.last_status_txt = txt
# 
#         def new_window3(
#             self,
#             pp_disp,
#             cancel,
#             dw_flags,
#             bstr_url_context,
#             bstr_url,
#             ):
#             print "Before_navigate_3", bstr_url
#             if self.new_win(bstr_url):
#                 cancel[0] = True
#             return cancel            

        # overwrite
        
        def get_shtml_window(self):
            return self.GetParent()

        def load_url(self, url):
            print("LoadURL:", url)
            self.LoadURL(url)
            #print("SetFocus1")
            #self.SetFocus()
            #self.GetParent().GetParent().SetFocus()
            print("SetFocus2")

        def _static_prefix(self):
            if wx.Platform == '__WXMSW__':
                p = '/' + wx.GetApp().root_path.replace('\\','/')
            else:
                p = wx.GetApp().root_path.replace('\\','/')
            return "static://" + p + "/static/"

        def load_str(self, data, base=None):
            #print("LOAD_STR:")
            #self.wb.SetPage(data, base if base else self._static_prefix())

            #self.load_url("about:blank")
            #self.LoadURL("about:blank")
            #self.SetPage(data, "")
            #self.LoadURL("about:blank")
            #self.SetPage("<html><head></head><body>Hello world</body></html>", "")
            self.SetPage(data, "")
            #self.data = (data, base)
            #self.wb.LoadURL("about:blank")
            #pass

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
            okno.Body['EDITOR'].SetValue(norm_html(self.GetPageSource()))
            okno.Body['EDITOR'].GotoPos(0)

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


    def Html2(*args, **kwds):
        kwds2 = {}
        kwds2['name'] = kwds['name']
        kwds2['size'] = kwds['size']
        if 'backend' in kwds:
            kwds2['backend'] = kwds['backend']
        else:
            if platform.system() == "Windows":
                kwds2['backend'] = "wxWebViewChromium"
            #kwds['backend'] = "wxWebViewIE"

        wb = wx.html2.WebView.New(*args, **kwds2)
        wb.__class__ = type('BrowserCtrl',(wb.__class__,BaseBrowser),{})
        wb.Init(*args, **kwds)

        return wb

    schcli.guictrl.schctrl.HTML2 = Html2

