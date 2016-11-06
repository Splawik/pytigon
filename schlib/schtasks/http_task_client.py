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

#from django.core.context_processors import csrf
from django.template.context_processors import csrf


from schlib.schhttptools import httpclient
import schlib.schtasks.base_task as btask
from schlib.schtools.schjson import json_dumps

class HttpClientProcessManager(btask.ProcessManager):

    def __init__(self, base_address):
        self.http = httpclient.HttpClient(base_address)

    def put(self, request_or_username, title, func,  *args, **kwargs):
        param = {}

        if type(request_or_username) == str:
            param['username'] = request_or_username
        else:
            if request_or_username.user.is_authenticated():
                param['username'] = request_or_username.user.username
            else:
                param['username'] = 'guest'

        param['func'] = func
        param['title'] = title
        if kwargs:
            param['param'] = json_dumps(kwargs)

        ret = self.http.get(None, "/tasks/put", param)
        return self.http.to_python()

    def put_message(self, id, message):
        param = { 'id': id, 'message': message }
        ret = self.http.get(None, "/tasks/put_message", param)
        return self.http.to_python()

    def get_messages(self, id, id_start=0):
        param = { 'id': id, 'id_start': id_start }
        ret = self.http.get(None, "/tasks/get_messages", param)
        return self.http.to_python()

    def pop_messages(self, id):
        param = { 'id': id }
        ret = self.http.get(None, "/tasks/pop_messages", param)
        return self.http.to_python()

    def kill_thread(self, id):
        param = { 'id': id }
        ret = self.http.get(None, "/tasks/kill_thread", param)
        return self.http.to_python()

    def remove_thread(self, id):
        param = { 'id': id }
        ret = self.http.get(None, "/tasks/remove_thread", param)
        return self.http.to_python()

    def list_threads(self, all=False):
        param = { 'all': all }
        ret = self.http.get(None, "/tasks/list_threads", param)
        return self.http.to_python()

    def thread_info(self, id):
        param = { 'id': id }
        ret = self.http.get(None, "/tasks/thread_info", param)
        return self.http.to_python()

    def kill_all(self):
        ret = self.http.get(None, "/tasks/kill_all")
        return self.http.to_python()

    def wait_for_result(self):
        ret = self.http.get(None, "/tasks/wait_for_result")
        return self.http.to_python()

def get_process_manager(href=None):
    if not btask._PROCESS_MANAGER:
        btask._PROCESS_MANAGER=HttpClientProcessManager(href if href else 'http://127.0.0.1:8080')
    return btask._PROCESS_MANAGER

