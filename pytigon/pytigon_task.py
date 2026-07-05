#!/usr/bin/env python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.

"""Pytigon task scheduler entry point.

Runs scheduled tasks defined by pytigon application modules. Supports
both direct view invocation and scheduled background task execution.

Usage:
    pytigon_task.py -a argument1=value1 -a argument2=value2 -u user -p password appset[:view]
"""

import getopt
import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Module-level logger
LOGGER = logging.getLogger("pytigon_task")


def usage():
    """Print usage information for pytigon_task."""
    print(
        "pytigon_task.py -a argument1=value1 -a argument2=value2 "
        "-u user -p password appset[:view]"
    )


def _login(http, username, password):
    """Perform login via the embedded HTTP client.

    Args:
        http: HttpClient instance.
        username: Login username.
        password: Login password.
    """
    if username:
        parm = {"username": username, "password": password, "next": "/schsys/ok/"}
        http.post(
            None,
            "/schsys/do_login/",
            parm,
            credentials=(username, password),
        )


if __name__ == "__main__":
    from pytigon_lib.schhttptools import httpclient
    from pytigon_lib.schtasks import schschedule
    from pytigon_lib.schtools.main_paths import get_main_paths

    paths = get_main_paths()

    sys.path.append(paths["PRJ_PATH"])
    sys.path.append(paths["PRJ_PATH_ALT"])

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "ha:u:p:",
            ["help", "arguments=", "username=", "password="],
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    prj = None
    view = None
    arguments = {}
    username = None
    password = None

    # Parse positional argument: project[:view]
    if args:
        parts = args[0].split(":")
        prj = parts[0]
        if len(parts) > 1:
            view = parts[1]

    if not prj:
        usage()
        sys.exit(1)

    force_get = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-a", "--arguments"):
            pos = arg.replace("__", " ").split("=")
            if len(pos) == 2:
                arguments[pos[0]] = pos[1]
            else:
                force_get = True
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg

    cwd_path = os.path.join(paths["PRJ_PATH"], prj)
    sys.path.insert(0, cwd_path)
    cwd_path2 = os.path.join(paths["PRJ_PATH_ALT"], prj)
    sys.path.insert(0, cwd_path2)

    os.environ["PYTIGON_TASK"] = "1"
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings_app"
    httpclient.init_embeded_django()
    http = httpclient.HttpClient("http://127.0.0.2")

    if view:
        _login(http, username, password)
        if arguments or force_get:
            ret, newaddr = http.post(None, view, arguments)
        else:
            ret, newaddr = http.get(None, view)
    else:
        from apps import APPS
        from django.conf import settings

        from pytigon_lib.schdjangoext.django_manage import cmd
        from pytigon_lib.schtools import sch_import

        # Build mail configuration from Django settings if available
        mail_conf = None
        if hasattr(settings, "EMAIL_IMAP_HOST"):
            mail_conf = {
                "server": settings.EMAIL_IMAP_HOST,
                "username": settings.EMAIL_HOST_USER,
                "password": settings.EMAIL_HOST_PASSWORD,
                "inbox": settings.EMAIL_IMAP_INBOX,
                "outbox": settings.EMAIL_IMAP_OUTBOX,
            }

        xmlrpc_port = getattr(settings, "XMLRPC_PORT", None)

        scheduler = schschedule.SChScheduler(mail_conf, xmlrpc_port)

        run_scheduler = False

        for app in APPS:
            try:
                module = sch_import(app + ".tasks")
            except Exception:
                LOGGER.exception("Failed to import tasks module for app '%s'", app)
                continue

            if hasattr(module, "init_schedule"):
                run_scheduler = True
                try:
                    module.init_schedule(scheduler, cmd, http)
                except Exception:
                    LOGGER.exception("Failed to init_schedule for app '%s'", app)

        _login(http, username, password)

        if run_scheduler:
            scheduler.run()
