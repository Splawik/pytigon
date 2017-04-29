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
import platform
import os


def init_paths():
    from schlib.schtools.platform_info import platform_name
    
    base_path = __file__.replace("__init__.py", "")

    if base_path == "":
        base_path = "./"

    pname = platform_name()

    if pname == 'Android':
        p = base_path + "../android"
        p2 = base_path + "../ext_lib"
        p = os.path.abspath(p)
        p2 = os.path.abspath(p2)
        sys.path.insert(0, p)
        sys.path.append(p2)
    else:
        if pname == "Windows":
            p = base_path + "../python/lib/site-packages"
        else:
            platform_name
            p = base_path + "../python/lib/python%d.%d/site-packages" % (sys.version_info[0], sys.version_info[1])

        p2 = base_path + "../ext_lib"

        p = os.path.abspath(p)
        p2 = os.path.abspath(p2)
        sys.path.insert(0, p)
        sys.path.append(p2)

        tmp = []
        for pos in sys.path:
            if not pos in tmp:
                if not '.zip' in pos:
                    tmp.append(pos)
        sys.path = tmp

