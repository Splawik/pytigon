# -*- coding: utf-8 -*-

import django
from django.db import models

from schlib.schdjangoext.fields import *
from schlib.schdjangoext.models import *

import schlib.schdjangoext.fields as ext_models

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from schlib.schhtml.htmltools import superstrip


from schtools.models import *



from schlib.schtools.schjson import json_dumps, json_loads
#from schlib.schdjangoext.django_ihtml import ihtml_to_html
#from django.template import Context, Template
from django.db.models import Max, Min

from schelements.models import *




class ReportDef(BaseObject):
    """
    Declaration:
        return Form()
    
    Template: django template
    
    child(name):
        child_header(name)
        child_table(name)
        
        <html></html>
    
    
    
    to_html:
        convert form data to html
        
    """
    class Meta:
        verbose_name = _("Report definition")
        verbose_name_plural = _("Reports definitions")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schreports'


        ordering = ['id']
        
        
    

    

    def getsubrep(self, name):
        return ReportDef.objects.get(name = self.name + "/" + name)
        
    
admin.site.register(ReportDef)


class Report(JSONModel):
    
    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schreports'


        ordering = ['id']
        
        ordering = ['parent_id', 'order', 'id']
        
        
        
    

    parent = ext_models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=False, verbose_name='Parent', )
    order = models.IntegerField('Order number', null=True, blank=True, editable=True, )
    report_def_name = models.CharField('Report definition name', null=False, blank=False, editable=True, max_length=64)
    date = models.DateTimeField('Date', null=True, blank=True, editable=True, )
    

    def template_for_object(self, context, doc_type):
        if doc_type=='pdf':
            x = ReportDef.objects.filter(name=self.report_def_name)
            if x.count()>0:
                return "%s/report_%s_pdf.html" % (x[0].app, self.report_def_name)
        return None
    
    @staticmethod    
    def get_rep_types():
        repdef_list = ReportDef.objects.exclude(name__contains='/')
        return [pos.name for pos in repdef_list]
    
    
    @staticmethod    
    def get_rep_by_nagid(nagid):
        r = Report.objects.filter(order=nagid)
        if r.count()>0:
            return r[0]
        else:
            return None
    
    @staticmethod    
    def filter(f):
        if f == 'main_reports':
            return Report.objects.filter(parent=None)
        else:
            return Report.objects.all()
    
    def getsubreps(self, name):
        return Report.objects.filter(parent=self).filter(report_def_name__endswith=name)
            
    def to_html(self):
        rep_def = ReportDef.objects.get(name = self.report_def_name)
        return rep_def.to_html(self)
    
    #def  __getattr__(self, name):    
    #    if name.startswith('json_'):
    #        if not hasattr(self, '_data'):
    #            self._data = json_loads(self.data)
    #        if name[5:] in self._data:
    #            return self._data[name[5:]]
    #        else:
    #            return None
    #    else:
    #        return super().__getattr__(name)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.parent:
                m = Report.objects.filter(parent=self.parent).aggregate(Max('order'))['order__max']
                if m:
                    self.order = m + 1
                else:
                    self.order = 1        
        super().save(*args, **kwargs)
    
    
    
    
admin.site.register(Report)


class CommonGroupDef(BaseObject):
    
    class Meta:
        verbose_name = _("Common group definition")
        verbose_name_plural = _("Common groups definition")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schreports'


        ordering = ['id']
        
        
    

    on_new_elem_event = models.TextField('On new elemetn event', null=True, blank=True, editable=False, )
    allowed_new_fields = models.TextField('Allowed new fields', null=True, blank=True, editable=False, )
    

    
admin.site.register(CommonGroupDef)


class CommonGroup(JSONModel):
    
    class Meta:
        verbose_name = _("Common group")
        verbose_name_plural = _("Common groups")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schreports'


        ordering = ['id']
        
        
    

    parent = ext_models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, editable=True, verbose_name='Parent', )
    title = models.CharField('Title', null=True, blank=True, editable=True, max_length=64)
    group_def_name = models.CharField('Group definition name', null=False, blank=False, editable=True, max_length=64)
    tag_name = models.CharField('Tag name', null=True, blank=True, editable=True, max_length=64)
    

    
admin.site.register(CommonGroup)


class Plot( models.Model):
    
    class Meta:
        verbose_name = _("Plot")
        verbose_name_plural = _("Polts")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schreports'


        ordering = ['id']
        
        
    

    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    group = models.CharField('Group', null=False, blank=False, editable=True, max_length=64)
    get_data = models.TextField('Get data', null=True, blank=True, editable=False, )
    get_layout = models.TextField('Get layout', null=True, blank=True, editable=False, )
    on_event = models.TextField('On event', null=True, blank=True, editable=False, )
    permission = models.CharField('Permission', null=True, blank=True, editable=True, max_length=64)
    

    
admin.site.register(Plot)




