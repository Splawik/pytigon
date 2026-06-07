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

import time
from pytigon_lib.schdjangoext.tools import import_model
from pyexcel_ods3 import get_data
from pytigon_lib.schtools.schjson import json_dumps, json_loads
from pytigon_lib.schfs.vfstools import get_temp_filename
import openpyxl
import csv


PFORM = form_with_perms("schtools")


class ImportTableForm(forms.Form):
    import_file = forms.FileField(
        label=_("File to import"),
        required=True,
    )


def view_importtableform(request, *argi, **argv):
    return PFORM(request, ImportTableForm, "schtools/formimporttableform.html", {})


def autocomplete_search(request, type):

    q = request.GET.get("query", request.POST.get("query", None))
    if not q:
        return HttpResponse(content_type="text/plain")
    limit = request.GET.get("limit", request.POST.get("limit", 15))
    try:
        limit = int(limit)
    except ValueError:
        return HttpResponseBadRequest()
    if q != " ":
        tab = Autocomplete.objects.filter(type=typ, label__istartswith=q)[:limit]
    else:
        tab = Autocomplete.objects.filter(type=typ)[:limit]
    out_tab = []
    for pos in tab:
        out_tab.append(
            {"id": pos.id, "label": pos.label, "name": pos.label, "value": pos.value}
        )
    json_data = json.dumps(out_tab)
    return HttpResponse(json_data, content_type="application/x-javascript")


def set_user_param(request, **argv):

    key = request.POST.get("param", None)
    value = request.POST.get("value", None)
    user = request.user.username

    p = models.Parameter.objects.filter(type="sys_user", subtype=user, key=key)
    if len(p) > 0:
        obj = p[0]
    else:
        obj = models.Parameter()
        obj.type = "sys_user"
        obj.subtype = user
        obj.key = key

    obj.value = value
    obj.save()

    return HttpResponse("OK")


def get_user_param(request, **argv):

    key = request.POST.get("param", None)
    user = request.user.username

    p = models.Parameter.objects.filter(type="sys_user", subtype=user, key=key)
    if len(p) > 0:
        obj = p[0]
        return HttpResponse(obj.value)
    else:
        return HttpResponse("")


@dict_to_template("schtools/v_import_table.html")
def import_table(request, app, table):

    if request.FILES:
        if "import_file" in request.FILES:
            data = request.FILES["import_file"]
            name = data.name
            ext = name.split(".")[-1].lower()
            model = import_model(app, table)

            table = []

            if ext in ("xlsx", "xls", "ods"):
                if ext == "ods":
                    d = get_data(data)
                    # print("F0", d)
                    # buf = json_dumps(d)
                    for key in d:
                        table = d[key]
                        break
                else:
                    first_line = True
                    width = 0

                    file_name = get_temp_filename("temp.xlsx")
                    f = open(file_name, "wb")
                    f.write(data.read())
                    f.close()

                    workbook = openpyxl.load_workbook(
                        filename=file_name, read_only=True
                    )
                    worksheets = workbook.get_sheet_names()
                    worksheet = workbook.get_sheet_by_name(worksheets[0])

                    for row in list(worksheet.rows):
                        if first_line:
                            first_line = False
                            buf = []
                            i = 0
                            for pos in row:
                                value = pos.value
                                if value:
                                    buf.append(value)
                                else:
                                    break
                                i += 1
                            if len(buf) > 0:
                                count = len(buf)
                                table.append(buf)
                            else:
                                break
                        else:
                            if row[0].value:
                                buf = []
                                i = 0
                                for pos in row:
                                    if i >= count:
                                        break
                                    buf.append(pos.value)
                                    i += 1
                                table.append(buf)
                            else:
                                break
                    os.remove(file_name)
            elif ext in ("txt", "csv"):
                first_line = True
                sep_list = [
                    "\t",
                    ";",
                    ",",
                    "|",
                ]
                sep = None

                txt = data.read().decode("utf-8").replace("\r", "").split("\n")
                for line in txt:
                    for pos in sep_list:
                        if pos in line:
                            sep = pos
                            break
                    break

                if sep:
                    csv_reader = csv.reader(txt, delimiter=sep)
                    for row in csv_reader:
                        table.append(row)

            if table and len(table) > 1:
                header = list([pos.strip() for pos in table[0] if pos])
                tree = False
                tmp = []
                for pos in header:
                    if not pos in tmp:
                        tmp.append(pos)
                    else:
                        tree = True
                        id1 = tmp.index(pos)
                        id2 = len(tmp)
                        break

                for row in table[1:]:
                    if len(row) == len(header):
                        x = model()
                        parent = None
                        for index, (attr_name, value) in enumerate(zip(header, row)):
                            if tree:
                                if index == id1:
                                    if row[id2]:
                                        objs = model.objects.filter(
                                            **{attr_name: value}
                                        )
                                        if len(objs) == 1:
                                            parent = objs[0]
                                    else:
                                        setattr(x, attr_name, value)
                                elif index == id2:
                                    if row[id2]:
                                        setattr(x, attr_name, value)
                                        if parent:
                                            setattr(x, "parent", parent)
                                else:
                                    setattr(x, attr_name, value)
                            else:
                                setattr(x, attr_name, value)
                        x.save()

            return {"redirect": "/schsys/ok/"}
        else:
            form = ImportTableForm(request.POST, request.FILES)
    else:
        form = ImportTableForm()

    return {"form": form}
