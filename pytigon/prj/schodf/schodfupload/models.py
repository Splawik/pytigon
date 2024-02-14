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


class Rights(models.Model):

    class Meta:
        verbose_name = _("Rights")
        verbose_name_plural = _("Rights")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schodfupload"

        ordering = ["id"]

    title = models.CharField(
        "Title", null=True, blank=True, editable=True, max_length=64
    )


admin.site.register(Rights)
