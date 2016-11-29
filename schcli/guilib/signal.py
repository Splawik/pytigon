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

class Signal:
    def __init__(self):
        self._signals={}

    def register_signal(self, obj, signal):
        if signal not in self._signals:
            self._signals[signal] = []
        if not obj in self._signals[signal]:
            self._signals[signal].append(obj)

    def unregister_signal(self, obj, signal):
        if obj in self._signals[signal]:
            id = self._signals[signal].index(obj)
            del self._signals[signal][id]

    def signal(self, signal, *argi, **argv):
        if signal in self._signals:
            for obj in self._signals[signal]:
                getattr(obj, signal)(*argi, **argv)
