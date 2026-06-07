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
from django.http import Http404
from django.http import JsonResponse
from pytigon_lib.schdjangoext.fastform import form_from_str
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct
from django.conf import settings

import datetime
import pyarrow
import pyarrow.parquet
import duckdb
import numpy
import os
import os.path as os_path
import plotly
import plotly.graph_objects as go

import uuid
from io import StringIO

models.refresh_data("begin")


def project_view(request, prj_name):

    try:
        prj = models.Project.objects.get(name=prj_name)
    except:
        raise Http404

    models.refresh_data("before")

    session_key = "bi_" + prj_name
    if not session_key in request.session:
        request.session[session_key] = {}

    if prj.form:
        form_class = form_from_str(prj.form, init_data={"prj": prj, "models": models})
        if request.method == "POST":
            json_data = json.loads(request.body)
            modified = False
            for key, value in json_data.items():
                if key in ("name", "new_value"):
                    continue
                key2 = prj_name + "/" + key
                if not (
                    key2 in request.session[session_key]
                    and request.session[session_key][key2] == value
                ):
                    request.session[session_key][key2] = value
                    modified = True
            request.session.modified = modified
            return JsonResponse({"send_event": {"refresh_bi_project": prj.name}})
        else:
            data = {}
            for key, value in request.session[session_key].items():
                if key.startswith(prj_name + "/"):
                    key = key.split("/")[-1]
                    data[key] = value
            form = form_class(initial=data)
    else:
        form = None

    if prj.template:
        t = Template(ihtml_to_html(None, prj.template))
    else:
        template = '% extends "schbi/base_project.html"\n'
        t = Template(ihtml_to_html(None, template))

    data = {}
    if prj.view:
        data = run_code_from_db_field(
            f"bi_prj_{prj.name}_view.py",
            prj,
            "view",
            "view",
            request=request,
            module=ModuleStruct(globals(), locals()),
            prj=prj,
        )

    c = RequestContext(
        request,
        {"form": form, "bi_prj": prj, "data": data | request.session[session_key]},
    )
    return HttpResponse(t.render(c))


def page_view(request, page_id):

    try:
        page = models.Page.objects.get(pk=page_id)
    except:
        raise Http404

    models.refresh_data("before")

    session_key = "bi_" + page.parent.name
    if not session_key in request.session:
        request.session[session_key] = {}

    if page.form:
        form_class = form_from_str(page.form)

        if request.method == "POST":
            json_data = json.loads(request.body)
            modified = False
            for key, value in json_data.items():
                if key in ("name", "new_value"):
                    continue
                key2 = page.name + "/" + page.parent.name + "/" + key
                if not (
                    key2 in request.session[session_key]
                    and request.session[session_key][key2] == value
                ):
                    request.session[session_key][key2] = value
                    modified = True
            request.session.modified = modified
            return JsonResponse({"send_event": {"refresh_bi_page": page.name}})
        else:
            data = {}
            for key, value in request.session[session_key].items():
                if key.startswith(page.name + "/" + page.parent.name + "/"):
                    key = key.split("/")[-1]
                    data[key] = value
            form = form_class(initial=data)
    else:
        form = None

    if page.template:
        t = Template(ihtml_to_html(None, page.template))
    else:
        template = '% extends "schbi/base_page.html"\n'
        t = Template(ihtml_to_html(None, template))

    data = {}
    if page.view:
        data = run_code_from_db_field(
            f"bi_prj_{page.parent.name}_page_{page.name}_view.py",
            page,
            "view",
            "view",
            request=request,
            module=ModuleStruct(globals(), locals()),
            page=page,
        )

    c = RequestContext(
        request,
        {"form": form, "page": page, "data": data | request.session[session_key]},
    )
    return HttpResponse(t.render(c))


def chart_view(request, chart_id):

    try:
        chart = models.Chart.objects.get(pk=chart_id)
    except:
        raise Http404

    models.refresh_data("before")

    session_key = "bi_" + chart.parent.parent.name
    if not session_key in request.session:
        request.session[session_key] = {}

    if chart.form:
        form_class = form_from_str(chart.form)

        if request.method == "POST":
            json_data = json.loads(request.body)
            modified = False
            for key, value in json_data.items():
                if key in ("name", "new_value"):
                    continue
                key2 = (
                    chart.name
                    + "/"
                    + chart.parent.name
                    + "/"
                    + chart.parent.parent.name
                    + "/"
                    + key
                )
                if not (
                    key2 in request.session[session_key]
                    and request.session[session_key][key2] == value
                ):
                    request.session[session_key][key2] = value
                    modified = True
            request.session.modified = modified
            return JsonResponse({"send_event": {"refresh_bi_chart": chart.name}})
        else:
            data = {}
            for key, value in request.session[session_key].items():
                if key.startswith(
                    chart.name
                    + "/"
                    + chart.parent.name
                    + "/"
                    + chart.parent.parent.name
                    + "/"
                ):
                    key = key.split("/")[-1]
                    data[key] = value
            form = form_class(initial=data)
    else:
        form = None

    if chart.template:
        t = Template(ihtml_to_html(None, chart.template))
    else:
        template = '% extends "schbi/base_chart.html"\n'
        t = Template(ihtml_to_html(None, template))

    data = {}
    if chart.view:
        data = run_code_from_db_field(
            f"bi_prj_{chart.parent.parent.name}_chart_{chart.name}_view.py",
            chart,
            "view",
            "view",
            request=request,
            module=ModuleStruct(globals(), locals()),
            chart=chart,
        )
    c = RequestContext(
        request,
        {"form": form, "chart": chart, "data": data | request.session[session_key]},
    )
    return HttpResponse(t.render(c))
