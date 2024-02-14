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

from pytigon_lib.schtools.schjson import json_dumps, json_loads
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schdjangoext.fastform import form_from_str
from pytigon_lib.schviews import make_path
from schelements.models import DocReg, DocType, DocHead, Element
from django.db.models import F
from schelements.views import year_ago

from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct


def edit_group(request, group):
    group_def = models.CommonGroupDef.objects.get(name=group.group_def_name)

    if group_def.declaration:
        form_class = form_from_str(group_def.declaration)
    else:
        return HttpResponse("ERROR")

    if request.POST or request.FILES:
        if request.method == "POST":
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                data = run_code_from_db_field(
                    f"groupdef__save_fun_{group_def.pk}.py",
                    group_def,
                    "save_fun",
                    "save",
                    form=form,
                    obj=group,
                )
                if data == None:
                    data = form.cleaned_data

                if not data:
                    data = {}

                if "title" in data:
                    group.title = data["title"]
                    del data["title"]
                group.jsondata = data
                # group._data = data
                # group._data['json_update'] = True
                group.save()
                url = make_path("ok")
                return HttpResponseRedirect(url)

    if not request.POST:
        data = group.get_json_data()

        data_form = run_code_from_db_field(
            f"groupdef__load_fun_{group_def.pk}.py",
            group_def,
            "load_fun",
            "load",
            data=data,
        )
        if data != None:
            data_form = data

        if not data:
            data = {}

        data_form["title"] = group.title
        form = form_class(initial=data_form)

    # t = Template(ihtml_to_html(None, group_def.template))
    t = Template(group_def.template)
    c = RequestContext(request, {"form": form, "group": group, "group_def": group_def})

    return HttpResponse(t.render(c))


def move_rep(request, id, to_pos="+1"):
    obj = models.Report.objects.get(pk=id)
    url = make_path("ok")
    if not obj.parent:
        return HttpResponseRedirect(url)

    if type(to_pos) == str:
        if to_pos == "+1":
            objects = models.Report.objects.filter(parent=obj.parent).filter(
                order__gt=obj.order
            )
            if len(objects) > 0:
                obj2 = objects[0]
            else:
                return HttpResponseRedirect(url)
        elif to_pos == "-1":
            objects = models.Report.objects.filter(parent=obj.parent).filter(
                order__lt=obj.order
            )
            if len(objects) > 0:
                obj2 = list(objects)[-1]
            else:
                return HttpResponseRedirect(url)

        tmp_order = obj.order
        obj.order = obj2.order
        obj2.order = tmp_order
        obj.save()
        obj2.save()

    elif type(to_pos) == int:
        obj2 = models.Report.objects.get(pk=to_pos)
        order = obj2.order
        if obj.order < order:
            objects = (
                models.Report.objects.filter(parent=obj.parent)
                .filter(order__gt=obj2.order)
                .update(order=F("order") + 2)
            )
            obj.order = order + 1
        else:
            objects = (
                models.Report.objects.filter(parent=obj.parent)
                .filter(order__gte=obj2.order)
                .update(order=F("order") + 2)
            )
            obj.order = order
        obj.save()

    return actions.refresh(request)


def new_group(request, group_type, parent_id):

    # new_group/(?P<group_type>\w+)/(?P<parent_id\d+)/$
    if parent_id and int(parent_id) > 0:
        parent = models.CommonGroup.objects.get(id=int(parent_id))
    else:
        parent = None
    group = models.CommonGroup()
    if parent:
        group.parent = parent
        gparent = parent
        while gparent.parent:
            gparent = gparent.parent
        group.gparent = gparent
        group.gp_group_def_name = gparent.group_def_name
    else:
        group.gp_group_def_name = group_type

    group.group_def_name = group_type
    # group.save()

    if not group.gparent:
        group.gparent = group
        # group.save()

    return edit_group(request, group)

    # url = make_href("/schstruct/table/CommonGroup/%d/edit__group/?after_close=refresh" % group.id)
    # return HttpResponseRedirect(url)


def edit__group(request, group_id):

    group = models.CommonGroup.objects.get(pk=group_id)
    return edit_group(request, group)

    group_def = models.CommonGroupDef.objects.get(name=group.group_def_name)

    if group_def.declaration:
        form_class = form_from_str(group_def.declaration)
    else:
        return HttpResponse("ERROR")

    if request.POST or request.FILES:
        if request.method == "POST":
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                data = run_code_from_db_field(
                    f"groupdef__save_fun_{group_def.pk}.py",
                    group_def,
                    "save_fun",
                    "save",
                    form=form,
                    obj=group,
                )
                if data == None:
                    data = form.cleaned_data

                if not data:
                    data = {}

                if "title" in data:
                    group.title = data["title"]
                    del data["title"]
                group.jsondata = data
                # group._data = data
                # group._data['json_update'] = True
                group.save()
                url = make_path("ok")
                return HttpResponseRedirect(url)

    if not request.POST:
        data = group.get_json_data()

        data_form = run_code_from_db_field(
            f"groupdef__load_fun_{group_def.pk}.py",
            group_def,
            "load_fun",
            "load",
            data=data,
        )
        if data != None:
            data_form = data

        if not data:
            data = {}

        data_form["title"] = group.title
        form = form_class(initial=data_form)

    # t = Template(ihtml_to_html(None, group_def.template))
    t = Template(group_def.template)
    c = RequestContext(request, {"form": form, "group": group, "group_def": group_def})

    return HttpResponse(t.render(c))


def list_group_by_tag(request, group_tag, template):

    if template:
        target_template = "__" + template
    else:
        target_template = ""

    groups = models.CommonGroup.objects.filter(tag_name=group_tag)
    if len(groups) > 0:
        group = groups[0]
        url = make_href(
            "/schstruct/table/CommonGroup/%d/%d/form%s/tree/?only_content=1"
            % (group.id, group.id, target_template)
        )
    else:
        url = make_href(
            "/schstruct/table/CommonGroup/0/form%s/tree/?only_content=1"
            % target_template
        )
    return HttpResponseRedirect(url)
