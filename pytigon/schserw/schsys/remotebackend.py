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

"""Module contain RemoteUserBackend class"""

from django.contrib.auth.backends import RemoteUserBackend


class RemoteUserBackendMod(RemoteUserBackend):
    """Backend for apache authorization"""

    def clean_username(self, username):
        """Replace '\\' in username. For username in format: domain\\user cleaned version is domain_users."""
        return username.lower().replace("\\", "_").strip()
