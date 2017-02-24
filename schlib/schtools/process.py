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

import sys
from subprocess import Popen, PIPE

def py_run(cmd):
    """run python script

    args:
        cmd - array of parameters

    returns:
        array:
            return code,
            return stdout data
            return stderr data
    example:
        py_run(["manage.py", "help"])
    """
    process = Popen([sys.executable,]+cmd, stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if output:
        if type(output) != str:
            s = output.decode('utf-8')
        else:
            s = output
        output_tab = [ pos.replace('\r','') for pos in s.split('\n') ]
    else:
        output_tab = None

    if err:
        if type(err) != str:
            s = err.decode('utf-8')
        else:
            s = err
        err_tab = [pos.replace('\r', '') for pos in s.split('\n')]
    else:
        err_tab = None
    return (exit_code, output_tab, err_tab)
