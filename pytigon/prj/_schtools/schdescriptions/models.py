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


class Description(AssociatedModel):

    class Meta:
        verbose_name = _("Description")
        verbose_name_plural = _("Descriptions")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schdescriptions"

        ordering = ["id"]

        permissions = [
            ("admin_comment", "Can administer comments"),
        ]

    lang = models.CharField(
        "Language code", null=False, blank=False, editable=True, max_length=8
    )
    description = models.CharField(
        "Description", null=True, blank=True, editable=True, max_length=256
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


admin.site.register(Description)
