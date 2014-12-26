#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

from schlib.schdjangoext.dbtable import DbTable
from django.http import HttpResponse, HttpResponseRedirect
from schlib.schtools import schjson
from base64 import b32decode
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.conf import settings
from schlib.schmodels import import_model
from schlib.schtasks.base_task import get_process_manager


messageList = {
    'null': '',
    'error': 'Program error',
    'warning': 'Program warning',
    }


def message(
    request,
    titleid,
    messageid,
    id,
    ):
    global messageList
    title = messageList[titleid]
    if id != '0':
        message = messageList[messageid] % id
    else:
        message = messageList[messageid]
    c = RequestContext(request, {'title': title.decode('utf-8'), 'message'
                       : message.decode('utf-8')})
    return render_to_response('schsys/message.html', context_instance=c)


def tbl(
    request,
    app,
    tab,
    value=None,
    template_name=None,
    ):
    if request.POST:
        p = request.POST.copy()
        d = {}
        for (key, val) in list(p.items()):
            if key=='csrfmiddlewaretoken':
                d[str(key)] = val
            else:
                d[str(key)] = schjson.loads(val)
    else:
        d = {}
    if value and value != '':
        d['value'] = b32decode(value.encode('ascii'))
    dbtab = DbTable(app, tab)
    retstr = dbtab.command(d)
    return HttpResponse(retstr)


def datedialog(request, akcja):
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = b32decode(p['value'].encode('ascii'))
    else:
        value = ''
    if akcja == 'size':
        return HttpResponse(schjson.dumps((280, 200)))
    if akcja == 'dialog':
        if value.__class__ == int:
            import datetime
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            value = d
        c = RequestContext(request, {'value': value})
        return render_to_response('schsys/date.html', context_instance=c)
    if akcja == 'test':
        if value.__class__ == int:
            import datetime
            d = datetime.date.today()
            d = d + datetime.timedelta(int(value))
            return HttpResponse(schjson.dumps((1, d.isoformat(), (d, ))))
        else:
            if type(value)==bytes:
                value = value.decode('utf-8')
            return HttpResponse(schjson.dumps((1, value, (value,))))
        return HttpResponse('')
    return HttpResponse('')


def listdialog(request, akcja):
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = b32decode(p['value'].encode('ascii'))
        if value == None:
            value = ''
    else:
        value = ''

    if akcja == 'size':
        return HttpResponse(schjson.dumps((250, 300)))
    if akcja == 'dialog':
        c = RequestContext(request, {'value': value})
        return render_to_response('schsys/list.html', context_instance=c)
    if akcja == 'test':
        return HttpResponse(schjson.dumps((2, None, (None, ))))
    return HttpResponse('')


def treedialog(
    request,
    app,
    tab,
    id,
    akcja,
    ):
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = b32decode(p['value'].encode('ascii'))
        if value == None:
            value = ''
    else:
        value = ''
    if akcja == 'size':
        return HttpResponse(schjson.dumps((450, 400)))
    if akcja == 'dialog':
        model = import_model(app, tab)
        obj = None
        parent_pk = -1
        if int(id) >= 0:
            obj = model.objects.get(id=id)
            if obj and obj.parent:
                id2 = obj.parent.id
                if id2 and id2 > 0:
                    parent_pk = id2
        c = RequestContext(request, {
            'value': value,
            'app': app,
            'tab': tab,
            'pk': id,
            'parent_pk': parent_pk,
            'model': model,
            'object': obj,
            })
        return render_to_response('schsys/get_from_tree.html',
                                  context_instance=c)
    if akcja == 'test':
        return HttpResponse(schjson.dumps((2, None, (None, ))))
    return HttpResponse('')


def tabdialog(
    request,
    app,
    tab,
    id,
    akcja,
    ):
    if request.POST or request.GET:
        if request.POST:
            p = request.POST.copy()
        else:
            p = request.GET.copy()
        value = b32decode(p['value'].encode('ascii'))
        if value == None:
            value = ''
    else:
        value = ''
    if akcja == 'size':
        return HttpResponse(schjson.dumps((450, 400)))
    if akcja == 'dialog':
        model = import_model(app, tab)
        obj = None
        if int(id) >= 0:
            obj = model.objects.get(id=id)
        c = RequestContext(request, {
            'value': value,
            'app': app,
            'tab': tab,
            'id': id,
            'model': model,
            'obj': obj,
            })
        return render_to_response('schsys/get_from_tab.html',
                                  context_instance=c)
    if akcja == 'test':
        return HttpResponse(schjson.dumps((2, None, (None, ))))
    return HttpResponse('')


APP = None

def plugin_template(request, template_name):
    global APP
    if not APP:
        import wx
        APP = wx.GetApp()
    c = RequestContext(request)
    c['app'] = APP
    return render_to_response(template_name, context_instance=c)



def plugins(request, app, plugin_name):
    f = None
    try:
        f = open(settings.STATIC_ROOT + '/' + app + '/' + plugin_name + '.zip',
                 'rb')
    except:
        try:
            f = open(settings.ROOT_PATH + '/app_sets/' + app + '/schplugins/'
                      + plugin_name + '.zip', 'rb')
        except:
            raise Http404
    s = f.read()
    f.close()
    return HttpResponse(s, mimetype='application/zip')


def thread_list(request):
    l = get_process_manager().list_threads()
    user_dict = { 'object_list': l }
    c=RequestContext(request,user_dict)
    return render_to_response('schsys/thread_list.html', context_instance=c)


def thread_edit(request, thread_id):
    i = get_process_manager().thread_info(thread_id)
    if i:
        user_dict = { 'object': i }
    else:
        user_dict = { 'object': { 'id': 0, 'title': 'object deleted' }}
        
    c=RequestContext(request,user_dict)
    return render_to_response('schsys/thread_info.html', context_instance=c)


def thread_communicate(request, thread_id):
    if request.POST:
        if 'value' in request.POST:
            value = request.POST['value']
            get_process_manager().put_message(thread_id, value)
    l = get_process_manager().pop_messages(thread_id)
    value = schjson.json_dumps(l)
    return HttpResponse(value, mimetype="application/json")

def thread_get_messages(request, thread_id, start_id=0):
    if request.POST:
        if 'value' in request.POST:
            value = request.POST['value']
            get_process_manager().put_message(thread_id, value)
    l = get_task_manager().get_messages(thread_id, start_id)
    value = schjson.json_dumps(l)
    return HttpResponse(value)


def thread_kill(request, thread_id):
    get_process_manager().kill_thread(thread_id)
    return HttpResponseRedirect("/schsys/thread/-/form/list")
