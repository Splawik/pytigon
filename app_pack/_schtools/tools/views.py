#!/usr/bin/python

# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from schlib.schviews.form_fun import form_with_perms
from schlib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml
from schlib.schviews.viewtools import render_to_response

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime












def autocomplete_search(request, type):
    
    q = request.GET.get('query', request.POST.get('query', None))
    if not q:
        return HttpResponse(content_type='text/plain')
    limit = request.GET.get('limit', request.POST.get('limit', 15))
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
    



