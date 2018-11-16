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

from schlib.schtasks import schschedule
from schlib.schhttptools import httpclient

import logging

LOGGER = logging.getLogger("pytigon_task")

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
    if len(x)>1:
        VIEW = x[1]

if not APP_SET:
    usage()
    sys.exit()

ARGUMENTS = {}
FORCE_GET = False
for (opt, arg) in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit()
    elif opt in ('-a', '--arguments'):
        pos = arg.replace('__',' ').split('=')
        if len(pos)==2:
            ARGUMENTS[pos[0]]=pos[1]
        else:
            FORCE_GET = True
    elif opt in ('-u', '--username'):
        USERNAME = arg
    elif opt in ('-p', '--password'):
        PASSWORD = arg

CWD_PATH = os.path.join(paths['APP_PACK_PATH'], APP_SET)
sys.path.insert(0, CWD_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_app'
httpclient.init_embeded_django()
http = httpclient.HttpClient("http://127.0.0.2")

if VIEW:
    if USERNAME:
        parm={'username': USERNAME, 'password': PASSWORD, 'next': '/schsys/ok/',}
        ret, newaddr = http.post(None, '/schsys/do_login/', parm, credentials=(USERNAME, PASSWORD))
        http.clear_ptr()
    if ARGUMENTS or FORCE_GET:
        ret, newaddr = http.post(None, VIEW, ARGUMENTS) #, credentials=(USERNAME, PASSWORD))
    else:
        ret, newaddr = http.get(None, VIEW) #, credentials=(USERNAME, PASSWORD))
    print(http.str())
    http.clear_ptr()
else:
    from apps import APPS
    from schlib.schtools import sch_import
    from schlib.schdjangoext.django_manage import cmd
    from django.conf import settings
    from asgiref.sync import sync_to_async

    mail_conf = None
    if hasattr(settings, 'EMAIL_IMAP_HOST'):
        mail_conf = {}
        mail_conf['server'] = settings.EMAIL_IMAP_HOST
        mail_conf['username'] = settings.EMAIL_HOST_USER
        mail_conf['password'] = settings.EMAIL_HOST_PASSWORD
        mail_conf['inbox'] = settings.EMAIL_IMAP_INBOX
        mail_conf['outbox'] = settings.EMAIL_IMAP_OUTBOX

    xmlrpc_port = None
    if hasattr(settings, 'XMLRPC_PORT'):
        xmlrpc_port = settings.XMLRPC_PORT

    scheduler = schschedule.SChScheduler(mail_conf, xmlrpc_port)

    for app in APPS:
        try:
            module = sch_import(app+".tasks")
        except:
            LOGGER.exception("An error occurred durring import task")
        
        if hasattr(module, "init_schedule"):
            try:
                module.init_schedule(scheduler, sync_to_async(cmd), sync_to_async(http))
            except:
                LOGGER.exception("An error occurred durring init_schedule")

    if USERNAME:
        parm={'username': USERNAME, 'password': PASSWORD, 'next': '/schsys/ok/',}
        ret, newaddr = http.post(None, '/schsys/do_login/', parm, credentials=(USERNAME, PASSWORD))
        http.clear_ptr()
    
    scheduler.run()
