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

GET_CONFIG = """
def get_config(obj, request_param):
    config = {
        'displaylogo': True, 
    }
    return config
"""

GET_DATA = """
def get_data(obj, request_param):
    prj = apps.get_model("schbi", "project").objects.get(name="test_bi_prj")
    tbl_year = prj.get_data()["year_sample"]

    yy = request_param["param"].split("-")

    x = "select year as x, y1 as y from tbl_year"
    x += " where" if yy[0] or yy[1] else ""
    x += (" year >= " + yy[0]) if yy[0] else ""
    if yy[1]:
        if yy[0]:
            x += " and"
        x += " year <= " + yy[1]

    data = duckdb.execute(x).fetchnumpy()
    data['type'] = 'bar'

    return {
        'data': [data,],
        'events': ['click', 'hover=>plotly/plotly-status/',]
    }
"""

GET_LAYOUT = """
def get_layout(obj, request_param):
    layout = {
      "title": {
        "text": 'title'
      },
      "font": {"size": 18}
    };
    return layout
"""

ON_EVENT = """
def on_event(obj, data, request_param):
    ret = {
        'function': 'react',
        'data': [
            {
            'x': ['giraffes', 'monkeys'],
            'y': [20, 23],
            'type': 'bar',
            }
        ],
    }
    return ret
"""


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

    def get_get_config_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return GET_CONFIG

    def get_get_data_if_empty(self, request, template_name, ext, extra_context, target):
        return GET_DATA

    def get_get_layout_if_empty(
        self, request, template_name, ext, extra_context, target
    ):
        return GET_LAYOUT

    def get_on_event_if_empty(self, request, template_name, ext, extra_context, target):
        return ON_EVENT


admin.site.register(Plot)
