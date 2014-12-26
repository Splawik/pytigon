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

try:
    from Cython.Compiler import Main
except:
    pass

import os
import ctypes
import platform

_libtcc=None

def load_libtcc(base_path):
    global _libtcc
    if _libtcc:
        return True

    if platform.system() == "Linux":
        file_and_path_to_tcclib = base_path + "/tcc/libtcc.so.1.0"
    else:
        file_and_path_to_tcclib = base_path + "/tcc/libtcc.dll"
    try:
        libtcc=ctypes.cdll.LoadLibrary(file_and_path_to_tcclib)
    except:
        _libtcc = None
        return False
    return True

def _req0(funname,retval):
    if retval!=0:
        raise ValueError("%s returned error code %s." % (funname,retval))

def compile(path_ptx, base_path):
    for f in os.listdir(path_ptx):
        if f[-4:]=='.pyx':
            dest = path_ptx + "/" + f.replace('.pyx', '.c')
            dest = dest.replace('\\','/')
            src = path_ptx + "/" + f
            options = dict(Main.default_options)
            options['output_file'] = dest
            Main.compile(src, options)
            if load_libtcc(base_path):
                tccstate=_libtcc.tcc_new()
                _req0("set_output_type", _libtcc.tcc_set_output_type(tccstate,2))
                if platform.system() == "Linux":
                    _req0("add_file", _libtcc.tcc_add_include_path(tccstate, (base_path+"/ppython/include").encode('utf-8')))
                    _req0("add_file", _libtcc.tcc_add_file(tccstate,dest.encode('utf-8')))
                    _req0("output_file", _libtcc.tcc_output_file(tccstate, dest.replace('.c','.so').encode('utf-8')))
                else:
                    _req0("add_file", _libtcc.tcc_add_include_path(tccstate, (base_path+"/ppython/include").encode('utf-8')))
                    _req0("add_file", _libtcc.tcc_add_file(tccstate,dest.encode('utf-8')))
                    _req0("add_file", _libtcc.tcc_add_file(tccstate,(base_path + "/tcc/lib/python32.def").encode('utf-8')))
                    _req0("output_file", _libtcc.tcc_output_file(tccstate, dest.replace('.c','.pyd').encode('utf-8')))
                _libtcc.tcc_delete(tccstate)


