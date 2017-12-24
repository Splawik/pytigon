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


from tools.models import *



from schlib.schtools.schjson import json_dumps, json_loads
#from schlib.schdjangoext.django_ihtml import ihtml_to_html
#from django.template import Context, Template
from django.db.models import Max, Min





class ReportDef( models.Model):
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
        
        
    

    app = models.CharField('Application', null=False, blank=False, editable=True, max_length=16)
    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    description = models.CharField('Description', null=False, blank=False, editable=True, max_length=64)
    declaration = models.TextField('Declaration', null=True, blank=True, editable=False, )
    template_src = models.TextField('Template source', null=True, blank=True, editable=False, )
    template = models.TextField('Template', null=True, blank=True, editable=False, )
    to_html_rec = models.TextField('Convert fields to html', null=True, blank=True, editable=False, )
    save_fun = models.TextField('Save function', null=True, blank=True, editable=False, )
    load_fun = models.TextField('Load function', null=True, blank=True, editable=False, )
    

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




