#!/usr/bin/python

# -*- coding: utf-8 -*-

from django.core.files.storage import default_storage

def filesystemcmd(cproxy, *args, **kwargs):
    """bacground tasks related to file system"""
    param = kwargs['user_parm']
    cmd = param['cmd']
    files = param['files']
    dest = param['dest'] + "/"
    if cmd == 'DELETE':
        for f in files:
            try:
                if default_storage.fs.isfile(f):
                    default_storage.fs.remove(f)
                else:
                    default_storage.fs.removedir(f, recursive=True, force=True)
            except:
                pass
    elif cmd == 'COPY':
        for f in files:
            try:
                name = f.rsplit('/',1)[-1]
                if default_storage.fs.isfile(f):
                    default_storage.fs.copy(f, dest+name, overwrite=True)
                else:
                    default_storage.fs.copydir(f, dest+name, overwrite=True, ignore_errors=True)
            except:
                pass
    elif cmd == 'MOVE':
        for f in files:
            try:
                name = f.rsplit('/',1)[-1]
                if default_storage.fs.isfile(f):
                    default_storage.fs.move(f, dest+name, overwrite=True)
                else:
                    default_storage.fs.movedir(f, dest+name, overwrite=True, ignore_errors=True)
            except:
                pass
    cproxy.log("finish")
