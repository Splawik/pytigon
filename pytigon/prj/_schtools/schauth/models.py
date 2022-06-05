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


class UrlWithAuth(models.Model):
    class Meta:
        verbose_name = _("Url with authorization")
        verbose_name_plural = _("Urls with authorization")
        default_permissions = ("add", "change", "delete", "list")
        app_label = "schauth"

        ordering = ["id"]

    username = models.CharField(
        "User name", null=False, blank=False, editable=True, max_length=64
    )
    key = models.CharField(
        "Key",
        null=False,
        blank=False,
        editable=True,
        unique=True,
        db_index=True,
        max_length=255,
    )
    redirect_to = models.CharField(
        "Redirect to", null=True, blank=True, editable=True, max_length=255
    )
    post_data = models.TextField(
        "Post data",
        null=True,
        blank=True,
        editable=False,
    )


admin.site.register(UrlWithAuth)
