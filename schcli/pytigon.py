#! /usr/bin/python3
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY  ; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

"""This is the main Pytigon client moudule. Function :func:`~schcli.pytigon.main` create SchApp object, witch extends wxPython wx.App.
Function :func:`~schcli.pytigon.main` process pytigon command line arguments. Module supports:

- instalation of pytigon applications,

- Remote Procedure Calling protocol

- login to server process
"""

import os
import sys
import time
import platform
import zipfile
import getopt
import configparser
from urllib.parse import urljoin

if platform.system() == "Windows":
    # grouping pytigon applicactions in the windows taskbar
    import ctypes

    myappid = 'slawomir_cholaj.pytigon.main.01'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

CWD_PATH = os.path.join(os.getcwd(), '..')
SCR_PATH = os.path.dirname(__file__)
if SCR_PATH == '':
    SCR_PATH = CWD_PATH
else:
    SCR_PATH = os.path.join(SCR_PATH, '..')

ROOT_PATH = SCR_PATH

if ROOT_PATH.startswith('.'):
    ROOT_PATH = CWD_PATH + '/' + ROOT_PATH
sys.path.append(ROOT_PATH)
sys.path.append(ROOT_PATH + '/schappdata')

os.environ["LD_LIBRARY_PATH"] = ROOT_PATH + '/ext_prg/tcc'

from schlib import init_paths

init_paths()

if platform.system() == "Windows":
    sys.path.insert(0, ROOT_PATH + '/ext_lib_cli_win')
else:
    sys.path.insert(0, ROOT_PATH + '/ext_lib_cli_lin')

_INSPECTION = False
_DEBUG = False
_TRACE = False
_VIDEO = False
_APP_SIZE = (1024, 768)
_RPC = False
_WEBSOCKET = None

def usage():
    print(process_argv.__doc__)

def process_argv(argv):
    """Run pytigon application: pytigon.py [option]... arg

    command line arguments:
        arg: application package name, schdevtools for example
             or address of http server, http://www.pytigon.cloud for example
             or pytigon script name, test.schdevtools.schsimplescripts.ptig for example
             or pytigon installation file name
             or django management command in format: manage_[[package name]], manage_schdevtools runserver for example
             or python script, test.py for example

        options:
            -h, --help - show help

            -b --embededbrowser - run embeded browseer window
            -s --embededserver - run in background embeded http server
            -m --menu_always - show menu event then configuration says otherwise
            --no_splash - do not show splash window
            --no_gui - run program without gui
            --server_only - run only http server
            --channels - start with channels library
            --websocket_id=relative address - embed websocket client, address can be mulitipart,
                           parts separated by a semicolon
            --no_gui - run program without gui

            --migrate - run django command: manage.py migrate
            --loaddb - run django command: manage.py loaddb

            --rpc=<port> - set tcp port of rpc
            --video - record video session

            -p <parameters>, --param=<parameters> - parametres of request to http server

            -d --debug - debug mode
            --inspection - turn on wxPython inspection
            --trace - show trace of python calls
    """
    try:
        (opts, args) = getopt.getopt(argv, 'h:dmpbsu:p:', [
            'help',
            'username=',
            'password=',
            'embededbrowser',
            'embededserver',
            'websocket_id=',
            'channels',
            'migrate',
            'loaddb',
            'server_only',
            'debug',
            'rpc=',
            'param=',
            'inspection',
            'trace',
            'video',
            'no_gui',
            'no_splash',
            'menu_always',
        ])
    except getopt.GetoptError:
        usage()
        return None

    ret = { 'args': args}

    for (opt, arg) in opts:
        if opt in ('-h', '--help'):
            usage()
            return None
        elif opt == '--migrate':
            ret['sync'] = True
        elif opt == '--loaddb':
            ret['loaddb'] = True
        elif opt == '--server_only':
            ret['server_only'] = True
        elif opt in ('-u' '--username'):
            ret['username'] = arg
        elif opt in ('-p' '--password'):
            ret['password'] = arg
        elif opt in ('-b' '--embededbrowser'):
            ret['embeded_browser'] = True
        elif opt in ('-s', '--embededserver'):
            ret['address'] = 'embeded'
            ret['extern_app_set'] = True
        elif opt == '--no_gui':
            ret['nogui'] = True
        elif opt in ('-m', '--menu_always'):
            ret['menu_always'] = True
        elif opt in ('--rpc'):
            ret['rpc'] = int(arg)
        elif opt in ('-p', '--param'):
            ret['param'] = arg
        elif opt in ('--channels'):
            ret['channels'] = True
        elif opt in ('--websocket_id',):
            ret['websocket'] = arg
        elif opt in ('--no_splash'):
            ret['no_splash'] = True
        elif opt in ('-d', '--debug'):
            global _DEBUG
            _DEBUG = True
        elif opt in ('--inspection',):
            global _INSPECTION
            _INSPECTION = True
        elif opt in ('--trace',):
            global _TRACE
            _TRACE = True
        elif opt in ('--video',):
            global _VIDEO, _APP_SIZE
            _APP_SIZE = (1280, 720)
            _VIDEO = True
    return ret

_PARAM = process_argv(sys.argv[1:])
if _PARAM == None:
    sys.exit(0)

from schserw import settings as schserw_settings

sys.path.append(schserw_settings.APP_PACK_PATH)

from schlib.schtools.install_init import init
init("_schall", schserw_settings.ROOT_PATH, schserw_settings.DATA_PATH, schserw_settings.APP_PACK_PATH, schserw_settings.STATIC_APP_ROOT, [schserw_settings.MEDIA_ROOT, schserw_settings.UPLOAD_PATH])

import wx
_ = wx.GetTranslation

def process_adv_argv():
    global _PARAM
    if not ('args' in _PARAM and len(_PARAM['args']) > 0):
        _app = wx.App()

        choices = [ff for ff in os.listdir(schserw_settings.APP_PACK_PATH + "/") if not ff.startswith('_')]
        dlg = wx.SingleChoiceDialog(None, _('select the application to run'), _("Pytigon"), choices,wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            arg = dlg.GetStringSelection()
            dlg.Destroy()

        else:
            dlg.Destroy()
            sys.exit(0)

        _app.MainLoop()
        _app = None

    else:
        arg = _PARAM['args'][0].strip()
    if not (arg == 'embeded' or '.' in arg or '/' in arg):
        CWD_PATH = schserw_settings.APP_PACK_PATH + "/" + arg
        if not os.path.exists(os.path.join(CWD_PATH, "settings_app.py")):
            print(_("Application pack: '%s' does not exists") % arg)
            sys.exit(0)
        else:
            sys.path.insert(0, CWD_PATH)
            try:
                from apps import GUI_COMMAND_LINE
                x = GUI_COMMAND_LINE.split(' ')
                param = process_argv(x)
                for key, value in param.items():
                    if not key in _PARAM:
                        _PARAM[key] = value
            except:
                pass

process_adv_argv()

if 'channels' in _PARAM or 'rpc' in _PARAM:
    from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
    import asyncio
    from asyncio.events import get_event_loop

    class SChAsyncApp(WxAsyncApp):
        async def MainLoop(self):
            evtloop = wx.GUIEventLoop()
            with wx.EventLoopActivator(evtloop):
                while not self.exiting:
                    if platform.system() == "Darwin":
                        evtloop.DispatchTimeout(0)
                    else:
                        while self.HasPendingEvents():
                            self.ProcessPendingEvents()
                        while evtloop.Pending():
                            evtloop.Dispatch()
                    await asyncio.sleep(0.005)
                    evtloop.ProcessIdle()


from schcli.guilib import image
from schcli.guilib import pytigon_install
from schcli.guilib.logindialog import LoginDialog
from schcli.guiframe import appframe
from schcli.guilib.threadwindow import SchThreadManager
from schlib.schfs.vfstools import extractall
from schlib.schparser.html_parsers import SimpleTabParser
from schcli.guilib.tools import standard_tab_colour, colour_to_html
from schlib.schhttptools import httpclient
from schcli.guilib.httperror import http_error
from schcli.guiframe import browserframe
from schlib.schtools import createparm
from schlib.schparser.html_parsers import ShtmlParser
import schcli.guictrl.tag

if 'rpc' in _PARAM or 'websocket' in _PARAM:
    import twisted.internet.asyncioreactor
    twisted.internet.asyncioreactor.install()

    from twisted.internet import reactor
    import twisted
    if 'rpc' in _PARAM:
        from twisted.web import xmlrpc, server
        _RPC = True
    if 'websocket' in _PARAM:
        from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
        _WEBSOCKET = _PARAM['websocket']

if not 'channels' in _PARAM:
    os.environ['PYTIGON_WITHOUT_CHANNELS'] = "1"

# import gc
# gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)
# gc.disable()

wx.RegisterId(10000)
wx.outputWindowClass = None

if _INSPECTION:
    import wx.lib.mixins.inspection

    App = wx.lib.mixins.inspection.InspectableApp

    if _TRACE:
        def trace_calls(frame, event, arg):
            if event != 'call':
                return
            co = frame.f_code
            func_name = co.co_name
            if func_name == 'write':
                # Ignore write() calls from print statements
                return
            for pos in ('process_window_event', 'idle', 'timer', 'update_ui'):
                if pos in func_name:
                    return
            if 'process_window_event' in func_name or 'idle' in func_name or 'idle' in func_name:
                return
            func_line_no = frame.f_lineno
            func_filename = co.co_filename
            if not 'wx/core' in func_filename:
                return
            caller = frame.f_back
            caller_line_no = caller.f_lineno
            caller_filename = caller.f_code.co_filename
            print('Call to %s on line %s of %s from line %s of %s' % \
                  (func_name, func_line_no, func_filename,
                   caller_line_no, caller_filename))
            return


        sys.settrace(trace_calls)

else:
    if 'channels' in _PARAM or 'rpc' in _PARAM:
        App = SChAsyncApp
    else:
        App = wx.App

if _RPC:
    _BASE_APP = xmlrpc.XMLRPC
else:
    class _base:
        pass

    _BASE_APP = _base


class SchApp(App, _BASE_APP):
    """It is a subclass of wxPython wx.App. Depending on the command line parameters it is also subclass of
    xmlrpc.XMLRPC and wx.lib.mixins.inspection.InspectableApp.
    """

    def __init__(self):
        """Construct an application."""
        global _PARAM
        App.__init__(self)
        if _RPC:
            xmlrpc.XMLRPC.__init__(self)

        if not 'no_splash' in _PARAM and not 'nogui' in _PARAM and not 'server_only' in _PARAM:
            bitmap = wx.Bitmap(SCR_PATH + '/pytigon_splash.jpeg', wx.BITMAP_TYPE_JPEG)
            splash = wx.adv.SplashScreen(bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                         100, None, -1, wx.DefaultPosition, wx.DefaultSize,
                                         wx.BORDER_SIMPLE | wx.STAY_ON_TOP)
            splash.Update()
            wx.Yield()

        config_name = os.path.join(SCR_PATH, "pytigon.ini")
        self.config = configparser.ConfigParser()
        self.config.read(config_name)

        self.app_size = _APP_SIZE

        self.locale = None
        self.ext_app = []
        self.ext_app_http = {}
        self.lock = None

        self.base_address = None

        self.scr_path = SCR_PATH
        self.root_path = ROOT_PATH
        self.cwd_path = CWD_PATH

        self.http = None
        self.images = None
        self.mp = None

        self.server = None
        self.cwd = None
        self.inst_dir = None
        self.start_pages = []

        self.csrf_token = None
        self.title = None
        self.plugins = None
        self.extern_data = {}

        self.thread_manager = None
        self.task_manager = None

        self.menu_always = False
        self.authorized = False
        self.rpc = None
        self.websockets = {}

        self.gui_style = \
            'app.gui_style = tree(toolbar(file(exit,open),clipboard, statusbar))'

        self.COLOUR_HIGHLIGHT = \
            colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.COLOUR_BACKGROUND = \
            colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.COLOUR_SHADOW = \
            colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW))
        self.COLOUR_DKSHADOW = \
            colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.COLOUR_ACTIVECATPION = \
            colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.COLOUR_INFOBK = \
            colour_to_html(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))

        self.ctrl_process = {}

    def register_ctrl_process_fun(self, tag, fun):
        """Register function, which is called when widget connected to the specified tag is created.

        Args:
            tag: it must be the name of class in schcli/guictrl/schctrl typed in lowercase, preceded by "ctrl".
            For example: ctrlgrid, ctrltable, ctrllistbox are valid tag names.

            fun: a callback function with is called with one parameter - widget defined in schcli/guictrl/schctrl instance.

        Returns:
            None

        Example:
            see: schappdata/schplugins/standard/keymap/__init__.py
        """

        if tag in self.ctrl_process:
            self.ctrl_process[tag].append(fun)
        else:
            self.ctrl_process[tag] = [fun, ]

    # some XML-RPC function calls for twisted server
    def xmlrpc_stop(self):
        """Closes the wx application."""
        self.frame.Close()  # Sending closing event
        return 'Shutdown initiated'

    def xmlrpc_title(self, title):
        """Set the main window title

        Args:
            title - new title of application top window
        """
        self.GetTopWindow().SetTitle(title)
        return title

    def get_locale_object(self):
        """Get locale object

        Returns:
            application wx.Locale object
        """
        return self.locale

    def _init2(self, address, app):
        self.base_address = address
        self.base_app = app
        if self.base_app:
            self.base_path = urljoin(self.base_address, self.base_app)
        else:
            self.base_path = self.base_address
        if app and app != '':
            href = "/" + app + "/"
        else:
            href = "/"

        self.http = httpclient.AppHttp(address+"/", self)
        ret, newaddr = self.http.get(self, href)
        if ret != 200:
            if not login(href, auth_type='basic'):
                return 0
            else:
                self.authorized = True
            ret, newaddr = self.http.get(href, "/")

        if ret != 200:
            return ret

        if app and app != '':
            self.images = image.SchImage('/' + app + '/site_media/app.png')
            self.http.get(self, '/' + app + '/')
        else:
            self.images = image.SchImage('/site_media/app.png')
            self.http.get(self, '/')
        ret_str = self.http.str()
        self.mp = SimpleTabParser()
        self.mp.feed(ret_str)
        self.mp.close()
        self.http.clear_ptr()

        return ret

    def _re_init(self, address, app):
        self.base_address = address
        self.base_app = app
        if self.base_app:
            self.base_path = urljoin(self.base_address, self.base_app)
        else:
            self.base_path = self.base_address

        if app and app != '':
            self.http.get(self, '/' + app + '/')
        else:
            self.http.get(self, '/')
        ret = self.http.str()
        self.mp = SimpleTabParser()
        self.mp.feed(ret)
        self.mp.close()
        self.http.clear_ptr()

    def make_href(self, href):
        if self.base_app and href.startswith('/'):
            return '/' + self.base_app + href
        else:
            return href

    def SetTopWindow(self, frame):
        wx.App.SetTopWindow(self, frame)
        icon = wx.Icon(SCR_PATH + '/pytigon.ico', wx.BITMAP_TYPE_ICO)
        frame.SetIcon(icon)

        if hasattr(frame, 'statusbar') and frame.statusbar:
            self.thread_manager = SchThreadManager(self, frame.statusbar)
        if _INSPECTION:
            self.ShowInspectionTool()

    def register_extern_app(self, address, app):
        self.ext_app.append((app, address))

    def get_http_for_adr(self, address):
        for app in self.ext_app:
            if address.upper().startswith(app[1]):
                if app[0] in self.ext_app_http:
                    return self.ext_app_http[app[0]]
                else:
                    http = httpclient.AppHttp(app[1], app[0])
                    self.exft_app_http[app[0]] = http
                    return http
        return self.http

    def get_http(self, win):
        """Get :class:`~schlib.schhttptools.httpclient.HttpClient` object

        With returned object you can directly make requests to http server.

        Args:
            win - wx.Window derived object

        Returns:
            :class:`~schlib.schhttptools.httpclient.HttpClient` object
        """
        winparent = win
        while winparent:
            if hasattr(winparent, 'get_app_http'):
                return winparent.get_app_http()
            winparent = winparent.GetParent()
        return self.http

    def read_html(self, win, address_or_parser, parameters):
        """Prepare request to http server and read result

        Args:
            win: wx.Window derived object
            address_or_parser: can be: address of http page (str type) or
            :class:'~schlib.schparser.html_parsers.ShtmlParser'
            parameters: dict

        Returns :class:'~schlib.schparser.html_parsers.ShtmlParser' object
        """
        if type(address_or_parser) == str:
            http = self.get_http(win)

            if parameters and type(parameters) == dict:
                adr = address_or_parser
                (err, url) = http.post(self, adr, parm=parameters)
            else:
                if parameters:
                    adrtmp = createparm.create_parm(address_or_parser, parameters)
                    if adrtmp:
                        adr = adrtmp[0] + adrtmp[1] + adrtmp[2]
                    else:
                        adr = address_or_parser
                else:
                    adr = address_or_parser
                (err, url) = http.get(win, adr)
            if err == 404:
                raise Exception('http', '404')
            ptr = http.str()
            mp = ShtmlParser()
            mp.process(ptr, address_or_parser)
            mp.address = adr
            http.clear_ptr()
        else:
            adr = None
            if address_or_parser:
                mp = address_or_parser
            else:
                mp = ShtmlParser()
                mp.process('<html><body></body></html>')
                mp.address = None
        return (mp, adr)

    def get_tab(self, nr):
        """Return setup tab

        When pytigon client connect to server it receive html page with few configuration tables.
        This function return rendered table.

        Args:
            nr: table number

        Returns:
            table - :class:'~schlib.schparser.html_parsers.SimpleTabParser' object

        """
        return self.mp.tables[nr]

    # def get_active_window(self):
    #    return self.GetTopWindow()

    # def get_main_windows(self):
    #    return [self.GetTopWindow()]

    # def append_thread(self, thread_address):
    #    if self.thread_manager:
    #        self.thread_manager.append(thread_address)

    # def timer(self):
    #    if self.thread_manager:
    #        self.thread_manager.timer()

    def get_working_dir(self):
        """return pytigon working director - ~/.pytigon"""
        return os.path.join(os.path.expanduser('~'), '.pytigon/')

    def _get_parm_for_server(self):
        ret = ''
        for pos in standard_tab_colour():
            ret = ret + pos[0] + ':' + pos[1] + ','
        return ret[:-1].replace('#', '')

    def _install_plugins(self):
        home_dir = self.get_working_dir()
        p = self.plugins
        if p:
            sys.path.append(home_dir)
            for plugin in p:
                if not '/' in plugin:
                    continue
                if plugin == '' or plugin.startswith('standard/'):
                    continue
                print(plugin)
                app_name = plugin.split('/')[0]
                plugin_name = plugin.split('/')[1]
                if plugin_name == 'install':
                    plugins_cache = ''
                else:
                    plugins_cache = 'plugins_cache/'
                if not os.path.exists(home_dir + plugins_cache + str(app_name)):
                    os.mkdir(home_dir + plugins_cache + str(app_name))
                    ini = open(home_dir + plugins_cache + str(app_name)
                               + '/__init__.py', 'w')
                    ini.write(' ')
                    ini.close()
                if not os.path.exists(home_dir + plugins_cache + str(plugin)
                                              + '.zip'):
                    http = wx.GetApp().http
                    http.get(self, '/schsys/plugins/' + str(plugin) + '/')
                    z_data = http.ptr()
                    x = open(home_dir + plugins_cache + str(plugin) + '.zip',
                             'wb')
                    x.write(z_data)
                    x.close()
                    http.clear_ptr()
                    zip_name = home_dir + plugins_cache + str(plugin) + '.zip'
                    extract_to = home_dir + plugins_cache + str(app_name)
                    zip_handle = zipfile.ZipFile(zip_name)
                    extractall(zip_handle, extract_to)
                    zip_handle.close()

    def on_exit(self):
        if self.task_manager:
            if len(self.task_manager.list_threads(all=False)) > 0:
                dlg = wx.MessageDialog(None, _("There are background tasks - kill?"), _("Warning"),
                                       wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_YES:
                    self.task_manager.kill_all()

    def run_script(self, app_name, script_path):
        with open(script_path, "rb") as s:
            wx.CallAfter(self.GetTopWindow().new_main_page, '/' + app_name + '/run_script/', "Run script",
                         {'script': s.read()})


    def on_websocket_connect(self, client, websocket_id, response):
        print("On websocket connected", websocket_id, response.peer)

    def on_websocket_open(self, client, websocket_id):
        print("On websocket open", websocket_id)

    def on_websocket_message(self, client, websocket_id, msg, binary):
        print("On websocket message:", websocket_id, msg, binary)

    def websocket_send(self, websocket_id, msg):
        if websocket_id in self.websockets:
            self.websocket[websocket_id].sendMessage(msg)

def login(base_href, auth_type=None, username = None):
    """Show login form"""
    dlg = LoginDialog(None, 101, _("Pytigon - login"), username=username)

    while dlg.ShowModal() == wx.ID_OK:

        username = dlg.text1.GetValue()
        password = dlg.text2.GetValue()

        parm = {'username': username,
                'password': password,
                'next': '/schsys/ok/',
                'client_param': wx.GetApp()._get_parm_for_server(),
                }

        if auth_type == None:
            wx.GetApp().http.post(wx.GetApp(), '/schsys/do_login/?from_pytigon=1', parm, credentials=(username, password))

            ret_str = wx.GetApp().http.str()
            if 'RETURN_OK' in ret_str:
                dlg.Destroy()
                return True
            else:
                if not 'id_password' in ret_str:
                    dlg.Destroy()
                    return False
                else:
                    dlg.message.SetLabel(_('Failed login attempt!'))
        else:
            ret, newaddr = wx.GetApp().http.get(wx.GetApp(), base_href, credentials=(username, password))
            if ret == 200:
                dlg.Destroy()
                return True
            else:
                dlg.message.SetLabel(_('Failed login attempt! http error: %s') % ret)
    dlg.Destroy()
    return False


def _main_init():
    global CWD_PATH, _PARAM, app

    args = _PARAM['args']
    apps = []
    address = 'http://127.0.0.2'
    app_title = _("Pytigon")
    app_name = ''

    app = SchApp()
    if 'menu_always' in _PARAM:
        app.menu_always = True
    if 'rpc' in _PARAM:
        app.rpc = int(_PARAM['rpc'])
    if 'param' in _PARAM:
        app.param = _PARAM['param']
    if 'embeded_browser' in _PARAM:
        app.embeded_browser = True
    else:
        app.embeded_browser = False
    if 'extern_app_set' in _PARAM:
        extern_app_set = True
    else:
        extern_app_set = False
    if 'address' in _PARAM:
        address = _PARAM['address']

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_app'

    if len(args) > 0:
        if '.ptig' in args[0].lower():
            prg_name = args[0].split('/')[-1].split('\\')[-1]
            x = prg_name.split('.')
            if len(x)==2 or ( len(x)>2 and x[-2].lower()=='inst'):
                prg_name2 = x[0]
                path = os.path.join(schserw_settings.APP_PACK_PATH, '_schremote')
                sys.path.append(path)
                if not pytigon_install.install(args[0], prg_name2):
                    return (None, None)
                #sys.path.remove(path)
                return (None, None)
                CWD_PATH = schserw_settings.APP_PACK_PATH + "/" + prg_name2
            else:
                if len(x)>3:
                    prg_name2 = x[0]
                    app_name2 = x[-2]
                    app_pack = x[-3]
                    CWD_PATH = schserw_settings.APP_PACK_PATH + "/" + app_pack.strip()
                    if not os.path.exists(os.path.join(CWD_PATH, "settings_app.py")):
                        print(_("Application pack: '%s' does not exists") % app_pack.strip())
                        return (None, None)
                    wx.CallAfter(app.run_script, app_name2, args[0])
                else:
                    print(_("Name of script: '%s' is not valid") % prg_name)
                    return (None, None)
        else:
            arg = args[0].strip()
            if arg == 'embeded' or '.' in arg or '/' in arg:
                if arg != 'embeded':
                    CWD_PATH = schserw_settings.APP_PACK_PATH + '/_schremote'

                tmp = arg.replace('//', '$$$')
                if '/' in arg:
                    x = tmp.split('/', 1)
                    address = x[0].replace('$$$', '//')
                    if len(x)>1:
                        app_name = x[1]
                        if app_name.endswith('/'):
                            app_name = app_name[:-1]
                else:
                    address = arg

                extern_app_set = True
            else:
                CWD_PATH = schserw_settings.APP_PACK_PATH + "/" + arg
                if not os.path.exists(os.path.join(CWD_PATH, "settings_app.py")):
                    print(_("Application pack: '%s' does not exists") % arg)
                    return (None, None)

    sys.path.insert(0, CWD_PATH)

    httpclient.init_embeded_django()

    if not ( 'channels' in _PARAM or 'rpc' in _PARAM):
        wx.Yield()

    import settings_app
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_app'
    from django.conf import settings
    if 'sync' in _PARAM:
        from django.core.management.commands.migrate import Command as migrate_command
        migrate = migrate_command()
        try:
            migrate.run_from_argv(['manage.py', 'migrate'])
        except SystemExit:
            pass
    if 'loaddb' in _PARAM:
        from django.core.management.commands.loaddata import Command as load_command
        load = load_command()
        try:
            load.run_from_argv(['manage.py', 'loaddata'])
        except:
            pass

    cwd = CWD_PATH
    inst_dir = SCR_PATH
    if inst_dir == '':
        inst_dir = cwd

    settings.TEMPLATES[0]['DIRS'].insert(0, inst_dir + '/schappdata/schplugins')
    settings.TEMPLATES[0]['DIRS'].insert(0, cwd + '/schappdata/schplugins')
    settings.TEMPLATES[0]['DIRS'].insert(0, inst_dir + '/../templates')
    settings.TEMPLATES[0]['DIRS'].insert(0, cwd + '/templates')

    for a in apps:
        settings.INSTALLED_APPS.append(a)

    port = 0
    if 'server_only' in _PARAM:
        port = 80
        if ':' in address:
            l = address.split(':')
            if len(l) == 3:
                port = int(l[2])
        address = 'embeded'
    if address == 'embeded':
        import socket
        from schlib.schdjangoext.server import run_server
        if 'server_only' in _PARAM:
            address = '127.0.0.1'
        else:
            address = '127.0.0.3'
        if port == 0:
            port = 8000
        test = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while test:
            try:
                s.bind((address, port))
                s.close()
                s = None
                test = False
            except:
                port += 1

        server = run_server(address, port, prod=False)
        address = 'http://' + address + ':' + str(port)
    else:
        from schlib.schtasks.base_task import get_process_manager
        app.task_manager = get_process_manager()
        server = None

    settings.BASE_URL = 'http://' + address
    settings.URL_ROOT_FOLDER = ''

    init_ret = app._init2(address, app_name)
    if init_ret != 200:
        return (False, False)

    if app.authorized:
        reinit = False
    else:
        reinit = True

    app.server = server
    app.cwd = cwd
    app.inst_dir = inst_dir

    tab = app.get_tab(0)

    app.title = app_title

    autologin = True
    for row in tab:
        if row[0].data == 'autologin':
            if row[1].data == '1':
                autologin = True
            else:
                autologin = False
        elif row[0].data == 'gui_style':
            app.gui_style = row[1].data
        elif row[0].data == 'csrf_token':
            app.csrf_token = row[1].data
        elif 'start_page' in row[0].data:
            app.start_pages.extend([x for x in row[1].data.split(';') if x and x != 'None'])
        elif row[0].data == 'title':
            app.title = row[1].data
        elif row[0].data == 'plugins':
            if row[1].data and row[1].data != "":
                app.plugins = row[1].data.split(';')

    if 'server_only' in _PARAM:
        app.gui_style = 'app.gui_style = tray(file(exit,open))'

    app._install_plugins()

    ready_to_run = True


    if not app.authorized and ( (autologin and not 'username' in _PARAM) or ('username' in _PARAM and 'password' in _PARAM)):
        if 'username' in _PARAM:
            username2 = _PARAM['username']
            password2 = _PARAM['password']
        else:
            username2 = 'auto'
            password2 = 'anawa'

        ready_to_run = False
        app.http.post(app, "/" + app_name + '/schsys/do_login/?from_pytigon=1' if app_name else '/schsys/do_login/?from_pytigon', {
            #'csrfmiddlewaretoken': app.csrf_token,
            'username': username2,
            'password': password2,
            'next': address + "/" + app_name + '/schsys/ok/' if app_name else  address + '/schsys/ok/',
            'client_param': app._get_parm_for_server(),
        })
        ret_str = app.http.str()
        if 'RETURN_OK' in ret_str:
            app.authorized = True
            ready_to_run = True
    if not app.authorized and 'username' in _PARAM:
        ready_to_run = False
        href = "/" + app_name + "/" if app_name else "/"
        if login(href, auth_type=None, username=_PARAM['username']):
            app.authorized = True
            ready_to_run = True
    if reinit:
        app._re_init(address, app_name)
    return (ready_to_run, True if 'nogui' in _PARAM else False)


def _main_run():
    app = wx.GetApp()
    app.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    app.locale.AddCatalogLookupPathPrefix(SCR_PATH + '/schcli/locale')

    app.locale.AddCatalog('wx')
    app.locale.AddCatalog('pytigon')

    if app.embeded_browser:
        frame = browserframe.SchBrowserFrame(
            None,
            app.gui_style,
            wx.ID_ANY,
            app.title,
            wx.DefaultPosition,
            wx.Size(_APP_SIZE[0], _APP_SIZE[1]),
        )
    else:
        frame = appframe.SchAppFrame(
            app.gui_style,
            app.title,
            wx.DefaultPosition,
            wx.Size(_APP_SIZE[0], _APP_SIZE[1]),
            video = _VIDEO
        )

    frame.CenterOnScreen()

    if not 'tray' in app.gui_style:
        frame.Show()

    destroy_fun_tab = frame.destroy_fun_tab
    httpclient.set_http_error_func(http_error)

    def idle_fun():
        wx.GetApp().web_ctrl.OnIdle(None)

    httpclient.set_http_idle_func(idle_fun)

    if app.task_manager:
        frame.idle_objects.append(app.task_manager)

    if _RPC:
        reactor.listenTCP(app.rpc, server.Site(app))

    if _WEBSOCKET:
        if ';' in _WEBSOCKET:
            websockets  = _WEBSOCKET.split(';')
        else:
            websockets = [ _WEBSOCKET, ]

        for websocket_id in websockets:
            class PytigonClientProtocol(WebSocketClientProtocol):
                def __init__(self):
                    nonlocal app, websocket_id
                    super().__init__()
                    self.app = app
                    self.websocket_id = websocket_id
                    app.websockets[websocket_id] = self

                def onConnect(self, response):
                    self.app.on_websocket_connect(self, self.websocket_id, response)

                def onOpen(self):
                    self.app.on_websocket_open(self, self.websocket_id)

                def onMessage(self, msg, binary):
                    self.app.on_websocket_message(self, websocket_id, msg, binary)
                    # reactor.callLater(1, self.sendHello)

            ws_address = app.base_address.replace('http', 'ws').replace('https', 'wss')
            ws_address += websocket_id
            factory = WebSocketClientFactory(ws_address)
            factory.protocol = PytigonClientProtocol
            connectWS(factory)

    if _INSPECTION == True:
        app.MainLoop()
    else:
        if 'channels' in _PARAM or 'rpc' in _PARAM:
            loop = get_event_loop()
            loop.run_until_complete(app.MainLoop())
        else:
            app.MainLoop()

    if app.task_manager:
        app.task_manager.wait_for_result()
    if app.server:
        app.server.stop()
    del app
    for pos in destroy_fun_tab:
        pos()


def main():

    ready_to_run, nogui = _main_init()
    if ready_to_run:
        if nogui:
            while (True):
                time.sleep(100)
        else:
            _main_run()


if __name__ == '__main__':
    main()
