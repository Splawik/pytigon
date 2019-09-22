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

from django.urls import resolve

def year_ago():
    dt = datetime.date.today()    
    try:
        dt = dt.replace(year=dt.year-1)
    except ValueError:
        dt = dt.replace(year=dt.year-1, day=dt.day-1)
    return dt

def change_status(request, pk, action='accept'):    
    doc_head = models.DocHead.objects.get(pk=pk)
    doc_type = doc_head.doc_type_parent
    doc_reg = doc_type.parent
    action_name = request.GET.get('x1', '')
    reg_status_list = models.DocRegStatus.objects.filter(parent=doc_reg, name=action_name)
    if len(reg_status_list)==1:
        reg_status = reg_status_list[0]
    else: 
        reg_status = None

    if reg_status:

        if action=='accept':
            proc = reg_status.accept_proc
        else:
            proc = reg_status.undo_proc
        exec(proc)

        if 'get_form' in locals():
            form_class = locals()['get_form'](request, doc_head, reg_status, doc_type, doc_reg)
        else:
            form_class = None
            
        if 'get_description' in locals():
            description = locals()['get_description'](request, doc_head, reg_status, doc_type, doc_reg)
        else:
            description = None

        if request.POST:
            if form_class:
                form = form_class(request.GET, request.POST)
            else:
                form = None
            
            doc_status = models.DocHeadStatus()
            doc_status.parent = doc_head
            
            
            if action == 'accept':
                errors = locals()['accept'](request, doc_head, reg_status, doc_type, doc_reg, form, doc_status)
                new_status = action_name
            else:
                errors, new_status = locals()['undo'](request, doc_head, reg_status, doc_type, doc_reg, form, doc_status)
                        
            if not errors:
                
                doc_status.name = new_status
                if action=='accept':
                    doc_status.description = new_status + " <- " + doc_head.status
                else:
                    doc_status.description = action_name + " -> " + new_status

                doc_head.status = new_status
                doc_head.save()
                
                if action != 'accept':
                    models.DocItem.objects.filter(parent=doc_head, level__gte = reg_status.order).delete()
                
                doc_status.date = datetime.datetime.now()
                doc_status.operator = request.user.username
                doc_status.save()
                
                
                return { 'redirect': '/schsys/ok/' }
            else:
                return { 'error': status }
        else:        
            if form_class:
                form = form_class()
            else:
                form = None
            return { 'error': False, 'form': form, 'doc_head': doc_head, 'doc_type': doc_type, 'doc_reg': doc_reg, 'reg_status': reg_status, 
                'action_name': action_name, 'description': description 
            }
    else:
        return { 'error': "Status %s doesn't exists" % action_name }
 

PFORM = form_with_perms('schelements') 


class _FilterFormDocHead(forms.Form):
    date_from = forms.DateField(label=_('Date from'), required=True, initial=year_ago,)
    date_to = forms.DateField(label=_('Data to'), required=True, )
    target = forms.CharField(label=_('Target'), required=False, max_length=None, min_length=None)
    number = forms.CharField(label=_('Number'), required=False, max_length=None, min_length=None)
    
    def process(self, request, queryset=None):
    
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']
        target = self.cleaned_data['target']
        number = self.cleaned_data['number']
        
        if date_from:
            queryset = queryset.filter(date__gte = date_from)
        if date_to:
            queryset = queryset.filter(date__lt = date_to + datetime.timedelta(days=1))
        if target:
            queryset = queryset.filter(org_chart_parent__name__icontains = target)
        if number:
            queryset = queryset.filter(number__icontains = number)
        
        return queryset
    
    def process_empty_or_invalid(self, request, queryset):
        return queryset.filter(date__gte = year_ago())
        

def view__filterformdochead(request, *argi, **argv):
    return PFORM(request, _FilterFormDocHead, 'schelements/form_filterformdochead.html', {})








def view_doc_heads(request, filter, target, vtype):
    
    regs = models.DocReg.objects.filter(name = filter.replace('_','/'))
    if regs.count()>0:
        new_url = make_href("/schelements/table/DocHead/%s/%s/%slist/" % (filter, target, vtype))
        view, args, kwargs = resolve(new_url)
        kwargs['request'] = request
            
        #def init(view_obj):
        #    view_obj.template_name = "abc"    
        #kwargs['init'] = init
        
        return view(*args, **kwargs)
    else:
        return HttpResponse("Error - %s document register doesn't exists" % filter)
    






def view_doc_items(request, parent_id):
    
    items = models.DocItem.objects.filter(parent=parent_id)
    if items.count()>0:
        new_url = make_href("/schelements/table/DocHead/%s/%s/%slist" % (filter, target, vtype))
        view, args, kwargs = resolve(new_url)
        kwargs['request'] = request
        return view(*args, **kwargs)
    else:
        return HttpResponse("Error - %s document register doesn't exists" % filter)
    






def edit_head(request, id):
    
    return HttpResponse("Error")
    






def edit_item(request, id):
    
    return HttpResponse("Error")
    

@dict_to_template('schelements/v_approve.html')




def approve(request, pk):
    
    return change_status(request, pk, action='accept')    
    

@dict_to_template('schelements/v_discard.html')




def discard(request, pk):
    
    return change_status(request, pk, action='undo')    
    


 
