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

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime



PFORM = form_with_perms('schsimplecontrolsdemo') 


class TestForm(forms.Form):
    test_field_1 = forms.CharField(label=_('Test field 1'), required=True, )
    test_field_2 = forms.BooleanField(label=_('Test field 2'), required=True, )
    test_field_3 = forms.DateField(label=_('Test field 3'), required=True, )
    test_field_4 = forms.EmailField(label=_('Test field 4'), required=False, )
    integer_field = forms.IntegerField(label=_('Integer field'), required=True, )
    float_field = forms.FloatField(label=_('FloatField'), required=True, )
    
    def process(self, request, queryset=None):
    
        object_list = [
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8],
        ]
        
        return { 'object_list': object_list }
    

def view_testform(request, *argi, **argv):
    return PFORM(request, TestForm, 'schsimplecontrolsdemo/formtestform.html', {})






@dict_to_json

def json_test(request, x, y):
    
    return (int(x)+int(y), x, y)
    



