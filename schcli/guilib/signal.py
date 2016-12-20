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
    """Helper class for sending signals between windows"""
    def __init__(self):
        self._signals={}

    def register_signal(self, obj, signal_name):
        """Register obj to receive signal.
        Object must have a function with name: signal_name
        Function must accept arguments passed to method: signal

        Args:
            obj - object to receive signals
            signal_name - name of signal
        """
        if signal_name not in self._signals:
            self._signals[signal_name] = []
        if not obj in self._signals[signal_name]:
            self._signals[signal_name].append(obj)

    def unregister_signal(self, obj, signal_name):
        """Unregister obj to receive signal

        Args:
            obj - object to receive signals
            signal_name - name of signal
        """
        if obj in self._signals[signal_name]:
            id = self._signals[signal_name].index(obj)
            del self._signals[signal_name][id]

    def signal(self, signal_name, *argi, **argv):
        """Send signal

        Args:
            signal_name - name of signal
            *argi, **argv - parameters of signal
        """
        if signal_name in self._signals:
            for obj in self._signals[signal_name]:
                getattr(obj, signal_name)(*argi, **argv)
