#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


def setup_databases(app_name):

    p = os.path.expanduser("~")
    db_name = os.path.join(p, ".pytigon/%s/%s.db" % (app_name, app_name))

    dbs = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "pytigon",
            "USER": "postgres",
            "PASSWORD": "anawaanawa",
            "HOST": "pytigon.cloud",
            #'HOST': '192.168.1.10',
        },
    }
    # auth = (
    #   'schserw.schsys.remotebackend.RemoteUserBackendMod',
    # )
    # return (dbs, auth)
    return (dbs, None)
