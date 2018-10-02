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

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import os
import sys
import getopt
import time

from schserw.main_paths import get_main_paths
paths = get_main_paths()

import schedule
from schlib.schhttptools import httpclient

def usage():
    print("pytigon_task.py -a argument1=value1 -a argument2=value2 -u user -p password appset")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'ha:u:p:', [
        'help',
        'arguments=',
        'username=',
        'password=',
        ])
except getopt.GetoptError:
    usage()
    sys.exit(2)

APP_SET = None
VIEW = None
ARGUMENTS = {}
USERNAME =  None
PASSWORD = None

if len(args)>0:
    x = args[0].split(':')
    APP_SET = x[0]

if not APP_SET:
    usage()
    sys.exit()

ARGUMENTS = {}
for (opt, arg) in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit()
    elif opt in ('-a', '--arguments'):
        pos = arg.replace('__',' ').split('=')
        if len(pos)==2:
            ARGUMENTS[pos[0]]=pos[1]
    elif opt in ('-u', '--username='):
        USERNAME = arg
    elif opt in ('-p', '--password='):
        PASSWORD = arg

CWD_PATH = os.path.join(paths['APP_PACK_PATH'], APP_SET)
sys.path.insert(0, CWD_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_app'
httpclient.init_embeded_django()
http = httpclient.HttpClient("http://127.0.0.2")

from apps import APPS
from schlib.schtools import sch_import
from schlib.schdjangoext.django_manage import cmd

for app in APPS:
    try:
        module = sch_import(app+".tasks")
    except:
        pass

    if hasattr(module, "init_schedule"):
        module.init_schedule(cmd, http)

if USERNAME:
    parm={'username': USERNAME, 'password': PASSWORD, 'next': '/schsys/ok/',}
    ret, newaddr = http.post(None, '/schsys/do_login/', parm, credentials=(USERNAME, PASSWORD))
    http.clear_ptr()

while True:
    schedule.run_pending()
    time.sleep(10)
