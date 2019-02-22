#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import os
import datetime
import zipfile
from shutil import move
from pathlib import Path

from django.conf import settings
from schlib.schdjangoext.django_manage import *
from schlib.schfs.vfstools import extractall
from schlib.schtools.process import py_run
from schlib.schtools.cc import check_compiler, compile


def post_install(base_path, app_path):
    ret_output = []
    ret_errors = []
    ret = 0

    test_cc =  check_compiler(base_path)

    applib = os.path.join(app_path, 'applib')
    p = Path(applib)
    fl = p.glob('**/*.pyx')
    for pos in fl:
        pyx_filename = p.joinpath(pos).as_posix()
        if test_cc:
            c_filename = pyx_filename.replace('.pyx', '.c')
            (ret_code, output, err) = py_run(['-m', 'cython',  pyx_filename])
            if ret_code:
                ret = ret_code
            if output:
                for pos in output:
                    ret_output.append(pos)
            if err:
                for pos in err:
                    ret_errors.append(pos)
            if os.path.exists(c_filename):
                (ret_code, output, err) = compile(base_path, c_filename, pyd=True)
                if ret_code:
                    ret = ret_code
                os.unlink(c_filename)
                if output:
                    for pos in output:
                        ret_output.append(pos)
                if err:
                    for pos in err:
                        ret_errors.append(pos)
        else:
            out_filename = pyx_filename.replace('.pyx', '.py')
            with open(pyx_filename, "rt") as f_in:
                with open(out_filename, "wt") as f_out:
                    f_out.write(f_in.read())
    if check_compiler(base_path):
        fl = p.glob('**/*.c')
        for pos in fl:
            c_filename = p.joinpath(pos).as_posix()
            if os.path.exists(c_filename):
                (ret_code, output, err) = compile(base_path, c_filename, pyd=False)
                if ret_code:
                    ret = ret_code
                if output:
                    for pos in output:
                        ret_output.append(pos)
                if err:
                    for pos in err:
                        ret_errors.append(pos)

    return (ret, ret_output, ret_errors)


def install():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")
    appset_name = settings.APPSET_NAME
    data_path = settings.DATA_PATH
    root_path = settings.ROOT_PATH
    app_pack_path = settings.APP_PACK_PATH
    app_data_path = os.path.join(data_path, appset_name)
    db_path = os.path.join(app_data_path, appset_name+".db")
    if os.path.exists(db_path):
        return True
    else:
        if 'local' in settings.DATABASES:
            db_profile = 'local'
        else:
            db_profile = 'default'

        db_path_new = os.path.join(app_data_path, appset_name + ".new")
        db_path_old = os.path.join(app_data_path, appset_name + ".old")
        new_db = False
        old_db = False

        if os.path.exists(db_path_old):
            old_db = True
            os.rename(db_path_old, db_path)
        elif os.path.exists(db_path_new):
            new_db = True
            os.rename(db_path_new, db_path)

        try:
            cmd(['migrate', '--database', db_profile])
        except:
            print("Migration for database: " + db_profile + " - fails")
        if db_profile != 'default':
            try:
                cmd(['migrate', '--database', 'default'])
            except:
                print("Migration for database: defautl - fails")

        if old_db:
            pass
        elif new_db:
            if db_profile != 'default':
                temp_path = os.path.join(data_path, 'temp')
                if not os.path.exists(temp_path):
                    os.mkdir(temp_path)
                json_path = os.path.join(temp_path, appset_name + '.json')
                cmd(['dumpdata', '--database', db_profile, '--format', 'json', '--indent', '4',
                     '-e', 'auth', '-e', 'contenttypes', '-e', 'sessions', '-e', 'sites', '-e', 'admin',
                     '--output', json_path])
                cmd(['loaddata', '--database', 'default', json_path])
                from django.contrib.auth.models import User
                User.objects.db_manager('default').create_superuser('auto', 'auto@pytigon.com', 'anawa')
        else:
            from django.contrib.auth.models import User
            User.objects.db_manager(db_profile).create_superuser('auto', 'auto@pytigon.com', 'anawa')
            if db_profile != 'default':
                User.objects.db_manager('default').create_superuser('auto', 'auto@pytigon.com', 'anawa')
    ret = post_install(root_path, app_pack_path)
    if ret:
        for pos in ret:
            print(pos)

def export_to_local_db():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")
    if 'local' in settings.DATABASES:
        db_profile = 'local'
    else:
        db_profile = 'default'

    if db_profile != 'default':
        appset_name = settings.APPSET_NAME
        data_path = settings.DATA_PATH
        app_data_path = os.path.join(data_path, appset_name)
        db_path = os.path.join(app_data_path, appset_name+".db")

        if os.path.exists(db_path):
            os.rename(db_path, db_path + "." + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".bak")

        cmd(['migrate', '--database', db_profile])

        temp_path = os.path.join(data_path, 'temp')
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        json_path = os.path.join(temp_path, appset_name + '.json')
        cmd(['dumpdata', '--database', 'default', '--format', 'json', '--indent', '4',
             '-e', 'auth', '-e', 'contenttypes', '-e', 'sessions', '-e', 'sites', '-e', 'admin',
             '--output', json_path])
        cmd(['loaddata', '--database', db_profile, json_path])
        from django.contrib.auth.models import User
        User.objects.db_manager(db_profile).create_superuser('auto', 'auto@pytigon.com', 'anawa')



def extract_ptig(zip_file, name):

    ret = []
    ret.append("Install file: " + name)
    test_update = True

    extract_to = os.path.join(settings.APP_PACK_PATH, name)
    ret.append("install to: " + extract_to)

    if not os.path.exists(settings.APP_PACK_PATH):
        os.mkdir(settings.APP_PACK_PATH)
    if not os.path.exists(extract_to):
        os.mkdir(extract_to)
        test_update = False

    zipname = datetime.datetime.now().isoformat('_')[:19].replace(':', '').replace('-', '')
    zipname2 = os.path.join(extract_to, zipname + ".zip")
    if test_update:
        backup_zip = zipfile.ZipFile(zipname2, 'a')
        exclude = ['.*settings_local.py.*', ]
    else:
        backup_zip = None
        exclude = None

    extractall(zip_file, extract_to, backup_zip=backup_zip, exclude=exclude,
               backup_exts=['py', 'txt', 'wsgi', 'ihtml', 'htlm', 'css', 'js', ])

    if backup_zip:
        backup_zip.close()
    zip_file.close()

    src_db = os.path.join(extract_to, name + ".db")
    if os.path.exists(src_db):
        ret.append("Synchronize database:")
        dest_path_db = os.path.join(settings.DATA_PATH, name)

        if not os.path.exists(settings.DATA_PATH):
            os.mkdir(settings.DATA_PATH)
        if not os.path.exists(dest_path_db):
            os.mkdir(dest_path_db)
        dest_db = os.path.join(dest_path_db, name + ".db")
        if not os.path.exists(dest_db):
            move(src_db, os.path.join(dest_path_db, name + ".new"))
        else:
            os.rename(dest_db, os.path.join(dest_path_db, name + ".old"))

        (ret_code, output, err) = py_run([os.path.join(extract_to, 'manage.py'), 'post_installation'])

        if output:
            for pos in output:
                ret.append(pos)
        if err:
            ret.append("ERRORS:")
            for pos in err:
                ret.append(pos)

    return ret
