#! /usr/bin/python
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
import getopt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if __name__ == "__main__":
    from pytigon_lib.schtools.main_paths import get_main_paths

    paths = get_main_paths()

    sys.path.append(paths["PRJ_PATH"])
    sys.path.append(paths["PRJ_PATH_ALT"])

    from pytigon_lib.schtasks import schschedule
    from pytigon_lib.schhttptools import httpclient

    import logging

    LOGGER = logging.getLogger("pytigon_task")

    def usage():
        print(
            "pytigon_task.py -a argument1=value1 -a argument2=value2 -u user -p password appset"
        )

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "ha:u:p:", ["help", "arguments=", "username=", "password="]
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    PRJ = None
    VIEW = None
    ARGUMENTS = {}
    USERNAME = None
    PASSWORD = None

    if len(args) > 0:
        x = args[0].split(":")
        PRJ = x[0]
        if len(x) > 1:
            VIEW = x[1]

    if not PRJ:
        usage()
        sys.exit()

    ARGUMENTS = {}
    FORCE_GET = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-a", "--arguments"):
            pos = arg.replace("__", " ").split("=")
            if len(pos) == 2:
                ARGUMENTS[pos[0]] = pos[1]
            else:
                FORCE_GET = True
        elif opt in ("-u", "--username"):
            USERNAME = arg
        elif opt in ("-p", "--password"):
            PASSWORD = arg

    CWD_PATH = os.path.join(paths["PRJ_PATH"], PRJ)
    sys.path.insert(0, CWD_PATH)
    CWD_PATH2 = os.path.join(paths["PRJ_PATH_ALT"], PRJ)
    sys.path.insert(0, CWD_PATH2)

    os.environ["PYTIGON_TASK"] = "1"
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings_app"
    httpclient.init_embeded_django()
    http = httpclient.HttpClient("http://127.0.0.2")

    if VIEW:
        if USERNAME:
            parm = {"username": USERNAME, "password": PASSWORD, "next": "/schsys/ok/"}
            response = http.post(
                None, "/schsys/do_login/", parm, credentials=(USERNAME, PASSWORD)
            )
        if ARGUMENTS or FORCE_GET:
            ret, newaddr = http.post(
                None, VIEW, ARGUMENTS
            )  # , credentials=(USERNAME, PASSWORD))
        else:
            ret, newaddr = http.get(None, VIEW)  # , credentials=(USERNAME, PASSWORD))
    else:
        from apps import APPS
        from pytigon_lib.schtools import sch_import
        from pytigon_lib.schdjangoext.django_manage import cmd
        from django.conf import settings

        mail_conf = None
        if hasattr(settings, "EMAIL_IMAP_HOST"):
            mail_conf = {}
            mail_conf["server"] = settings.EMAIL_IMAP_HOST
            mail_conf["username"] = settings.EMAIL_HOST_USER
            mail_conf["password"] = settings.EMAIL_HOST_PASSWORD
            mail_conf["inbox"] = settings.EMAIL_IMAP_INBOX
            mail_conf["outbox"] = settings.EMAIL_IMAP_OUTBOX

        xmlrpc_port = None
        if hasattr(settings, "XMLRPC_PORT"):
            xmlrpc_port = settings.XMLRPC_PORT

        scheduler = schschedule.SChScheduler(mail_conf, xmlrpc_port)

        run_scheduler = False

        for app in APPS:
            try:
                module = sch_import(app + ".tasks")
            except:
                LOGGER.exception("An error occurred durring import task")

            if hasattr(module, "init_schedule"):
                run_scheduler = True
                try:
                    module.init_schedule(scheduler, cmd, http)
                except:
                    LOGGER.exception("An error occurred durring init_schedule")

        if USERNAME:
            parm = {"username": USERNAME, "password": PASSWORD, "next": "/schsys/ok/"}
            response = http.post(
                None, "/schsys/do_login/", parm, credentials=(USERNAME, PASSWORD)
            )

        if run_scheduler == True:
            scheduler.run()
