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


from datetime import datetime
from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct

NEW = """#Example: 
#import datetime
#
#def new_action_item(action, data):
#    pass

"""

CLOSE = """#Example: 
#import datetime
#
#def close_action(ction):
#    pass

"""

EMAIL = """#Example: 
#import datetime
#
#def email_text(action, email_type):
#    pass

"""


class ActionType(models.Model):

    class Meta:
        verbose_name = _("Action type")
        verbose_name_plural = _("Action types")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schactions"

        ordering = ["id"]

        permissions = [
            ("admin_actiontype", "Can administer action types"),
        ]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, db_index=True, max_length=64
    )
    script_for_new_item = models.TextField(
        "Script for new task",
        null=True,
        blank=True,
        editable=False,
    )
    script_for_close_item = models.TextField(
        "Script for close action",
        null=True,
        blank=True,
        editable=False,
    )
    script_for_email_text = models.TextField(
        "Script for get email text",
        null=True,
        blank=True,
        editable=False,
    )

    @staticmethod
    def new_action(action_type_name, data=None):
        action_type_obj = ActionType.objects.filter(name=action_type_name).first()
        if action_type_obj:
            action = Action()
            action.action_type = action_type_obj
            action.start_date = timezone.now()
            action.group = "default"
            return run_code_from_db_field(
                f"actiontype__new_action_item_{action_type_obj.name}.py",
                action_type_obj,
                "script_for_new_item",
                "new_action_item",
                action=action,
                data=data,
            )

    @staticmethod
    def close_action(action):
        action_type_obj = action.parent
        return run_code_from_db_field(
            f"actiontype__close_action_{action_type_obj.name}.py",
            action_type_obj,
            "script_for_close_item",
            "close_action",
            action=action,
        )

    @staticmethod
    def email_text(action, email_type):
        action_type_obj = action.parent
        return run_code_from_db_field(
            f"actiontype__email_text_{action_type_obj.name}.py",
            action_type_obj,
            "script_for_email_text",
            "email_text",
            action=action,
            email_type=email_type,
        )

    def get_script_for_new_item_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return NEW

    def get_script_for_close_item_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return CLOSE

    def get_script_for_email_text_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return EMAIL


admin.site.register(ActionType)


class Action(AssociatedJSONModel):

    class Meta:
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schactions"

        ordering = ["id"]

        permissions = [
            ("admin_action", "Can administer actions"),
        ]

    action_type = ext_models.PtigForeignKey(
        ActionType,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=True,
        verbose_name="Action type",
    )
    parent_action = ext_models.PtigForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Parent action",
    )
    description = models.CharField(
        "Description", null=False, blank=False, editable=True, max_length=256
    )
    start_date = models.DateTimeField(
        "Start date", null=False, blank=False, editable=True, auto_now_add=True
    )
    deadline = models.DateTimeField(
        "Deadline",
        null=True,
        blank=True,
        editable=True,
    )
    email_action_owner = models.EmailField(
        "Email address of the action owner",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
    )
    email_action_done = models.EmailField(
        "Email - action done",
        null=True,
        blank=True,
        editable=True,
    )
    email_deadline_exceeded = models.EmailField(
        "Email - deadline exceeded",
        null=True,
        blank=True,
        editable=True,
    )
    info = models.TextField(
        "Info",
        null=True,
        blank=True,
        editable=False,
    )
    has_attachment = models.BooleanField(
        "Has an attachment",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )
    has_workflow = models.BooleanField(
        "Has a workflow",
        null=True,
        blank=True,
        editable=True,
        default=False,
    )
    status = models.CharField(
        "None", null=True, blank=True, editable=True, db_index=True, max_length=16
    )

    @classmethod
    def filter(cls, value, view=None, request=None):
        if value:
            app, tbl, id, grp = value.split("__")
            return cls.objects.filter(
                application=app, table=tbl, parent_id=id, group=grp
            )
        else:
            return cls.objects.all()

    def close_action(self):
        return ActionType.close_action(self)

    def email_text(self, email_type):
        return ActionType.email_text(self, email_type)


admin.site.register(Action)
