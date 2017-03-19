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

import wx

from cefpython3 import cefpython as cef

CEF_INITIATED = False
TIMER = None


def cef_close(frame):
    global CEF_INITIATED, TIMER
    if CEF_INITIATED:
        if TIMER:
            TIMER.Stop()
            TIMER = None

def cef_init():
    global CEF_INITIATED, TIMER
    if not CEF_INITIATED:
        CEF_INITIATED = True

        def on_timer(event):
            cef.MessageLoopWork()

        frame = wx.GetApp().GetTopWindow()
        frame.on_cef_timer = on_timer

        TIMER = wx.Timer(frame)
        TIMER.Start(25)

        frame.Bind(wx.EVT_TIMER, on_timer, TIMER)

        settings = {
            "debug": False,
            "log_severity": cef.LOGSEVERITY_INFO,
            "locales_dir_path": cef.GetModuleDirectory() + "/locales",
            "resources_dir_path": cef.GetModuleDirectory(),
            "browser_subprocess_path": cef.GetModuleDirectory() + "/subprocess",
            "downloads_enabled": True,
            "remote_debugging_port": -1,
            "context_menu": {
                "enabled": True,
                "navigation": True,
                "print": True,
                "view_source": True,
                "external_browser": True,
                "devtools": True,
            },
            "ignore_certificate_errors": True,
        }
        cef.Initialize(settings)

        frame.run_on_close.append(cef_close)


def cef_shutdown():
    global CEF_INITIATED, TIMER
    if CEF_INITIATED:
        if TIMER:
            TIMER.Stop()
            TIMER = None
        cef.Shutdown()


class WebRequestClient:
    _resourceHandler = None
    _data = b""
    _dataLength = -1
    _response = None

    def OnUploadProgress(self, web_request, current, total):
        pass

    def OnDownloadProgress(self, web_request, current, total):
        pass

    def OnDownloadData(self, web_request, data):
        if type(data) == str:
            self._data += data.encode('utf-8')
        else:
            self._data += data

    def OnRequestComplete(self, web_request):
        self._response = web_request.GetResponse()
        self._data = self._resourceHandler._clientHandler._OnResourceResponse(
            self._resourceHandler._browser,
            self._resourceHandler._frame,
            web_request.GetRequest(),
            web_request.GetRequestStatus(),
            web_request.GetRequestError(),
            web_request.GetResponse(),
            self._data)

        if self._data:
            self._dataLength = len(self._data)
        self._resourceHandler._responseHeadersReadyCallback.Continue()

class ResourceHandler:
    _resourceHandlerId = None
    _clientHandler = None
    _browser = None
    _frame = None
    _request = None
    _responseHeadersReadyCallback = None
    _webRequest = None
    _webRequestClient = None
    _offsetRead = 0

    def ProcessRequest(self, request, callback):
        url = request.GetUrl()
        if '127.0.0.2' in url:
            request.SetUrl(url.replace('http:', 'memory:'))
        self._responseHeadersReadyCallback = callback
        self._webRequestClient = WebRequestClient()
        self._webRequestClient._resourceHandler = self
        request.SetFlags(cef.Request.Flags["AllowCachedCredentials"] | cef.Request.Flags["AllowCookies"])
        self._webRequest = cef.WebRequest.Create(request, self._webRequestClient)
        return True

    def GetResponseHeaders(self, response, response_length_out, redirect_url_out):
        wrcResponse = self._webRequestClient._response
        response.SetStatus(wrcResponse.GetStatus())
        response.SetStatusText(wrcResponse.GetStatusText())
        response.SetMimeType(wrcResponse.GetMimeType())
        if wrcResponse.GetHeaderMultimap():
            response.SetHeaderMultimap(wrcResponse.GetHeaderMultimap())
        response_length_out[0] = self._webRequestClient._dataLength
        if not response_length_out[0]:
            pass

    def ReadResponse(self, data_out, bytes_to_read, bytes_read_out, callback):
        if self._offsetRead < self._webRequestClient._dataLength:
            dataChunk = self._webRequestClient._data[self._offsetRead:(self._offsetRead + bytes_to_read)]
            self._offsetRead += len(dataChunk)
            data_out[0] = dataChunk
            bytes_read_out[0] = len(dataChunk)
            return True
        self._clientHandler._ReleaseStrongReference(self)
        return False

    def CanGetCookie(self, cookie):
        return True

    def CanSetCookie(self, cookie):
        return True

    def Cancel(self):
        pass

class ClientHandler:
    mainBrowser = None

    _resourceHandlers = {}
    _resourceHandlerMaxId = 0

    def __init__(self, htmlwin):
        self.htmlwin = htmlwin

    def GetResourceHandler(self, browser, frame, request):
        if request.GetUrl().startswith("http://127.0.0.2/") or request.GetUrl().startswith("memory://127.0.0.2/"):
            resHandler = ResourceHandler()
            resHandler._clientHandler = self
            resHandler._browser = browser
            resHandler._frame = frame
            resHandler._request = request
            self._AddStrongReference(resHandler)
            return resHandler
        else:
            return None

    def _OnResourceResponse(self, browser, frame, request, requestStatus, requestError, response, data):
        if request.GetUrl().startswith("http://127.0.0.2/") or request.GetUrl().startswith("memory://127.0.0.2/"):
            uri = request.GetUrl()
            data, file_name = self.htmlwin._get_http_file(uri.replace('memory:', 'http:'))
            if file_name:
                with open(file_name, "rb") as f:
                    data = f.read()

        if type(data) == str:
            return data.encode('utf-8')
        else:
            return data

    def _AddStrongReference(self, resHandler):
        self._resourceHandlerMaxId += 1
        resHandler._resourceHandlerId = self._resourceHandlerMaxId
        self._resourceHandlers[resHandler._resourceHandlerId] = resHandler

    def _ReleaseStrongReference(self, resHandler):
        if resHandler._resourceHandlerId in self._resourceHandlers:
            del self._resourceHandlers[resHandler._resourceHandlerId]
        else:
            print("_ReleaseStrongReference() FAILED: resource handler " \
                  "not found, id = %s" % (resHandler._resourceHandlerId))

    def OnAddressChange(self, browser, frame, url):
        event = wx.CommandEvent()
        event.SetString(url)
        if self.htmlwin: self.htmlwin.on_address_changed(event)

    def OnStatusMessage(self, browser, value):
        event = wx.CommandEvent()
        event.SetString(value)
        if self.htmlwin: self.htmlwin.on_status_message(event)

    def OnTitleChange(self, browser, title):
        event = wx.CommandEvent()
        event.SetString(title)
        if self.htmlwin: self.htmlwin.on_title_changed(event)

    def OnLoadStart(self, browser, frame):
        #if self.htmlwin: self.htmlwin.loading += 1
        event = wx.CommandEvent()
        event.SetString(frame.GetUrl())
        if self.htmlwin: self.htmlwin.on_load_start(event)
        if self.htmlwin: self.htmlwin.progress_changed(0)

    def OnLoadEnd(self, browser, frame, http_code):
        if frame == browser.GetMainFrame():
            event = wx.CommandEvent()
            event.SetString(frame.GetUrl())
            if self.htmlwin:
                self.htmlwin.on_load_end(event)
                self.htmlwin.progress_changed(100)
        #if self.htmlwin: self.htmlwin.loading -= 1

    def OnLoadError(self, browser, frame, error_code, error_text_out, failed_url):
        event = wx.CommandEvent()
        # event.SetString(error_text_out)
        print(error_text_out)
        if self.htmlwin:
            self.htmlwin.on_load_error(event)
            self.htmlwin.progress_changed(100)
        #if self.htmlwin: self.htmlwin.loading -= 1

    def OnTooltip(self, browser, text):
        event = wx.CommandEvent()
        event.SetString(text[0])
        if self.htmlwin: self.htmlwin.on_status_message(event)

    def OnBeforeBrowse(self, browser, frame, request, is_redirect):
        if wx.GetKeyState(wx.WXK_CONTROL):
            if self.htmlwin: self.htmlwin.new_win(request.GetUrl())
            return True
        else:
            return False

    def OnBeforeResourceLoad(self, browser, frame, request):
        return False


class FocusHandler(object):
    def OnGotFocus(self, browser, **_):
        if platform.system() != "Windows":
            browser.SetFocus(True)


class CEFControl(wx.Control):
    def __init__(self, parent, url="", size=(-1, -1), *args, **kwargs):
        kwargs['style'] = wx.WANTS_CHARS | wx.NO_BORDER
        wx.Control.__init__(self, parent, id=wx.ID_ANY, size=size, *args, **kwargs)
        self.url = url
        self.browser = None

        cef_init()

        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        if self.GetHandle():
            self.on_paint(None)
        else:
            self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_paint(self, event):
        if not self.browser:
            self.Unbind(wx.EVT_PAINT)
            self.embed_browser()

            self.client_handler = ClientHandler(self)
            self.browser.SetClientHandler(self.client_handler)
            self.client_handler.mainBrowser = self.browser
            if self.url:
                self.load_url(self.url)
        if event:
            event.Skip()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        (width, height) = self.GetClientSize()
        window_info.SetAsChild(self.GetHandle(), [0, 0, width, height])
        self.browser = cef.CreateBrowserSync(window_info, url = self.url)
        self.browser.SetClientHandler(FocusHandler())

        if self.url:
            self.browser.GetMainFrame().LoadUrl(self.url)
        else:
            self.browser.GetMainFrame().LoadUrl("about:blank")

    def load_url(self, url):
        if self.browser:
            self.browser.GetMainFrame().LoadUrl(url)
        else:
            self.url = url

    def get_browser(self):
        return self.browser

    def on_set_focus(self, event):
        cef.WindowUtils.OnSetFocus(self.GetHandle(), 0, 0, 0)
        event.Skip()

    def on_size(self, event):
        if not self.browser:
            return
        if platform.system() == "Windows":
            cef.WindowUtils.OnSize(self.browser_panel.GetHandle(), 0, 0, 0)
        else:
            (x, y) = (0, 0)
            (width, height) = event.GetSize()
            self.browser.SetBounds(x, y, width, height)
        self.browser.NotifyMoveOrResizeStarted()

    def on_close(self, event):
        if not self.browser:
            return

        self.browser.ParentWindowWillClose()
        event.Skip()
        self.browser = None
