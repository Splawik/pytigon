# -*- coding: utf-8 -*-
import os
import PythonTidy

#dirnames = ['./schcli', './schlib', './schserw', './prj', './templates_src']
dirnames = ['./prj/schods', ]

signature="""#!/usr/bin/python
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
"""


def tidy_clean(dirname):
    for ff in os.listdir(dirname):
        name = os.path.join(dirname, ff)
        if os.path.isdir(name):
            dirname2 = os.path.join(dirname, ff)
            tidy_clean(dirname2)
        else:
            if name[-3:] == '.py':
                try:
                        PythonTidy.tidy_up(file_in=name, file_out=name+".clean")
                except:
                        if name[-11:] == '__init__.py':
                                try:
                                        f = open(name,"r")
                                        buf = f.read()
                                        f.close()
                                        f2 = open(name+".clean", "w")
                                        f2.write(buf)
                                        f2.close()
                                except:
                                       print name
                        else:
                                f = open(name,"r")
                                buf = f.read()
                                f.close()
                                f2 = open(name+".clean", "w")
                                f2.write(buf)
                                f2.close()
                                print name

                        f = open(name,"r")
                        buf = f.read()
                        f.close()
                        f2 = open(name+".bak", "w")
                        f2.write(buf)
                        f2.close()

                        f = open(name+".clean","r")
                        buf = f.read()
                        f.close()
                        f2 = open(name, "w")
                        f2.write(buf)
                        f2.close()


                #f = open(name, "r")
                #s = f.read()
                #f.close()
                #f2 = open(name+".bak", "w")
                #f2.write(s)
                #f2.close()
                #f3 = open(name, "w")
                #f3.write(signature)
                #f3.write("\n")
                #f3.write(s)
                #f3.close()

for dirname in dirnames:
    tidy_clean(dirname)

