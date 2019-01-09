from schlib.schandroid.android_client import InterfaceManager, PytigonApp

import socket
import fcntl
import struct

from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread, Runnable


PytigonWebViewFragment = autoclass("cloud.pytigon.libpytigon.PytigonWebViewFragment")
ACTIVITY = autoclass("org.kivy.android.PythonActivity").mActivity
SERVICE = None
CTX = None
FRAGMENT = False


class PytigonWebViewClientCallback(PythonJavaClass):
    __javainterfaces__ = ["cloud/pytigon/libpytigon/PytigonWebViewClientCallback"]
    __javacontext__ = "app"

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    @java_method("(Landroid/webkit/WebView;Ljava/lang/String;)V")
    def onPageFinished(self, view, url):
        print("python:pytigon:X1")
        self.parent.on_page_finish(view, url)

    @java_method("()V")
    def onDestroy(self):
        self.parent.on_fragment_finished()


class InterfaceManager2(InterfaceManager):
    def on_app_chosen(self, app="schdevtools"):
        super().on_app_chosen(app)

        def _create_webview():
            self.create_webview()

        Runnable(_create_webview)()

    def on_clock(self, dt):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", 8000))
        print("python:pytigon:clock")

        if result == 0:

            def _create_webview():
                self.create_webview()

            Runnable(_create_webview)()

            return False
        else:
            return True

    def start_service(self):
        global SERVICE, CTX
        SERVICE = autoclass("cloud.pytigon.ServicePytigon")
        CTX = autoclass("org.kivy.android.PythonActivity").mActivity
        CTX.nativeSetEnv("PYTIGON_APP", self.app)
        SERVICE.start(CTX, self.app)

    def create_webview(self):
        global FRAGMENT
        callback = PytigonWebViewClientCallback(self)
        fragment = PytigonWebViewFragment()
        start_url = "file://" + self.base_path + "/static/android/loader.html"
        fragment.set_callback_info(callback, self.base_path, start_url, self.app)

        fragmentManager = ACTIVITY.getFragmentManager()
        fragmentTransaction = fragmentManager.beginTransaction()
        v = ACTIVITY.getWindow().getDecorView().getRootView()
        v.setId(1234)
        fragmentTransaction.add(1234, fragment, "PytigonWebView")
        fragmentTransaction.addToBackStack("PytigonFrag")
        fragmentTransaction.commit()
        FRAGMENT = True

        def _start_service():
            self.start_service()

        Runnable(_start_service)()

    def on_fragment_finished(self):
        global FRAGMENT
        FRAGMENT = False
        if SERVICE:
            SERVICE.stop(CTX)


class PytigonApp2(PytigonApp):
    def build(self):
        self.bind(on_start=self.post_build_init)
        return InterfaceManager2(orientation="vertical", padding=(10), spacing=(20))

    def hook_keyboard(self, window, key, *largs):
        global FRAGMENT
        if key == 27:
            if FRAGMENT:
                ACTIVITY.getFragmentManager().popBackStack()
                return True
            else:
                return False


PytigonApp2().run()
if SERVICE:
    SERVICE.stop(CTX)
