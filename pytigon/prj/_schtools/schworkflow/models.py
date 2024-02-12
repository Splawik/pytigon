import django
from django.db import models
from django.utils import timezone

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
import pytigon_lib.schdjangoext.fields as ext_models
from pytigon_lib.schtools import schjson

from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.utils import timezone

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


import datetime

from pytigon_lib.schtools.tools import get_request
from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct

NEW = """#Example: 
#import datetime
#
#def new_workflow_item(workflow_item, data):
#    pass

"""

REFRESH = """#Example: 
#import datetime
#
#def refresh_workflow_queue(workflow_type_obj):
#    pass

"""

HANDLE = """#Example: 
#import datetime
#
#def handle_workflow_event(workflow_type_obj, event):
#    pass

"""

ACCEPT = """#Example: 
#import datetime
#
#def accept_workflow_item(workflow_item):
#    pass

"""

REJECT = """#Example: 
#import datetime
#
#def reject_workflow_item(workflow_item):
#    pass

"""


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
    ("0", "active"),
    ("1", "accepted"),
    ("2", "rejected"),
    ("8", "next"),
    ("9", "cancelled"),
]


class WorkflowType(models.Model):

    class Meta:
        verbose_name = _("Workflow type")
        verbose_name_plural = _("Workflow types")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schworkflow"

        ordering = ["id"]

        permissions = [
            ("admin_workflowtype", "Can administer workflow types"),
        ]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    script_for_new_item = models.TextField(
        "Script for new workflow item",
        null=True,
        blank=True,
        editable=False,
    )
    script_for_accept_item = models.TextField(
        "Script for accept workflow item",
        null=True,
        blank=True,
        editable=False,
    )
    script_for_reject_item = models.TextField(
        "Script for reject workflow item",
        null=True,
        blank=True,
        editable=False,
    )
    script_for_refresh_queue = models.TextField(
        "Script for refresh workflow queue",
        null=True,
        blank=True,
        editable=False,
    )
    script_for_handle_event = models.TextField(
        "Script for handle event",
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.name

    @staticmethod
    def new_workflow_item(workflow_type_name, data):
        workflow_type_obj = WorkflowType.objects.filter(name=workflow_type_name).first()
        if workflow_type_obj:
            workflow_item = WorkflowItem()
            workflow_item.workflow_type = workflow_type_obj
            workflow_item.level = 0
            workflow_item.creation_date = timezone.now()
            return run_code_from_db_field(
                f"workflowtype__new_workflow_item_{workflow_type_obj.name}.py",
                workflow_type_obj,
                "script_for_new_item",
                "new_workflow_item",
                workflow_item=workflow_item,
                data=data,
            )

    @staticmethod
    def refresh_workflow_queue(workflow_type_name):
        workflow_type_obj = WorkflowType.objects.filter(name=workflow_type_name).first()
        if workflow_type_obj:
            return run_code_from_db_field(
                f"workflowtype__refresh_workflow_queue_{workflow_type_obj.name}.py",
                workflow_type_obj,
                "script_for_refresh_queue",
                "refresh_workflow_queue",
                workflow_type_obj=workflow_type_obj,
            )
        return None

    @staticmethod
    def handle_workflow_event(workflow_type_name, event):
        workflow_type_obj = WorkflowType.objects.filter(name=workflow_type_name).first()
        if workflow_type_obj:
            return run_code_from_db_field(
                f"workflowtype__handle_workflow_event_{workflow_type_obj.name}.py",
                workflow_type_obj,
                "script_for_handle_event",
                "handle_workflow_event",
                workflow_type_obj=workflow_type_obj,
                event=event,
            )
        return None

    @staticmethod
    def accept_workflow_item(workflow_item):
        workflow_type_obj = workflow_item.workflow_type
        if workflow_type_obj:
            return run_code_from_db_field(
                f"workflowtype__accept_workflow_item_{workflow_type_obj.name}.py",
                workflow_type_obj,
                "script_for_accept_item",
                "accept_workflow_item",
                workflow_item=workflow_item,
            )
        return None

    @staticmethod
    def reject_workflow_item(workflow_item):
        workflow_type_obj = workflow_item.workflow_type
        if workflow_type_obj:
            return run_code_from_db_field(
                f"workflowtype__reject_workflow_item_{workflow_type_obj.name}.py",
                workflow_type_obj,
                "script_for_reject_item",
                "reject_workflow_item",
                workflow_item=workflow_item,
            )
        return None

    def get_script_for_new_item_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return NEW

    def get_script_for_refresh_queue_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return REFRESH

    def get_script_for_handle_event_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return HANDLE

    def get_script_for_accept_item_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return ACCEPT

    def get_script_for_reject_item_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return REJECT


admin.site.register(WorkflowType)


class WorkflowItem(AssociatedJSONModel):

    class Meta:
        verbose_name = _("Workflow item")
        verbose_name_plural = _("Workflow items")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schworkflow"

        ordering = ["id"]

        permissions = [
            ("admin_workflowitem", "Can administer workflow items"),
        ]

    workflow_type = ext_models.PtigForeignKey(
        WorkflowType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Workflow type",
        db_index=True,
    )
    level = models.IntegerField(
        "Level",
        null=True,
        blank=True,
        editable=True,
        default=0,
    )
    user_email = models.EmailField(
        "User s email",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
    )
    creation_date = models.DateTimeField(
        "Creation date", null=False, blank=False, editable=True, auto_now=True
    )
    acceptance_date = models.DateTimeField(
        "Acceptance date",
        null=True,
        blank=True,
        editable=True,
    )
    title = models.CharField(
        "Title", null=True, blank=True, editable=True, db_index=True, max_length=128
    )
    item_type = models.CharField(
        "Item type", null=True, blank=True, editable=True, max_length=16
    )
    status = models.CharField(
        "Status",
        null=True,
        blank=True,
        editable=True,
        default="0",
        choices=workflow_item_status_choices,
        max_length=1,
    )

    @classmethod
    def filter(cls, value, view=None, request=None):
        if value:
            app, tbl, id, grp = value.split("__")
            if grp and grp.startswith("-"):

                def get_user_email():
                    r = get_request()
                    if r:
                        if r.user:
                            if r.user.email:
                                return r.user.email
                    return ""

                objects = cls.objects
                if grp[1:] == "current_user":
                    email = get_user_email()
                    objects = objects.filter(user_email__iexact=email)
                elif grp[1:] == "current_user_and_active":
                    email = get_user_email()
                    objects = objects.filter(user_email__iexact=email, status="0")
                elif grp[1:] == "current_user_active_and_next":
                    email = get_user_email()
                    objects = objects.filter(
                        user_email__iexact=email, status_in=("0", "8")
                    )
                elif grp[1:] == "active":
                    objects = objects.filter(status="0")
                elif grp[1:] == "active_and_next":
                    objects = objects.filter(status_in=("0", "8"))
                return objects
            else:
                return cls.objects.filter(
                    application=app, table=tbl, parent_id=id, group=grp
                )
        else:
            return cls.objects.all()

    def init_new(self, request, view, value=None):
        if value:
            app, tbl, id, grp = value.split("__")
            return {"application": app, "table": tbl, "parent_id": id, "group": grp}
        else:
            return {
                "application": "default",
                "table": "default",
                "parent_id": 0,
                "group": "default",
            }

    def accept_workflow_item(self):
        return WorkflowType.accept_workflow_item(self)

    def reject_workflow_item(self):
        return WorkflowType.reject_workflow_item(self)


admin.site.register(WorkflowItem)
