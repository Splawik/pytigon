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

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

import os
import sys


def compile_messages():
    basedir = None
    if os.path.isdir(os.path.join("conf", "locale")):
        basedir = os.path.abspath(os.path.join("conf", "locale"))
    elif os.path.isdir("locale"):
        basedir = os.path.abspath("locale")
    else:
        print(
            "this script should be run from the django svn tree or your project or app tree"
        )
        sys.exit(1)
    for (dirpath, dirnames, filenames) in os.walk(basedir):
        for f in filenames:
            if f.endswith(".po"):
                sys.stderr.write("processing file %s in %s\n" % (f, dirpath))
                pf = os.path.splitext(os.path.join(dirpath, f))[0]
                cmd = 'C:/Programy/GnuWin32/bin/msgfmt -o "%s.mo" "%s.po"' % (pf, pf)
                os.system(cmd)


if __name__ == "__main__":
    compile_messages()
