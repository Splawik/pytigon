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

from pytigon_lib.schtable.vfstable import (
    vfstable_view,
    vfsopen,
    vfssave,
    vfsview,
    vfsopen_page,
    vfsconvert,
)
from schtools.models import Parameter
import django.contrib.auth


PFORM = form_with_perms("schcommander")


class FileManager(forms.Form):
    folder = forms.CharField(
        label=_("Folder"),
        required=True,
    )
    sort = forms.ChoiceField(
        label=_("Sort"), required=True, choices=models.file_manager_sort_choices
    )


def view_filemanager(request, *argi, **argv):
    return PFORM(request, FileManager, "schcommander/formfilemanager.html", {})


class Move(forms.Form):
    dest = forms.ChoiceField(label=_("Destination"), required=False, choices=[])


def view_move(request, *argi, **argv):
    return PFORM(request, Move, "schcommander/formmove.html", {})


class Copy(forms.Form):
    dest = forms.ChoiceField(label=_("Destination"), required=False, choices=[])


def view_copy(request, *argi, **argv):
    return PFORM(request, Copy, "schcommander/formcopy.html", {})


class MkDir(forms.Form):
    dest = forms.CharField(
        label=_("Folder name"),
        required=False,
        widget=forms.TextInput(
            {
                "width": 280,
            }
        ),
    )


def view_mkdir(request, *argi, **argv):
    return PFORM(request, MkDir, "schcommander/formmkdir.html", {})


class Rename(forms.Form):
    dest = forms.CharField(
        label=_("Name"),
        required=False,
        max_length=None,
        min_length=None,
        widget=forms.TextInput(
            {
                "width": 280,
            }
        ),
    )


def view_rename(request, *argi, **argv):
    return PFORM(request, Rename, "schcommander/formrename.html", {})


class NewFile(forms.Form):
    dest = forms.CharField(
        label=_("Name"),
        required=False,
        max_length=None,
        min_length=None,
        widget=forms.TextInput(
            {
                "width": 280,
            }
        ),
    )


def view_newfile(request, *argi, **argv):
    return PFORM(request, NewFile, "schcommander/formnewfile.html", {})


class Delete(forms.Form):
    dest = forms.BooleanField(
        label=_("Recycle bin"),
        required=False,
        initial=True,
    )


def view_delete(request, *argi, **argv):
    return PFORM(request, Delete, "schcommander/formdelete.html", {})


class Setup(forms.Form):
    path1 = forms.CharField(
        label=_("Path 1"),
        required=False,
        max_length=None,
        min_length=None,
        widget=forms.TextInput(
            {
                "width": 280,
            }
        ),
    )
    path2 = forms.CharField(
        label=_("Path 2"),
        required=False,
        max_length=None,
        min_length=None,
        widget=forms.TextInput(
            {
                "width": 280,
            }
        ),
    )
    glob = forms.BooleanField(
        label=_("Default for all users"),
        required=False,
    )


def view_setup(request, *argi, **argv):
    return PFORM(request, Setup, "schcommander/formsetup.html", {})


def grid(request, folder, value):

    return vfstable_view(request, folder, value)


def open(request, file_name):

    return vfsopen(request, file_name)


def save(request, file_name):

    return vfssave(request, file_name)


def open_page(request, file_name, page):

    return vfsopen_page(request, file_name, page)


def view(request, file_name):

    return HttpResponse(vfsview(request, file_name))


def convert_html(request, file_name):

    headers = {
        "Content-Type": "text/html",
        "Content-Disposition": 'attachment; filename="file.html"',
    }

    return HttpResponse(vfsconvert(request, file_name, "html"), headers=headers)


def convert_pdf(request, file_name):

    headers = {
        "Content-Type": "application/pdf",
        "Content-Disposition": 'attachment; filename="file.pdf"',
    }
    return HttpResponse(vfsconvert(request, file_name, "pdf"), headers=headers)


def convert_docx(request, file_name):

    headers = {
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "Content-Disposition": 'attachment; filename="file.docx"',
    }
    return HttpResponse(vfsconvert(request, file_name, "docx"), headers=headers)


def convert_xlsx(request, file_name):

    headers = {
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "Content-Disposition": 'attachment; filename="file.xlsx"',
    }
    return HttpResponse(vfsconvert(request, file_name, "xlsx"), headers=headers)


def convert_spdf(request, file_name):

    headers = {
        "Content-Type": "application/spdf",
        "Content-Disposition": 'attachment; filename="file.spdf"',
    }
    return HttpResponse(vfsconvert(request, file_name, "spdf"), headers=headers)
