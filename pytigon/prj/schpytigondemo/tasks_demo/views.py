from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django import forms
from django.template.loader import render_to_string
from django.template import Context, Template
from django.template import RequestContext
from django.conf import settings
from django.views.generic import TemplateView

from pytigon_lib.schviews.form_fun import form_with_perms
from pytigon_lib.schviews.viewtools import (
    dict_to_template,
    dict_to_odf,
    dict_to_pdf,
    dict_to_json,
    dict_to_xml,
    dict_to_ooxml,
    dict_to_txt,
    dict_to_hdoc,
)
from pytigon_lib.schviews.viewtools import render_to_response
from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schdjangoext import formfields as ext_form_fields
from pytigon_lib.schviews import actions

from django.utils.translation import gettext_lazy as _

from . import models
import os
import sys
import datetime
from django.utils import timezone

from django_q.tasks import async_task, result
import time


@dict_to_template("tasks_demo/v_test_task.html")
def test_task(request, **argv):

    id = "test1"
    task_id = async_task("tasks_demo.tasks.test_task", task_publish_id=id, param=123)
    return {"task_id": task_id, "id": "demo__" + id}


@dict_to_template("tasks_demo/v_test_task2.html")
def test_task2(request, **argv):

    task_id = async_task("tasks_demo.tasks.test_task2")
    return {"ret": task_id}
