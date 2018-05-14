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

import wx

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

from schserw import settings as schserw_settings

from schlib.schtools.install_init import init
init("_schall", schserw_settings.ROOT_PATH, schserw_settings.DATA_PATH, schserw_settings.APP_PACK_PATH, [schserw_settings.MEDIA_ROOT, schserw_settings.UPLOAD_PATH])


#def install_0():
#    # function create pytigon system folders if they do not exist.
#    home_dir = os.path.join(os.path.expanduser('~'), '.pytigon/')
#    if not os.path.exists(home_dir):
#        os.mkdir(home_dir)
#        os.mkdir(home_dir + '.cache/')
#        os.mkdir(home_dir + 'plugins_cache')
#        ini = open(home_dir + 'plugins_cache/__init__.py', 'w')
#        ini.write(' ')
#        ini.close()
#
#
#install_0()

INSPECTION = False
if any(s.startswith('--inspection') for s in sys.argv):
    INSPECTION = True

_DEBUG = False
if any(s.startswith('--debug') for s in sys.argv):
    _DEBUG = True

_TRACE = False
if any(s.startswith('--trace') for s in sys.argv):
    _TRACE = True

_VIDEO = False
if any(s.startswith('--video') for s in sys.argv):
    _VIDEO = True

if any(s.startswith('--rpc') for s in sys.argv):
    import wxreactor

    wxreactor.install()
    from twisted.internet import reactor
    from twisted.web import xmlrpc, server

    RPC = True
else:
    RPC = False

# import gc
# gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)
# gc.disable()

wx.RegisterId(10000)
_ = wx.GetTranslation
wx.outputWindowClass = None

if INSPECTION:
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
    App = wx.App

if RPC:
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

        App.__init__(self)
        if RPC:
            xmlrpc.XMLRPC.__init__(self)

        if not '--no_splash' in sys.argv:
            bitmap = wx.Bitmap(SCR_PATH + '/pytigon_splash.jpeg', wx.BITMAP_TYPE_JPEG)
            splash = wx.adv.SplashScreen(bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                         1000, None, -1, wx.DefaultPosition, wx.DefaultSize,
                                         wx.BORDER_SIMPLE | wx.STAY_ON_TOP)
        wx.Yield()

        config_name = os.path.join(SCR_PATH, "pytigon.ini")
        self.config = configparser.ConfigParser()
        self.config.read(config_name)

        self.is_hybrid = False
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
        if INSPECTION:
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


def login(base_href, auth_type=None):
    """Show login form"""
    dlg = LoginDialog(None, 101, _("Pytigon - login"))

    while dlg.ShowModal() == wx.ID_OK:

        username = dlg.text1.GetValue()
        password = dlg.text2.GetValue()

        parm = {'username': username,
                'password': password,
                'next': '/schsys/ok',
                'client_param': wx.GetApp()._get_parm_for_server(),
                }

        if auth_type == None:
            wx.GetApp().http.post(wx.GetApp(), '/schsys/do_login/', parm, credentials=(username, password))

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



def _main_init(argv):
    global CWD_PATH
    apps = []
    sync = False
    loaddb = False
    nogui = False
    server_only = False
    address = 'http://127.0.0.2'
    embed_diango = True
    app_title = _("Pytigon")
    embeded_browser = False
    extern_app_set = False
    app_name = ''

    try:
        (opts, args) = getopt.getopt(argv, 'h:dmp', [
            'help',
            # 'app_set=',
            'hybrid',
            'syncdb',
            'loaddb',
            'server_only',
            'href=',
            'nogui',
            'menu_always',
            'debug',
            'embededbrowser',
            'rpc=',
            'no_splash',
            'param=',
            'inspection',
            'trace',
            'video',
        ])
    except getopt.GetoptError:
        usage()
        return (None, None)

    app = SchApp()

    for (opt, arg) in opts:
        if opt in ('-h', '--help'):
            usage()
            return (0, 0)
        elif opt == '-d':
            global _DEBUG
            _DEBUG = 1
        elif opt == '--syncdb':
            sync = True
        elif opt == '--loaddb':
            loaddb = True
        elif opt == '--server_only':
            server_only = True
        elif opt == '--embededbrowser':
            embeded_browser = True
        elif opt == '--href':
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
        elif opt == '--hybrid':
            app.is_hybrid = True
        elif opt == '--nogui':
            nogui = True
        elif opt in ('-m', '--menu_always'):
            app.menu_always = True
        elif opt in ('--rpc'):
            app.rpc = int(arg)
        elif opt in ('-p', '--param'):
            app.param = arg

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_app'

    if len(args) > 0:
        if '.ptig' in args[0].lower():
            prg_name = args[0].split('/')[-1].split('\\')[-1]
            x = prg_name.split('.')
            if len(x)==2 or ( len(x)>2 and x[-2].lower()=='inst'):
                prg_name2 = x[0]
                if not pytigon_install.install(args[0], prg_name2):
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
            CWD_PATH = schserw_settings.APP_PACK_PATH + "/" + args[0].strip()
            if not os.path.exists(os.path.join(CWD_PATH, "settings_app.py")):
                print(_("Application pack: '%s' does not exists") % args[0].strip())
                return (None, None)
    elif extern_app_set:
        pass
    else:
        choices = [ff for ff in os.listdir(schserw_settings.APP_PACK_PATH + "/") if not ff.startswith('_')]

        dlg = wx.SingleChoiceDialog(None,
                                    _('select the application to run')
                                    , app_title, choices,
                                    wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.GetStringSelection()
            CWD_PATH = schserw_settings.APP_PACK_PATH + '/' + dlg.GetStringSelection()
            dlg.Destroy()
        else:
            dlg.Destroy()
            wx.Yield()
            return (None, None)

    sys.path.insert(0, CWD_PATH)

    httpclient.init_embeded_django()

    if address == 'http://127.0.0.2':
        embed_diango = True
    else:
        embed_diango = True

    if embed_diango:
        import settings_app
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_app'
        from django.conf import settings
        if sync:
            from django.core.management.commands.syncdb import Command as sync_command
            sync = sync_command()
            try:
                sync.run_from_argv(['manage.py', 'syncdb'])
            except SystemExit:
                pass
        if loaddb:
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
    if embed_diango:
        settings.TEMPLATES[0]['DIRS'].insert(0, inst_dir + '/schappdata/schplugins')
        settings.TEMPLATES[0]['DIRS'].insert(0, cwd + '/schappdata/schplugins')
        settings.TEMPLATES[0]['DIRS'].insert(0, inst_dir + '/../templates')
        settings.TEMPLATES[0]['DIRS'].insert(0, cwd + '/templates')

        for a in apps:
            settings.INSTALLED_APPS.append(a)

    port = 0
    if server_only:
        port = 80
        if ':' in address:
            l = address.split(':')
            if len(l) == 3:
                port = int(l[2])
        address = 'embeded'
    if address == 'embeded':
        import socket
        from schlib.schdjangoext.server import run_server
        if server_only:
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

    if embed_diango:
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
    app.embeded_browser = embeded_browser
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

    if server_only:
        app.gui_style = 'app.gui_style = tree(toolbar(file(exit,open),clipboard, statusbar))'

    app._install_plugins()

    ready_to_run = True

    username = 'auto'
    password = 'anawa'

    #if extern_app_set:
    #    app.http.get("", "http://127.0.0.2/")
    #    app.http.post("", "http://127.0.0.2/schsys/do_login/", {
    #        'username': username,
    #        'password': password,
    #        'next': "http://127.0.0.2/schsys/ok",
    #        'client_param': app._get_parm_for_server()
    #    })

    if not app.authorized and autologin:
        ready_to_run = False
        app.http.post(app, "/" + app_name + '/schsys/do_login/' if app_name else '/schsys/do_login/', {
            'csrfmiddlewaretoken': app.csrf_token,
            'username': username,
            'password': password,
            'next': address + "/" + app_name + '/schsys/ok/' if app_name else  address + '/schsys/ok/',
            'client_param': app._get_parm_for_server(),
        })
        ret_str = app.http.str()
        if 'RETURN_OK' in ret_str:
            app.authorized = True
            ready_to_run = True
    if not app.authorized:
        ready_to_run = False
        href = "/" + app_name + "/" if app_name else "/"
        if login(href, auth_type=None):
            app.authorized = True
            ready_to_run = True
    if reinit:
        app._re_init(address, app_name)
    return (ready_to_run, nogui)


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
            wx.Size(800, 700),
        )
    else:
        frame = appframe.SchAppFrame(
            app.gui_style,
            app.title,
            wx.DefaultPosition,
            wx.Size(800, 700),
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

    if RPC:
        reactor.registerWxApp(app)
        reactor.listenTCP(app.rpc, server.Site(app))
        reactor.run()
    else:
        app.MainLoop()

    if app.task_manager:
        app.task_manager.wait_for_result()
    if app.server:
        app.server.stop()
    del app
    for pos in destroy_fun_tab:
        pos()


def usage():
    print(main.__doc__)


def main(argv):
    """Run pytigon application: pytigon.py [option]... arg

    command line arguments:
        arg: application package name or pytigon installation file name

        options:

            -h, --help - show help

            --href=<address> - address of http server, http://www.pytigon.cloud for example

            -p <parameters>, --param=<parameters> - parametres of request to http server

            --hybrid - hybrid mode

            --server_only - run only http server

            --syncdb - run django command: manage.py syncdb

            --loaddb - run django command: manage.py loaddb

            --nogui - run program without gui

            --embededbrowser - run in background embeded http server

            -m --menu_always - show menu event then configuration says otherwise

            --no_splash - do not show splash window

            --rpc=<port> - set tcp port of rcp

            -d --debug - debug mode

            --inspection - turn on wxPython inspection

            --trace - show trace of python calls

            --video - record video session
    """

    ready_to_run, nogui = _main_init(argv)
    if ready_to_run:
        if nogui:
            while (True):
                time.sleep(100)
        else:
            _main_run()


if __name__ == '__main__':
    main(sys.argv[1:])
