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

import json 
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Autocomplete


def autocomplete_search(request, typ):
    if not request.REQUEST.get('query'):
        return HttpResponse(content_type='text/plain')
    q = request.REQUEST.get('query')
    limit = request.REQUEST.get('limit', 15)
    try:
        limit = int(limit)
    except ValueError:
        return HttpResponseBadRequest()
    if q != ' ':
        tab = Autocomplete.objects.filter(type=typ, label__istartswith=q)[:limit]
    else:
        tab = Autocomplete.objects.filter(type=typ)[:limit]
    out_tab = []
    for pos in tab:
        out_tab.append({'id': pos.id, 'label': pos.label, 'name': pos.label, 'value': pos.value})
    json_data = json.dumps(out_tab)
    return HttpResponse(json_data, content_type='application/x-javascript')


