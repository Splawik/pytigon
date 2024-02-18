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


def move_doc(request, id, to_pos="+1"):
    obj = models.Doc.objects.get(pk=id)
    url = make_path("ok")
    if not obj.parent:
        return HttpResponseRedirect(url)

    if type(to_pos) == str:
        if to_pos == "+1":
            objects = models.Doc.objects.filter(parent=obj.parent).filter(
                order__gt=obj.order
            )
            if len(objects) > 0:
                obj2 = objects[0]
            else:
                return HttpResponseRedirect(url)
        elif to_pos == "-1":
            objects = models.Doc.objects.filter(parent=obj.parent).filter(
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
        obj2 = models.Doc.objects.get(pk=to_pos)
        order = obj2.order
        if obj.order < order:
            objects = (
                models.Doc.objects.filter(parent=obj.parent)
                .filter(order__gt=obj2.order)
                .update(order=F("order") + 2)
            )
            obj.order = order + 1
        else:
            objects = (
                models.Doc.objects.filter(parent=obj.parent)
                .filter(order__gte=obj2.order)
                .update(order=F("order") + 2)
            )
            obj.order = order
        obj.save()

    return actions.refresh(request)


PFORM = form_with_perms("schdoc")


class _FilterFormDoc(forms.Form):
    date_from = forms.DateField(
        label=_("Date from"),
        required=False,
        initial=year_ago,
    )
    date_to = forms.DateField(
        label=_("Date to"),
        required=False,
    )


def view__filterformdoc(request, *argi, **argv):
    return PFORM(request, _FilterFormDoc, "schdoc/form_filterformdoc.html", {})


def new_doc(request, doc_type, doc_type_name):

    # new_doc/(?P<doc_type>\w+)/(?P<doc_type_name>\w+)/$
    dochead_type = DocType.objects.filter(name=doc_type_name)
    if len(dochead_type) == 1:
        doc = DocHead()
        doc.doc_type_parent = dochead_type[0]
        doc.date = timezone.now()
        doc.status = "edit"
        doc.operator = request.user.username
        doc.save()

        doc2 = models.Doc()
        doc2.parent = None
        doc2.order = 0
        doc2.parent_doc = doc
        doc2.doc_def_name = doc_type
        doc2.date = timezone.now()
        doc2.save()
        url = make_href("/schdoc/table/Doc/%d/edit__doc/" % doc2.id)
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("Error - document type: %s doesn't exists" % doc_type_name)


def edit__doc(request, doc_id, doc=None):

    if doc == None:
        doc = models.Doc.objects.get(pk=doc_id)
    doc_def = models.DocDef.objects.get(name=doc.doc_def_name)

    if doc_def.declaration:
        form_class = form_from_str(doc_def.declaration)
    else:
        return "ERROR"

    if request.POST or request.FILES:
        if request.method == "POST":
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                data = run_code_from_db_field(
                    f"docdef__save_fun_{doc_def.pk}.py",
                    doc_def,
                    "save_fun",
                    "save",
                    form=form,
                    obj=doc,
                )
                if data == None:
                    data = form.cleaned_data

                if data != None:
                    doc.jsondata = data
                    doc.save()
                    url = make_path("ok")
                    return HttpResponseRedirect(url)

    if not request.POST:
        data = doc.get_json_data()

        data_form = run_code_from_db_field(
            f"docdef__save_fun_{doc_def.pk}.py", doc_def, "load_fun", "load", data=data
        )

        if data_form == None:
            data_form = data

        form = form_class(initial=data_form)

    # t = Template(ihtml_to_html(None, doc_def.template))
    t = Template(doc_def.template)
    c = RequestContext(request, {"form": form, "doc": doc, "doc_def": doc_def})

    return HttpResponse(t.render(c))


def new_subdoc(request, parent_doc_id, doc_type):

    doc_parent = models.Doc.objects.get(pk=parent_doc_id)
    doc = models.Doc()
    doc.parent = doc_parent
    doc.order = 0
    doc.doc_def_name = doc_parent.doc_def_name + "/" + doc_type
    doc.date = timezone.now()
    return edit__doc(request, 0, doc)


def edit_subdoc(request, parent_doc_id, doc_type, view_type):

    parent_doc = models.Doc.objects.get(pk=parent_doc_id)
    parent_doc_def = models.DocDef.objects.get(name=parent_doc.doc_def_name)
    doc_def = parent_doc_def.getsubdoc(doc_type)
    subdocs = parent_doc.getsubdocs(doc_type)

    cdict = {}
    cdict["parent_doc"] = parent_doc
    cdict["parent_doc_def"] = parent_doc_def
    cdict["doc_type"] = doc_type
    cdict["view_type"] = view_type
    cdict["documents"] = parent_doc.getsubdocs(doc_type)
    cdict["doc_def"] = doc_def

    txt = ihtml_to_html(None, doc_def.to_html_rec)
    t = Template(txt)
    c = RequestContext(request, cdict)

    return HttpResponse(t.render(c))


def move_up(request, pk):

    return move_doc(request, pk, "-1")


def move_down(request, pk):

    return move_doc(request, pk, "+1")


def edit__doc2(request, dochead_id):

    docs = models.Doc.objects.filter(parent_doc__id=dochead_id)
    if docs.count() > 0:
        new_url = make_href("/schdoc/table/Doc/%d/edit__doc/" % docs[0].id)
        return HttpResponseRedirect(new_url)
    else:
        return HttpResponse("Error - document doesn't exist")


def repaction(request, dochead_id, doc_action):

    doc = DocHead.objects.get(pk=dochead_id)
    docs = models.Doc.objects.filter(parent_doc=doc)
    if docs.count() > 0:
        url = make_href(
            "/schdoc/table/Doc/%d/%s/" % (docs[0].id, doc_action.replace("__", "/"))
        )
        return HttpResponseRedirect(url)
    else:
        return HttpResponse("Error - document: %d doesn't exists" % dochead_id)


def move_to(request, doc_id, to_pos):

    return move_doc(request, doc_id, int(to_pos))
