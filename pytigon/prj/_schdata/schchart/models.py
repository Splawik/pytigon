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


from pytigon_lib.schtools.schjson import json_dumps, json_loads

# from schlib.schdjangoext.django_ihtml import ihtml_to_html
# from django.template import Context, Template
from django.db.models import Max, Min

from schelements.models import *


class Plot(models.Model):
    class Meta:
        verbose_name = _("Plot")
        verbose_name_plural = _("Polts")
        default_permissions = ("add", "change", "delete", "view", "list", "administer")
        app_label = "schchart"

        ordering = ["id"]

    name = models.CharField(
        "Name", null=False, blank=False, editable=True, max_length=64
    )
    group = models.CharField(
        "Group", null=False, blank=False, editable=True, max_length=64
    )
    get_config = models.TextField(
        "Get config",
        null=True,
        blank=True,
        editable=False,
    )
    get_data = models.TextField(
        "Get data",
        null=True,
        blank=True,
        editable=False,
    )
    get_layout = models.TextField(
        "Get layout",
        null=True,
        blank=True,
        editable=False,
    )
    on_event = models.TextField(
        "On event",
        null=True,
        blank=True,
        editable=False,
    )
    permission = models.CharField(
        "Permission", null=True, blank=True, editable=True, max_length=64
    )


admin.site.register(Plot)
