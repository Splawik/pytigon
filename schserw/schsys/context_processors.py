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

import uuid
from urllib.parse import urlparse

from django.conf import settings 
from django.core.urlresolvers import get_script_prefix
from django.contrib.auth.models import Permission

from schlib.schdjangoext.django_init import get_app_name


# browser_type: 0 - python client 1 - web client 2 - hybrid - web client in
# python client 3 - python client -> web client


mobiles = """sony,symbian,nokia,samsung,mobile,windows ce,epoc,opera mini,nitro,j2me,midp-,cldc-,netfront,mot,up.browser,
up.link,audiovox,blackberry,ericsson,panasonic,philips,sanyo,sharp,sie-,portalmmm,blazer,avantgo,danger,palm,series60,
palmsource,pocketpc,smartphone,rover,ipaq,au-mic,alcatel,ericy,up.link,docomo,vodafone/,wap1.,wap2.,plucker,480x640,sec,
fennec,android,google wireless transcoder,nintendo,webtv,playstation""".replace('\n','').replace('\r','').split(',')

def test_mobile(request):
    if "HTTP_X_OPERAMINI_FEATURES" in request.META:
        return True
    if "HTTP_ACCEPT" in request.META:
        s = request.META["HTTP_ACCEPT"].lower()
        if 'application/vnd.wap.xhtml+xml' in s:
            return True    
    if "HTTP_USER_AGENT" in request.META:
        s = request.META["HTTP_USER_AGENT"].lower()
        for ua in mobiles:
            if ua in s:
                return True                
    return False


def test_tablet(request):
    s = request.META["HTTP_USER_AGENT"].lower()
    if 'tablet' in s:
        return True
    else:
        return False


def standard_web_browser(request):
    if 'browser_type' in request.GET:
        return int(request.GET['browser_type'])
    if request and request.META['HTTP_USER_AGENT'].lower().startswith('py'):
        if 'WebKit' in request.META['HTTP_USER_AGENT']:
            return 3
        else:
            return 0
    else:
        if 'HYBRID_BROWSER' in request.session or 'hybrid' in request.GET:
            return 2
        elif 'only_content' in request.GET:
            return 5
        else:
            return 1


def browser_type(request):
    if hasattr(settings, 'THEMES'):
        themes = settings.THEMES
    else:
        themes = ['auto', 'auto', 'auto']

    if standard_web_browser(request):
        if test_mobile(request):
            if test_tablet(request):
                if themes[1]=='auto' or not themes[1]:
                    return 'tablet_standard'
                else:
                    return themes[1]
            else:
                if themes[2]=='auto' or not themes[2]:
                    return 'smartfon_standard'
                else:
                    return themes[2]
        else:
            if themes[0]=='auto' or not themes[0]:
                return 'desktop_standard'
            else:
                return themes[0]
    else:
        return 'schweb'


def default_template(b_type):
    return "template/%s.html" % b_type



class AppManager:
    def __init__(self, request):
        self.request = request

    def appname(self):
        path = self.request.path
        elementy = path.split('/')
        base_url = get_script_prefix()
        nr = base_url.count('/')
        return elementy[nr]

    def appid(self):
        path = self.request.path
        elementy = path.split('/')
        base_url = get_script_prefix()
        nr = base_url.count('/')
        if elementy[nr]=='schwiki':
            return elementy[nr+1]
        else:
            return elementy[nr]

    def get_main_title(self):
        apps = self.get_apps()
        for app in apps:
            if app[4]=='main':
                return app[0]
        return ""

    def get_apps(self, app_set=None):
        ret = []

        if app_set:
            _temp = __import__(app_set+".apps")
            apps = _temp.apps.APPS
        else:
            apps = None

        for _app in settings.INSTALLED_APPS:
            if apps:
                test = False
                name = _app if type(_app) == str else _app.name
                if name.startswith(app_set):
                    test = True
                else:
                    for app in apps:
                        if name in app:
                            test = True
                            break
                if not test:
                    continue

            app = get_app_name(_app)
            if self.request.get_host()=='127.0.0.2' and app=='schserw.schsys':
                continue
            try:
                module_title = None
                title = None
                perms = None
                url = None
                elementy = app.split('.')
                appname = elementy[-1]
                module = __import__(elementy[0])
                if len(elementy) > 1:
                    module2 = getattr(module, elementy[-1])
                else:
                    module2 = module
                if module2:
                    module_title = module2.ModuleTitle
                    title = module2.Title
                    perms = module2.Perms
                    index = module2.Index
                    if hasattr(module2, 'UserParam'):
                        user_param = module2.UserParam
                    else:
                        user_param = {}
                    ret.append((title, perms, index, appname, module_title, elementy[0], user_param))
            except:
                pass
        return ret

    def get_menu_id(self):
        i = 0
        apps = self.get_apps_width_perm()
        for app in apps:
            if app[3] == self.appid():
                return i
            i += 1
        return 0

    def get_app_items(self, app_pack=None):
        apps = self.get_apps(app_pack)
        ret = []
        for app in apps:
            app_name = app[3]
            app_title = app[0]
            module_title = app[4]
            module_name = app[5]
            user_param = app[6]
            if app_name != None and app_name != '':
                try:
                    module = __import__(module_name)
                    if module_name != app_name:
                        module2 = getattr(module, app_name)
                    else:
                        module2 = module
                    if module2:
                        for pos in module2.Urls:
                            ret.append((module_title, app_title, app_name, app_name + '/' + pos[0], pos[1],
                                        pos[2], pos[3], app[1], user_param,))
                        if hasattr(module2, 'AdditionalUrls'):
                            if callable(module2.AdditionalUrls):
                                urls2 = module2.AdditionalUrls()
                            else:
                                urls2 = module2.AdditionalUrls
                        for pos in urls2:
                            ret.append((module_title, app_title, app_name, app_name + '/' + pos[0], pos[1], pos[2],
                                        pos[3], app[1], user_param,))
                except:
                    pass
        return ret

    def get_apps_width_perm(self, app_pack=None):
        ret = []
        items = self.get_app_items()
        no_empty_apps = []
        for item in items:
            app_name = item[2]
            if not app_name in no_empty_apps:
                no_empty_apps.append(app_name)
        for item in self.get_apps(app_pack):
            if item[3] in settings.HIDE_APPS:                
                continue
            if item[3] in no_empty_apps:
                if item[1]:
                    if self.request.user.has_module_perms(item[3]):
                        ret.append(item)
                else:
                    ret.append(item)
        return ret

    def get_app_items_width_perm(self, app_pack=None):
        ret = []
        for item in self.get_app_items(app_pack):
            if item[2] in settings.HIDE_APPS:                
                continue
            if not item[7] or self.request.user.has_module_perms(item[2]):
                if item[5]:
                    if self.request.user.has_perm(item[5]):
                        ret.append(item)
                else:
                    ret.append(item)
            else:
                if len(Permission.objects.filter(content_type__app_label = item[2]))==0:
                    if item[5]:
                        if self.request.user.has_perm(item[5]):
                            ret.append(item)
                    else:
                        ret.append(item)
        return ret


def uuid(path):
    if ':' in path:
        path2 = path.split(':')[1]
    else:
        path2 = path
    if '?' in path:
        path2 = path.split('?')[0]
    else:
        path2 = path

    path2 = path.replace('/','_')
    return path2


def sch_standard(request):
    standard = standard_web_browser(request)

    r = urlparse(request.path)
    rr = r.path.split('/')
    if len(rr)>0:
        if rr[-1]:
            last_fragment = rr[-1]
        else:
            if len(rr)>1:
                last_fragment = rr[-2]
            else:
                last_fragment = ""
    else:
        last_fragment = r.path

    if last_fragment =='edit' or last_fragment == 'add':
        form_edit = True
    else:
        form_edit = False
    if last_fragment == 'add':
        form_add = True
    else:
        form_add = False
    if last_fragment == 'delete':
        form_delete = True
    else:
        form_delete = False

    if '/view' in request.path:
        form_info = True
    else:
        form_info = False

    if form_edit or form_delete or form_info:
        show_form = True
    else:
        show_form = False
    if '/grid' in request.path:
        form_grid = True
    else:
        form_grid = False
    if '_ext' in request.path:
        form_ext = True
    else:
        form_ext = False
    if '/_' in request.path:
        readonly = True
        ro = '_'
    else:
        readonly = False
        ro = ''
    if 'form/list' in request.path: 
        list_view = True
    else:
        list_view = False
    if '_set' in request.path or '/sublist' in request.path or '/get' in request.path:
        show_title_bar=True
    else:
        show_title_bar=False
    if '/get' in request.path:
        get = True
    else:
        get = False
    if settings.URL_ROOT_FOLDER and len(settings.URL_ROOT_FOLDER) > 0:
        url_base = '/' + settings.URL_ROOT_FOLDER
    else:
        url_base = ''

    lng = request.LANGUAGE_CODE[:2].lower()

    b_type = browser_type(request)
    x = b_type.split('_')
    b_type = x[0]
    if len(x)>1:
        b_type2 = x[1]
    else:
        b_type2 = 'standard'

    if standard == 2:
        d_template = default_template('hybrid')
        d_template2 = default_template(b_type)
    elif standard==5:
        d_template = default_template('only_content')
        d_template2 = default_template(b_type)
    else:
        d_template = default_template(b_type)
        d_template2 = d_template

    if lng and lng != 'en':
        d_template = d_template.replace('.html', '_'+lng+'.html')
        d_template2 = d_template2.replace('.html', '_'+lng+'.html')

    ret = {
        'standard_web_browser': standard,
        'app_manager': AppManager(request),
        'form_edit': form_edit,
        'form_add': form_add,
        'form_delete': form_delete,
        'form_ext': form_ext,
        'form_list': list_view,
        'readonly': readonly,
        'ro': ro,
        'form_info': form_info,
        'form_grid': form_grid,
        'URL_ROOT_FOLDER': settings.URL_ROOT_FOLDER,
        'URL_BASE': url_base,
        'show_form': show_form,
        'browser_type': b_type,
        'application_type': b_type2,
        'default_template': d_template,
        'default_template2': d_template2,
        'appset_name': settings.APPSET_NAME,
        'appset_title': settings.APPSET_TITLE,
        'show_title_bar': show_title_bar,
        'get': get,
        'settings': settings,
        'uuid': uuid(request.path),
        'lang': request.LANGUAGE_CODE[:2].lower(),
        'DEBUG': settings.DEBUG,
        }
    if 'client_param' in request.session:
        ret.update(request.session['client_param'])
    return ret

