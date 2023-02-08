
import django
from django.db import models

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
import pytigon_lib.schdjangoext.fields as ext_models
from pytigon_lib.schtools import schjson

from django.utils.translation import gettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip




def new_workflow_item(type_name, params):
    pass
    
def accept(pk):
    pass
    
def reject(pk):
    pass

def refresh(type_name):
    pass
    
def handle_event(event):
    pass





workflow_item_status_choices = [
    ("0","active"),
    ("1","accepted"),
    ("2","rejected"),
    ("9","in line"),
    
    ]




class WorkflowType( models.Model):
    
    class Meta:
        verbose_name = _("Workflow type")
        verbose_name_plural = _("Workflow types")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schworkflow'


        ordering = ['id']
        
        
    

    name = models.CharField('Name', null=False, blank=False, editable=True, max_length=64)
    script_for_new_item = models.TextField('Script for new workflow item', null=True, blank=True, editable=False, )
    script_for_accept_item = models.TextField('Script for accept workflow item', null=True, blank=True, editable=False, )
    script_for_reject_item = models.TextField('Script for reject workflow item', null=True, blank=True, editable=False, )
    script_for_refresh_queue = models.TextField('Script for refresh workflow queue', null=True, blank=True, editable=False, )
    script_for_handle_event = models.TextField('Script for handle event', null=True, blank=True, editable=False, )
    

    
admin.site.register(WorkflowType)


class WorkflowItem(JSONModel):
    
    class Meta:
        verbose_name = _("Workflow item")
        verbose_name_plural = _("Workflow items")
        default_permissions = ('add', 'change', 'delete', 'list')
        app_label = 'schworkflow'


        ordering = ['id']
        
        
    

    parent_id = models.IntegerField('Parent id', null=False, blank=False, editable=False, db_index=True,)
    workflow_type = ext_models.PtigForeignKey(WorkflowType, on_delete=models.CASCADE, null=False, blank=False, editable=True, verbose_name='Workflow type', )
    application = models.CharField('Application', null=False, blank=False, editable=False, db_index=True,max_length=64)
    table = models.CharField('Table', null=False, blank=False, editable=False, default="default",db_index=True,max_length=64)
    group = models.CharField('Group', null=True, blank=True, editable=False, default="default",db_index=True,max_length=64)
    creation_date = models.DateTimeField('Creation date', null=False, blank=False, editable=True, auto_now=True)
    acceptance_date = models.DateTimeField('Acceptance date', null=True, blank=True, editable=True, )
    user_email = models.EmailField('User's email', null=True, blank=True, editable=True, db_index=True,)
    title = models.CharField('Title', null=True, blank=True, editable=False, db_index=True,max_length=128)
    item_type = models.CharField('Item type', null=True, blank=True, editable=True, max_length=16)
    status = models.CharField('Status', null=True, blank=True, editable=True, choices=workflow_item_status_choices,max_length=1)
    

    
admin.site.register(WorkflowItem)





