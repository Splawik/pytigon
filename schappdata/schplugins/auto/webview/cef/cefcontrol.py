# Additional wx specific layer of abstraction for the cefpython
# __author__ = "Greg Kacy <grkacy@gmail.com>"

#-------------------------------------------------------------------------------

import platform
import os, sys
from cefpython import cefpython_py35 as cefpython

import wx

def GetApplicationPath(file=None):
    import re, os
    # If file is None return current directory without trailing slash.
    if file is None:
        file = ""
    # Only when relative path.
    if not file.startswith("/") and not file.startswith("\\") and (
            not re.search(r"^[\w-]+:", file)):
        if hasattr(sys, "frozen"):
            path = os.path.dirname(sys.executable)
        elif "__file__" in globals():
            path = os.path.dirname(os.path.realpath(__file__))
        else:
            path = os.getcwd()
        path = path + os.sep + file
        path = re.sub(r"[/\\]+", re.escape(os.sep), path)
        path = re.sub(r"[/\\]+$", "", path)
        return path
    return str(file)

def ExceptHook(excType, excValue, traceObject):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
    import traceback, os, time, codecs
    # This hook does the following: in case of exception write it to
    # the "error.log" file, display it to the console, shutdown CEF
    # and exit application immediately by ignoring "finally" (_exit()).
    errorMsg = "\n".join(traceback.format_exception(excType, excValue,
            traceObject))
    errorFile = GetApplicationPath("error.log")
    try:
        appEncoding = cefpython.g_applicationSettings["string_encoding"]
    except:
        appEncoding = "utf-8"
    if type(errorMsg) == bytes:
        errorMsg = errorMsg.decode(encoding=appEncoding, errors="replace")
    try:
        with codecs.open(errorFile, mode="a", encoding=appEncoding) as fp:
            fp.write("\n[%s] %s\n" % (
                    time.strftime("%Y-%m-%d %H:%M:%S"), errorMsg))
    except:
        print("cefpython: WARNING: failed writing to error file: %s" % (
                errorFile))
    # Convert error message to ascii before printing, otherwise
    # you may get error like this:
    # | UnicodeEncodeError: 'charmap' codec can't encode characters
    errorMsg = errorMsg.encode("ascii", errors="replace")
    errorMsg = errorMsg.decode("ascii", errors="replace")
    print("\n"+errorMsg+"\n")
    cefpython.QuitMessageLoop()
    cefpython.Shutdown()
    os._exit(1)

#-------------------------------------------------------------------------------

TIMER_MILLIS = 10

#-------------------------------------------------------------------------------

class CEFControl(wx.Control):
    """Standalone CEF component. The class provides facilites for interacting with wx message loop"""
    def __init__(self, parent, url="", size=(-1, -1), *args, **kwargs):
        kwargs['style'] = wx.WANTS_CHARS
        wx.Control.__init__(self, parent, id=wx.ID_ANY, size=size, *args, **kwargs)
        self.url = url
        windowInfo = cefpython.WindowInfo()
        windowInfo.SetAsChild(self.GetHandle())
        self.browser = cefpython.CreateBrowserSync(windowInfo,
            browserSettings={"plugins_disabled": False}, navigateUrl=url)

        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def GetBrowser(self):
        '''Returns the CEF's browser object'''
        return self.browser

    #def __del__(self):
     #   '''cleanup stuff'''
     #   self.timer.Stop()
     #   self.browser.CloseBrowser()

    def OnSetFocus(self, event):
        cefpython.WindowUtils.OnSetFocus(self.GetHandle(), 0, 0, 0)
        event.Skip()


    def OnSize(self, event):
        cefpython.WindowUtils.OnSize(self.GetHandle(), 0, 0, 0)

#-------------------------------------------------------------------------------
print("==============================")
print( cefpython.GetModuleDirectory() )

def initCEF(settings=None):
    sys.excepthook = ExceptHook
    if not settings:
        settings = {
            "debug": True,
            "log_severity": cefpython.LOGSEVERITY_INFO,
            "log_file": GetApplicationPath("debug.log"),
            "release_dcheck_enabled": True,
            "locales_dir_path": cefpython.GetModuleDirectory()+"/locales",
            "resources_dir_path": cefpython.GetModuleDirectory(),
            #"browser_subprocess_path": cefpython.GetModuleDirectory() + "/cefclient.exe",
            "browser_subprocess_path": cefpython.GetModuleDirectory() + "/subprocess_32bit.exe",
            #'no_sandbox': True,
            "unique_request_context_per_browser": True,
            "downloads_enabled": True,
            "remote_debugging_port": 0,
            "context_menu": {
                "enabled": True,
                "navigation": True, # Back, Forward, Reload
                "print": True,
                "view_source": True,
                "external_browser": True, # Open in external browser
                "devtools": True, # Developer Tools
            },
            "ignore_certificate_errors": True,
            #"single_process": True,
        }
    cefpython.Initialize(settings)

def shutdownCEF():
    cefpython.Shutdown()

def loop():
    cefpython.MessageLoopWork()

def quit():
    cefpython.QuitMessageLoop()