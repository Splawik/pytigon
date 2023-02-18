from cefpython3 import cefpython as cef
import platform
import time
import http.client
import asyncio
from pytigon.pytigon_request import request as pytigon_request, init
import sys
import ctypes

LOADER = """   
    <style>
        .centered {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
    </style>
    <p class="centered">Loading ...</img>
"""


def exists(site, path="/"):
    if "127.0.0.2" in site:
        return True
    try:
        conn = http.client.HTTPConnection(site.split("//")[1])
        conn.request("HEAD", path)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
    except:
        False


def check_versions():
    ver = cef.GetVersion()
    print("[pytigon] CEF Python {ver}".format(ver=ver["version"]))
    print("[pytigon] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[pytigon] CEF {ver}".format(ver=ver["cef_version"]))
    print(
        "[pytigon] Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]
        )
    )
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


class KeyEvent:
    def __init__(self, event):
        self.event = event
        m = event["modifiers"]
        if m & 2:
            self.shift_down = True
        else:
            self.shift_down = False
        if m & 4:
            self.control_down = True
        else:
            self.control_down = False
        if m & 8:
            self.alt_down = True
        else:
            self.alt_down = False

        self.KeyCode = event["windows_key_code"]

    def AltDown(self):
        return self.alt_down

    def ControlDown(self):
        return self.control_down

    def ShiftDown(self):
        return self.shift_down

    def Skip(self):
        pass


class ClientHandler:
    _resourceHandlers = {}
    _resourceHandlerMaxId = 0

    close = False

    def OnBeforeClose(self, browser):
        self.close = True

    def GetResourceHandler(self, browser, frame, request):
        if not "127.0.0.2" in request.GetUrl():
            return None
        resHandler = ResourceHandler()
        resHandler._clientHandler = self
        resHandler._browser = browser
        resHandler._frame = frame
        resHandler._request = request
        self._AddStrongReference(resHandler)
        return resHandler

    def _AddStrongReference(self, resHandler):
        self._resourceHandlerMaxId += 1
        resHandler._resourceHandlerId = self._resourceHandlerMaxId
        self._resourceHandlers[resHandler._resourceHandlerId] = resHandler

    def _ReleaseStrongReference(self, resHandler):
        if resHandler._resourceHandlerId in self._resourceHandlers:
            del self._resourceHandlers[resHandler._resourceHandlerId]
        else:
            print(
                "_ReleaseStrongReference() FAILED: resource handler "
                "not found, id = %s" % (resHandler._resourceHandlerId)
            )


class ResourceHandler:
    _resourceHandlerId = None
    _clientHandler = None
    _browser = None
    _frame = None
    _request = None
    _responseHeadersReadyCallback = None
    _web_request = None
    _web_request_client = None
    _offsetRead = 0

    def ProcessRequest(self, request, callback):
        self._responseHeadersReadyCallback = callback
        self._web_request_client = WebRequestClient()
        self._web_request_client._resourceHandler = self
        request.SetFlags(
            cef.Request.Flags["AllowCachedCredentials"]
            | cef.Request.Flags["AllowCookies"]
        )
        self._web_request = cef.WebRequest.Create(request, self._web_request_client)
        return True

    def GetResponseHeaders(self, response, responseLengthOut, redirect_url_out):
        assert self._web_request_client._response, "Response object empty"
        wrcResponse = self._web_request_client._response
        response.SetStatus(wrcResponse.GetStatus())
        response.SetStatusText(wrcResponse.GetStatusText())
        response.SetMimeType(wrcResponse.GetMimeType())
        if wrcResponse.GetHeaderMultimap():
            response.SetHeaderMultimap(wrcResponse.GetHeaderMultimap())
        responseLengthOut[0] = self._web_request_client._dataLength
        if not responseLengthOut[0]:
            pass

    def ReadResponse(self, data_out, bytes_to_read, bytes_read_out, callback):
        if self._offsetRead < self._web_request_client._dataLength:
            dataChunk = self._web_request_client._data[
                self._offsetRead : (self._offsetRead + bytes_to_read)
            ]
            self._offsetRead += len(dataChunk)
            data_out[0] = dataChunk
            bytes_read_out[0] = len(dataChunk)
            return True

        self._clientHandler._ReleaseStrongReference(self)
        print("no more data, return False")
        return False

    def CanGetCookie(self, cookie):
        # Return true if the specified cookie can be sent
        # with the request or false otherwise. If false
        # is returned for any cookie then no cookies will
        # be sent with the request.
        return True

    def CanSetCookie(self, cookie):
        # Return true if the specified cookie returned
        # with the response can be set or false otherwise.
        return True

    def Cancel(self):
        # Request processing has been canceled.
        pass


class WebRequestClient:
    _resourceHandler = None
    _data = ""
    _dataLength = -1
    _response = None

    def OnUploadProgress(self, web_request, current, total):
        pass

    def OnDownloadProgress(self, web_request, current, total):
        pass

    def OnDownloadData(self, web_request, data):
        self._data += data

    def OnRequestComplete(self, web_request):
        statusText = "Unknown"
        if web_request.GetRequestStatus() in cef.WebRequest.Status:
            statusText = cef.WebRequest.Status[web_request.GetRequestStatus()]
        self._response = web_request.GetResponse()
        if web_request.GetRequest().GetMethod() == "POST":
            params = web_request.GetRequest().GetPostData()
            ret = pytigon_request(web_request.GetRequest().GetUrl(), params)
        else:
            ret = pytigon_request(web_request.GetRequest().GetUrl(), None)

        self._data = ret.ptr()
        self._dataLength = len(self._data)

        self._resourceHandler._responseHeadersReadyCallback.Continue()


def create_browser(
    url=None, title="Pytigon", parent_win=None, x=200, y=200, width=1024, height=768
):

    info = cef.WindowInfo()
    if parent_win:
        info.SetAsChild(parent_win.Handle, [x, y, x + width, y + height])
    else:
        info.SetAsChild(0, [x, y, x + width, y + height])

    browser = cef.CreateBrowserSync(
        window_info=info, url=cef.GetDataUrl(LOADER), window_title=title
    )

    if platform.system() == "Windows":
        window_handle = browser.GetOuterWindowHandle()
        insert_after_handle = 0
        SWP_NOMOVE = 0x0002
        ctypes.windll.user32.SetWindowPos(
            window_handle, insert_after_handle, 0, 0, 900, 640, SWP_NOMOVE
        )

    client_handler = ClientHandler()

    browser.SetClientHandler(client_handler)

    if url:
        while True:
            test = exists(url)
            if test:
                break
            else:
                print("wait")
                time.sleep(1)

        browser.LoadUrl(url)

    return browser, client_handler


async def run_async(
    url, title="Pytigon", parent_win=None, x=200, y=200, width=1024, height=768
):
    def py_function(value, js_callback):
        url = value[0]
        params = value[1]
        url2 = url.replace("file:///home/sch/prj/pytigon/pytigon", "http://127.0.0.2")
        print(url2, params)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2")
        # print(url, url2)
        ret = request(url2 + "/", params)
        # print(ret.str())
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3")
        # ret = "Hello world!"
        ret = (
            """<base href="file:///home/sch/prj/pytigon/pytigon/" target="_blank">"""
            + ret.str()
        )
        ret = ret.replace(
            "window.BASE_PATH = '/'",
            "window.BASE_PATH = 'file:///home/sch/prj/pytigon/pytigon/'",
        )
        js_callback.Call(ret, py_callback)

    def py_callback(value):
        print("Value sent from Javascript: " + value)

    browser, client_handler = create_browser(
        None, title, parent_win, x, y, width, height
    )

    bindings = cef.JavascriptBindings()
    bindings.SetFunction("py_function", py_function)
    bindings.SetFunction("py_callback", py_callback)
    browser.SetJavascriptBindings(bindings)

    for i in range(0, 10):
        cef.MessageLoopWork()
        await asyncio.sleep(0.01)

    browser.LoadUrl(url)

    async def loop():
        nonlocal client_handler
        while not client_handler.close:
            cef.MessageLoopWork()
            await asyncio.sleep(0.01)

    await loop()

    del browser


def initialize():
    check_versions()
    sys.excepthook = cef.ExceptHook

    settings = {
        "debug": False,
        "log_severity": cef.LOGSEVERITY_DISABLE,  # cef.LOGSEVERITY_INFO,
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
    switches = {
        # "disable-gpu": "1",
        "no-proxy-server": "1",
        "disable-web-security": "1",
    }

    cef.Initialize(settings, switches=switches)


def shutdown():
    cef.Shutdown()


def run(
    url, app, title="Pytigon", parent_win=None, x=200, y=200, width=1024, height=768
):
    initialize()
    init(app, "auto", "anawa")
    asyncio.run(run_async(url, title, parent_win, x, y, width, height))
    shutdown()
