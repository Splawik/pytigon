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


from .editor import init_control as init_control_edit
from .grid import init_control as init_control_grid

def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    app.register_ctrl_process_fun('ctrlstyledtext', init_control_edit)
    app.register_ctrl_process_fun('ctrlgrid', init_control_grid)
    app.register_ctrl_process_fun('ctrltable', init_control_grid)
