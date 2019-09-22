# -*- coding: utf-8 -*-

import django
from django.db import models

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *

import pytigon_lib.schdjangoext.fields as ext_models

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


from schtools.models import *



from django.contrib.auth.models import User, Group
from django.template.base import Template
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from django.template.loader import select_template
import datetime
from django.db import transaction



element_type_choice = (
    ("C","Currency"),
    ("M","Material"),
    ("D","Device"),
    ("I","Intellectual"),
    ("S","Service"),
    ("R","Raw material"),
    ("N","Intermediate"),
    ("P","Product"),
    ("DI","Device IT"),
    ("DP","Production machine"),
    ("DV","Vehicle"),
    
    )

target_type_choice = (
    ("F","Firm"),
    ("P","Person"),
    ("E","Employee"),
    ("S","Section"),
    
    )

account_type_choice_2 = (
    ("B","Balance"),
    ("O","Off-balance"),
    ("N","Non-financial"),
    
    )

account_type_choice_1 = (
    ("S","Synthetic"),
    ("A","Analytical"),
    
    )

orgchart_type_choice = (
    ("F","Firm"),
    ("D","Division"),
    ("R","Department"),
    ("S","Position"),
    ("E","Employee"),
    ("L","Location"),
    ("O","Other"),
    ("P","Person"),
    ("M","Machine"),
    
    )

accdoc_type_choices = (
    ("A","Account"),
    
    )

accdoc_status_choices = (
    ("0","Edit"),
    ("1","Approved"),
    ("2","Settled"),
    ("3","Posted 1"),
    ("4","Posted 2"),
    ("5","Frozen"),
    ("9","Canceled"),
    
    )

doctype_status = (
    ("0","Disabled"),
    ("1","Activ"),
    
    )




class Element(JSONModel):
    
    class Meta:
        verbose_name = _("Element")
        verbose_name_plural = _("Element")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    type = models.CharField('Element type', null=False, blank=False, editable=True, choices=element_type_choice,max_length=3)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=256)
    

    def __str__(self):
        return self.description
    
admin.site.register(Element)


class OrgChartElem(TreeModel):
    
    class Meta:
        verbose_name = _("Organizational chart")
        verbose_name_plural = _("Organizational chart")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    
    parent = ext_models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    

    parent = ext_models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Parent', )
    type = models.CharField('Organisation type', null=False, blank=False, editable=True, choices=orgchart_type_choice,max_length=1)
    grand_parent1 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 1', related_name='grandparent1')
    grand_parent2 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 2', related_name='grandparent2')
    grand_parent3 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 3', related_name='grandparent3')
    grand_parent4 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 4', related_name='grandparent4')
    code = models.CharField('Code', null=True, blank=True, editable=True, max_length=16)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    key =  models.ForeignKey('auth.Group', on_delete=models.CASCADE, null=True, blank=True,)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=64)
    

    def init_new(self, request, view, param=None):
        defaults = { 'type': 'S' }
        return defaults
    
    def get_name(self):
        return self.name
    
    def firm(self):
        tab = self.parents()
        for pos in tab:
            if pos.type=='F':
                return pos
        return None
    
    def division(self):
        tab = self.parents()
        for pos in tab:
            if pos.type=='D':
                return pos
        return None
    
    def departament(self):
        return None
    
    def position(self):
        return None
    
    def location(self):
        return None
    
    def related(self):
        ret = ""
        for obj in (self.grand_parent1, self.grand_parent2, self.grand_parent3, self.grand_parent4):
            if obj:
                if ret == "":
                    ret = obj.name
                else:
                    ret = ret + "; " + obj.name
        return ret
    
    def parents(self):
        p = []
        parent = self.parent
        while(parent):
            p.append(parent)
            if parent==parent.parent:
                break
            parent = parent.parent
        return p
    
    def path(self):
        p = self.parents()
        n=""
        for parent in p:
            if parent.code and parent.code!="":
                n = "/" + przodek.code + n
            else:
                n = "/?" + n
        return n + "/" + self.code
    
    def href_path(self):
        p = self.parents()
        n=""
        for parent in p:
            href = "<a target='_refresh_data' href='../../%s/form/tree'>" % parent.id
            if parent.code and parent.code!="":
                n = href + parent.code + "</a>/" + n
            else:
                n = href + "?</a>/" + n
        return "<a target='_refresh_data' href='../../0/form/tree'>/</a>" + n + self.code
    
    def href_path_list(self):
        p = self.parents()
        n=[]
        for parent in p:
            href = "<a target='_refresh_data' href='../../%s/form/tree'>" % parent.id
            if parent.code and parent.code!="":
                n.append(href + parent.code + "</a>")
            else:
                n.append(href + "?</a>")
        n.append("<a target='_refresh_data' href='../../0/form/tree'>/</a>")
        return n
    
    
    def __str__(self):
        p = self.parents()
        if self.code and self.code!="":
            n = self.code + ":" + self.name
        else:
            n = self.name
        for parent in p:
            if parent.code and parent.code!="":
                n = parent.code + "/" + n
            else:
                n = "?/" + n
        return n
    
    @staticmethod
    def gen_url(value):
        if value:
            id = int(value)
        else:
            id = -1
        return "/schsys/treedialog/schelements/OrgChart/%s/" % id
        
    
admin.site.register(OrgChartElem)


class Classifier(TreeModel):
    
    class Meta:
        verbose_name = _("Classifier")
        verbose_name_plural = _("Classifier")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    
    parent = ext_models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    

    parent = ext_models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=32)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    

    def __str__(self):
        return self.description
    
admin.site.register(Classifier)


class DocReg( models.Model):
    
    class Meta:
        verbose_name = _("Document register")
        verbose_name_plural = _("Document registers")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    app = models.CharField('Application', null=False, blank=False, editable=True, max_length=16)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=32)
    group = models.CharField('Group', null=True, blank=True, editable=True, max_length=64)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    head_form = models.TextField('Head form', null=True, blank=True, editable=False, )
    item_form = models.TextField('Item form', null=True, blank=True, editable=False, )
    save_head_fun = models.TextField('Save head function', null=True, blank=True, editable=False, )
    save_item_fun = models.TextField('Save item function', null=True, blank=True, editable=False, )
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def get_parent(self):
        if '/' in self.name:
            x = self.name.rsplit('/',1)
            objs = DocReg.objects.filter(name=x[0])
            if len(objs)==1:
                return objs[0]
        return None
    
    def get_last_subname(self):
        if '/' in self.name:
            return self.name.rsplit('/',1)[1]
        else:
            return self.name
    
admin.site.register(DocReg)


class DocType( models.Model):
    
    class Meta:
        verbose_name = _("Type of document")
        verbose_name_plural = _("Types of documents")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(DocReg, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=16)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    correction = ext_models.NullBooleanField('Correction', null=True, blank=True, editable=True, )
    head_form = models.TextField('Head form', null=True, blank=True, editable=False, )
    item_form = models.TextField('Item form', null=True, blank=True, editable=False, )
    save_head_fun = models.TextField('Save head function', null=True, blank=True, editable=False, )
    save_item_fun = models.TextField('Save item function', null=True, blank=True, editable=False, )
    doctype_status = models.CharField('Status of document type', null=True, blank=True, editable=True, choices=doctype_status,max_length=1)
    

    
admin.site.register(DocType)


class DocHead(JSONModel):
    
    class Meta:
        verbose_name = _("Document header")
        verbose_name_plural = _("Document headers")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parents = models.ManyToManyField('self', null=False, blank=False, editable=False, verbose_name='Parents', )
    doc_type_parent = ext_models.HiddenForeignKey(DocType, on_delete=models.CASCADE, null=False, blank=False, editable=False, verbose_name='Document type parent', )
    org_chart_parent = ext_models.HiddenForeignKey(OrgChartElem, on_delete=models.CASCADE, null=True, blank=True, editable=False, verbose_name='Organization chart parent', )
    number = models.CharField('Document number', null=True, blank=True, editable=True, max_length=32)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=64)
    date = models.DateTimeField('Date', null=False, blank=False, editable=False, )
    status = models.CharField('Status', null=True, blank=True, editable=False, max_length=16)
    operator = models.CharField('Operator', null=True, blank=True, editable=False, max_length=32)
    param1 = models.CharField('Parameter 1', null=True, blank=True, editable=True, max_length=16)
    param2 = models.CharField('Parameter 2', null=True, blank=True, editable=True, max_length=16)
    param3 = models.CharField('Parameter 3', null=True, blank=True, editable=True, max_length=16)
    

    @classmethod
    def get_documents_for_reg(cls, value):
        reg = DocReg.objects.filter(name = value.replace('_', '/'))
        ret = []
        if len(reg) == 1:
            docs = DocType.objects.filter(parent=reg[0])
            for doc in docs:
                ret.append(doc)
        return ret
    
    @classmethod
    def filter(cls, value):
        if value:
            rej = value.replace('_','/')
            return cls.objects.filter(doc_type_parent__parent__name = rej)
        else:
            return cls.objects.all()
    
    
    def init_new(self, request, view, add_param=None):
        if add_param:
            docs = DocType.objects.filter(name = add_param)
            if len(docs)==1: 
                self.doc_type_parent = docs[0]
                self.date = datetime.datetime.now()
                self.status = 'edit'
                self.operator = request.user.username
                
        return None
        
    
    @staticmethod
    def template_for_list(context, doc_type):
        if doc_type in ('html', 'json') and 'filter' in context:
            tmp = DocReg.objects.filter(name=context['filter'].replace('_','/'))
            if len(tmp)==1:
                names = []
                x = tmp[0]
                while x:
                    names.append((x.app+"/"+x.name.replace('/','_')+"_dochead_list.html").lower())
                    x = x.get_parent()
                
                template = select_template(names)
                if template:
                    return template
                
        return None
        
        
    def template_for_object(self, context, doc_type):
        if self.id and doc_type in ('html', 'json'):
            try:
                obj = DocHead.objects.get(pk=self.id)            
                reg = obj.doc_type_parent.parent
                names = []
                names.append((reg.app+"/"+obj.doc_type_parent.name+"_dochead_edit.html").lower())        
                names.append((reg.app+"/"+reg.name.replace('/', '_') + "_dochead_edit.html").lower())
                x = reg.get_parent()
                while x:
                    names.append((x.app+"/"+x.name.replace('/', '_') + "_dochead_edit.html").lower())
                    x = x.get_parent()
            
                template = select_template(names)
                if template:
                    return template
            except:
                return None
        return None
        
    
    def get_form_source(self):
        if self.id:
            obj = DocHead.objects.get(pk=self.id)            
            if obj.doc_type_parent.head_form:
               return obj.doc_type_parent.head_form 
               
            x = obj.doc_type_parent.parent
            while x:
                if x.head_form:
                    return x.head_form
                x = x.get_parent()
        
        return None
    
    
    def save(self, *args, **kwargs):
        if self.id:
            obj = DocHead.objects.get(pk=self.id)
            save_fun_src = None
            if obj.doc_type_parent.save_head_fun:
                save_fun_src = obj.doc_type_parent.save_head_fun
            else:
                x = obj.doc_type_parent.parent
                while x:
                    if x.save_head_fun:
                        save_fun_src = x.save_head_fun
                        break
                    x = x.get_parent()
            if save_fun_src:
                exec(save_fun_src)
            
        super().save(*args, **kwargs)
        
    def get_visible_statuses(self, request=None):
        if self.id:
            obj = DocHead.objects.get(pk=self.id)
            reg = obj.doc_type_parent.parent
            while reg:
                statuses = reg.docregstatus_set.all().order_by('order')
                if len(statuses)>0:
                    ret = []
                    for status in statuses:
                        if status.can_set_proc:
                            exec(status.can_set_proc)
                            data = locals()['can_set_proc'](request, self)
                            if data:
                                ret.append(status)
                        else:
                            ret.append(status)
    
                    return ret
                    
                reg = reg.get_parent()
                
        return []
    
    def status_can_be_undo(self, request=None):
        if self.id:
            obj = DocHead.objects.get(pk=self.id)
            reg = obj.doc_type_parent.parent
            statuses = reg.docregstatus_set.filter(name=obj.status)
            if len(statuses)==1:
                status = statuses[0]
                if status.can_undo_proc:
                    exec(status.can_undo_proc)
                    data = locals()['can_undo_proc'](request, self)
                    if data:
                        return True
                    else:
                        return False
            if obj.status == "" or obj.status == "edit":
                return False
            else:
                return True
        
        return False        
        
    
admin.site.register(DocHead)


class DocItem(JSONModel):
    
    class Meta:
        verbose_name = _("Document item")
        verbose_name_plural = _("Document items")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(DocHead, on_delete=models.CASCADE, null=False, blank=False, editable=False, verbose_name='Parent', )
    parent_item = ext_models.HiddenForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=False, verbose_name='Parent item', )
    order = models.IntegerField('Order', null=False, blank=False, editable=False, default=1,)
    date = models.DateField('Date', null=False, blank=False, editable=False, )
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=255)
    amount = models.DecimalField('Amount', null=True, blank=True, editable=True, max_digits=16, decimal_places=2)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Element', )
    level = models.IntegerField('Level', null=False, blank=False, editable=False, default=0,)
    param1 = models.CharField('Parameter 1', null=True, blank=True, editable=False, max_length=16)
    param2 = models.CharField('Parameter 2', null=True, blank=True, editable=False, max_length=16)
    param3 = models.CharField('Parameter 3', null=True, blank=True, editable=False, max_length=16)
    

    @staticmethod
    def template_for_list(context, doc_type):
        if doc_type in ('html', 'json'):
            if 'parent_pk' in context['view'].kwargs:
                parent_pk = int(context['view'].kwargs['parent_pk'])
                dochead = DocHead.objects.get(pk=parent_pk)
                reg = dochead.doc_type_parent.parent            
                names = []
                names.append((reg.app+"/"+dochead.doc_type_parent.name+"_docitem_list.html").lower())
                names.append((reg.app+"/"+reg.name.replace('/', '_') + "_docitem_list.html").lower())
                
                x = reg.get_parent()
                while x:
                    names.append(x.app+"/"+x.name.replace('/', '_') + "_docitem_list.html")
                    x = x.get_parent()
                    
                template = select_template(names)
                if template:
                    return template
                
        return None
        
        
    def template_for_object(self, context, doc_type):
        if doc_type in ('html', 'json'):
            try:
                obj = DocItem.objects.get(pk=self.id)            
                dochead = obj.parent
                reg = dochead.doc_type_parent.parent            
                names = []
                names.append((reg.app+"/"+dochead.doc_type_parent.name+"_docitem_edit.html").lower())
                names.append((reg.app+"/"+reg.name.replace('/', '_') + "_docitem_edit.html").lower())
                
                x = reg.get_parent()
                while x:
                    names.append(x.app+"/"+x.name.replace('/', '_') + "_docitem_edit.html")
                    x = x.get_parent()
                    
                template = select_template(names)
                if template:
                    return template
            except:
                return None
                            
        return None
        
    
    def get_form_source(self):
        #obj = DocItem.objects.get(pk=self.id)            
        obj = self
        if obj.parent.doc_type_parent.item_form:
           return obj.parent.doc_type_parent.item_form 
           
        x = obj.parent.doc_type_parent.parent
        while x:
            if x.item_form:
                return x.item_form
            x = x.get_parent()
        
        return None
    
    def init_new(self, request, view, param=None):
        if 'parent_pk' in view.kwargs:
            parent_pk = view.kwargs['parent_pk']
            parent = DocHead.objects.get(pk=parent_pk)
            items = DocItem.objects.filter(parent=parent).order_by('-order')
            if len(items)>0:
                max_nr = int(items[0].order)+1
            else:
                max_nr = 1
            
            if request.POST:
                return { 'parent': str(parent.id), 'order': max_nr, 'date': datetime.datetime.now(), 'level': 0 }
            
        return None
    
    
    def save(self, *args, **kwargs):
        if self.id:
            obj = DocItem.objects.get(pk=self.id).parent
            save_fun_src = None
            if obj.doc_type_parent.save_head_fun:
                save_fun_src = obj.doc_type_parent.save_item_fun
            else:
                x = obj.doc_type_parent.parent
                while x:
                    if x.save_head_fun:
                        save_fun_src = x.save_item_fun
                        break
                    x = x.get_parent()
            if save_fun_src:
                exec(save_fun_src)
            
        super().save(*args, **kwargs)
        
    
admin.site.register(DocItem)


class DocRegStatus( models.Model):
    
    class Meta:
        verbose_name = _("Document status")
        verbose_name_plural = _("Document status")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(DocReg, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    order = models.IntegerField('Order', null=False, blank=False, editable=True, )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=16)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=64)
    icon = models.CharField('Icon', null=True, blank=True, editable=True, max_length=64)
    accept_proc = models.TextField('Accept status procedure', null=True, blank=True, editable=False, )
    undo_proc = models.TextField('Undo status procedure', null=True, blank=True, editable=False, )
    can_set_proc = models.TextField('Check if status can be set', null=True, blank=True, editable=False, )
    can_undo_proc = models.TextField('Check if status can be removed', null=True, blank=True, editable=False, )
    

    
admin.site.register(DocRegStatus)


class DocHeadStatus(JSONModel):
    
    class Meta:
        verbose_name = _("Document head status")
        verbose_name_plural = _("Documents head status")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(DocHead, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    date = models.DateTimeField('Date', null=False, blank=False, editable=True, )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=16)
    description = models.CharField('Description', null=True, blank=True, editable=False, max_length=64)
    operator = models.CharField('Operator', null=True, blank=True, editable=True, max_length=32)
    

    
admin.site.register(DocHeadStatus)


class Account(TreeModel):
    
    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Account")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    
    parent = ext_models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    

    parent = ext_models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Parent', )
    type1 = models.CharField('Type 1', null=True, blank=True, editable=False, choices=account_type_choice_1,max_length=1)
    type2 = models.CharField('Type 2', null=True, blank=True, editable=True, choices=account_type_choice_2,max_length=1)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=32)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=256)
    root_classifier1 = ext_models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Root classifier 1', related_name='baseaccount_rc1_set')
    root_classifier2 = ext_models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Root classifier 2', related_name='baseaccount_rc2_set')
    root_classifier3 = ext_models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Root classifier 3', related_name='baseaccount_rc3_set')
    enabled = ext_models.NullBooleanField('Enabled', null=False, blank=False, editable=True, default=True,)
    

    def save(self, *args, **kwargs):
        if self.parent:
            self.parent.type1='S'
            self.parent.save()
            self.type2 = self.parent.type2
        self.type1 = 'A'
        super().save(*args, **kwargs)
    
    def __str__(self):
        x = self
        ret = self.name
        while(x.parent):
            x = x.parent
            ret = x.name + "/" + ret
        ret+=": "
        ret+=self.description
        return ret
            
    
admin.site.register(Account)


class AccountState( models.Model):
    
    class Meta:
        verbose_name = _("State of account")
        verbose_name_plural = _("States of account")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    target = models.ForeignKey(OrgChartElem, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Target', )
    classifier1value = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Classifier 1 value', related_name='account_c1_set')
    classifier2value = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Classifier 2 value', related_name='account_c2_set')
    classifier3value = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Classifier 3 value', related_name='account_c3_set')
    period = models.CharField('Period', null=True, blank=True, editable=True, max_length=10)
    subcode = models.CharField('Subcode', null=True, blank=True, editable=True, max_length=16)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Element', )
    debit = models.DecimalField('Debit', null=False, blank=False, editable=True, max_digits=16, decimal_places=2)
    credit = models.DecimalField('Credit', null=False, blank=False, editable=True, max_digits=16, decimal_places=2)
    aggregate = ext_models.NullBooleanField('Aggregate', null=False, blank=False, editable=True, default=False,)
    

    
admin.site.register(AccountState)


class AccountOperation( models.Model):
    
    class Meta:
        verbose_name = _("Account operation")
        verbose_name_plural = _("Account operations")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.HiddenForeignKey(DocItem, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    date = models.DateTimeField('Date', null=False, blank=False, editable=False, default=datetime.datetime.now,)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=255)
    payment = models.CharField('Name of payment', null=True, blank=True, editable=True, max_length=64)
    account_state = ext_models.ForeignKey(AccountState, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Account state', related_name='accountoper_set')
    sign = models.IntegerField('Sign - debit or credit', null=False, blank=False, editable=True, )
    amount = models.DecimalField('Amount', null=False, blank=False, editable=True, max_digits=16, decimal_places=2)
    enabled = ext_models.NullBooleanField('Enabled', null=True, blank=True, editable=False, default=False,)
    

    def get_account_state(self, account, element, period, target, classifier1=None, classifier2=None, classifier3=None, subcode="", aggregate=False):
        if type(account)==str:
            _account = Account.objects.filter(name=account)[0]
        else:
            _account = account
        
        if type(element)==str:
            _element = Element.objects.filter(name=element)[0]
        else:
            _element = element    
    
        if type(target)==str:
            _target = OrgChartElem.objects.filter(code=target)[0]
        else:
            _target = target
        
        
        objs = AccountState.objects.filter(parent=_account, target=_target, classifier1value=classifier1, classifier2value=classifier2, classifier3value=classifier3, period=period, subcode=subcode, element=_element)    
        if objs.count() > 0:
            return objs[0]
        else:
            obj = AccountState()
            obj.parent = _account
            obj.target = _target
            obj.classifier1value = classifier1
            obj.classifier2value = classifier2
            obj.classifier3value = classifier3
            obj.period = period
            obj.subcode = subcode
            obj.element = _element
            obj.aggregate=aggregate
            obj.debit = 0
            obj.credit = 0
            obj.save()
            return obj
        
    def update_account_state(self, debit, credit):
        s = self.account_state
        account = s.parent
        for period in [s.period, '*']:        
            for target in [s.target, None]:
                for subcode in [s.subcode, "*"]:
                    state = self.get_account_state(account, s.element, period, target, subcode=subcode, aggregate=True)
                    state.debit += debit
                    state.credit += credit
                    state.save()
        account = account.parent
        subcode = "*"
        while account:
            for period in [s.period, '*']:        
                for target in [s.target, None]:
                    state = self.get_account_state(account, s.element, period, target, subcode=subcode, aggregate=True)
                    state.debit += debit
                    state.credit += credit
                    state.save()
            account = account.parent
            
    def confirm(self):
        ret = False
        with transaction.atomic():                
            self.refresh_from_db()
            if not self.enabled:
                self.enabled = True
                if self.sign > 0:
                    self.update_account_state(0, self.amount)
                else:
                    self.update_account_state(self.amount, 0)
                self.save()
                ret = True
        return ret
    
    def cancel_confirmation(self):
        ret = False
        with transaction.atomic():                
            self.refresh_from_db()
            if self.enabled:
                self.enabled = False
                if self.sign > 0:
                    self.update_account_state(0, -1 * self.amount)
                else:
                    self.update_account_state(-1 * self.amount, 0)
                self.save()
                ret = True
        return ret
    
admin.site.register(AccountOperation)


class BaseObject( models.Model):
    
    class Meta:
        verbose_name = _("Base object")
        verbose_name_plural = _("Base objects")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        abstract = True
        
        
        
    

    app = models.CharField('Application', null=False, blank=False, editable=True, max_length=16)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    declaration = models.TextField('Declaration', null=True, blank=True, editable=False, )
    template_src = models.TextField('Template source', null=True, blank=True, editable=False, )
    template = models.TextField('Template', null=True, blank=True, editable=False, )
    to_html_rec = models.TextField('Convert fields to html', null=True, blank=True, editable=False, )
    save_fun = models.TextField('Save function', null=True, blank=True, editable=False, )
    load_fun = models.TextField('Load function', null=True, blank=True, editable=False, )
    to_str_fun = models.TextField('Object to str function', null=True, blank=True, editable=False, )
    action_template = models.TextField('Action template', null=True, blank=True, editable=False, )
    

    def to_str(self, obj):
        if self.to_str_fun:
            tmp = "def _to_str(self):\n" + "\n".join([ "    " + pos for pos in self.to_str_fun.split('\n')])
            exec(tmp)
            return locals()['_to_str'](obj)
        else:
            if obj.title:
                return obj.title + " ["+self.name+"]"
            else:
                return str(obj) + " ["+self.name+"]"
    
    def get_action_template(self):
        if self.action_template:
            return ihtml_to_html(None, self.action_template)
        else:
            return None
    





