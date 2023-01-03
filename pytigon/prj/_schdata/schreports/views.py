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

from pytigon_lib.schtools.schjson import json_dumps, json_loads
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schdjangoext.fastform import form_from_str
from pytigon_lib.schviews import make_path
from schelements.models import DocReg, DocType, DocHead, Element
from django.db.models import F
from schelements.views import year_ago


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


PFORM = form_with_perms("schreports")


class _FilterFormReport(forms.Form):
    date_from = forms.DateField(
        label=_("Data od"),
        required=False,
        initial=year_ago,
    )
    date_to = forms.DateField(
        label=_("Data do"),
        required=True,
    )

    def process(self, request, queryset=None):

        date_from = self.cleaned_data["date_from"]
        date_to = self.cleaned_data["date_to"]

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        return queryset

    def process_empty_or_invalid(self, request, queryset):
        return queryset.filter(date__gte=year_ago())


def view__filterformreport(request, *argi, **argv):
    return PFORM(
        request, _FilterFormReport, "schreports/form_filterformreport.html", {}
    )


def new_rep(request, rep_type, doc_type_name):

    # new_rep/(?P<rep_type>\w+)/(?P<doc_type_name>\w+)/$
    doc_type = DocType.objects.filter(name=doc_type_name)
    if len(doc_type) == 1:
        doc = DocHead()
        doc.doc_type_parent = doc_type[0]
        doc.date = datetime.datetime.now()
        doc.status = "edit"
        doc.operator = request.user.username
        doc.save()

        rep = models.Report()
        rep.parent = None
        rep.order = 0
        rep.parent_doc = doc
        rep.report_def_name = rep_type
        rep.date = datetime.datetime.now()
        rep.save()
        url = make_href("/schreports/table/Report/%d/edit__rep/" % rep.id)
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("Error - document type: %s doesn't exists" % doc_type_name)


def edit__rep(request, rep_id, rep=None):

    if rep == None:
        rep = models.Report.objects.get(pk=rep_id)
    rep_def = models.ReportDef.objects.get(name=rep.report_def_name)

    if rep_def.declaration:
        form_class = form_from_str(rep_def.declaration)
    else:
        return "ERROR"

    if request.POST or request.FILES:
        if request.method == "POST":
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                if rep_def.save_fun:
                    exec(rep_def.save_fun)
                    data = locals()["save"](form, rep)
                else:
                    data = form.cleaned_data
                if data != None:
                    rep.jsondata = data
                    rep.save()
                    url = make_path("ok")
                    return HttpResponseRedirect(url)

    if not request.POST:
        data = rep.get_json_data()

        if rep_def.load_fun:
            exec(rep_def.load_fun)
            data_form = locals()["load"](data)
        else:
            data_form = data
        form = form_class(initial=data_form)

    t = Template(ihtml_to_html(None, rep_def.template))
    c = RequestContext(request, {"form": form, "rep": rep, "rep_def": rep_def})

    return HttpResponse(t.render(c))


def new_subrep(request, parent_rep_id, rep_type):

    rep_parent = models.Report.objects.get(pk=parent_rep_id)
    rep = models.Report()
    rep.parent = rep_parent
    rep.order = 0
    rep.report_def_name = rep_parent.report_def_name + "/" + rep_type
    rep.date = datetime.datetime.now()
    return edit__rep(request, 0, rep)

    # rep_parent = models.Report.objects.get(pk=parent_rep_id)
    # rep = models.Report()
    # rep.parent = rep_parent
    # rep.order = 0
    # rep.report_def_name = rep_parent.report_def_name + "/" + rep_type
    # rep.date = datetime.datetime.now()
    # rep.save()
    # url = make_href("/schreports/table/Report/%d/edit__rep/" % rep.id)
    # return HttpResponseRedirect(url)


def edit_subrep(request, parent_rep_id, rep_type, view_type):

    parent_rep = models.Report.objects.get(pk=parent_rep_id)
    parent_rep_def = models.ReportDef.objects.get(name=parent_rep.report_def_name)
    rep_def = parent_rep_def.getsubrep(rep_type)
    subreps = parent_rep.getsubreps(rep_type)

    cdict = {}
    cdict["parent_rep"] = parent_rep
    cdict["parent_rep_def"] = parent_rep_def
    cdict["rep_type"] = rep_type
    cdict["view_type"] = view_type
    cdict["reports"] = parent_rep.getsubreps(rep_type)
    cdict["rep_def"] = rep_def

    txt = ihtml_to_html(None, rep_def.to_html_rec)
    t = Template(txt)
    c = RequestContext(request, cdict)

    return HttpResponse(t.render(c))


def move_up(request, pk):

    return move_rep(request, pk, "-1")


def move_down(request, pk):

    return move_rep(request, pk, "+1")


def edit__rep2(request, dochead_id):

    reps = models.Report.objects.filter(parent_doc__id=dochead_id)
    if reps.count() > 0:
        new_url = make_href("/schreports/table/Report/%d/edit__rep/" % reps[0].id)
        return HttpResponseRedirect(new_url)
    else:
        return HttpResponse("Error - report doesn't exist")


def repaction(request, dochead_id, rep_action):

    doc = DocHead.objects.get(pk=dochead_id)
    reps = models.Report.objects.filter(parent_doc=doc)
    if reps.count() > 0:
        url = make_href(
            "/schreports/table/Report/%d/%s/"
            % (reps[0].id, rep_action.replace("__", "/"))
        )
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("Error - document: %d doesn't exists" % dochead_id)


def move_to(request, rep_id, to_pos):

    return move_rep(request, rep_id, int(to_pos))


@dict_to_json
def plot_service(request, **argv):

    if "param" in request.GET:
        request_param = request.GET["param"]
    else:
        request_param = None

    param = json_loads(request.body.decode("utf-8"))

    action = param["action"]
    name = param["name"]

    objs = models.Plot.objects.filter(name=name)
    if len(objs) == 1:
        obj = objs[0]
    else:
        obj = None

    if obj:
        if action == "get_config":
            if obj.get_config:
                tmp = "def _get_config(request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.get_config.split("\n")]
                )
                exec(tmp)
                config = locals()["_get_config"](request_param)
            else:
                config = {
                    "displayModeBar": False,
                    "showLink": False,
                    "displaylogo": False,
                    "scrollZoom": True,
                    "modeBarButtonsToRemove": ["sendDataToCloud"],
                }
            return config
        elif action == "get_data":
            if obj.get_data:
                tmp = "def _get_data(request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.get_data.split("\n")]
                )
                exec(tmp)
                data = locals()["_get_data"](request_param)
            else:
                data = {}
            return data
        elif action == "get_layout":
            if obj.get_layout:
                tmp = "def _get_layout(request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.get_layout.split("\n")]
                )
                exec(tmp)
                layout = locals()["_get_layout"](request_param)
            else:
                layout = {}
            return layout
        elif action == "on_event":
            if obj.on_event:
                tmp = "def _on_event(data, request_param):\n" + "\n".join(
                    ["    " + pos for pos in obj.on_event.split("\n")]
                )
                exec(tmp)
                ret = locals()["_on_event"](param, request_param)
                return ret
            else:
                return {}
        else:
            return {"error": "Action not found"}

    return {"error": "Plot object not found"}


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
    group.save()

    if not group.gparent:
        group.gparent = group
        group.save()

    url = make_href("/schreports/table/CommonGroup/%d/edit__group/" % group.id)
    return HttpResponseRedirect(url)


def edit__group(request, group_id):

    group = models.CommonGroup.objects.get(pk=group_id)
    group_def = models.CommonGroupDef.objects.get(name=group.group_def_name)

    if group_def.declaration:
        form_class = form_from_str(group_def.declaration)
    else:
        return HttpResponse("ERROR")

    if request.POST or request.FILES:
        if request.method == "POST":
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                if group_def.save_fun:
                    exec(group_def.save_fun)
                    data = locals()["save"](form, group)
                else:
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

        if group_def.load_fun:
            exec(group_def.load_fun)
            data_form = locals()["load"](data)
        else:
            data_form = data

        if not data:
            data = {}

        data_form["title"] = group.title
        form = form_class(initial=data_form)

    t = Template(ihtml_to_html(None, group_def.template))
    c = RequestContext(request, {"form": form, "group": group, "group_def": group_def})

    return HttpResponse(t.render(c))


def list_group_by_tag(request, group_tag):

    groups = models.CommonGroup.objects.filter(tag_name=group_tag)
    if len(groups) > 0:
        group = groups[0]
        url = make_href(
            "/schreports/table/CommonGroup/%d/%d/form/tree/?only_content=1"
            % (group.id, group.id)
        )
    else:
        url = make_href("/schreports/table/CommonGroup/0/form/tree/?only_content=1")
    return HttpResponseRedirect(url)
