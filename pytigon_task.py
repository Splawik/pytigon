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

import platform
import getopt

CWD_PATH = os.getcwd()
SCR_PATH = os.path.dirname(__file__)
if SCR_PATH == '':
    SCR_PATH = CWD_PATH
ROOT_PATH = SCR_PATH
if ROOT_PATH.startswith('.'):
    ROOT_PATH = CWD_PATH + '/' + ROOT_PATH
EXT_LIB_PATH = ROOT_PATH + '/..'
sys.path.append(ROOT_PATH)
sys.path.append(ROOT_PATH + '/schappdata')
sys.path.insert(0, ROOT_PATH + '/ext_lib')
if platform.system() == "Windows":
    sys.path.insert(0, ROOT_PATH + '/ext_lib_cli_win')
else:
    sys.path.insert(0, ROOT_PATH + '/ext_lib_cli_lin')

print(sys.argv[1:])

from schlib.schhttptools import httpclient
from schlib.schhttptools import htmltab

def usage():
    print("pytigon_task.py -a argument1=value1 -a argument2=value2 -u user -p password app_set:/view_name")

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
USERNAME = 'auto'
PASSWORD = 'anawa'

if len(args)>0 and ':' in args[0]:
    x = args[0].split(':')
    APP_SET = x[0]
    VIEW = x[1]

if not APP_SET or not VIEW:
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

CWD_PATH = ROOT_PATH + '/app_pack/' + APP_SET
sys.path.insert(0, CWD_PATH)
print(CWD_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_app'
httpclient.init_embeded_django()
http = httpclient.HttpClient("http://127.0.0.2")

ret, newaddr = http.get(None, '/')
ret_str = http.str()
mp = htmltab.SimpleTabParserBase()
mp.feed(ret_str)
mp.close()
csrf_token = ""
for pos in mp.tables[0]:
    if pos[0].strip()=='csrf_token':
        csrf_token = pos[1].split('value')[1].split("\"")[1]
http.clear_ptr()

parm={'csrfmiddlewaretoken': csrf_token, 'username': USERNAME, 'password': PASSWORD, 'next': '/schsys/ok',}
ret, newaddr = http.post(None, '/schsys/do_login/', parm, credentials=(USERNAME, PASSWORD))
http.clear_ptr()

ret, newaddr = http.post(None, VIEW, parm=ARGUMENTS)
ret_str = http.str()
http.clear_ptr()

print(ret_str)
