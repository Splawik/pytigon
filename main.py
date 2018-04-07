import kivy
from kivy.app import App                                                                        
from kivy.lang import Builder                                                                   

from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.properties import NumericProperty

from kivy.utils import platform                                                                 
from kivy.clock import Clock                                                                    
from kivy.uix.spinner import Spinner
from kivy.uix.scatter import Scatter
from kivy.graphics.svg import Svg

import os
import socket
import time

from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread, Runnable

PytigonWebViewFragment = autoclass('tk.pytigon.libpytigon.PytigonWebViewFragment')
ACTIVITY = autoclass('org.kivy.android.PythonActivity').mActivity                              
SERVICE = None
CTX  = None
MAX_SEL_APP = 10
FRAGMENT = False


p1 = p2 = None
if 'SECONDARY_STORAGE' in os.environ:
    p1 = os.path.join(os.environ['SECONDARY_STORAGE'], ".pytigon")
if 'EXTERNAL_STORAGE' in os.environ:
    p2 = os.path.join(os.environ['EXTERNAL_STORAGE'], ".pytigon")
if p1:
    if os.path.exists(p2):
        STORAGE = p2[:-8]
    else:
        STORAGE = p1[:-8]
else:
    STORAGE = p2[:-8]


class PytigonWebViewClientCallback(PythonJavaClass):
    __javainterfaces__ = [ 'tk/pytigon/libpytigon/PytigonWebViewClientCallback' ]
    __javacontext__ = 'app'
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
    def onPageFinished(self, view, url):        
        print("python:pytigon:X1")
        self.parent.on_page_finish(view, url)

    @java_method('()V')
    def onDestroy(self):
        self.parent.on_fragment_finished()

Builder.load_string(''' 
<InterfaceManager>:
    canvas.before:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center

    canvas.after:
        PopMatrix
''')

class InterfaceManager(BoxLayout):
    angle = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        base_path = os.path.dirname(os.path.abspath(__file__))        

        self.base_path = base_path
        
        self.webview = None
        self.app = None
        self.timer = None
        self.show_first_form()

    def  show_first_form(self):
        global STORAGE
        x = [ pos for pos in os.listdir(os.path.join(os.path.join(STORAGE, "pytigon"), "app_pack")) if not pos.startswith('_')  ]
        print("python:Pytigon:F0:", os.path.join(os.path.join(STORAGE, "pytigon"), "app_pack"))
        if len(x)>1:             
            print("python:Pytigon:F1")
            if len(x)>MAX_SEL_APP:
                dy = MAX_SEL_APP - 1
            else:
                dy = len(x)
        
            for pos in x[:dy]:
                button = Button(id=pos, text=pos, size_hint=(1,1))
                button.bind(on_press=self.chose_callback)
                self.add_widget(button)

            if len(x)>MAX_SEL_APP:
                spinner = Spinner(
                    text='Other applications',
                    values= x[dy:],
                    size_hint=(.5, 1),
                    pos_hint={'center_x': 0.5, }
                    )
                spinner.bind(text=self.spinner_callback)
                self.add_widget(spinner)
        else:
            print("python:Pytigon:F2", x)            
            if len(x)>0:
                print("python:Pytigon:F3")
                self.on_app_chosen(x[0])
            else:
                print("python:Pytigon:F4")
                self.on_app_chosen()
        

    def show_second_form(self):
        self.clear_widgets() 
        self.img = Image( size_hint = (0.5, 0.5), pos_hint = {'center_x': 0.5, 'center_y': 0.5}, source = 'loader.png')
        self.add_widget(self.img)
        anim = Animation(angle = -360, duration=2) 
        anim += Animation(angle = -360, duration=2)
        anim.repeat = True
        anim.start(self)

    def spinner_callback(self, spinner, text):                
        self.on_app_chosen(text)
    
    def chose_callback(self, instance):
        self.on_app_chosen(instance.id)

    def on_app_chosen(self, app="schdevtools"):
        #self.show_second_form()
        self.app = app
        #def _start_service():
        #    self.start_service()
        #Runnable(_start_service)()        
        #Clock.schedule_interval(self.on_clock, 0.5)
        
        def _create_webview():
            self.create_webview()
        Runnable(_create_webview)()

    def on_clock(self, dt):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',8000))
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
        SERVICE = autoclass('tk.pytigon.ServicePytigon')
        CTX = autoclass('org.kivy.android.PythonActivity').mActivity
        CTX.nativeSetEnv("PYTIGON_APP", self.app)
        SERVICE.start(CTX, self.app)


    def create_webview(self):
        global FRAGMENT
        callback = PytigonWebViewClientCallback(self)
        fragment = PytigonWebViewFragment()
        start_url = "file://"+self.base_path+"/static/android/loader.html"
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
        
    def on_page_finish(self, view, url):
        print("python:Pytigon:XXXXXX1", url)

    def on_fragment_finished(self):
        global FRAGMENT
        FRAGMENT = False
        if SERVICE:
            SERVICE.stop(CTX)

    def on_angle(self, item, angle):
        if angle == -360:
            item.angle = 0


class PytigonApp(App):
    def build(self):
        self.bind(on_start=self.post_build_init)
        return InterfaceManager(orientation='vertical', padding=(10), spacing=(20))


    def post_build_init(self, ev):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)


    def hook_keyboard(self, window, key, *largs):
        global FRAGMENT
        if key == 27:
            if FRAGMENT:
                ACTIVITY.getFragmentManager().popBackStack()
                return True
            else:
                return False

    def on_stop(self):
        print("python:Pytigon:on_stop")
        

PytigonApp().run()
if SERVICE:
    SERVICE.stop(CTX)
