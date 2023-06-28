import django
from django.db import models
from django.utils import timezone

from pytigon_lib.schdjangoext.fields import *
from pytigon_lib.schdjangoext.models import *
import pytigon_lib.schdjangoext.fields as ext_models
from pytigon_lib.schtools import schjson

from django.utils.translation import gettext_lazy as _
from django.contrib import admin

import os, os.path
import sys
from pytigon_lib.schhtml.htmltools import superstrip


from pytigon_lib.schtools.tools import get_request


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
        default_permissions = ("add", "change", "delete", "list")
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
            code = workflow_type_obj.script_for_new_item
            if workflow_type_obj.script_for_new_item:
                exec(workflow_type_obj.script_for_new_item)
                if "new_workflow_item" in locals():
                    return locals()["new_workflow_item"](workflow_type_obj, data)

    @staticmethod
    def refresh_workflow_queue(workflow_type_name):
        workflow_type_obj = WorkflowType.objects.filter(name=workflow_type_name).first()
        if workflow_type_obj:
            code = workflow_type_obj.script_for_refresh_queue
            if workflow_type_obj.script_for_refresh_queue:
                exec(workflow_type_obj.script_for_refresh_queue)
                if "refresh_workflow_queue" in locals():
                    return locals()["refresh_workflow_queue"](workflow_type_obj)

    @staticmethod
    def handle_workflow_event(workflow_type_name, event):
        workflow_type_obj = WorkflowType.objects.filter(name=workflow_type_name).first()
        if workflow_type_obj:
            code = workflow_type_obj.script_for_handle_event
            if workflow_type_obj.script_for_handle_event:
                exec(workflow_type_obj.script_for_handle_event)
                if "handle_workflow_event" in locals():
                    return locals()["handle_workflow_event"](workflow_type_obj, event)

    @staticmethod
    def accept_workflow_item(workflow_item):
        workflow_type_obj = workflow_item.workflow_type
        if workflow_type_obj:
            code = workflow_type_obj.script_for_accept_item
            if workflow_type_obj.script_for_accept_item:
                exec(workflow_type_obj.script_for_accept_item)
                if "accept_workflow_item" in locals():
                    return locals()["accept_workflow_item"](
                        workflow_type_obj, workflow_item
                    )

    @staticmethod
    def reject_workflow_item(workflow_item):
        workflow_type_obj = workflow_item.workflow_type
        if workflow_type_obj:
            code = workflow_type_obj.script_for_reject_item
            if workflow_type_obj.script_for_reject_item:
                exec(workflow_type_obj.script_for_reject_item)
                if "reject_workflow_item" in locals():
                    return locals()["reject_workflow_item"](
                        workflow_type_obj, workflow_item
                    )


admin.site.register(WorkflowType)


class WorkflowItem(JSONModel):
    class Meta:
        verbose_name = _("Workflow item")
        verbose_name_plural = _("Workflow items")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schworkflow"

        ordering = ["id"]

        permissions = [
            ("admin_workflowitem", "Can administer workflow items"),
        ]

    parent_id = models.IntegerField(
        "Parent id",
        null=False,
        blank=False,
        editable=False,
        db_index=True,
    )
    workflow_type = ext_models.PtigForeignKey(
        WorkflowType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Workflow type",
        db_index=True,
    )
    application = models.CharField(
        "Application",
        null=False,
        blank=False,
        editable=False,
        db_index=True,
        max_length=64,
    )
    table = models.CharField(
        "Table",
        null=False,
        blank=False,
        editable=False,
        default="default",
        db_index=True,
        max_length=64,
    )
    group = models.CharField(
        "Group",
        null=True,
        blank=True,
        editable=False,
        default="default",
        db_index=True,
        max_length=64,
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
