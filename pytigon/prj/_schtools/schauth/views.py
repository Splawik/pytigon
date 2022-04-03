from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import (
    dict_to_template,
    dict_to_odf,
    dict_to_pdf,
    dict_to_json,
    dict_to_xml,
    dict_to_ooxml,
    dict_to_txt,
)
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schdjangoext import formfields as ext_form_fields
from pytigon_lib.schviews import actions

from django.utils.translation import gettext_lazy as _

from . import models
import os
import sys
import datetime

from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth import get_user_model


def auth(request, key, path):

    if key == "POST":
        key = request.POST.get("key", "")
    objects = models.UrlWithAuth.objects.filter(key=key)
    if len(objects) == 1:
        username = objects[0].username
        users = get_user_model().objects.filter(username=username)
        if len(users) == 1:
            login(request, users[0])
            if path:
                new_url = make_href(path)
            else:
                new_url = make_href(objects[0].redirect_to)
                if not new_url.startswith("/"):
                    new_url = "/" + new_url
    else:
        new_url = make_href("/")

    p = request.get_full_path()
    if "?" in p:
        x = p.split("?", 1)
        if x[1]:
            new_url += "?" + x[1]

    return HttpResponseRedirect(new_url)


auth.csrf_exempt = True
