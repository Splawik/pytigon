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
from .cefcontrol import initCEF, shutdownCEF, loop, CEFControl, quit
from schcli.guilib.tools import get_colour

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

    from schlib.schindent.indent_tools import norm_html
    from schcli.guictrl.schctrl import SchBaseCtrl
    import schcli.guictrl.schctrl
    from schcli.guilib import schevent
    try:
        from urllib.parse import quote as escape
    except:
        from urllib import quote as escape

    from tempfile import NamedTemporaryFile

    def cef_init():
        global CEF_INITIATED, TIMER
        if not CEF_INITIATED:
            initCEF()
            CEF_INITIATED = True
            frame = wx.GetApp().GetTopWindow()
            TIMER = wx.Timer(frame)
            def on_timer(event):
                loop()
            frame.on_cef_timer = on_timer
            frame.Bind(wx.EVT_TIMER, frame.on_cef_timer, TIMER)
            TIMER.Start(25)

    def cef_shutdown():
        print("#####################################################################################################")
        if CEF_INITIATED:
            shutdownCEF()
            TIMER.Stop()

    class NullClientHandler:
        pass

    class ClientHandler:
        mainBrowser = None

        def __init__(self, htmlwin):
            self.htmlwin = htmlwin

        def OnAddressChange(self, browser, frame, url):
            event = wx.CommandEvent()
            #event.SetString(url.decode('utf-8'))
            event.SetString(url)
            if self.htmlwin: self.htmlwin.on_address_changed(event)
            
        #def OnStatusMessage(self, browser, text): #, statusType):
        if True:
            #def OnStatusMessage(self, browser, text, statusType):
            def OnStatusMessage(self, browser, value):
                event = wx.CommandEvent()
                event.SetString(value)
                if self.htmlwin: self.htmlwin.on_status_message(event)
        else:
            #def OnStatusMessage(self, browser, text):
            def OnStatusMessage(self, browser, value):
                event = wx.CommandEvent()
                event.SetString(value)
                if self.htmlwin: self.htmlwin.on_status_message(event)


        def OnTitleChange(self, browser, title):
            event = wx.CommandEvent()
            event.SetString(title)
            if self.htmlwin: self.htmlwin.on_title_changed(event)

        def OnLoadStart(self, browser, frame):
            print("START")
            if self.htmlwin: self.htmlwin.loading += 1
            event = wx.CommandEvent()
            event.SetString(frame.GetUrl())
            if self.htmlwin: self.htmlwin.on_load_start(event)
            if self.htmlwin: self.htmlwin.progress_changed(0)

        def OnLoadEnd(self, browser, frame, httpStatusCode):
            if frame == browser.GetMainFrame():
                event = wx.CommandEvent()
                event.SetString(frame.GetUrl())
                if self.htmlwin:
                    self.htmlwin.on_load_end(event)
                    self.htmlwin.progress_changed(100)
            if self.htmlwin: self.htmlwin.loading -= 1
            print("END", self.htmlwin.loading)

        def OnLoadError(self, browser, frame, errorCode, failedURL, errorText):
            event = wx.CommandEvent()
            #event.SetString(failedURL)
            #print(failedURL)
            if self.htmlwin:
                self.htmlwin.on_load_error(event)
                self.htmlwin.progress_changed(100)
            if self.htmlwin: self.htmlwin.loading -= 1
            print("ERROR")

        def OnTooltip(self, browser, text):
            event = wx.CommandEvent()
            event.SetString(text[0])
            if self.htmlwin: self.htmlwin.on_status_message(event)

        def OnBeforeBrowse(self, browser, frame, request, isRedirect):
            print(">>>", request.GetUrl())
            if wx.GetKeyState(wx.WXK_CONTROL):
                if self.htmlwin: self.htmlwin.new_win(request.GetUrl())
                return True
            else:
                return False

        #def OnBeforeResourceLoad(self, browser, request, redirectUrl, streamReader, response, loadFlags):
        def OnBeforeResourceLoad(self, browser, frame, request):
            if self.htmlwin: self.htmlwin.loading += 1
            url = request.GetUrl()
            #print("|||", url)
            if url.startswith('static://') or url.startswith('file://'):
                rp =  wx.GetApp().root_path
                rp += url.replace('static://', '/').replace('file://', '/')
                if ':/static' in rp:
                    rp = wx.GetApp().root_path.replace("\\",'') + "/static" + rp.split(':/static')[1]
                file_path = rp.split('?')[0]
                try:
                    f = open(file_path, "rb")
                    buf = f.read()
                    f.close()
                except:
                    buf = None
                    print("Resource error:", file_path)
                if buf and len(buf)>0:
                    response.SetStatus(200)
                    response.SetStatusText("OK")
                    if '.css' in url:
                        response.SetMimeType("text/css")
                    if '.js' in url:
                        response.SetMimeType("application/javascript")
                    streamReader.SetData(buf)

            #print("OnBeforeResourceLoad(): request.GetUrl() = %s" % (
            #        request.GetUrl()))
            if request.GetMethod() == "POST":
                if request.GetUrl().startswith("https://accounts.google.com/ServiceLogin"):
                    postData = request.GetPostData()
                    postData["Email"] = "--changed via python"
                    request.SetPostData(postData)
                    print("OnBeforeResourceLoad(): modified POST data: %s" % (request.GetPostData()))
            if request.GetUrl().endswith("replace-on-the-fly.css"):
                print("OnBeforeResourceLoad(): replacing css on the fly")
                response.SetStatus(200)
                response.SetStatusText("OK")
                response.SetMimeType("text/css")
                streamReader.SetData("body { color: red; }")

            if self.htmlwin: self.htmlwin.loading -= 1

    class Html2(CEFControl, SchBaseCtrl, base_web_browser):

        logged = False

        def __init__(self, *args, **kwds):
            cef_init()

            wx.GetApp().web_ctrl = self

            SchBaseCtrl.__init__(self, args, kwds)
            if 'style' in kwds:
                kwds['style'] |= wx.WANTS_CHARS
            else:
                kwds['style'] = wx.WANTS_CHARS

            CEFControl.__init__(self, *args, **kwds)

            self.client_handler = ClientHandler(self)
            self.browser.SetClientHandler(self.client_handler)

            self.client_handler.mainBrowser = self.browser

            href = self.href
            base_web_browser.__init__(self)
            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('set_handle_info', 'browser', self)

            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('show_info')
            
            #self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)
            #self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)
            self.Bind(wx.EVT_CLOSE, self.on_close)

            self.edit = False

            self.loading = 0
            #self.exist = True
            self.browser.GetMainFrame().LoadUrl("about:blank")

            if href != None:
                self.go(href)

            self.afetr_init()


        def html_from_str(self, str_body):
            color = get_colour(wx.SYS_COLOUR_3DFACE)
            return ("<!DOCTYPE html><html><head><base href=\"%s\" target=\"_blank\"></head><body bgcolor='%s'>" % ( self._static_prefix(), color) ) + str_body+"</body></html>"
            #return ("<!DOCTYPE html><html><head><base href=\"static:///\" target=\"_blank\"></head><body bgcolor='%s'>" % color ) + str_body+"</body></html>"


        #def on_destroy(self, event):
        def on_close(self, event):
            print("X1")
            #del self.browser
            self.browser.StopLoad()
            print("X2")
            while self.loading:
                wx.Yield()
            #quit()
            self.client_handler.htmlwin = None
            print("X3")
            #del self.browser
            #if self.loaded:
            #self.browser.StopLoad()
            #self.browser.GetMainFrame().LoadUrl("about:blank")
            #self.browser.CloseBrowser(False)
            #self.browser.GetCefBrowserHost().get().CloseBrowser(True)
            #self.browser.ParentWindowWillClose()
            #self.browser.GetCefBrowserHost().get().ParentWindowWillClose()
            #print("X3")
            #del self.client_handler.mainBrowser
            #del self.browser
            #self.browser = None
            #print("X3.5")
            #self.Destroy()
            #print("X4")
            event.Skip()
            print("X5")


        def get_shtml_window(self):
            return self.GetParent()

        def load_url(self, url):
            self.loaded = True
            #self.browser.GetMainFrame().LoadUrl(url.replace('file:///',''))
            print("load_url:", url)
            #self.browser.GetMainFrame().LoadUrl(url)
            if wx.Platform == '__WXMSW__':
                self.browser.GetMainFrame().LoadUrl(url.replace("file:///",''))
            else:
                self.browser.GetMainFrame().LoadUrl(url)

        def _static_prefix(self):
            rp =  wx.GetApp().root_path
            if rp[0]=='/':
                rpp = "file://"+rp.replace('\\','/')+"/"
            else:
                rpp = "file:///"+rp.replace('\\','/')+"/"
            return rpp


        def load_str(self, data):
            #self.browser.GetMainFrame().LoadUrl("about:blank")
            self.browser.GetMainFrame().LoadString(data,self._static_prefix())

        def on_back(self, event):
            self.browser.GoBack()

        def on_forward(self, event):
            self.browser.GoForward()

        def on_stop(self, event):
            self.browser.StopLoad()

        def on_refresh(self, event):
            self.browser.Reload()

        def can_go_back(self):
            return self.browser.CanGoBack()

        def can_go_forward(self):
            return self.browser.CanGoForward()

        def execute_javascript(self, script):
            frame = self.browser.GetMainFrame()
            frame.ExecuteJavascript(script)

        def on_source(self, event):
            okno = self.GetParent().new_main_page('^standard/editor/editor.html',
                    self.GetParent().GetTab().title + ' - page source', None)
            okno.Body['EDITOR'].SetValue(norm_html(self.browser.GetPageSource()))
            okno.Body['EDITOR'].GotoPos(0)

        def on_edit(self, event):
            self.edit = not self.edit
            self.browser.SetEditable(self.edit)

    schcli.guictrl.schctrl.HTML2 = Html2

    return cef_shutdown


