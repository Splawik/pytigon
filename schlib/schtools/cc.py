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
import platform
from schlib.schtools.process import run

def check_compiler(base_path):
    tcc_dir = os.path.join(base_path, "ext_prg", "tcc")
    if platform.system() == 'Windows':
        compiler = os.path.join(tcc_dir, "tcc.exe")
    else:
        compiler = os.path.join(tcc_dir, "tcc")
    return os.path.exists(compiler)


def compile(base_path, input_file_name, output_file_name=None, pyd=True):
    tcc_dir = os.path.join(base_path, "ext_prg", "tcc")
    include1 = os.path.join(tcc_dir, "include")
    include2 = os.path.join(include1, "python3.7")
    tmp = os.getcwd()
    os.chdir(tcc_dir)

    if output_file_name:
        ofn = output_file_name
    else:
        if platform.system() == 'Windows':
            if pyd:
                ofn = input_file_name.replace('.c', '') + ".pyd"
            else:
                ofn = input_file_name.replace('.c', '') + ".dll"
            compiler = ".\\tcc.exe"
        else:
            ofn = input_file_name.replace('.c', '')+".so"
            compiler = "./tcc"

    cmd = [compiler, input_file_name, '-o', ofn, '-shared']
    for include in (include1, include2):
        cmd.append('-I' + include + '')

    (ret_code, output, err) = run(cmd)
    os.chdir(tmp)
    return (ret_code, output, err)
