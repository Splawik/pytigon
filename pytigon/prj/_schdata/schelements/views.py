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

from django.urls import resolve
from django.conf import settings
from django.db import transaction
from django_select2.forms import HeavySelect2Widget, ModelSelect2Widget
from django.core.validators import int_list_validator

from pytigon_lib.schtools.tools import content_to_function
from pytigon_lib.schdjangoext.fastform import form_from_str
from django.db.models import Q, F


def year_ago():
    dt = datetime.date.today()
    try:
        dt = dt.replace(year=dt.year - 1)
    except ValueError:
        dt = dt.replace(year=dt.year - 1, day=dt.day - 1)
    return dt


def change_status(request, pk, action="accept"):
    doc_head = models.DocHead.objects.get(pk=pk)
    doc_type = doc_head.doc_type_parent
    doc_reg = doc_type.parent
    action_name = request.GET.get("x1", "")
    reg_status_list = models.DocRegStatus.objects.filter(
        parent=doc_reg, name=action_name
    )
    if len(reg_status_list) == 1:
        reg_status = reg_status_list[0]
    else:
        reg_status = None
    form = None

    if reg_status:
        if action == "accept":
            form_txt = reg_status.accept_form
            fun = content_to_function(
                reg_status.accept_proc,
                "request, doc_head, reg_status, doc_type, doc_reg, doc_status, form",
                globals_dict={
                    "models": models,
                },
            )
        else:
            form_txt = reg_status.undo_form
            fun = content_to_function(
                reg_status.undo_proc,
                "request, doc_head, reg_status, doc_type, doc_reg, doc_status, form",
                globals_dict={
                    "models": models,
                },
            )

        params = {
            "request": request,
            "doc_head": doc_head,
            "doc_type": doc_type,
            "doc_reg": doc_reg,
        }
        if form_txt:
            form_class = form_from_str(form_txt, params)
        else:
            form_class = None

        if (not form_class) or request.POST:
            if form_class:
                form = form_class(request.GET, request.POST)
            else:
                form = None

            if (not form) or form.is_valid():
                doc_status = models.DocHeadStatus()
                doc_status.parent = doc_head

                try:
                    with transaction.atomic():
                        errors = fun(
                            request,
                            doc_head,
                            reg_status,
                            doc_type,
                            doc_reg,
                            doc_status,
                            form,
                        )
                except ValueError as err:
                    errors = err.args

                if not errors:
                    if action_name and action_name != doc_head.status:
                        doc_head.status = action_name
                        doc_head.save()

                    if action != "accept":
                        models.DocItem.objects.filter(
                            parent=doc_head, level__gte=reg_status.order
                        ).delete()

                    doc_status.date = datetime.datetime.now()
                    doc_status.operator = request.user.username
                    doc_status.save()

                    return actions.update_row_ok(
                        request, int(doc_head.id), str(doc_head)
                    )
                else:
                    return {
                        "errors": errors,
                        "form": form,
                        "doc_head": doc_head,
                        "doctype": doc_type,
                        "doc_reg": doc_reg,
                        "reg_status": reg_status,
                        "action_name": action_name,
                    }
        if not form:
            if form_class:
                form = form_class()
            else:
                form = None
            return {
                "error": False,
                "form": form,
                "doc_head": doc_head,
                "doctype": doc_type,
                "doc_reg": doc_reg,
                "reg_status": reg_status,
                "action_name": action_name,
            }
    else:
        return {"error": "Status %s doesn't exists" % action_name}


PFORM = form_with_perms("schelements")


class _FilterFormDocHead(forms.Form):
    date_from = forms.DateField(
        label=_("Date from"),
        required=False,
        initial=year_ago,
    )
    date_to = forms.DateField(
        label=_("Data to"),
        required=False,
    )
    target = forms.CharField(
        label=_("Target"), required=False, max_length=None, min_length=None
    )
    number = forms.CharField(
        label=_("Number"), required=False, max_length=None, min_length=None
    )

    def process(self, request, queryset=None):

        date_from = self.cleaned_data["date_from"]
        date_to = self.cleaned_data["date_to"]
        target = self.cleaned_data["target"]
        number = self.cleaned_data["number"]

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lt=date_to + datetime.timedelta(days=1))
        if target:
            queryset = queryset.filter(parent_element__name__icontains=target)
        if number:
            queryset = queryset.filter(number__icontains=number)

        return queryset

    def process_empty_or_invalid(self, request, queryset):
        return queryset.filter(date__gte=year_ago())


def view__filterformdochead(request, *argi, **argv):
    return PFORM(
        request, _FilterFormDocHead, "schelements/form_filterformdochead.html", {}
    )


class _FilterFormAccountState(forms.Form):
    account_target = ext_form_fields.ModelSelect2Field(
        label=_("Target"),
        required=False,
        queryset=models.Element.objects.filter(type="O-DIV"),
        search_fields=["name__istartswith"],
        attrs={"data-minimum-input-length": 0},
    )
    account = ext_form_fields.ModelSelect2Field(
        label=_("Account"),
        required=False,
        queryset=models.Account.objects.all(),
        search_fields=["name__istartswith"],
        attrs={"data-minimum-input-length": 0},
    )
    classifier1 = forms.CharField(
        label=_("Classifier 1"), required=False, max_length=None, min_length=None
    )
    classifier2 = forms.CharField(
        label=_("Classifier 2"), required=False, max_length=None, min_length=None
    )
    classifier3 = forms.CharField(
        label=_("classifier3"), required=False, max_length=None, min_length=None
    )
    subcode = forms.CharField(
        label=_("Subcode"), required=False, max_length=None, min_length=None
    )
    period = forms.CharField(
        label=_("Period"), required=False, max_length=None, min_length=None
    )
    not_null = forms.BooleanField(
        label=_("Not null"),
        required=False,
    )
    not_empty = forms.BooleanField(
        label=_("Not empty"),
        required=False,
    )
    analytical = forms.BooleanField(
        label=_("Analytical"),
        required=False,
    )

    def process(self, request, queryset=None):

        return self.process_empty_or_invalid(request, queryset)

    def process_empty_or_invalid(self, request, queryset):
        if not self.is_bound:
            return queryset

        if self.data["account_target"]:
            queryset = queryset.filter(target__id=int(self.data["account_target"][0]))
        if self.cleaned_data["account"]:
            pass
        if self.cleaned_data["classifier1"]:
            pass
        if self.cleaned_data["classifier2"]:
            pass
        if self.cleaned_data["classifier3"]:
            pass
        if self.cleaned_data["subcode"]:
            pass

        if self.cleaned_data["period"]:
            if self.cleaned_data["period"] == "*":
                pass
            else:
                queryset = queryset.filter(period=self.cleaned_data["period"])
        else:
            queryset = queryset.filter(Q(period__isnull=True) | Q(period=""))

        if self.cleaned_data["not_null"]:
            queryset = queryset.exclude(debit=F("credit"))

        if self.cleaned_data["not_empty"]:
            queryset = queryset.exclude(debit=0, credit=0)

        if self.cleaned_data["analytical"]:
            queryset = queryset.filter(aggregate=False)

        return queryset


def view__filterformaccountstate(request, *argi, **argv):
    return PFORM(
        request,
        _FilterFormAccountState,
        "schelements/form_filterformaccountstate.html",
        {},
    )


def view_doc_heads(request, filter, target, vtype):

    regs = models.DocReg.objects.filter(name=filter.replace("_", "/"))
    if regs.count() > 0:
        new_url = make_href(
            "/schelements/table/DocHead/%s/%s/%slist/" % (filter, target, vtype)
        )
        view, args, kwargs = resolve(new_url)
        kwargs["request"] = request

        # def init(view_obj):
        #    view_obj.template_name = "abc"
        # kwargs['init'] = init

        return view(*args, **kwargs)
    else:
        return HttpResponse("Error - %s document register doesn't exists" % filter)


def view_doc_items(request, parent_id):

    items = models.DocItem.objects.filter(parent=parent_id)
    if items.count() > 0:
        new_url = make_href(
            "/schelements/table/DocHead/%s/%s/%slist" % (filter, target, vtype)
        )
        view, args, kwargs = resolve(new_url)
        kwargs["request"] = request
        return view(*args, **kwargs)
    else:
        return HttpResponse("Error - %s document register doesn't exists" % filter)


def edit_head(request, id):

    return HttpResponse("Error")


def edit_item(request, id):

    return HttpResponse("Error")


@dict_to_template("schelements/v_approve.html")
def approve(request, pk):

    return change_status(request, pk, action="accept")


@dict_to_template("schelements/v_discard.html")
def discard(request, pk):

    return change_status(request, pk, action="undo")


def view_elements(request, code):

    # if settings.URL_ROOT_FOLDER and len(settings.URL_ROOT_FOLDER) > 0:
    #    url_base = '/' + settings.URL_ROOT_FOLDER + '/'
    # else:
    #    url_base = '/'

    id = 0

    if code:
        objs = models.Element.objects.filter(code=code)
        if len(objs) > 0:
            id = objs[0].pk

    href2 = make_href(
        "/schelements/table/Element/%d/%d/form/treelist/?only_content" % (id, id),
        request.get_full_path(),
    )
    return HttpResponseRedirect(href2)


def view_elements_as_tree(request, code, filter, template):

    # if settings.URL_ROOT_FOLDER and len(settings.URL_ROOT_FOLDER) > 0:
    #    url_base = '/' + settings.URL_ROOT_FOLDER + '/'
    # else:
    #    url_base = '/'

    id = 0

    if code and code != "-":
        objs = models.Element.objects.filter(code=code)
        if len(objs) > 0:
            id = objs[0].pk

    if template:
        target = "form__" + template
    else:
        target = "form"

    href2 = make_href(
        "/schelements/table/Element/%d/%s/%s/tree/?only_content" % (id, filter, target),
        request.get_full_path(),
    )
    return HttpResponseRedirect(href2)
