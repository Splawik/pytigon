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

import os
import sys
import io
import time
import six

try:
    from urllib.parse import urlencode, urljoin
except:
    from urllib import urlencode
    from urlparse import urljoin

from schlib.schfs.vfstools import replace_dot
from schlib.schtools.schjson import json_dumps, json_loads

import email.generator
from mimetypes import guess_type

from schlib.schtools.encode import decode_utf
from os.path import basename
import http.cookies
import traceback

def init_embeded_django():
    from django.conf import settings

    import django.core.handlers.wsgi
    from wsgi_intercept.httplib2_intercept import install
    install()
    import wsgi_intercept
    application = django.core.handlers.wsgi.WSGIHandler()

    def create_fn():
        return application

    wsgi_intercept.add_wsgi_intercept('127.0.0.2', 80, create_fn)

    import django
    django.setup()
    import schserw.schsys.initdjango
    schserw.schsys.initdjango.init_django()


import httplib2
#import wx

Cookie = http.cookies.SimpleCookie()
BLOCK = False

def get_cookie_str():
    return Cookie.output(header="", sep=";")

def quote_plus(x):
    return x

def encode_file(boundary, key, file_name):
    f = open(str(file_name),"rb")
    t = 'application/octet-stream'
    
    lines= [
        '--' + boundary,
        'Content-Disposition: form-data; name="%s"; filename="%s"' \
            % (quote_plus(key), quote_plus(basename(file_name))),
        'Content-Type: %s' % t,
        '',
        f.read()
    ]
    
    f.close()
    
    return lines

def encode_multipart(boundary, data):
    lines = []
    for key, value in list(data.items()):
        #if type(key)=='bytes':
        #    key = key.decode('utf-8')
        #if type(value) == 'bytes':
        #    value = value.decode('utf-8')
        #if type(boundary)=='bytes':
        #    boundary = boundary.decode('utf-8')
        if value[0]=='@':
            if len(value)>1:
                lines.extend(encode_file(boundary, key, value[1:]))
        else:
            lines.extend([
                '--' + boundary,
                'Content-Disposition: form-data; name="%s"' % quote_plus(key),
                '',
                quote_plus(value)
            ])

    lines.extend([
        '--' + boundary + '--',
        '',
    ])
    lines2 = []
    for line in lines:
        if type(line) == bytes:
            lines2.append(line)
        else:
            lines2.append(line.encode('utf-8'))

    #print("LINES:", lines)
    return b'\r\n'.join(lines2)

count =  0

HttpErrorFunc = None

def set_http_error_func(func):
    global HttpErrorFunc
    HttpErrorFunc = func

HttpIdleFunc = None

def set_http_idle_func(func):
    global HttpIdleFunc
    HttpIdleFunc = func


def schurljoin(base, address):
    if address and len(address)>0 and base and len(base)>0 and base[-1]=='/' and address[0]=='/':
            return base+address[1:]
    else:
        return base + address

class HttpClient:

    def __init__(self, address):
        self.BaseAddress = address
        self.Location = None
        self.Last_address = None
        self.http = None
        self.last_addr = None
        self.ret_content_type = None
        self.resp = None

    def close(self):
        pass

    def WriteMemoryCallback(self, buf):
        self.contents = self.contents + buf

    def get(self, parent, address_str, parm=None, nullpost=False, user_agent=None, upload = False, credentials=False):
        global Cookie
        global BLOCK

        if BLOCK:
            while BLOCK:
                try:
                    if HttpIdleFunc:
                        HttpIdleFunc()
                    #wx.GetApp().web_ctrl.OnIdle(None)
                except:
                    return

        self.content_type = None
        self.contents = ""
        if address_str[0]=='^':
            address = 'http://127.0.0.2/schplugins/'+decode_utf(address_str[1:])
        else:
            address = decode_utf(address_str)

        if address[0] == '/' or address[0]=='.':
            if False and len(address) > 1 and address[1] == '_':
                adr = "http://local" + address
            else:
                adr = schurljoin(self.BaseAddress,address)
                #adr = self.BaseAddress + address
        else:

            adr = address

        adr = replace_dot(adr)
        adr = adr.replace(' ', '%20')
        print(">>>>>>>>", adr)

        post = None
        if parm == None:
            if nullpost:
                post = urlencode({'submit': "OK"})
        else:
            if parm.__class__ == str:
                post = parm
            else:
                if 'csrftoken' in Cookie:
                    parm['csrfmiddlewaretoken'] = Cookie['csrftoken'].value
                post = urlencode(parm)
                
        if not self.http:
            #self.http = httplib2.Http(os.path.join(os.path.expanduser("~"), ".pytigon/.cache"))
            self.http = httplib2.Http(os.path.join(os.path.expanduser("~")))

        if credentials:
            self.http.add_credentials(credentials[0], credentials[1])

        #print("HTTP: ", adr)
        if adr.startswith('file://'):
            file_name = adr[7:]
            if file_name[0]=='/' and file_name[2]==':':
                file_name = file_name[1:]
            f = open(file_name, "rb")
            self.contents = f.read()
            f.close()
            self.content_type = ["text/html", "charset=utf-8"]
            return (200, adr)
        else:

            headers = {'cache-control': 'no-cache'}
            if user_agent:
                headers['user-agent'] = user_agent

            s = get_cookie_str()
            if len(s)>0:
                headers['Cookie'] = s


            if post:
                if upload:
                    #boundary = mimetools.choose_boundary()
                    #boundary = email.generator.makeboundary()
                    try:
                        boundary = email.generator._make_boundary()
                    except:
                        try:
                            boundary = email.generator.makeboundary()
                        except:
                            boundary = mimetools.choose_boundary()

                    headers['content-type'] = 'multipart/form-data; boundary=%s' % boundary
                    body = encode_multipart(boundary, parm)
                    headers['content-length'] = str(len(body))
                    self.last_addr = adr
                    b2 = io.BytesIO(body)                    
                    (resp, self.contents) = self.http.request(adr, "POST", b2, headers=headers)
                else:
                    headers['Content-type'] = 'application/x-www-form-urlencoded; '
                    self.last_addr = adr
                    (resp, self.contents) = self.http.request(adr, "POST", post, headers=headers)
            else:

                #try:
                if True:
                    self.last_addr = adr
                    #print("adr:", str(adr))
                    (resp, self.contents) = self.http.request(str(adr), "GET", headers=headers)
                    if 'content-type' in resp:
                        self.ret_content_type=resp['content-type']
                    else:
                        self.ret_content_type=None
                #except:
                #    return (404,0)

        httpcode = int(resp['status'])
        if 'content-location' in resp:
            newaddress=resp['content-location']
        else:
            newaddress = adr

        self.Last_address = newaddress

        if 'set-cookie' in resp:
            x = resp['set-cookie']
            Cookie.load(x)

        if httpcode in (301, 302):
            self.Location = resp['location']

            if self.Location:
                if self.Location[-1]!='/':
                    self.Location = self.Location + "/"
                return self.get(parent, self.Location,  parm, nullpost, user_agent, upload)

        content_type = resp['content-type']

        self.content_type = None
        if content_type:
            self.content_type = content_type.lower().split(";")

        if int(resp['status']) != 200:
            print(adr, " httpcode:", resp)

        self.resp = resp

        #print("TYPE:", self.content_type)
        if self.content_type and len(self.content_type)>1 and  self.content_type[0]=='text/html' and 'utf-8' in self.content_type[1]:
            if "traceback" in str(self.contents):
                resp['status'] = 500

        if int(resp['status']) == 500 or int(resp['status']) in (301, 302):
            if HttpErrorFunc:
                BLOCK = True
                HttpErrorFunc(parent, self.contents)
                BLOCK = False
            else:
                f = open("last_error.html", "wb")
                f.write(self.contents)
                f.close()
        return (int(resp['status']), newaddress)

    def ptr(self):
        return self.contents

    def str(self, conwert_local_path = False):
        self.file()
        decode = 'utf-8'
        if self.content_type:
            if (self.content_type)[0].strip().startswith("text"):
                if len(self.content_type) > 1 and (self.content_type)[1].find("iso-8859-2") >= 0:
                    decode = "iso-8859-2"
                ret =  self.contents.decode(decode)
            else:
                #print("Str:", self.content_type)
                if 'application/json' in self.content_type:
                    ret = self.contents.decode('utf-8')
                else:
                    ret = self.contents
        else:
            ret = self.contents

        if conwert_local_path and settings:
            src = settings.URL_ROOT_FOLDER+"/static"
            dst = settings.ROOT_PATH+'/static'
            ret = ret.replace(src,"file://"+dst)

            src="href=\"/"
            dst = "href=\""+self.Last_address
            ret = ret.replace(src,dst)
            src="href='/"
            dst = "href='"+self.Last_address
            ret = ret.replace(src,dst)

            src="href=\"."
            dst = "href=\""+self.Last_address+"."
            ret = ret.replace(src,dst)
            src="href='."
            dst = "href='"+self.Last_address+"."
            ret = ret.replace(src,dst)
            src="action=\"/"
            dst="action=\""+settings.BASE_URL + settings.URL_ROOT_FOLDER + "/"
            ret = ret.replace(src,dst)
        return ret

    def to_python(self):
        #print("to_python:", self.str())
        return json_loads(self.str())


    def file(self):
        p = httplib2.urlnorm(self.last_addr)
        defrag_uri = p[3]
        cacheFullPath = os.path.join(self.http.cache.cache, self.http.cache.safe(defrag_uri))
        return cacheFullPath

    def clear_ptr(self):
        self.contents = ""


class AppHttp(HttpClient):

    def __init__(self, address, app):
        HttpClient.__init__(self, address)
        self.app = app

    def get(self, parent, address_str,  parm=None, nullpost=False, user_agent=None, upload = False, credentials=False):
        ret = HttpClient.get(self, parent, address_str, parm, nullpost, user_agent, upload, credentials=credentials)
        return ret

def conwert_local_path_fun(url):
    src = settings.BASE_URL + settings.URL_ROOT_FOLDER+"/static"
    dst = "file://" + settings.ROOT_PATH+'/static'
    return url.replace(src,dst).replace('/static', dst)


def local_media_path():
    return "file://" + settings.ROOT_PATH+'/static'

