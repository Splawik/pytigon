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
#copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

from __future__ import print_function
from __future__ import unicode_literals
from schcli.guilib import schimage

"""pytigon application - main module"""

import os
import sys
import time
import datetime

INSPECTION = False
CWD_PATH = os.getcwd()
SCR_PATH = os.path.dirname(__file__)
if SCR_PATH == '':
    SCR_PATH = CWD_PATH
#ROOT_PATH = SCR_PATH + '/..'
ROOT_PATH = SCR_PATH
if ROOT_PATH.startswith('.'):
    ROOT_PATH = CWD_PATH + '/' + ROOT_PATH
EXT_LIB_PATH = ROOT_PATH + '/..'
sys.path.append(ROOT_PATH)
sys.path.append(ROOT_PATH + '/schappdata')
sys.path.insert(0, ROOT_PATH + '/ext_lib_cli')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_desk_local'            

def install_0():
    """install plugin
    """

    home_dir = os.path.join(os.path.expanduser('~'), '.pytigon/')
    if not os.path.exists(home_dir):
        os.mkdir(home_dir)
        os.mkdir(home_dir + '.cache/')
        os.mkdir(home_dir + 'plugins_cache')
        ini = open(home_dir + 'plugins_cache/__init__.py', 'w')
        ini.write(' ')
        ini.close()

install_0()
sys.path = [xp for xp in sys.path if not ('plat-win' in xp or 'python27.zip' in xp
             or 'lib-tk' in xp)]

import zipfile
import getopt
import wx
from shutil import move

#from schcli.guictrl.grid import popupdata

from schcli.guilib.logindialog import LoginDialog
from schcli.guiframe import appframe
from schcli.guilib.schthreadwindow import SchThreadManager
from schlib.schtools.tools import extractall
from schlib.schhttptools import htmltab
from schcli.guilib.tools import standard_tab_colour
from schlib.schhttptools import httpclient
from schcli.guilib.httperror import http_error
#from wx import wizard
try:
    from wx.adv import Wizard, WizardPageSimple
except:
    from wx.wizard import Wizard, WizardPageSimple

wx.RegisterId(10000)
_ = wx.GetTranslation

_DEBUG = False

if INSPECTION:
    import wx.lib.mixins.inspection
    #InspectionMixin = wx.lib.mixins.inspection.InspectionMixin
    App = wx.lib.mixins.inspection.InspectableApp 
else:
    #class InspectionNone(object):
    #    def __init__(self):
    #        pass

    #InspectionMixin = InspectionNone
    App = wx.App


#class SchApp(wx.App, InspectionMixin):
class SchApp(App):

    """Pytigon application
    """

    def __init__(self):
        #wx.App.__init__(self, False)
        #InspectionMixin.__init__(self)
        App.__init__(self)
        self.is_hybrid = False
        self.locale = None
        self.log = None
        self.ext_app = []
        self.ext_app_http = {}
        self.lock = None

        self.base_address = None
        self.scr_path = None
        self.root_path = None
        self.cwd_path = None
        self.HTTP = None
        self.IMAGES = None
        self.mp = None

        self.server = None
        self.cwd = None
        self.inst_dir = None
        self.start_pages = []

        self.csrf_token = None
        self.title = None
        self.plugins = None

        self.thread_manager = None
        self.task_manager = None

        self.gui_style = \
            'app.gui_style = tree(toolbar(file(exit,open),clipboard, statusbar,=,trayicon))'

        self.COLOUR_HIGHLIGHT = \
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT).GetAsString(wx.C2S_HTML_SYNTAX)
        self.COLOUR_BACKGROUND = \
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE).GetAsString(wx.C2S_HTML_SYNTAX)
        self.COLOUR_SHADOW = \
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW).GetAsString(wx.C2S_HTML_SYNTAX)
        self.COLOUR_DKSHADOW = \
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW).GetAsString(wx.C2S_HTML_SYNTAX)
        self.COLOUR_ACTIVECATPION = \
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION).GetAsString(wx.C2S_HTML_SYNTAX)
        self.COLOUR_INFOBK = \
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK).GetAsString(wx.C2S_HTML_SYNTAX)

    def get_locale_object(self):
        return self.locale

    def init2(self, address, app):
        self.base_address = address
        self.scr_path = SCR_PATH
        self.root_path = ROOT_PATH
        self.cwd_path = CWD_PATH
        #httpeasy.set_http_error_func(http_error)
        self.HTTP = httpclient.AppHttp(address, self)
        if app and app != '':
            self.IMAGES = schimage.SchImage('/' + app + '/site_media/app.png',
                    0)
            self.HTTP.get(self, '/' + app + '/')
        else:
            self.IMAGES = schimage.SchImage('/site_media/app.png', 0)
            self.HTTP.get(self, '/')
        ret = self.HTTP.str()
        self.mp = htmltab.SimpleTabParser()
        self.mp.feed(ret)
        self.mp.close()
        self.HTTP.clear_ptr()

    def re_init(self, address, app):
        self.HTTP = httpclient.AppHttp(address, self)
        if app and app != '':
            self.HTTP.get(self, '/' + app + '/')
        else:
            self.HTTP.get(self, '/')
        ret = self.HTTP.str()
        self.mp = htmltab.SimpleTabParser()
        self.mp.feed(ret)
        self.mp.close()
        self.HTTP.clear_ptr()

    def SetTopWindow(self, frame):
        wx.App.SetTopWindow(self, frame)
        if frame.statusbar:
            self.thread_manager = SchThreadManager(self, frame.statusbar)
        #self.ShowInspectionTool()

    def register_extern_app(self, address, app):
        self.ext_app.append((app, address))

    def get_http_for_adr(self, address):
        for app in self.ext_app:
            if address.upper().startswith(app[1]):
                if app[0] in self.ext_app_http:
                    return self.ext_app_http[app[0]]
                else:
                    http = httpclient.AppHttp(app[1], app[0])
                    self.ext_app_http[app[0]] = http
                    return http
        return self.HTTP

    def get_http(self, win):
        winparent = win
        while winparent:
            if hasattr(winparent, 'get_app_http'):
                return winparent.get_app_http()
            winparent = winparent.GetParent()
        return self.HTTP

    def get_log(self):
        return self.log

    def get_tab(self, nr):
        return self.mp.tables[nr]

    def get_active_window(self):
        return self.GetTopWindow()

    def get_main_windows(self):
        return [self.GetTopWindow()]


    def append_thread(self, thread_address):
        if self.thread_manager:
            self.thread_manager.append(thread_address)

    def timer(self):
        if self.thread_manager:
            self.thread_manager.timer()

    def get_working_dir(self):
        return os.path.join(os.path.expanduser('~'), '.pytigon/')

    def get_parm_for_server(self):
        ret = ''
        for pos in standard_tab_colour():
            ret = ret + pos[0] + ':' + pos[1] + ','
        return ret[:-1].replace('#', '')

    def install_plugins(self):
        home_dir = self.get_working_dir()
        p = self.plugins
        if p:
            sys.path.append(home_dir)
            for plugin in p:
                if plugin == '':
                    continue
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
                    http = wx.GetApp().HTTP
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


def make_page_title(wiz_pg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wiz_pg.SetSizer(sizer)
    title = wx.StaticText(wiz_pg, -1, title)
    title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
    sizer.Add(wx.StaticLine(wiz_pg, -1), 0, wx.EXPAND | wx.ALL, 5)
    return sizer


class TitledPage(WizardPageSimple):

    def __init__(
        self,
        parent,
        lp,
        title,
        ):

        WizardPageSimple.__init__(self, parent)
        self.sizer = make_page_title(self, title)
        self.lp = lp


class InstallWizard(Wizard):

    def __init__(
        self,
        file_name,
        zip_file,
        app_name,
        licence_txt,
        readme_txt,
        ):

        Wizard.__init__(self, None, -1, 'Install app')
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.on_wiz_page_changing)
        self.zip_file = zip_file
        self.app_name = app_name
        page1 = TitledPage(self, 1, _('Program description'))
        self.page1 = page1
        page2 = TitledPage(self, 2, _('License'))
        page3 = TitledPage(self, 3, _('Run'))

        r_txt = wx.TextCtrl(page1, -1, size=wx.Size(600, 300),
                            style=wx.TE_MULTILINE | wx.TE_READONLY)
        r_txt.SetValue(readme_txt)
        page1.sizer.Add(r_txt)
        self.FitToPage(page1)
        l_txt = wx.TextCtrl(page2, -1, licence_txt, size=wx.Size(600, 300),
                            style=wx.TE_MULTILINE | wx.TE_READONLY)
        page2.sizer.Add(l_txt)
        page2.sizer.AddSpacer(5)
        self.licence = wx.CheckBox(page2, -1, _('Accept'))
        page2.sizer.Add(self.licence)
        page3.sizer.Add(wx.StaticText(page3, -1, _('Run the installed program or cancel')))
        WizardPageSimple.Chain(page1, page2)
        WizardPageSimple.Chain(page2, page3)
        self.GetPageAreaSizer().Add(page1)

    def run(self):
        return self.RunWizard(self.page1)

    def on_wiz_page_changing(self, event):
        if event.GetPage().lp == 2 and event.GetDirection():
            value = self.licence.GetValue()
            if not value:
                wx.MessageBox(_('You must accept the license or cancel the installation!')
                              , _('Installation'))
                event.Veto()
                return
            else:
                if self.install():
                    return
                else:
                    wx.MessageBox(_('Installation error!'), _('Installation'))
                    event.Veto()
                    return
        if event.GetPage().lp == 3 and not event.GetDirection():
            wx.MessageBox(_('Program installed, use the uninstaller!')
                          , _('Installation'))
            event.Veto()
            return
        event.Skip()

    def install(self):
        test_update = True
        extract_to = ROOT_PATH + '/app_sets/' + self.app_name
        try:
            if not os.path.exists(ROOT_PATH + '/app_sets'):
                os.mkdir(ROOT_PATH + '/app_sets')
            if not os.path.exists(extract_to):
                os.mkdir(extract_to)
                test_update = False
            zipname = datetime.datetime.now().isoformat('_')[:19].replace(':','').replace('-','')
            zipname2 = os.path.join(extract_to, zipname+".zip")
            if test_update:
                backup_zip = zipfile.ZipFile(zipname2, 'a')
                exclude = ['.*settings_local.py.*',]
            else:
                backup_zip = None
                exclude = None
            extractall(self.zip_file, extract_to, backup_zip=backup_zip, exclude=exclude, backup_exts=['py', 'txt', 'wsgi', 'ihtml', 'htlm', 'css', 'js',])
            if backup_zip:
                backup_zip.close()
            self.zip_file.close()
            src_db = os.path.join(extract_to, self.app_name+".db")
            if os.path.exists(src_db):
                dest_path_db = os.path.join( os.path.join(os.path.expanduser("~"), ".pytigon"), self.app_name)
                if not os.path.exists(dest_path_db):
                    os.mkdir(dest_path_db)
                dest_db = os.path.join(dest_path_db,self.app_name+".db")
                if not os.path.exists(dest_db):
                    move(src_db, dest_db )

            return True
        except:
            pass
        return False


def install_pti(pti, app_name):
    try:
        zip_file = zipfile.ZipFile(str(pti))
        l = zip_file.open('LICENSE.txt')
        licence_txt = l.read().decode('utf-8')
        l.close()
        r = zip_file.open('README.txt')
        readme_txt = r.read().decode('utf-8')
        r.close()
        wizard2 = InstallWizard(pti, zip_file, app_name, licence_txt, readme_txt)
        if wizard2.run():
            return True
        else:
            return False
    except:
        wx.MessageBox(_('Installation error!'), _('Installation'))
        return False


def main_init(argv):
    apps = []
    sync = False
    loaddb = False
    nogui = False
    server_only = False
    address = 'http://127.0.0.2'
    embed_diango = True
    app_title = _("Pytigon system")
    app = SchApp()
    if len(argv)==1 and '.ptig' in argv[0].lower():
        if zipfile.is_zipfile(argv[0]):
            argv2 = argv
            pass
        else:
            f = open(argv[0],"rt")
            buf = f.read()
            argv2 = buf.split(' ')
    else:
        argv2 = argv
    try:
        (opts, args) = getopt.getopt(argv2, 'ha:d', [
            'help',
            'app_set=',
            'hybrid',
            'syncdb',
            'loaddb',
            'server_only',
            'href=',
            'nogui',
            ])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    test_app_set = False
    for (opt, arg) in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt == '-d':
            global _DEBUG
            _DEBUG = 1
        elif opt in ('-a', '--app_set'):
            global CWD_PATH
            CWD_PATH = ROOT_PATH + '/app_sets/' + arg.strip()
            test_app_set = True            
        elif opt == '--syncdb':
            sync = True
        elif opt == '--loaddb':
            loaddb = True
        elif opt == '--server_only':
            server_only = True
        elif opt == '--href':
            address = arg
        elif opt == '--hybrid':
            app.is_hybrid = True
        elif opt == '--nogui':
            nogui = True
    #os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_desk_local'            
    if not test_app_set:
        choices = []
        if len(args) > 0:
            if len(args) > 1:
                usage()
                sys.exit(2)
            if len(args) == 1:
                prg_name = args[0].split('/')[-1].split('\\')[-1]
                if '.ptig' in prg_name.lower():
                    prg_name2 = prg_name.split('.')[0]
                    #if not os.path.exists(ROOT_PATH + '/app_sets/' + prg_name2):
                    if not install_pti(args[0], prg_name2):
                        return (None, None)
                    CWD_PATH = ROOT_PATH + '/app_sets/' + prg_name2
                else:
                    usage()
                    sys.exit(2)
        else:
            for ff in os.listdir(ROOT_PATH + '/app_sets/'):
                choices.append(ff)
            dlg = wx.SingleChoiceDialog(None,
                                        _('select the application to run')
                                        , app_title, choices,
                                        wx.CHOICEDLG_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.GetStringSelection()
                CWD_PATH = ROOT_PATH + '/app_sets/' + dlg.GetStringSelection()
                dlg.Destroy()
            else:
                dlg.Destroy()
                return (None, None)
    sys.path.append(CWD_PATH)

    httpclient.init_embeded_django()

    # wx.DateTime_SetCountry(wx.DateTime.USA)
    #wx.DateTime_SetCountry(wx.DateTime.Gr_Poland)


    #wx.DateTime.SetCountry(wx.DateTime.Gr_Poland)


    # locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    # locale.AddCatalogLookupPathPrefix(SCR_PATH+"/locale") locale.AddCatalog("wx")
    # locale.AddCatalog("scskr")

    if address == 'http://127.0.0.2':
        embed_diango = True
    else:
        embed_diango = True

    if embed_diango:
        #try:
        #print(sys.path)
        import settings_desk_local
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_desk_local'
        #except:
        #    try:
        #        import schserw.settings_desk
        #        os.environ['DJANGO_SETTINGS_MODULE'] = 'schserw.settings_desk'
        #    except:
        #       print 'No settings module!'
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
        settings.TEMPLATE_DIRS.insert(0, inst_dir + '/schappdata/schplugins')
        settings.TEMPLATE_DIRS.insert(0, cwd + '/schappdata/schplugins')
        settings.TEMPLATE_DIRS.insert(0, inst_dir + '/../templates')
        settings.TEMPLATE_DIRS.insert(0, cwd + '/templates')
        for a in apps:
            settings.INSTALLED_APPS.append(a)

    app_name = ''
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
        from schserw.cherrypy_server import CherryServer
        #from schcli.tasks.cherrypy_task import get_process_manager
        from schlib.schtasks.base_task import get_process_manager
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
        task_manager = get_process_manager()
        server = CherryServer(address, port)
        print('Start serwer: ', address, port)
        server.start()
        address = 'http://' + address + ':' + str(port)
    else:
        from schlib.schtasks.base_task import get_process_manager
        task_manager = get_process_manager()
        server = None

    if embed_diango:
        settings.BASE_URL = 'http://' + address
        settings.URL_POSTFIX = ''

    app.init2(address, app_name)
    app.task_manager = task_manager
    app.server = server
    app.cwd = cwd
    app.inst_dir = inst_dir
    tab = app.get_tab(0)
    login = False
    reinit = True
    app.title = app_title

    for row in tab:
        if row[0].data == 'login':
            if row[1].data == '1':
                login = True
                reinit = True
            else:
                login = False
        elif row[0].data == 'gui_style':
            app.gui_style = row[1].data
        elif row[0].data == 'csrf_token':
            app.csrf_token = row[1].data
        elif 'start_page' in row[0].data:
            app.start_pages.append(row[1].data)
        elif row[0].data == 'title':
            app.title = row[1].data
        elif row[0].data == 'plugins':
            app.plugins = row[1].data.split(';')
    if server_only:
        app.gui_style = \
            'app.gui_style = tree(toolbar(file(exit,open),clipboard, statusbar,=,trayicon))'

    app.install_plugins()
    ready_to_run = True
    autologin = True
    if autologin:
        username = 'auto'
        password = 'anawa'
        app.HTTP.Get(app, '/schsys/do_login/', {
            'csrfmiddlewaretoken': app.csrf_token,
            'username': username,
            'password': password,
            'next': '/schsys/ok',
            'client_param': app.get_parm_for_server(),
            })
        ret_str = app.HTTP.Str()
        ready_to_run = True
        login = False
    if login:
        ready_to_run = False
        dlg = LoginDialog(None, 101, _("Pytigon - login"))
        while dlg.ShowModal() == wx.ID_OK:
            username = dlg.text1.GetValue()
            password = dlg.text2.GetValue()
            app.HTTP.Get(app, '/schsys/do_login/', {
                'username': username,
                'password': password,
                'next': '/schsys/ok',
                'client_param': app.get_parm_for_server(),
                })
            ret_str = app.HTTP.Str()
            if 'RETURN_OK' in ret_str:
                ready_to_run = True
                break
            else:
                if not 'id_password' in ret_str:
                    break
                else:
                    dlg.message.SetLabel(_('Failed login attempt!'))
    if reinit:
        app.re_init(address, app_name)
    return (ready_to_run, nogui)


def main():
    app = wx.GetApp()
    app.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
    app.locale.AddCatalogLookupPathPrefix(SCR_PATH + '/schcli/locale')

    print(SCR_PATH + '/locale')

    app.locale.AddCatalog('wx')
    app.locale.AddCatalog('pytigon')

    frame = appframe.SchAppFrame(
        None,
        app.gui_style,
        wx.ID_ANY,
        app.title,
        wx.DefaultPosition,
        wx.Size(800, 700),
        )
    frame.CenterOnScreen()
    app.SetTopWindow(frame)
    if not 'tray' in app.gui_style:
        frame.Show()
    if len(app.start_pages) > 0:
        for page in app.start_pages:
            url_page = page.split(';')
            if len(url_page) == 2:
                frame._on_html(url_page[0] + ',' + app.base_address
                                + url_page[1])

    destroy_fun_tab = frame.destroy_fun_tab
    httpclient.set_http_error_func(http_error)
    app.MainLoop()
    if app.task_manager:
        app.task_manager.wait_for_result()
    if app.server:
        app.server.stop()
    del app
    for pos in destroy_fun_tab:
        pos()


def usage():
    print("""
    pytigon.py -h -g -a app_set
    -h --help
        wyswietla streszczona pomoc
    -d
        wlacza tryb debugowania
    -a --app_set ...
        uruchamia wskazany modul
    -u --url adres
        adres serwera
    -g --gui_style style
        styl gui
    --user=user
    --password=password
    """)

if __name__ == '__main__':
    ready_to_run, nogui = main_init(sys.argv[1:])
    if ready_to_run:
        if nogui:
            while(True):
                time.sleep(100)
        else:
            main()

    #for key in sys.modules: print key
