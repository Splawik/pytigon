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


from django.http import HttpResponse

_NEW_ROW_OK_HTML = """
<head>
    <meta name="RETURN" content="RETURN_OK" />
    <script>ret_ok(%s,"%s");</script>
</head>
<body></body>
"""

_NEW_ROW_OK_SHTML = """
<head>
    <meta name="RETURN" content="RETURN_OK" />
    <meta name="target" content="code" />
</head>
<body>
    <script language=python>
page = self.get_parent_page().get_parent_page()
if page:
    page.signal('return_new_row', id=%s, title="%s")
self.ok()
    </script>
</body>
"""

_UPDATE_ROW_OK_HTML = """
<head>
    <meta name="RETURN" content="RETURN_OK" />
    <script>ret_ok(%s,"%s");</script>
</head>
<body></body>
"""

_UPDATE_ROW_OK_SHTML = """
<head>
    <meta name="RETURN" content="RETURN_OK" />
    <meta name="target" content="code" />
</head>
<body>
    <script language=python>
page = self.get_parent_page().get_parent_page()
if page:
    page.signal('return_updated_row', id=%s, title="%s")
self.ok()
    </script>
</body>
"""


def new_row_action(request, id, title):
    if request.META['HTTP_USER_AGENT'].lower().startswith('py'):
        return HttpResponse(_NEW_ROW_OK_SHTML % (id, title))
    else:
        return HttpResponse(_NEW_ROW_OK_HTML % (id, title))


def update_row_action(request, id, title):
    if request.META['HTTP_USER_AGENT'].lower().startswith('py'):
        return HttpResponse(_UPDATE_ROW_OK_SHTML % (id, title))
    else:
        return HttpResponse(_UPDATE_ROW_OK_HTML % (id, title))
