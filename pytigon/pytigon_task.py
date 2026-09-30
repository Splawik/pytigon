#!/usr/bin/env python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3, or (at your option) any later
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

import argparse
import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Module-level logger
LOGGER = logging.getLogger("pytigon_task")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    Returns:
        argparse.ArgumentParser: The configured parser.
    """
    parser = argparse.ArgumentParser(
        prog="pytigon_task.py",
        description=(
            "Run a pytigon view directly, or start the task scheduler for an app."
        ),
    )
    parser.add_argument(
        "-a",
        "--arguments",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="argument passed to the view; use '__' for a space in the value. "
        "May be given more than once.",
    )
    parser.add_argument("-u", "--username", help="login username")
    parser.add_argument("-p", "--password", help="login password")
    parser.add_argument(
        "target",
        metavar="APPSET[:VIEW]",
        help="application name, optionally followed by ':' and a view to call",
    )
    return parser


def parse_arguments(raw_arguments):
    """Turn the raw ``-a`` values into a dict.

    Args:
        raw_arguments: List of ``KEY=VALUE`` strings.

    Returns:
        tuple: ``(arguments, force_get)``. ``force_get`` is True when any value
        was malformed, in which case the view is called with GET instead of
        POST.
    """
    arguments = {}
    force_get = False
    for raw in raw_arguments:
        # partition (not split) so a value may itself contain "=".
        key, separator, value = raw.replace("__", " ").partition("=")
        if separator:
            arguments[key] = value
        else:
            force_get = True
    return arguments, force_get


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


def _run_view(http, view, arguments, force_get):
    """Invoke a single view over HTTP.

    Args:
        http: HttpClient instance.
        view: View address.
        arguments: Dict of view parameters.
        force_get: Call with GET even when arguments are present.

    Returns:
        tuple: ``(body, new_address)`` as returned by the client.
    """
    if force_get:
        return http.get(None, view, arguments)
    if arguments:
        return http.post(None, view, arguments)
    return http.get(None, view)


def _run_scheduler(arguments, force_get, username, password, http):
    """Start the task scheduler for the selected application.

    Args:
        arguments: Dict of parameters.
        force_get: Whether parameters should be sent via GET.
        username: Login username.
        password: Login password.
        http: HttpClient instance.

    Returns:
        int: Process exit code. 1 when no application registered any task, so
        the caller does not report success for a run that did nothing.
    """
    from apps import APPS  # noqa: PLC0415 - needs the app on sys.path first
    from django.conf import settings

    from pytigon_lib.schdjangoext.django_manage import cmd
    from pytigon_lib.schtasks import schschedule
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

    if not run_scheduler:
        LOGGER.warning("No application defined init_schedule; nothing to run")
        return 1

    _login(http, username, password)
    scheduler.run()
    return 0


def main(argv=None) -> int:
    """Run the task scheduler or a single view.

    Args:
        argv: Argument list without the program name. Defaults to ``sys.argv[1:]``.

    Returns:
        int: Process exit code.
    """
    from pytigon_lib.schhttptools import httpclient
    from pytigon_lib.schtools.main_paths import get_main_paths

    paths = get_main_paths()

    sys.path.append(paths["PRJ_PATH"])
    sys.path.append(paths["PRJ_PATH_ALT"])

    options = build_parser().parse_args(argv)

    prj, _, view = options.target.partition(":")
    if not prj:
        build_parser().error("no application given")

    arguments, force_get = parse_arguments(options.arguments)

    sys.path.insert(0, os.path.join(paths["PRJ_PATH"], prj))
    sys.path.insert(0, os.path.join(paths["PRJ_PATH_ALT"], prj))

    os.environ["PYTIGON_TASK"] = "1"
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings_app"
    httpclient.init_embeded_django()
    http = httpclient.HttpClient("http://127.0.0.2")

    if view:
        _login(http, options.username, options.password)
        _run_view(http, view, arguments, force_get)
        return 0

    return _run_scheduler(
        arguments, force_get, options.username, options.password, http
    )


if __name__ == "__main__":
    sys.exit(main())
