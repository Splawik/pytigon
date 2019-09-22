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












def akceptacja1(request, pk):
    
    pass
    






def akceptacja2(request, pk):
    
    pass
    






def pdf(request, pk):
    
    audyt = models.Audyt.objects.get(id=pk)
    
    t = Template(audyt.parent.dane)
    c = Context({"object": audyt})
    ret_str = t.render(c)
    sql_list = ret_str.split("|||")
    tab = []
    for sql in sql_list:
        with  settings.DB:
            db.execute(sql)
            object_list=db.fetchall()
            tab.append(list(object_list))
    
    t = Template(audyt.parent.template)
    c = Context({"object": audyt, "tab": tab })
    ret_str = t.render(c)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename='raport.pdf'"
    
    response.write(ret_str)
    return response
    

@dict_to_template('audyty/v_change_accept.html')




def change_accept(request, pk):
    
    return {}
    



