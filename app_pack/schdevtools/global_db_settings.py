
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import pymysql
pymysql.install_as_MySQLdb()

def setup_databases(app_name):

    p = os.path.expanduser("~")
    db_name = os.path.join(p, ".pytigon/%s/%s.db" % (app_name, app_name))

    dbs =    {'default':  
                    {  
                        'ENGINE': 'django.db.backends.mysql',
                        'NAME': 'sch',
                        'USER': 'root',
                        'PASSWORD': 'AnawaAnawa1',
                        'HOST': 'pytigondev.tk',
                    },
    }
    #auth = (
    #   'schserw.schsys.remotebackend.RemoteUserBackendMod',
    #)
    #return (dbs, auth)
    return (dbs, None)