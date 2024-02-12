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


PFORM = form_with_perms("forms_demo")


class form_test(forms.Form):
    bolean_field = forms.BooleanField(
        label=_("Boleand field"),
        required=False,
    )
    char_field = forms.CharField(
        label=_("Char field"), required=True, max_length=None, min_length=None
    )
    choice_field = forms.ChoiceField(
        label=_("Choice field"), required=False, choices=models.test_choice
    )
    multiplechoice_field = forms.MultipleChoiceField(
        label=_("Multiple choice field"), required=False, choices=models.test_choice
    )
    date_field = forms.DateField(
        label=_("Date field"),
        required=True,
    )
    datetime_field = forms.DateTimeField(
        label=_("DateTime field"),
        required=True,
    )
    time_field = forms.TimeField(
        label=_("Time field"),
        required=False,
    )
    decimal_field = forms.DecimalField(
        label=_("Decimal field"),
        required=False,
        max_value=1000000,
        min_value=-1000000,
        max_digits=12,
        decimal_places=4,
    )
    integer_field = forms.IntegerField(
        label=_("Integer field"), required=False, max_value=100, min_value=0
    )
    float_foield = forms.FloatField(
        label=_("Float field"), required=False, max_value=1000000, min_value=-1000000
    )
    email_field = forms.EmailField(
        label=_("Email field"),
        required=True,
    )

    def process(self, request, queryset=None):

        object_list = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
        ]

        return {"object_list": object_list}


def view_form_test(request, *argi, **argv):
    return PFORM(request, form_test, "forms_demo/formform_test.html", {})


class form_test2(forms.Form):
    image_field = forms.ImageField(
        label=_("Image field"),
        required=True,
    )
    file_field = forms.FileField(
        label=_("File fileld"),
        required=True,
    )
    file_path_field = forms.FilePathField(
        label=_("File path field"),
        required=True,
        path="/",
        match=None,
        recursive=False,
        allow_files=True,
        allow_folders=False,
    )
    ip_field = forms.GenericIPAddressField(
        label=_("IP field"), required=True, protocol="both", unpack_ipv4=False
    )
    url_field = forms.URLField(
        label=_("URL field"), required=True, max_length=None, min_length=None
    )
    regex_field = forms.RegexField(
        label=_("Regular expression field"),
        required=True,
        regex="^\d{11}$",
        max_length=None,
        min_length=None,
    )
    slug_field = forms.SlugField(
        label=_("Slug field"),
        required=True,
    )
    uuid_field = forms.UUIDField(
        label=_("UUID field"),
        required=True,
    )
    typedchoice_field = forms.TypedChoiceField(
        label=_("Typed choice field"),
        required=False,
        coerce=int,
        empty_value="",
        choices=models.test_choice,
    )
    typedmultipechoice_field = forms.TypedMultipleChoiceField(
        label=_("Typed multiple choice field"),
        required=False,
        coerce=int,
        empty_value="",
        choices=models.test_choice,
    )
    user_field = forms.CharField(max_length=100)

    def process(self, request, queryset=None):

        object_list = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
        ]

        return {"object_list": object_list}


def view_form_test2(request, *argi, **argv):
    return PFORM(request, form_test2, "forms_demo/formform_test2.html", {})


class form_test3(forms.Form):
    selec2_field = ext_form_fields.Select2Field(
        label=_("Select2 field"), required=False, choices=models.test_choice
    )
    select2multipe_field = ext_form_fields.Select2MultipleField(
        label=_("Select2 multiple field"), required=False, choices=models.test_choice
    )
    heavyselect2_field = ext_form_fields.HeavySelect2Field(
        label=_("Heavy select2 field"),
        required=False,
        data_url="/forms_demo/select2query/",
    )
    heavyselec2multiple_field = ext_form_fields.HeavySelect2MultipleField(
        label=_("Heavy select2 multiple field"),
        required=False,
        data_url="/forms_demo/select2query/",
    )
    modelselect2_field = ext_form_fields.ModelSelect2Field(
        label=_("Model select2 field"),
        required=False,
        queryset=models.Select2Example.objects.all(),
        search_fields=[
            "name__icontains",
        ],
    )
    modelselect2multipe_field = ext_form_fields.ModelSelect2MultipleField(
        label=_("Model select2 multiple field"),
        required=False,
        queryset=models.Select2Example.objects.all(),
        search_fields=[
            "name__icontains",
        ],
    )
    modelchoice_field = forms.ModelChoiceField(
        label=_("Model choice field"),
        required=False,
        queryset=models.Select2Example.objects.all(),
    )
    modelmultiplechoice_field = forms.ModelMultipleChoiceField(
        label=_("Model multiple choice field"),
        required=False,
        queryset=models.Select2Example.objects.all(),
    )

    def process(self, request, queryset=None):

        object_list = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
        ]

        return {"object_list": object_list}


def view_form_test3(request, *argi, **argv):
    return PFORM(request, form_test3, "forms_demo/formform_test3.html", {})


class form_test4(forms.Form):
    test = forms.CharField(
        label=_("test"), required=True, max_length=None, min_length=None
    )
    test2 = forms.ChoiceField(
        label=_("Test2"), required=True, choices=models.test_choice
    )

    def process(self, request, queryset=None):

        object_list = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
        ]

        return {"object_list": object_list}


def view_form_test4(request, *argi, **argv):
    return PFORM(request, form_test4, "forms_demo/formform_test4.html", {})


@dict_to_json
def select2query(request, **argv):

    term = request.GET.get("term", "")
    numbers = ["Zero", "One", "Two", "Three", "Four", "Five"]
    numbers2 = [item for item in enumerate(numbers) if term in item[1]]
    results = [{"id": item[0], "text": item[1]} for item in numbers2]
    return {"err": None, "results": results}


@dict_to_template("forms_demo/v_list2.html")
def list2(request, **argv):

    prev_value = request.GET.get("q")
    return {"prev_value": prev_value}


@dict_to_template("forms_demo/v_list3.html")
def list3(request, **argv):

    prev_value = request.GET.get("q")
    return {"prev_value": prev_value}
