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
import sys
import time
from cefpython.cefwxpanel import initCEF, shutdownCEF, CEFWindow
import cefpython
from schcli.guilib.tools import get_colour

cef_count = 0

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
        global cef_count, timer
        if cef_count == 0:
            initCEF()
            cef_count =  1

    def cef_shutdown():
        shutdownCEF()

    class NullClientHandler:
        pass

    class ClientHandler:
        def __init__(self, htmlwin):
            self.htmlwin = htmlwin

        def OnAddressChange(self, browser, frame, url):
            event = wx.CommandEvent()
            #event.SetString(url.decode('utf-8'))
            event.SetString(url)
            if self.htmlwin: self.htmlwin.on_address_changed(event)
            
        #def OnStatusMessage(self, browser, text): #, statusType):
        if True:
            def OnStatusMessage(self, browser, text, statusType):
                event = wx.CommandEvent()
                event.SetString(text)
                if self.htmlwin: self.htmlwin.on_status_message(event)
        else:
            def OnStatusMessage(self, browser, text):
                event = wx.CommandEvent()
                event.SetString(text)
                if self.htmlwin: self.htmlwin.on_status_message(event)


        def OnTitleChange(self, browser, title):
            event = wx.CommandEvent()
            event.SetString(title)
            if self.htmlwin: self.htmlwin.on_title_changed(event)

        def OnLoadStart(self, browser, frame):
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

        def OnLoadError(self, browser, frame, errorCode, failedURL, errorText):
            event = wx.CommandEvent()
            #event.SetString(failedURL)
            #print(failedURL)
            if self.htmlwin:
                self.htmlwin.on_load_error(event)
                self.htmlwin.progress_changed(100)
            
        def OnTooltip(self, browser, text):
            event = wx.CommandEvent()
            event.SetString(text[0])
            if self.htmlwin: self.htmlwin.on_status_message(event)

        def OnBeforeBrowse(self, browser, frame, request, navType, isRedirect):
            print(">>>", request.GetUrl())
            if navType == 0 and wx.GetKeyState(wx.WXK_CONTROL):
                if self.htmlwin: self.htmlwin.new_win(request.GetUrl())
                return True
            else:
                return False

        def OnBeforeResourceLoad(self, browser, request, redirectUrl, streamReader, response, loadFlags):
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

        def OnKeyEvent(self, browser, eventType, keyCode, modifiers, isSystemKey, isAfterJavascript):
            #if eventType == cefpython.KEYEVENT_KEYDOWN and keyCode ==  ord('J') and modifiers == cefpython.KEY_ALT:
            if eventType == 2 and keyCode in (ord('J'), ord('K')) and modifiers == 4:
                return True
            return False

        #def OnBeforePopup(self, parentBrowser, popupFeatures, windowInfo, url, settings):
        #def OnPopupShow(self, browser, show):
        #    return True

        #def RunModal(self, browser):
        #    return True

    class Html2(CEFWindow, SchBaseCtrl, base_web_browser):

        logged = False

        def __init__(self, *args, **kwds):
            cef_init()

            wx.GetApp().web_ctrl = self

            SchBaseCtrl.__init__(self, args, kwds)
            CEFWindow.__init__(self, *args, **kwds)
            self.client_handler = ClientHandler(self)
            self.browser.SetClientHandler(self.client_handler)
            #print(">>>", self.browser)
            href = self.href
            base_web_browser.__init__(self)
            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('set_handle_info', 'browser', self)

            if hasattr(self.GetParent(), 'any_parent_command'):
                self.GetParent().any_parent_command('show_info')
            
            self.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)
            self.Bind(wx.EVT_WINDOW_DESTROY, self.on_destroy)

            self.edit = False
            #self.exist = True
            self.loaded = False

            if href != None:
                self.go(href)

            self.afetr_init()


        def html_from_str(self, str_body):
            color = get_colour(wx.SYS_COLOUR_3DFACE)
            return ("<!DOCTYPE html><html><head><base href=\"%s\" target=\"_blank\"></head><body bgcolor='%s'>" % ( self._static_prefix(), color) ) + str_body+"</body></html>"
            #return ("<!DOCTYPE html><html><head><base href=\"static:///\" target=\"_blank\"></head><body bgcolor='%s'>" % color ) + str_body+"</body></html>"


        def on_destroy(self, event):
            self.client_handler.htmlwin = None
            if self.loaded:
                self.browser.CloseBrowser()
            event.Skip()

        def __getattribute__(self, attr):
            try:
                ret = SchBaseCtrl.__getattribute__(self, attr)
            except:
                try:
                    ret = base_web_browser.__getattribute__(self, attr)
                except:
                    ret = getattr(self.browser, attr)
            return ret

        # overwrite
        
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
            self.GoBack()

        def on_forward(self, event):
            self.GoForward()

        def on_stop(self, event):
            self.StopLoad()

        def on_refresh(self, event):
            self.Reload()

        def can_go_back(self):
            return self.CanGoBack()

        def can_go_forward(self):
            return self.CanGoForward()

        def execute_javascript(self, script):
            frame = self.GetMainFrame()
            frame.ExecuteJavascript(script)

        def on_source(self, event):
            okno = self.GetParent().new_main_page('^standard/editor/editor.html',
                    self.GetParent().GetTab().title + ' - page source', None)
            okno.Body['EDITOR'].SetValue(norm_html(self.GetPageSource()))
            okno.Body['EDITOR'].GotoPos(0)

        def on_edit(self, event):
            self.edit = not self.edit
            self.SetEditable(self.edit)


    schcli.guictrl.schctrl.HTML2 = Html2

    return cef_shutdown
    #return True


