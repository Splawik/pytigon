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

from pytigon_lib.schtools.schjson import json_loads

from django.apps import apps
import pyarrow
import duckdb
import numpy
import plotly


@dict_to_json
def plot_service(request, **argv):
    request_param = {"argv": argv}
    request_param["GET"] = request.GET
    if "param" in request.GET:
        request_param["param"] = request.GET["param"]
    else:
        request_param["param"] = None

    param = json_loads(request.body.decode("utf-8"))

    request_param["body"] = param

    action = param["action"]
    name = param["name"]

    objs = models.Plot.objects.filter(name=name)
    if len(objs) == 1:
        obj = objs[0]
    else:
        obj = None

    if obj:
        if action == "get_config":
            if obj.get_config:
                tmp = "def _get_config(obj, request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.get_config.split("\n")]
                )
                l = locals()
                exec(tmp, globals(), l)
                config = l["_get_config"](obj, request_param)
            else:
                config = {
                    "displayModeBar": False,
                    "showLink": False,
                    "displaylogo": False,
                    "scrollZoom": True,
                    "modeBarButtonsToRemove": ["sendDataToCloud"],
                }
            return config
        elif action == "get_data":
            if obj.get_data:
                tmp = "def _get_data(obj, request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.get_data.split("\n")]
                )
                l = locals()
                exec(tmp, globals(), l)
                data = l["_get_data"](obj, request_param)
            else:
                data = {}
            return data
        elif action == "get_layout":
            if obj.get_layout:
                tmp = "def _get_layout(obj, request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.get_layout.split("\n")]
                )
                l = locals()
                exec(tmp, globals(), l)
                layout = l["_get_layout"](obj, request_param)
            else:
                layout = {}
            return layout
        elif action == "on_event":
            if obj.on_event:
                tmp = "def _on_event(obj, data, request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.on_event.split("\n")]
                )
                l = locals()
                exec(tmp, globals(), l)
                ret = l["_on_event"](obj, param, request_param)
                return ret
            else:
                return {}
        else:
            return {"error": "Action not found"}

    return {"error": "Plot object not found"}
