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

import schprofile.models


class Comment(AssociatedJSONModel):

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schcomments"

        ordering = ["id"]

        permissions = [
            ("admin_comment", "Can administer comments"),
        ]

    comment = models.TextField(
        "Comment",
        null=True,
        blank=True,
        editable=True,
    )
    sender = models.ForeignKey(
        schprofile.models.UserProxy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Sender",
        related_name="comment_sender_set",
    )
    recipient = models.ForeignKey(
        schprofile.models.UserProxy,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=True,
        verbose_name="Recipient",
        related_name="comment_recipient_set",
    )
    recipients = models.CharField(
        "Recipients", null=True, blank=True, editable=True, max_length=256
    )
    time = models.DateTimeField(
        "Time", null=True, blank=True, editable=False, auto_now_add=True
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

    def save_from_request(self, request, view_type, param):
        if not self.sender:
            self.sender = request.user
        super().save()


admin.site.register(Comment)
