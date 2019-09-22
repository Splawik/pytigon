#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General PubliLicense
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import sys
import xmlrpc.client
from time import sleep
import subprocess
import os
import os.path

_base_path = __file__.replace("sched.py", "")
if _base_path == "":
    _base_path =  os.getcwd()

PYTIGON_PATH = os.path.normpath(os.path.join(_base_path, "../.."))

with xmlrpc.client.ServerProxy("http://localhost:8090/") as proxy:
    repeat = True
    run = False
    while repeat:
        repeat = False
        try:
            proxy.test()
        except ConnectionRefusedError as error:
            repeat = True
            if not run:
                run = True
                subprocess.Popen([sys.executable, os.path.join(PYTIGON_PATH,'pytigon'), '--rpc=8090', '--no_splash', 'scheditor' ])
            sleep(0.2)

    if sys.argv and len(sys.argv)>1:
        file_name = sys.argv[1]
        if file_name:
            if not (file_name[0] in ('/', '\\') or (len(file_name)>1 and file_name[1] == ':')):
                x = os.getcwd()
                file_name = os.path.join(x, file_name)
            
            if len(file_name)>1 and file_name[1]==':' and file_name[0].lower()=='c':            
                proxy.edit("/osfs"+file_name[2:])
            else:
                proxy.edit("/osfs"+file_name)
