#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from schlib.schviews.form_fun import form_with_perms
from schlib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime












def autocomplete_search(request, type):
    
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
    


