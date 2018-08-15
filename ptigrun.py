#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY  ; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import sys
import subprocess
import os

from schcli.pytigon import main

def run():
    if len(sys.argv)>1 and sys.argv[1].startswith('manage'):
        if '_' in sys.argv[1]:
            x = sys.argv[1].split('_',1)
            app = x[1]
            base_path = __file__.replace("ptigrun.py", "")
            if base_path == "":
                base_path = os.getcwd()
            else:
                os.chdir(base_path)
    
            path2 = os.path.join(base_path, "app_pack")
            path3 = os.path.join(path2, app)
            os.chdir(path3)
            subprocess.run(["../../python/bin/python", "manage.py"] + sys.argv[2:])            
            os.chdir(base_path)
        else:
            subprocess.run(["./python/bin/python", "manage.py"] + sys.argv[2:])
    else:
        main(sys.argv[1:])

if __name__ == '__main__':
    run()

