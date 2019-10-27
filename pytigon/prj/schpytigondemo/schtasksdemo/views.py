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

from pytigon_lib.schtasks.task import get_process_manager
import time
 








@dict_to_json

def gen_task1(request):
    
    task_manager = get_process_manager()
    task_manager.put(request, "Task title fun1", "@tasks_demo:fun1", user_parm = 123)
    return { "ret": "OK" }
    




@dict_to_json

def gen_task2(request):
    
    task_manager = get_process_manager()
    task_manager.put(request, "Task title fun2", "@tasks_demo:fun2", user_parm = 123)
    return { "ret": "OK" }
    




@dict_to_json

def gen_task3(request):
    
    task_manager = get_process_manager()
    task_manager.put(request, "Task title fun3", "@tasks_demo:fun3", user_parm = 123)
    return { "ret": "OK" }
    




@dict_to_json

def from_script(request):
    
    id = request.POST.get('id', 3)
    c = int(request.POST.get('count', '10'))
    date_rap = request.POST.get('date_rap', datetime.datetime.now().isoformat()[:19].replace('T', ' '))
    date_gen = request.POST.get('date_gen',datetime.datetime.now().isoformat()[:19].replace('T', ' '))
    
    for i in range(c):
        print("x"+str(i))
        time.sleep(1)
        
    return { "test": "OK", 'id': id, 'date_rap': date_rap, 'date_gen': date_gen, 'count': c }
        
    


 
