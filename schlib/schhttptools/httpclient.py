#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Pu`blic License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

"""Module contains classed for define http client

"""

from django.conf import settings
import requests

from schlib.schfs.vfstools import norm_path
from schlib.schtools.schjson import json_loads
import threading

def init_embeded_django():
    import django.core.handlers.wsgi
    from wsgi_intercept import requests_intercept, add_wsgi_intercept
    requests_intercept.install()

    import django
    django.setup()

    application = django.core.handlers.wsgi.WSGIHandler()
    def create_fn():
        return application

    add_wsgi_intercept('127.0.0.2', 80, create_fn)

    import schserw.schsys.initdjango
    schserw.schsys.initdjango.init_django()


BLOCK = False
COOKIES_EMBEDED = {}
COOKIES = {}
HTTP_LOCK = threading.Lock()


HTTP_ERROR_FUNC = None

def set_http_error_func(func):
    global HTTP_ERROR_FUNC
    HTTP_ERROR_FUNC = func

HTTP_IDLE_FUNC = None

def set_http_idle_func(func):
    global HTTP_IDLE_FUNC
    HTTP_IDLE_FUNC = func

def schurljoin(base, address):
    if address and len(address)>0 and base and len(base)>0 and base[-1]=='/' and address[0]=='/':
            return base+address[1:]
    else:
        return base + address



class HttpClient:
    """Http client class"""

    def __init__(self, address):
        """Constructor

        Args:
            address: base address for http requests
        """
        self.base_address = address
        self.http = None
        self.content = ""
        self.ret_content_type = None
        self.http_cache = {}

    def close(self):
        pass

    def post(self, parent, address_str, parm=None, upload = False, credentials=False, user_agent=None):
        """Prepare post request to the http server

        Args:
            parent - parent wx.Window derived object
            address_str - request address
            param - python dict with request parameters
            upload - True or False
            credentials - default False
            user_agent - default None
        """
        return self.get(parent, address_str, parm, upload, credentials, user_agent, True)

    def get(self, parent, address_str, parm=None, upload = False, credentials=False, user_agent=None, post_request=False):
        """Prepare get request to the http server

        Args:
            parent - parent wx.Window derived object
            address_str - request address
            param - python dict with request parameters
            upload - True or False
            credentials - default False
            user_agent - default None
        """
        global COOKIES
        global COOKIES_EMBEDED
        global BLOCK
        if BLOCK:
            while BLOCK:
                try:
                    if HTTP_IDLE_FUNC:
                        HTTP_IDLE_FUNC()
                except:
                    return (500, address_str)


        self.content = ""
        if address_str[0]=='^':
            address = 'http://127.0.0.2/schplugins/'+address_str[1:]
        else:
            address = address_str

        if address[0] == '/' or address[0]=='.':
            adr = schurljoin(self.base_address, address)
        else:
            adr = address

        #adr = replace_dot(adr)
        adr = norm_path(adr)
        #adr = adr.replace(' ', '%20')

        if adr.startswith("http://127.0.0.2/"):
            cookies = COOKIES_EMBEDED
        else:
            cookies = COOKIES

        print(">>>>>>>>", adr)

        if not post_request and not '?' in adr:
            if adr in self.http_cache:
                self.ret_content_type = self.http_cache[adr][0]
                self.content = self.http_cache[adr][1]
                return (200, adr)

        if adr.startswith('http://127.0.0') and ('/static/' in adr or '/site_media' in adr) and not '?' in adr:
            if '/static/' in adr:
                path = settings.STATICFILES_DIRS[0]+adr.replace('http://127.0.0.2', '').replace('/static','')
            else:
                path = settings.MEDIA_ROOT+adr.replace('http://127.0.0.2', '').replace('/site_media','')

            try:
                with open(path, "rb") as f:
                    self.content = f.read()
                    self.ret_content_type = "text/html"
                return (200, adr)
            except:
                self.content = b""
                self.ret_content_type = "text/html"
                return (404, adr)

        if adr.startswith('file://'):
            file_name = adr[7:]
            if file_name[0]=='/' and file_name[2]==':':
                file_name = file_name[1:]
            f = open(file_name, "rb")
            self.content = f.read()
            f.close()
            self.ret_content_type = "text/html charset=utf-8"
            return (200, adr)


        if parm == None:
            parm = {}

        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
        headers['Referer'] = adr


        HTTP_LOCK.acquire()
        try:

            if post_request:
                if 'csrftoken' in cookies:
                    parm['csrfmiddlewaretoken'] = cookies['csrftoken']
                if upload:
                    files = {}
                    for key, value in parm.items():
                        if type(value)==str and value.startswith('@'):
                            files[key]=open(value[1:], "rb")
                    for key in files:
                        del parm[key]
                    if credentials:
                        self.http = requests.post(adr, data=parm, files=files, headers=headers, auth=credentials, allow_redirects=True, cookies=cookies)
                    else:
                        self.http = requests.post(adr, data=parm, files=files, headers=headers, allow_redirects=True, cookies=cookies)
                else:
                    if credentials:
                        self.http = requests.post(adr, data=parm, headers=headers, auth=credentials, allow_redirects=True, cookies=cookies)
                    else:
                        self.http = requests.post(adr, data=parm, headers=headers, allow_redirects=True, cookies=cookies)
            else:
                if credentials:
                    self.http = requests.get(adr, data=parm, headers=headers, auth=credentials, allow_redirects=True, cookies=cookies)
                else:
                    self.http = requests.get(adr, data=parm, headers=headers, allow_redirects=True, cookies=cookies)
        finally:
            HTTP_LOCK.release()

        self.content = self.http.content

        if self.http.status_code != 200:
            print(adr, " httpcode:", self.http.status_code)
            if self.http.status_code == 500:
                print(self.content)

        if 'content-type' in self.http.headers:
            self.ret_content_type=self.http.headers['content-type']
        else:
            self.ret_content_type=None

        if self.http.history:
            for r in self.http.history:
                for key, value in r.cookies.items():
                    cookies[key] = value

        if self.http.cookies:
            for key, value in self.http.cookies.items():
                cookies[key] = value

        if self.ret_content_type and 'text/' in self.ret_content_type: # and 'utf-8' in self.ret_content_type:
            if "Traceback" in str(self.content) and 'copy-and-paste'in str(self.content):
                if HTTP_ERROR_FUNC:
                    BLOCK = True
                    HTTP_ERROR_FUNC(parent, self.content)
                    BLOCK = False
                else:
                    with open("last_error.html", "wb") as f:
                        f.write(self.content)
                return (500, self.http.url)

        if not post_request and not '?' in adr and type(self.content)==bytes and b'Cache-control' in self.content:
            self.http_cache[adr]=(self.ret_content_type, self.content)

        return (self.http.status_code, self.http.url)


    def ptr(self):
        """Return request content"""
        return self.content

    def str(self):
        """Return request content converted to string"""
        decode = 'utf-8'
        if self.ret_content_type:
            if 'text' in self.ret_content_type:
                if "iso-8859-2" in self.ret_content_type:
                    decode = "iso-8859-2"
                ret =  self.content.decode(decode)
            else:
                if 'application/json' in self.ret_content_type:
                    ret = self.content.decode('utf-8')
                else:
                    ret = self.content
        else:
            ret = self.content
        return ret

    def to_python(self):
        """Return request content in json format converted to python object"""
        return json_loads(self.str())

    def clear_ptr(self):
        pass


    def show(self, parent):
        if HTTP_ERROR_FUNC:
            HTTP_ERROR_FUNC(parent, self.content)


class AppHttp(HttpClient):
    """Extended version of HttpClient"""

    def __init__(self, address, app):
        """Constructor

        Args:
            address - base request address
            app - application name
        """
        HttpClient.__init__(self, address)
        self.app = app


def join_http_path(base, ext):
    if base.endswith('/') and ext.startswith('/'):
        return base+ext[1:]
    else:
        return base + ext