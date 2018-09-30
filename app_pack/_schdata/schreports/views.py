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

from schlib.schviews.form_fun import form_with_perms
from schlib.schviews.viewtools import dict_to_template, dict_to_odf, dict_to_pdf, dict_to_json, dict_to_xml
from schlib.schviews.viewtools import render_to_response
from schlib.schdjangoext.tools import make_href

from django.utils.translation import ugettext_lazy as _

from . import models
import os
import sys
import datetime

from schlib.schtools.schjson import json_dumps, json_loads
from schlib.schdjangoext.django_ihtml import ihtml_to_html
from schlib.schdjangoext.fastform import form_from_str
from schlib.schviews import make_path
from schelements.models import DocReg, DocType, DocHead, OrgChartElem
from django.db.models import F
from schelements.views import year_ago

def move_rep(id, to_pos = "+1"):
    obj = models.Report.objects.get(pk=id)
    url = make_path('ok')
    if not obj.parent:
        return HttpResponseRedirect(url)
    
    if type(to_pos)==str:
        if to_pos=="+1":
            objects = models.Report.objects.filter(parent = obj.parent).filter(order__gt = obj.order)
            if len(objects)>0:
                obj2 = objects[0]
            else: 
                return HttpResponseRedirect(url)
        elif to_pos=='-1':    
            objects = models.Report.objects.filter(parent = obj.parent).filter(order__lt = obj.order)
            if len(objects)>0:
                obj2 = list(objects)[-1]
            else: 
                return HttpResponseRedirect(url)
                
        tmp_order = obj.order
        obj.order = obj2.order
        obj2.order = tmp_order
        obj.save()
        obj2.save()
        
    elif type(to_pos)==int:
        obj2 = models.Report.objects.get(pk=to_pos)
        order = obj2.order
        if obj.order < order:
            objects = models.Report.objects.filter(parent = obj.parent).filter(order__gt = obj2.order).update(order=F('order')+2)
            obj.order = order+1
        else:
            objects = models.Report.objects.filter(parent = obj.parent).filter(order__gte = obj2.order).update(order=F('order')+2)
            obj.order = order
        obj.save()

    url = make_path('ok')
    return HttpResponseRedirect(url)
 

PFORM = form_with_perms('schreports') 


class _FilterFormReport(forms.Form):
    date_from = forms.DateField(label=_('Data od'), required=None, initial=year_ago,)
    date_to = forms.DateField(label=_('Data do'), required=True, )
    
    def process(self, request, queryset=None):
    
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']
        
        if date_from:
            queryset = queryset.filter(date__gte = date_from)
        if date_to:
            queryset = queryset.filter(date__lte = date_to)
        return queryset
    
    def process_empty_or_invalid(self, request, queryset):
        return queryset.filter(date__gte = year_ago())

def view__filterformreport(request, *argi, **argv):
    return PFORM(request, _FilterFormReport, 'schreports/form_filterformreport.html', {})








def new_rep(request, rep_type,  doc_type_name):
    
    #new_rep/(?P<rep_type>\w+)/(?P<doc_type_name>\w+)/$
    doc_type = DocType.objects.filter(name=doc_type_name)
    if len(doc_type)==1:
        doc = DocHead()
        doc.doc_type_parent = doc_type[0]
        doc.date = datetime.datetime.now()
        doc.status = 'edit'
        doc.operator = request.user.username
        doc.save()
        
        rep = models.Report()
        rep.parent = None
        rep.order = doc.id
        rep.report_def_name = rep_type
        rep.date = datetime.datetime.now()
        rep.save()
        url = make_href("/schreports/table/Report/%d/edit__rep/" % rep.id)
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("Error - document type: %s doesn't exists" % doc_type_name)
    






def edit__rep(request, rep_id):
    
    rep = models.Report.objects.get(pk=rep_id)
    rep_def = models.ReportDef.objects.get(name=rep.report_def_name)
    
    if rep_def.declaration:
        form_class = form_from_str(rep_def.declaration)
    else:
        return "ERROR"
        
    if request.POST or request.FILES:    
        if request.method == 'POST':
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                if rep_def.save_fun:
                    exec(rep_def.save_fun)
                    data = locals()['save'](form, rep)
                else:
                    data = form.cleaned_data
                rep._data = data
                rep._data['json_update'] = True
                rep.save()
                url = make_path('ok')
                return HttpResponseRedirect(url)
        
    if not request.POST:
        data = rep.get_json_data()
        
        if rep_def.load_fun:
            exec(rep_def.load_fun)
            data_form = locals()['load'](data)
        else:
            data_form = data
        form = form_class(initial=data_form)
    
    t = Template(ihtml_to_html(None, rep_def.template))
    c = RequestContext(request, { 'form': form, 'rep': rep, 'rep_def': rep_def})
    
    return HttpResponse(t.render(c))
    






def new_subrep(request, parent_rep_id, rep_type):
    
    rep_parent = models.Report.objects.get(pk=parent_rep_id)
    rep = models.Report()
    rep.parent = rep_parent
    rep.order = 0
    rep.report_def_name = rep_parent.report_def_name + "/" + rep_type
    rep.date = datetime.datetime.now()
    rep.save()
    url = make_href("/schreports/table/Report/%d/edit__rep/" % rep.id)
    return HttpResponseRedirect(url)
    






def edit_subrep(request, parent_rep_id, rep_type,view_type):
    
    parent_rep = models.Report.objects.get(pk=parent_rep_id)
    parent_rep_def = models.ReportDef.objects.get(name=parent_rep.report_def_name)
    rep_def = parent_rep_def.getsubrep(rep_type)
    subreps = parent_rep.getsubreps(rep_type)
    
    cdict = {}    
    cdict['parent_rep'] = parent_rep
    cdict['parent_rep_def'] = parent_rep_def
    cdict['rep_type'] = rep_type
    cdict['view_type'] = view_type
    cdict['reports']= parent_rep.getsubreps(rep_type)
    cdict['rep_def'] = rep_def
    
    txt = ihtml_to_html(None, rep_def.to_html_rec)
    t = Template(txt)
    c = RequestContext(request,cdict)
    
    return HttpResponse(t.render(c))
    






def move_up(request, pk):
    
    return move_rep(pk, "-1")
    






def move_down(request, pk):
    
    return move_rep(pk, "+1")
    






def edit__rep2(request, dochead_id):
    
    reps = models.Report.objects.filter(order=dochead_id)
    if reps.count()>0:
        new_url = make_href("/schreports/table/Report/%d/edit__rep/" % reps[0].id)
        return HttpResponseRedirect(new_url)
    else:
        return HttpResponse("Error - report doesn't exist")
    






def repaction(request, dochead_id, rep_action):
    
    doc = DocHead.objects.get(pk=dochead_id)
    reps = models.Report.objects.filter(order=doc.id, parent=None)
    if reps.count()>0:
        url = make_href("/schreports/table/Report/%d/%s/" % (reps[0].id, rep_action.replace('__','/')))
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("Error - document: %d doesn't exists" % dochead_id)
        
    






def move_to(request, rep_id, to_pos):
    
    return move_rep(rep_id, int(to_pos))
    
    




@dict_to_json

def plot_service(request, **argv):
    
    param = json_loads(request.body.decode('utf-8'))
    
    action = param['action']
    name = param['name']
    
    objs = models.Plot.objects.filter(name=name)
    if len(objs) == 1:
        obj = objs[0]
    else:
        obj = None
    
    if obj:
        if action == 'get_data':
            if obj.get_data:
                tmp = "def _get_data():\n" + "\n".join([ "    " + pos for pos in obj.get_data.split('\n')])
                exec(tmp)
                data = locals()['_get_data']()        
            return data
        elif action == 'get_layout':
            if obj.get_layout:
                tmp = "def _get_layout():\n" + "\n".join([ "    " + pos for pos in obj.get_layout.split('\n')])
                exec(tmp)
                layout = locals()['get_layout']()        
            else:
                layout = {}
            return layout
        elif action == 'on_event':
            return {}
        else:
            return { 'error': 'Action not found'}
            
    return { 'error': 'Plot object not found'}
    


 
