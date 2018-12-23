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

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

import sys
import os

def init_paths():

    tmp = []
    for pos in sys.path:
        if not pos in tmp:
            if not pos.startswith('.'):
                tmp.append(pos)
    sys.path = tmp

    from schlib.schtools.platform_info import platform_name
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    pname = platform_name()

    if pname == 'Android':
        p = os.path.abspath(os.path.join(base_path, "..", "_android"))
        p2 = os.path.abspath(os.path.join(base_path, "..", "ext_lib"))
        if not p in sys.path: sys.path.insert(0, p)
        if not p2 in sys.path: sys.path.append(p2)
    else:
        if pname == "Windows":
            p = os.path.abspath(os.path.join(base_path, "..", "python" "lib", "site-packages"))
        else:
            p = os.path.abspath(os.path.join(base_path , "..", "python", "lib",\
                "python%d.%d/site-packages" % (sys.version_info[0], sys.version_info[1])))

        p2 = os.path.abspath(os.path.join(base_path, "..", "ext_lib"))

        if not p in sys.path: sys.path.insert(0, p)
        if not p2 in sys.path: sys.path.append(p2)
