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

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from pytigon_lib.schtools.main_paths import get_main_paths

from pytigon_lib.schhttptools import httpclient

HTTP = None


def init(prj, username, password):
    global HTTP

    paths = get_main_paths()
    cwd_path = os.path.join(paths["PRJ_PATH"], prj)
    sys.path.insert(0, cwd_path)

    os.environ["DJANGO_SETTINGS_MODULE"] = "settings_app"
    httpclient.init_embeded_django()
    HTTP = httpclient.HttpClient("http://127.0.0.2")

    if username:
        parm = {"username": username, "password": password, "next": "/schsys/ok/"}
        response = HTTP.post(
            None, "/schsys/do_login/", parm, credentials=(username, password)
        )


def request(url, params=None):
    if params:
        response = HTTP.post(None, url, params, user_agent="embeded")
    else:
        response = HTTP.get(None, url, user_agent="embeded")
    return response

