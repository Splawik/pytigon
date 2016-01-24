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

from schlib.schindent.indent_tools import indent_html

class LoginToSession(object):

    def process_request(self, request):
        if 'sessionid' in request.GET:
            from django.contrib.sessions.models import Session
            from django.contrib.auth.models import User
            from django.contrib.auth import login
            sessionid = request.GET['sessionid']
            session = Session.objects.get(session_key=sessionid)
            d = request.session.decode(session.session_data)
            uid = d.get('_auth_user_id')
            user = User.objects.get(pk=uid)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            #request.session['HYBRID_BROWSER'] = True
            if 'client_param' in request.GET:
                parm = request.GET['client_param']
                if parm != '':
                    request.session['client_param'] = dict([pos.split(':') for pos in parm.split(',')])
                    #request.session['client_param'] = parm


class ViewRequests(object):

    def process_request(self, request):
        print(request.method, request.path)
        #print(request.method, request.path, request.META )


class ViewPost(object):

    def process_request(self, request):
        try:
            if request.method == 'POST':
                print('=================== POST ======================')
                print(request.path)
                print(request.POST)
                print('===============================================')
        except:
            pass


class BeautyHtml():
    def process_response(self, request, response):
        if not response.streaming:
            if type(response.content)==str:
                response.content = "\n".join([ line for line in response.content.split('\n') if line.strip()])
            elif type(response.content)==bytes:
                response.content = "\n".join([ line for line in response.content.decode('utf-8').split('\n') if line.strip()])
        return response