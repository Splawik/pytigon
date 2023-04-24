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


@dict_to_template("templates_demo/v_excel_report.html")
def excel_report(request, **argv):

    object_list = []

    for i in range(1, 10000):
        object_list.append(("title " + str(i), i))

    return {
        "doc_type": "xlsx",
        "object_list": object_list,
        "sheet_names": ["abc", "def"],
        "sheet_name": "abc",
    }


@dict_to_template("templates_demo/v_odf_report.html")
def odf_report(request, **argv):

    object_list = []

    for i in range(1, 10000):
        object_list.append(("title " + str(i), i))

    return {
        "doc_type": "ods",
        "object_list": object_list,
        "sheet_names": ["abc", "def"],
        "sheet_name": "abc",
    }
