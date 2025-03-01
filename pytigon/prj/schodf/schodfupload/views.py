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

from pytigon_lib.schfs.vfstools import get_temp_filename
from pytigon_lib.schdjangoext.spreadsheet_render import render_to_response_odf


class y(object):
    name = "Hello world!"


class x(object):
    stanowisko = y()


PFORM = form_with_perms("schodfupload")


class OdfUploadForm(forms.Form):
    odf_file = forms.FileField(
        label=_("Odf file"),
        required=True,
    )

    def process(self, request, queryset=None):

        return {"object": x()}

    def render_to_response(self, request, template, context_instance):
        odfdata = request.FILES["odf_file"]
        file_name = get_temp_filename("temp.ods")

        plik = open(file_name, "wb")
        plik.write(odfdata.read())
        plik.close()

        return render_to_response_odf(file_name, context_instance=context_instance)


def view_odfuploadform(request, *argi, **argv):
    return PFORM(request, OdfUploadForm, "schodfupload/formodfuploadform.html", {})


def odf_upload(request, *args, **argv):

    return PFORM(request, OdfUploadForm, "schodfupload/odf_upload.html", {})
