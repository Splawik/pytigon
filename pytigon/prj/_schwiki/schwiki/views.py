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

from .models import Page
from pytigon_lib.schdjangoext.fastform import form_from_str
from django.template.loader import select_template
from django.http import JsonResponse
from pytigon_lib.schviews import make_path
from pytigon_lib.schtools.schjson import json_loads, json_dumps

from pytigon_lib.schtools.tools import bencode, bdecode, is_null

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from schwiki.applib import makdown_obj_simple, markdown_obj_subblocks
from pytigon_lib.schindent.indent_markdown import get_obj_renderer

from pytigon_lib.schdjangoext.import_from_db import run_code_from_db_field, ModuleStruct

template_start_wiki = """
{# -*- coding: utf-8 -*- #}

{% extends "schwiki/wiki_view.html" %}

{% load exfiltry %}
{% load exsyntax %}

"""

template_start = """
{# -*- coding: utf-8 -*- #}

{%% extends "schwiki/%s" %%}

{%% load exfiltry %%}
{%% load exsyntax %%}
"""

template_simple = """
{# -*- coding: utf-8 -*- #}

{% load exfiltry %}
{% load exsyntax %}
"""


# @cache_page(60 * 15)


def view_page(request, app_or_subject, page_path):

    transfer_to_cache = False
    key = ""

    if not request.user.has_perm("wiki.add_page"):
        key = "wiki_view_page_%s_%s" % (app_or_subject, page_path)
        data = cache.get(key)
        if data:
            return data
        else:
            transfer_to_cache = True

    desc = request.GET.get("desc", "")
    path, sep, page_name = page_path.rpartition("+")
    if page_name:
        page_name = page_name[0].upper() + page_name[1:]

    id = -1
    if path:
        path_list = path.split("+")
        if page_name in path_list:
            path_list = path_list[: path_list.index(page_name)]
        if len(path_list) > 10:
            path_list = path_list[1:]
        path = "+".join(
            path_list
            + [
                page_name,
            ]
        )
    else:
        path_list = None
        path = page_name

    path_list2 = []
    if path_list:
        for pos in path_list:
            try:
                # p = Page.objects.get(name=pos, subject=app_or_subject)
                p = Page.get_page(request, app_or_subject, name)
                if p.description:
                    path_list2.append(p.description)
                else:
                    path_list2.append(pos)
            except:
                path_list2.append(pos)

    page = Page.get_page(request, app_or_subject, page_name)
    if page:
        id = page.id
        content = page.content
        try:
            t = Template(template_simple + content)
            c = RequestContext(
                request,
                {
                    "object": page,
                    "wiki_path": path,
                },
            )
            # c = Context({'object': page, 'wiki_path': path, 'request': request })
            content = t.render(c)
        except:
            content = page.content
    else:
        page = Page()
        page.name = page_name
        page.description = desc
        page.subject = app_or_subject
        page.update_time = timezone.now()
        page.operator = request.user.username
        page.save()
        id = page.id
        content = None

    conf = None
    if page:
        conf_list = models.WikiConf.objects.filter(subject=page.subject)
        if len(conf_list) > 0:
            conf = conf_list[0]

    c = {
        "page_name": page_name,
        "subject": app_or_subject,
        "content": content,
        "wiki_path": path,
        "wiki_path_list": path_list,
        "wiki_path_desc": path_list2,
        "title": "?: " + page_name,
        "object": page,
        "description": desc if desc else page_name,
        "only_content": True,
        "conf": conf,
    }

    if page and page.base_template:
        base_template = page.base_template
    else:
        base_template = "schwiki/wiki_view.html"

    c["content"] = content

    ret = render(request, base_template, context=c)

    if transfer_to_cache:
        cache.set(key, ret, 60 * 60)

    return ret


def edit_page(request, app_or_subject, page_name):

    page = Page.get_page(request, subject=app_or_subject, name=page_name)
    if not page:
        page = Page(app=app, name=page_name, subject=app_or_subject)
        page.save()

    redir = make_href("/schwiki/table/Page/%d/edit/?childwin=1" % page.id)

    return HttpResponseRedirect(redir)


@dict_to_template("schwiki/v_publish.html")
def publish(request, pk):

    conf = models.WikiConf.objects.get(pk=pk)
    object_list = []

    pages1 = models.Page.objects.filter(
        subject=conf.subject,
        latest=True,
        published=False,
        operator=request.user.username,
    )
    pages2 = models.Page.objects.filter(
        subject=conf.subject, latest=True, published=False, operator__isnull=True
    )
    pages = list(pages1) + list(pages2)
    if len(pages) > 0:
        for page in pages:
            page.published = True
            page.save()

            info = run_code_from_db_field(
                f"wikiconf__publish_fun_{conf.pk}.py",
                conf,
                "publish_fun",
                "publish",
                page=page,
                conf=conf,
            )

            if info == None:
                object_list.append([page, ""])
            else:
                object_list.append([page, info])

    pages1 = models.Page.objects.filter(
        subject=conf.subject,
        latest=False,
        published=True,
        operator=request.user.username,
    ).update(published=False)
    pages2 = models.Page.objects.filter(
        subject=conf.subject, latest=False, published=True, operator__isnull=True
    ).update(published=False)

    return {"OK": True, "object_list": object_list}


@dict_to_template("schwiki/v_search.html")
def search(request, q):

    search_txt = bdecode(q).decode("utf-8")
    object_list = Page.objects.filter(content__iregex=search_txt)
    return {"object_list": object_list, "q": search_txt}


def edit_page_object(request, **argv):

    if request.body:
        data = json_loads(request.body)
        status = data["status"]
    else:
        return JsonResponse(
            {
                "status": "object_name not found!",
            }
        )
    if data and status in ("new_object", "edit_object"):
        if status == "new_object":
            obj_name = data["object_name"]
            param = None
        else:
            line = data["line"]
            x = line.split("#", 1)
            obj_name = x[0].strip()[1:].strip()
            if obj_name.endswith(":"):
                obj_name = obj_name[:-1]
            if len(x) > 1:
                s = x[1].strip()
                if s and s[0] == "{":
                    param = json_loads(s.replace("\\n", "\n"))
                else:
                    return {"param_line": s}
            else:
                param = None
        obj_conf = get_obj_renderer(obj_name)
        if obj_conf:
            form_source = obj_conf.get_edit_form()
            if form_source:
                if type(form_source) == str:
                    form_class = form_from_str(form_source)
                else:
                    form_class = form_source
                form = obj_conf.form_from_dict(form_class, param)
                template_name = obj_conf.get_edit_template_name()
                t = select_template(
                    [
                        template_name,
                    ]
                )
                c = {"form": form, "object_name": obj_name}
                return HttpResponse(t.render(c, request))
            else:
                line = "% " + obj_name
                return JsonResponse({"status": "return_line", "line": line})
    return JsonResponse({"status": "object_name not found!", "status": status})


def edit_page_object_form(request, object_name):

    obj_conf = get_obj_renderer(object_name)
    if obj_conf:
        form_source = obj_conf.get_edit_form()
        if form_source:
            if type(form_source) == str:
                form_class = form_from_str(form_source)
            else:
                form_class = form_source
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                param = obj_conf.convert_form_to_dict(form)
                line = json_dumps(param).replace("\n", "\\n")
                return JsonResponse(
                    {"status": "return_line", "line": line, "RETURN": "$$RETURN_JSON"}
                )
            else:
                t = select_template(
                    [
                        template_name1,
                        template_name2,
                    ]
                )
                c = {
                    "form": form,
                }
                return HttpResponse(t.render(c, request))
    return JsonResponse(
        {"status": "object_name not found!", "object_name": object_name}
    )


def edit_object_on_page(request, page_id, line_number):

    page = Page.objects.get(pk=page_id)
    data = page.content_src
    lines = data.split("\n")
    line = lines[line_number - 1]

    x = line.split("#", 1)
    obj_name = x[0].strip()[1:].strip()
    if obj_name.endswith(":"):
        obj_name = obj_name[:-1]
    if len(x) > 1:
        s = x[1].strip()
        param = json_loads(s.replace("\\n", "\n"))
    else:
        param = None

    obj_conf = get_obj_renderer(obj_name)
    if obj_conf:
        form_source = obj_conf.get_edit_form()
        if form_source:
            if type(form_source) == str:
                form_class = form_from_str(form_source)
            else:
                form_class = form_source
            form = obj_conf.form_from_dict(form_class, param)
            template_name = obj_conf.get_edit_template_name()
            t = select_template(
                [
                    template_name,
                ]
            )
            c = {
                "form": form,
                "object_name": obj_name,
                "on_page": True,
                "page_id": page_id,
                "line_number": line_number,
            }
            return HttpResponse(t.render(c, request))

    return HttpResponse("")


def edit_object_on_page_form(request, page_id, line_number, object_name):

    param_indent = 120

    obj_conf = get_obj_renderer(object_name)

    if obj_conf:
        form_source = obj_conf.get_edit_form()
        if form_source:
            if type(form_source) == str:
                form_class = form_from_str(form_source)
            else:
                form_class = form_source
            form = form_class(request.POST, request.FILES)
            if form.is_valid():

                def join_parameters(param, line):
                    x = line.split("#", 1)
                    if len(x) > 1:
                        try:
                            param2 = param
                            old_param = json_load(x[1])
                            for key in old_param:
                                if not key in param2 or param2[key] == None:
                                    param2[key] = old_param[key]
                            return param2
                        except:
                            pass
                    return param

                page = Page.objects.get(pk=page_id)
                data = page.content_src
                lines = data.split("\n")
                current_line = lines[line_number - 1]
                param = obj_conf.convert_form_to_dict(form)

                if len(current_line) >= 64 * 1024:
                    x = current_line.split("#", 1)
                    if len(x) > 1:
                        old_param = json_loads(x[1])
                        for key in old_param:
                            if not key in param or param[key] == None:
                                param[key] = old_param[key]

                x = current_line.lstrip()
                indent = len(current_line) - len(x)
                line = (indent * " ") + "% " + object_name
                c = obj_conf.get_info()
                if "inline_content" in c and c["inline_content"]:
                    line += ":"
                if param:
                    if len(line) < param_indent:
                        line += (param_indent - len(line)) * " "
                    line += "#"
                    line += json_dumps(param).replace("\n", "\\n")
                lines[line_number - 1] = line
                page.content_src = "\n".join(lines)
                page.save()
                return actions.ok(request)
            else:
                t = select_template(
                    [
                        template_name1,
                        template_name2,
                    ]
                )
                c = {
                    "form": form,
                }
                return HttpResponse(t.render(c, request))

    return actions.cancel(request)
