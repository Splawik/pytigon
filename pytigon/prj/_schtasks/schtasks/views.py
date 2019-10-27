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

from django.http import HttpResponse
from pytigon_lib.schtasks.base_task import get_process_manager
from pytigon_lib.schtools.schjson import json_dumps, json_loads

 

PFORM = form_with_perms('schtasks') 


class TaskListForm(forms.Form):
    time_from = forms.DateTimeField(label=_('Time from'), required=False, )
    time_to = forms.DateTimeField(label=_('Time to'), required=False, )
    only_my = forms.NullBooleanField(label=_('Only my'), required=False, )
    only_active = forms.NullBooleanField(label=_('Only active'), required=False, )
    
    def process(self, request, queryset=None):
    
        time_from = self.cleaned_data['time_from']
        time_to = self.cleaned_data['time_to']
        
        if time_from:
            _time_from = time_from.isoformat()
        else:
            _time_from = None
        if time_to:
            _time_to = time_to.isoformat()
        else:
            _time_to = None
        
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = 'guest'
        
        print("X1:", time_from, time_to)
        
        only_my = self.cleaned_data['only_my']
        only_active = self.cleaned_data['only_active']
        
        task_manager = get_process_manager()
        object_list  = []
        
        l = task_manager.list_threads(all=not only_active)
        for pos in l:
            test = True
            if time_from and pos['time_from'] <  time_from:
                test = False
            if time_to and (not pos['time_to'] or pos['time_to'] > time_to):
                test = False
            if only_my and pos['username'] != username:
                test = False
            if test:
                object_list.append(pos)
            
        return { "object_list": object_list, 'time_from': _time_from, 'time_to': _time_to, 'only_my': only_my, 'only_active': only_active }
    

def view_tasklistform(request, *argi, **argv):
    return PFORM(request, TaskListForm, 'schtasks/formtasklistform.html', {})








def put(request):
    
    fun = request.POST.get("func", "")
    title = request.POST.get("title", "")
    username = request.POST.get("username", "guest")
    param = json_loads(request.POST.get("param", "{}"))
    ret = get_process_manager().put(username, title, fun, **param)
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    






def put_message(request):
    
    id = request.POST.get("id", 0)
    message = request.POST.get("message", "")
    ret = get_process_manager().put_message(int(id), message)
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    






def get_messages(request):
    
    id = request.POST.get("id", 0)
    id_start = request.POST.get("id_start", 0)
    ret = get_process_manager().get_messages(int(id), int(id_start))
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    






def pop_messages(request):
    
    id = request.POST.get("id", 0)
    ret = get_process_manager().pop_messages(int(id))
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    






def kill_thread(request):
    
    id = request.POST.get("id", 0)
    ret = get_process_manager().kill_thread(int(id))
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    






def remove_thread(request):
    
    id = request.POST.get("id", 0)
    ret = get_process_manager().remove_thread(int(id))
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    






def list_threads(request):
    
    id = request.POST.get("id", 0)
    ret = get_process_manager().list_threads(int(id))
    ret2 = []
    for pos in ret:
        elem = {}
        elem['id'] = pos.id
        elem['title'] = pos.title
        elem['status'] = pos.status
        elem['username'] = pos.username
        elem['time_from'] = pos.time_from
        elem['time_to'] = pos.time_to
        ret2.append(elem)
    return HttpResponse(json_dumps(ret2), content_type = "application/json")
    






def thread_info(request):
    
    id = request.POST.get("id", 0)
    pos = get_process_manager().thread_info(int(id))
    
    elem = {}
    elem['id'] = pos.id
    elem['title'] = pos.title
    elem['status'] = pos.status
    elem['username'] = pos.username
    elem['time_from'] = pos.time_from
    elem['time_to'] = pos.time_to
    
    return HttpResponse(json_dumps(elem), content_type = "application/json")
    






def kill_all(request):
    
    id = request.POST.get("id", 0)
    ret = get_process_manager().kill_all(int(id))
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    






def wait_for_result(request):
    
    ret = get_process_manager().wait_for_result()
    return HttpResponse(json_dumps(ret), content_type = "application/json")
    

@dict_to_template('schtasks/v_edit_task.html')




def edit_task(request, id):
    
    if request.POST:
        task_manager = get_process_manager()
        task_manager.kill_thread(int(id))
        return { 'POST': "RETURN_OK" }
    else:
        task_manager = get_process_manager()
        object = task_manager.thread_info(int(id))
        messages = task_manager.get_messages(int(id))
        return { 'object': object, 'messages': messages }
    

@dict_to_template('schtasks/v_kill_task.html')




def kill_task(request, id):
    
    if request.POST:
        task_manager = get_process_manager()
        task_manager.kill_thread(int(id))
        return { 'POST': "RETURN_OK" }
    else:
        task_manager = get_process_manager()
        object = task_manager.thread_info(int(id))
        messages = task_manager.get_messages(int(id))
        return { 'object': object, 'messages': messages }
    




put.csrf_exempt = True
put_message.csrf_exempt = True
get_messages.csrf_exempt = True
pop_messages.csrf_exempt = True
kill_thread.csrf_exempt = True
remove_thread.csrf_exempt = True
list_threads.csrf_exempt = True
thread_info.csrf_exempt = True
kill_all.csrf_exempt = True
wait_for_result.csrf_exempt = True
 
