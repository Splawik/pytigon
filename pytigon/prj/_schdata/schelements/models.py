
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



from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from django.template.loader import select_template
import datetime
from django.db import transaction


def limit_element1():
    return {}
    
def limit_element2():
    return {}
    
def limit_element3():
    return {}
    
def limit_element4():
    return {}
    
    
LIMIT_ELEMENT1 = OverwritableCallable(limit_element1)
LIMIT_ELEMENT2 = OverwritableCallable(limit_element2)
LIMIT_ELEMENT3 = OverwritableCallable(limit_element3)
LIMIT_ELEMENT4 = OverwritableCallable(limit_element4)




simple_element_type_choice = [
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
    
    ]

target_type_choice = [
    ("F","Firm"),
    ("P","Person"),
    ("E","Employee"),
    ("S","Section"),
    
    ]

account_type_choice_2 = [
    ("B","Balance"),
    ("O","Off-balance"),
    ("N","Non-financial"),
    
    ]

account_type_choice_1 = [
    ("S","Synthetic"),
    ("A","Analytical"),
    
    ]

element_type_choice = [
    ("O-GRP","Owner/Group"),
    ("O-COM","Owner/Company"),
    ("O-DIV","Owner/Division"),
    ("O-DEP","Owner/Department"),
    ("O-POS","Owner/Position"),
    ("O-EMP","Owner/Employee"),
    ("O-LOC","Owner/Location"),
    ("O-PER","Owner/Person"),
    ("O-DEV","Owner/Device"),
    ("O-OTH","Owner/Other"),
    ("I-GRP","Item/Group"),
    ("O-ALI","Owner/Alias"),
    ("I-SRV","Item/Service"),
    ("I-INT","Item/Intellectual value"),
    ("I-CUR","Item/Currency"),
    ("I-MAT","Item/Material"),
    ("I-RAW","Item/Raw material"),
    ("I-PRD","Item/Product"),
    ("I-IPR","Item/Intermediate product"),
    ("I-MER","Item/Merchandise"),
    ("I-DEV","Item/Device"),
    ("I-PMA","Item/Production machine"),
    ("I-VEH","Item/Vehicle"),
    ("I-OTH","Item/Other"),
    ("I-ALI","Item/Alias"),
    ("C-SYS","Config/System"),
    ("C-UNT","Config/Unit of measure"),
    ("C-DIC","Config/Dictionary"),
    ("C-OTH","Config/Other"),
    ("C-ALI","Config/Alias"),
    
    ]

accdoc_type_choices = [
    ("A","Account"),
    
    ]

accdoc_status_choices = [
    ("0","Edit"),
    ("1","Approved"),
    ("2","Settled"),
    ("3","Posted 1"),
    ("4","Posted 2"),
    ("5","Frozen"),
    ("9","Canceled"),
    
    ]

doctype_status = [
    ("0","Disabled"),
    ("1","Activ"),
    
    ]




class Element(TreeModel):
    
    class Meta:
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    
    parent = ext_models.PtigTreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    

    parent = ext_models.PtigTreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Parent', )
    type = models.CharField('Element type', null=False, blank=False, editable=True, choices=element_type_choice,max_length=8)
    grand_parent1 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 1', related_name='grandparent1', limit_choices_to=limit_element1)
    grand_parent2 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 2', related_name='grandparent2', limit_choices_to=limit_element2)
    grand_parent3 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 3', related_name='grandparent3', limit_choices_to=limit_element3)
    grand_parent4 = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Grand parent 4', related_name='grandparent4', limit_choices_to=limit_element4)
    code = models.CharField('Code', null=True, blank=True, editable=True, max_length=16)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    key =  models.ForeignKey('auth.Group', on_delete=models.CASCADE, null=True, blank=True,)
    key_path = models.CharField('Key path', null=True, blank=True, editable=False, max_length=256)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=64)
    

    def init_new(self, request, view, param=None):
        defaults = { 'type': param }
        return defaults
    
    
    def save(self, *argi, **argv):
        if self.key:
            key_path = self.key.name
        else:
            key_path = ""
        tab = self.parents()
        for pos in tab:
            if pos.key:
                if key_path:
                    key_path = pos.key.name + '/' + key_path
                else:
                    key_path = pos.key.name
        
        self.key_path = key_path
        
        super().save(*argi, **argv)
    
    def get_name(self):
        return self.name
    
    def _get_parent_elem(element_type):
        tab = self.parents()
        for pos in tab:
            if pos.type==element_type:
                return pos
        return None
        
    
    def company(self):
        return self._get_parent_elem('O-COM')
    
    def division(self):
        return self._get_parent_elem('O-DIV')
    
    def departament(self):
        return self._get_parent_elem('O-DEP')
    
    def position(self):
        return self._get_parent_elem('O-POS')
    
    def location(self):
        return self._get_parent_elem('O-LOC')
    
    def owner_group(self):
        return self._get_parent_elem('O-GRP')
    
    def owner_grand_group(self):
        grp =  self._get_parent_elem('O-GRP')
        if grp:
            return grp._get_parent_elem('O-GRP')
        else:
            return None
    
    def item_group(self):
        return self._get_parent_elem('I-GRP')
    
    def item_grand_group(self):
        grp =  self._get_parent_elem('I-GRP')
        if grp:
            return grp._get_parent_elem('I-GRP')
        else:
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
        return "/schsys/treedialog/schelements/Element/%s/" % id
        
    def redirect_href(self, view, request):
        t = None
        if type(self)==Element:
            if 'add_param' in view.kwargs:
                t = view.kwargs['add_param']
            else:
                t = self.type
        if t:
            if hasattr(self, "get_structure"):
                s = self.get_structure()
                if t in s:
                    redirect = s[t]['app'] + "/table/" + s[t]['table']
                    return request.path.replace('schelements/table/Element',redirect)
        return None
    
    @staticmethod
    def _get_new_buttons(elem_type="ROOT"):
        buttons = []
        
        if hasattr(Element, "get_structure"):
            s = Element.get_structure()
            if elem_type in s:
                if 'next' in s[elem_type]:
                    for item in s[elem_type]['next']:
                        if item in s:
                            button = {}
                            button['type'] = item
                            if 'title' in s[item]:
                                button['title'] = s[item]['title']
                            else:
                                button['title'] = item
                            if 'app' in s[item]:
                                button['app'] = s[item]['app']
                            else:
                                button['app'] = ""
                            if 'table' in s[item]:
                                button['table'] = s[item]['table']
                            else:
                                button['table'] = ""
    
                            buttons.append(button)
        return buttons
        
    @staticmethod
    def get_root_new_buttons():
        return Element._get_new_buttons("ROOT")
    
    def get_new_buttons(self):
        if self.type in ('O-GRP', 'I-GRP'):
            obj = self
            while obj and obj.type in ('O-GRP', 'I-GRP'):
                obj = obj.parent
            if obj:
                buttons = self._get_new_buttons(obj.type)
            else:
                buttons = self._get_new_buttons("ROOT")
            if self.description and '(' in self.description and ')' in self.description:
                ret = []
                for button in buttons:
                    if button['type'] in self.description:
                        ret.append(button)
                return ret
            else:
                return buttons
            
        else:
            return self._get_new_buttons(self.type)
    
admin.site.register(Element)


class Classifier(TreeModel):
    
    class Meta:
        verbose_name = _("Classifier")
        verbose_name_plural = _("Classifier")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    
    parent = ext_models.PtigTreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    

    parent = ext_models.PtigTreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Parent', )
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
        
        
    

    parent = ext_models.PtigHiddenForeignKey(DocReg, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=16)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    correction = models.NullBooleanField('Correction', null=True, blank=True, editable=True, )
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
    doc_type_parent = ext_models.PtigHiddenForeignKey(DocType, on_delete=models.CASCADE, null=False, blank=False, editable=False, verbose_name='Document type parent', )
    parent_element = ext_models.PtigHiddenForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True, editable=False, verbose_name='Parent element', )
    number = models.CharField('Document number', null=True, blank=True, editable=True, max_length=32)
    date_c = models.DateTimeField('Creation date', null=False, blank=False, editable=False, default=datetime.datetime.now,)
    date = models.DateField('Date', null=True, blank=True, editable=True, )
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=128)
    comments = models.CharField('Comments', null=True, blank=True, editable=True, max_length=256)
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
    def template_for_list(model, context, view, doc_type):
        if doc_type in ('html', 'json') and 'filter' in context:
            tmp = DocReg.objects.filter(name=context['filter'].replace('_','/'))
            if len(tmp)==1:
                names = []
                names.append(view.template_name)
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
        
    def redirect_href(self, view, request):
        t = None
        if type(self)==DocHead:
            if 'add_param' in view.kwargs and view.kwargs['add_param'] != '-':
                t = view.kwargs['add_param']
                if t:
                    object_list = DocType.objects.filter(name=t)
                    if len(object_list):
                        t = object_list[0].parent.name
            else:
                t = self.doc_type_parent.parent.name
        if t:
            if hasattr(self, "get_structure"):
                s = self.get_structure()
                if t in s:
                    redirect = s[t]['app'] + "/table/" + s[t]['table']
                    return request.path.replace('schelements/table/DocHead',redirect)
        return None
    
    
admin.site.register(DocHead)


class DocItem(JSONModel):
    
    class Meta:
        verbose_name = _("Document item")
        verbose_name_plural = _("Document items")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.PtigHiddenForeignKey(DocHead, on_delete=models.CASCADE, null=False, blank=False, editable=False, verbose_name='Parent', )
    parent_item = ext_models.PtigHiddenForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=False, verbose_name='Parent item', )
    order = models.IntegerField('Order', null=False, blank=False, editable=False, default=1,)
    item = ext_models.PtigForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Item', )
    amount = models.DecimalField('Amount', null=True, blank=True, editable=True, max_digits=16, decimal_places=2)
    alt_amount = models.DecimalField('Amount', null=True, blank=True, editable=True, max_digits=16, decimal_places=2)
    alt_unit = models.CharField('Alternate unit', null=True, blank=True, editable=True, max_length=32)
    description = models.CharField('Description', null=True, blank=True, editable=True, max_length=255)
    level = models.IntegerField('Level', null=False, blank=False, editable=False, default=0,)
    active = models.BooleanField('Active item', null=False, blank=False, editable=True, default=True,)
    param1 = models.CharField('Parameter 1', null=True, blank=True, editable=False, max_length=16)
    param2 = models.CharField('Parameter 2', null=True, blank=True, editable=False, max_length=16)
    param3 = models.CharField('Parameter 3', null=True, blank=True, editable=False, max_length=16)
    

    @staticmethod
    def template_for_list(model, context, view, doc_type):
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
            except:
                dochead = context['view'].object.parent
    
            reg = dochead.doc_type_parent.parent            
            names = []
            names.append((reg.app+"/"+dochead.doc_type_parent.parent.name+"_docitem_edit.html").lower())
            names.append((reg.app+"/"+reg.name.replace('/', '_') + "_docitem_edit.html").lower())
            x = reg.get_parent()
            while x:
                names.append(x.app+"/"+x.name.replace('/', '_') + "_docitem_edit.html")
                x = x.get_parent()
            template = select_template(names)
            if template:
                return template                            
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
                return { 'parent': str(parent.id), 'order': max_nr, 'date_c': datetime.datetime.now(), 'level': 0 }
            
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
        
    
    
    def redirect_href(self, view, request):
        t = None
        if type(self)==DocItem:
            if 'add_param' in view.kwargs and view.kwargs['add_param']!='-':
                t = view.kwargs['add_param']
            else:
                t = self.parent.doc_type_parent.parent.name
        if t:
            if hasattr(self.parent, "get_structure"):
                s = self.parent.get_structure()
                if t in s:
                    old_path = request.path
                    redirect = s[t]['app'] + "/table/" + s[t]['child_table']
                    path = old_path.replace('schelements/table/DocItem',redirect)
                    if path == old_path:
                        if not '/'+s[t]['table']+'/' in old_path:
                            path = old_path.replace('/schelements/', '/'+s[t]['app']+'/')
                            path = path.replace('/DocHead/', '/'+s[t]['table']+'/')
                        else:
                            return None
                    return path
        return None
        
    
admin.site.register(DocItem)


class DocRegStatus( models.Model):
    
    class Meta:
        verbose_name = _("Document status")
        verbose_name_plural = _("Document status")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.PtigHiddenForeignKey(DocReg, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
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
        
        
    

    parent = ext_models.PtigHiddenForeignKey(DocHead, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
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
        
        
    
    parent = ext_models.PtigTreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    

    parent = ext_models.PtigTreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Parent', )
    type1 = models.CharField('Type 1', null=True, blank=True, editable=False, choices=account_type_choice_1,max_length=1)
    type2 = models.CharField('Type 2', null=True, blank=True, editable=True, choices=account_type_choice_2,max_length=1)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=32)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=256)
    root_classifier1 = ext_models.PtigForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Root classifier 1', related_name='baseaccount_rc1_set')
    root_classifier2 = ext_models.PtigForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Root classifier 2', related_name='baseaccount_rc2_set')
    root_classifier3 = ext_models.PtigForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Root classifier 3', related_name='baseaccount_rc3_set')
    enabled = models.NullBooleanField('Enabled', null=False, blank=False, editable=True, default=True,)
    

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
    target = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Target', related_name='state_targets')
    classifier1value = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Classifier 1 value', related_name='account_c1_set')
    classifier2value = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Classifier 2 value', related_name='account_c2_set')
    classifier3value = models.ForeignKey(Classifier, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Classifier 3 value', related_name='account_c3_set')
    period = models.CharField('Period', null=True, blank=True, editable=True, max_length=10)
    subcode = models.CharField('Subcode', null=True, blank=True, editable=True, max_length=16)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Element', )
    debit = models.DecimalField('Debit', null=False, blank=False, editable=True, max_digits=16, decimal_places=2)
    credit = models.DecimalField('Credit', null=False, blank=False, editable=True, max_digits=16, decimal_places=2)
    aggregate = models.NullBooleanField('Aggregate', null=False, blank=False, editable=True, default=False,)
    

    
admin.site.register(AccountState)


class AccountOperation( models.Model):
    
    class Meta:
        verbose_name = _("Account operation")
        verbose_name_plural = _("Account operations")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schelements'


        ordering = ['id']
        
        
    

    parent = ext_models.PtigHiddenForeignKey(DocItem, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Parent', )
    date = models.DateTimeField('Date', null=False, blank=False, editable=False, default=datetime.datetime.now,)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=255)
    payment = models.CharField('Name of payment', null=True, blank=True, editable=True, max_length=64)
    account_state = ext_models.PtigForeignKey(AccountState, on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Account state', related_name='accountoper_set', search_fields=['parent__name__icontains',])
    sign = models.IntegerField('Sign - debit or credit', null=False, blank=False, editable=True, )
    amount = models.DecimalField('Amount', null=False, blank=False, editable=True, max_digits=16, decimal_places=2)
    enabled = models.NullBooleanField('Enabled', null=True, blank=True, editable=False, default=False,)
    

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
            _target = Element.objects.filter(code=target)[0]
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
    






