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
    dict_to_hdoc,
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
from django.utils import timezone

import json
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from .models import history
from pytigon_lib.schhttptools import httpclient
from html.parser import HTMLParser
import re
from pytigon_lib.schhttptools import httpclient
from django_q.tasks import async_task, result

PFORM = form_with_perms("schbrowser")


class MultiDownload(forms.Form):
    base_address = forms.CharField(
        label=_("Base address"),
        required=True,
        initial="http://learningenglish.voanews.com",
        max_length=None,
        min_length=None,
    )
    source_page = forms.CharField(
        label=_("Source page"),
        required=False,
        initial="/archive/learningenglish-programs-radio-in-the-news/latest/1577/1577.html",
        max_length=None,
        min_length=None,
    )
    subpage_href = forms.CharField(
        label=_("Next page mask"),
        required=False,
        initial="/archive/learningenglish-programs-radio-in-the-news/.*;@/content/.*",
        max_length=None,
        min_length=None,
    )
    download_mask = forms.CharField(
        label=_("Download href mask"),
        required=False,
        initial=".*hq\.mp3.*",
        max_length=None,
        min_length=None,
    )
    levels = forms.IntegerField(
        label=_("Levels"), required=True, initial="10", max_value=None, min_value=None
    )
    test_only = forms.BooleanField(
        label=_("Test only"),
        required=False,
        initial=True,
    )

    def process(self, request, queryset=None):

        parm = {}
        parm["base_address"] = self.cleaned_data["base_address"]
        parm["source_page"] = self.cleaned_data["source_page"]
        parm["subpage_href"] = self.cleaned_data["subpage_href"]
        parm["download_mask"] = self.cleaned_data["download_mask"]
        parm["levels"] = self.cleaned_data["levels"]
        parm["test_only"] = self.cleaned_data["test_only"]

        if not "http" in parm["base_address"]:
            parm["base_address"] = "http://" + parm["base_address"]

        if not parm["source_page"]:
            parm["source_page"] = "/"

        task_manager = get_process_manager()
        _id = task_manager.put(
            request, "Scan html pages", "@schbrowser:scan_html", user_parm=parm
        )
        _id = async_task("schbrowser.tasks.scan_html", user_param=param)
        # l = task_manager.list_threads(all=True)
        object = task_manager.process_list[_id]
        # object = None
        # for pos in l:
        #    if pos.id == _id:
        #        object = pos
        #        break
        return {"ret": task_id}
        # return { "object": object }


def view_multidownload(request, *argi, **argv):
    return PFORM(request, MultiDownload, "schbrowser/formmultidownload.html", {})


def search(request):

    q = request.GET.get("term", request.POST.get("term", None))
    if not q:
        return HttpResponse(content_type="text/plain")

    limit = request.GET.get("limit", request.POST.get("limit", 15))

    try:
        limit = int(limit)
    except ValueError:
        return HttpResponseBadRequest()

    if q != " ":
        tab = history.objects.filter(url__istartswith=q)[:limit]
    else:
        tab = history.objects.all()[:limit]
    out_tab = []
    for pos in tab:
        out_tab.append({"id": pos.id, "label": pos.url, "value": pos.url})

    json_data = json.dumps(out_tab)
    return HttpResponse(json_data, content_type="application/x-javascript")
