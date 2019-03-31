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

import base64
import os

from django.conf import settings
from django.core.files.storage import default_storage
import requests
import asyncio
from threading import Thread

from schlib.schfs.vfstools import norm_path
from schlib.schtools.schjson import json_loads
from schlib.schhttptools.asgi_bridge import get_or_post, websocket

import threading
import logging

LOGGER = logging.getLogger("httpclient")

ASGI_APPLICATION = None

def init_embeded_django():
    global ASGI_APPLICATION
    os.environ['EMBEDED_DJANGO_SERVER'] = '1'
    import django
    django.setup()
    from channels.routing import get_default_application
    ASGI_APPLICATION = get_default_application()


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
    if address and len(address)>0 and base and len(base)>0 and base[-1]=='/' and address[0]=='/' and not base.endswith("://"):
            return base+address[1:]
    else:
        return base + address


class RetHttp():
    def __init__(self, url, ret_message):
        self.url = url
        self.history = None
        self.cookies = {}
        for key, value in ret_message.items():
            if key == 'body':
                self.content = value
            elif key == 'headers':
                self.headers = {}
                for pos in value:
                    if pos[0].decode('utf-8').lower() == 'set-cookie':
                        x  = pos[1].decode('utf-8')
                        x2 = x.split('=',1)
                        self.cookies[x2[0]] = x2[1]
                    else:
                        self.headers[pos[0].decode('utf-8').lower()] = pos[1].decode('utf-8')
            elif key == 'status':
                self.status_code = value
            elif key == 'type':
                self.type = value
            elif key == 'cookies':
                self.cookies = value
            elif key == 'history':
                self.history = value
            elif key == 'url':
                self.url = value


def asgi_get_or_post(application, url, headers, params={}, post=False, ret=[]):
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    ret2 = asyncio.get_event_loop().run_until_complete(get_or_post(application, url, headers, params=params, post=post))
    ret.append(ret2)

def requests_request(method, url, argv, ret=[]):
    ret2 = requests.request(method, url, **argv)
    ret.append(ret2)

def request(method, url, direct_access, argv, app=None):
    global ASGI_APPLICATION
    ret = []
    if direct_access and ASGI_APPLICATION:
        post = True if method == 'post' else False
        h = argv['headers']
        headers = []
        for key, value in h.items():
            headers.append((key.encode('utf-8'), value.encode('utf-8')))
        cookies = ""
        if 'cookies' in argv:
            for key, value in argv['cookies'].items():
                value2 = value.split(';',1)[0]
                cookies += f"{key}={value2};"
        if cookies:
            headers.append((b"cookie", cookies.encode('utf-8')))

        if post:
            t = Thread(target=asgi_get_or_post,
                       args=(ASGI_APPLICATION, url.replace('http://127.0.0.2', ''), headers, argv['data'], post, ret),
                       daemon=True)
            t.start()
            if app:
                try:
                    while t.is_alive():
                        app.Yield()
                except:
                    t.join()
            else:
                t.join()
        else:
            t = Thread(target=asgi_get_or_post,
                       args=(ASGI_APPLICATION, url.replace('http://127.0.0.2', ''), headers, {}, post, ret),
                       daemon=True)
            t.start()
            if app:
                try:
                    while t.is_alive():
                        app.Yield()
                except:
                    t.join()
            else:
                t.join()
        return RetHttp(url, ret[0])
    else:
        if app:
            t = Thread(target=requests_request,
                       args=(method, url, argv, ret),
                       daemon=True)
            t.start()
            try:
                while t.is_alive():
                    app.Yield()
            except:
                t.join()
        else:
            requests_request(method, url, argv, ret)
        return ret[0]


class HttpResponse():
    def __init__(self, url, ret_code=200, response=None, content=None, ret_content_type=None):
        self.url = url
        self.ret_code = ret_code
        self.response = response
        self.content = content
        self.ret_content_type = ret_content_type
        self.new_url = url

    def process_response(self, http_client, parent, post_request):
        global COOKIES
        global COOKIES_EMBEDED
        global BLOCK
        global HTTP_ERROR_FUNC

        if self.url.startswith("http://127.0.0.2/"):
            cookies = COOKIES_EMBEDED
        else:
            cookies = COOKIES

        self.content = self.response.content
        self.ret_code = self.response.status_code

        if self.response.status_code != 200:
            LOGGER.error({'address': self.url, 'httpcode': self.response.status_code})
            if self.response.status_code == 500:
                LOGGER.error({'content': self.content})

        if 'content-type' in self.response.headers:
            self.ret_content_type=self.response.headers['content-type']
        else:
            self.ret_content_type=None

        if self.response.history:
            for r in self.response.history:
                for key, value in r.cookies.items():
                    cookies[key] = value

        if self.response.cookies:
            for key, value in self.response.cookies.items():
                cookies[key] = value

        if self.ret_content_type and 'text/' in self.ret_content_type:
            if "Traceback" in str(self.content) and 'copy-and-paste' in str(self.content):
                if HTTP_ERROR_FUNC:
                    BLOCK = True
                    HTTP_ERROR_FUNC(parent, self.content)
                    BLOCK = False
                else:
                    with open(os.path.join(settings.DATA_PATH, "last_error.html"), "wb") as f:
                        f.write(self.content)
                self.ret_content_type = 500
                self.content = b""
                return

        if not post_request and not '?' in self.url and type(self.content)==bytes and ( b'Cache-control' in self.content or '/schplugins' in self.url ):
            http_client.http_cache[self.url]=(self.ret_content_type, self.content)

        self.new_url = self.response.url


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

    def json(self):
        return self.http.json()

    def to_python(self):
        """Return request content in json format converted to python object"""
        return json_loads(self.str())


class HttpClient:
    """Http client class"""

    def __init__(self, address):
        """Constructor

        Args:
            address: base address for http requests
        """
        self.base_address = address
        self.http_cache = {}
        self.app = None

    def close(self):
        pass

    def post(self, parent, address_str, parm=None, upload = False, credentials=False, user_agent=None, json_data = False, callback=None):
        """Prepare post request to the http server

        Args:
            parent - parent wx.Window derived object
            address_str - request address
            param - python dict with request parameters
            upload - True or False
            credentials - default False
            user_agent - default None
            json_data - send parm to server in json format
        """
        return self.get(parent, address_str, parm, upload, credentials, user_agent, True, json_data = json_data)

    def get(self, parent, address_str, parm=None, upload = False, credentials=False, user_agent=None, \
            post_request=False, json_data = False, callback = None):
        """Prepare get request to the http server

        Args:
            parent - parent wx.Window derived object
            address_str - request address
            param - python dict with request parameters
            upload - True or False
            credentials - default False
            user_agent - default None
        """
        if address_str.startswith('data:'):
            x = address_str.split(',', 1)
            if len(x)==2:
                t = x[0][5:].split(';')
                if t[1].strip()=='base64':
                    return HttpResponse(address_str, content=base64.b64decode(x[1].encode('utf-8')), ret_content_type=t[0])
            return HttpResponse(address_str, 500)

        global COOKIES
        global COOKIES_EMBEDED
        global BLOCK
        if BLOCK:
            while BLOCK:
                try:
                    if HTTP_IDLE_FUNC:
                        HTTP_IDLE_FUNC()
                except:
                    return HttpResponse(address_str, 500)

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
            direct_access = True
        else:
            cookies = COOKIES
            direct_access = False

        LOGGER.info(adr)

        if not post_request and not '?' in adr:
            if adr in self.http_cache:
                return HttpResponse(adr, content=self.http_cache[adr][1], ret_content_type=self.http_cache[adr][0])

        if adr.startswith('http://127.0.0') and ('/static/' in adr or '/site_media' in adr) and not '?' in adr:
            if '/static/' in adr:
                path = settings.STATICFILES_DIRS[0]+adr.replace('http://127.0.0.2', '').replace('/static','')
            else:
                path = settings.MEDIA_ROOT+adr.replace('http://127.0.0.2', '').replace('/site_media','')

            try:
                return HttpResponse(adr, content=default_storage.open(path).read(), ret_content_type="text/html")
            except:
                return HttpResponse(adr, 400, content=b"", ret_content_type="text/html")

        if adr.startswith('file://'):
            file_name = adr[7:]
            if file_name[0]=='/' and file_name[2]==':':
                file_name = file_name[1:]
            f = default_storage.open(file_name)
            return HttpResponse(adr, content=f.read(), ret_content_type="text/html charset=utf-8")

        if parm == None:
            parm = {}

        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
        headers['Referer'] = adr

        argv = { 'headers': headers, 'allow_redirects': True, 'cookies': cookies}
        if credentials:
            argv['auth'] = credentials

        method = "get"
        if post_request:
            method = "post"

            if json_data:
                argv['json'] = parm
            else:
                argv['data'] = parm

            if 'csrftoken' in cookies:
                headers['X-CSRFToken'] = cookies['csrftoken'].split(';',1)[0]

            if upload:
                files = {}
                for key, value in parm.items():
                    if type(value)==str and value.startswith('@'):
                        files[key]=open(value[1:], "rb")
                for key in files:
                    del parm[key]

                argv['files'] = files
            else:
                if json_data:
                    argv['json'] = parm
        else:
            argv['data'] = parm

        response = request(method, adr, direct_access, argv, self.app)
        http_response = HttpResponse(adr, response=response)
        http_response.process_response(self, parent, post_request)

        return http_response


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


async def local_websocket(path, input_queue, output):
    global COOKIES_EMBEDED
    global ASGI_APPLICATION

    user_agent = ""
    headers = []
    headers.append((b'User-Agent', user_agent))
    headers.append((b'Referer', path))

    cookies = ""
    if COOKIES_EMBEDED:
        if 'csrftoken' in COOKIES_EMBEDED:
            headers.append(('X-CSRFToken', COOKIES_EMBEDED['csrftoken'].split(';', 1)[0]))
        for key, value in COOKIES_EMBEDED.items():
            value2 = value.split(';',1)[0]
            cookies += f"{key}={value2};"
    if cookies:
        headers.append((b"cookie", cookies.encode('utf-8')))

    return await websocket(ASGI_APPLICATION, path, headers, input_queue, output)
