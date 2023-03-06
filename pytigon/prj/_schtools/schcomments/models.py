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


from schelements.models import *


from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(JSONModel):
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schcomments"

        ordering = ["id"]

    application = models.CharField(
        "Application",
        null=True,
        blank=True,
        editable=False,
        db_index=True,
        max_length=64,
    )
    table = models.CharField(
        "Table", null=True, blank=True, editable=False, db_index=True, max_length=64
    )
    group = models.CharField(
        "Group", null=True, blank=True, editable=False, db_index=True, max_length=64
    )
    parent_id = models.IntegerField(
        "Parent id",
        null=True,
        blank=True,
        editable=True,
        db_index=True,
    )
    comment = models.TextField(
        "Comment",
        null=True,
        blank=True,
        editable=True,
    )
    sender = models.ForeignKey(
        UserProxy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Sender",
    )
    recipient = models.ForeignKey(
        UserProxy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Recipient",
    )
    recipients = models.CharField(
        "Recipients", null=True, blank=True, editable=True, max_length=256
    )
    time = models.DateTimeField(
        "Time", null=True, blank=True, editable=True, auto_now_add=True
    )

    @classmethod
    def filter(cls, value):
        if value:
            app, tbl, id, grp = value.split("__")
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


admin.site.register(Comment)


class UserProxy(User):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schcomments"

        ordering = ["id"]

        proxy = True


admin.site.register(UserProxy)
