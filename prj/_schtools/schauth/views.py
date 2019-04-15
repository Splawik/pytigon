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
from schlib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User

 










def auth(request, key, path):
    
    objects = models.UrlWithAuth.objects.filter(key=key)
    if len(objects) == 1:
        username = objects[0].username
        users = User.objects.filter(username=username)
        if len(users)==1:
            login(request, users[0])
            if path:
                new_url = make_href(path)
            else:
                new_url = make_href(objects[0].redirect_to)
            return HttpResponseRedirect(new_url)
    
    new_url = reverse('start')
    return HttpResponseRedirect(new_url)
    




auth.csrf_exempt = True
 
