#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of ERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

from base64 import b64encode
import re
import os

from django import template
from django.template.loader import get_template
from django.template import Template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.base import token_kwargs, TemplateSyntaxError, Node

from pytigon_lib.schtools.href_action import standard_dict, actions_dict, action_fun
from pytigon_lib.schdjangoext.tools import import_model, make_href

from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schdjangoext.models import TreeModel
from pytigon_lib.schtools.wiki import wiki_from_str, wikify
from pytigon_lib.schdjangoext.tools import make_href as mhref

from django.forms import FileInput, CheckboxInput, RadioSelect, CheckboxSelectMultiple
from django.utils.safestring import SafeText, SafeString
from django import forms
from django_select2 import forms as s2forms

from pyquery import PyQuery as pq


register = template.Library()

## tools


def inclusion_tag(file_name):
    def dec(func):
        def func2(context, *argi, **argv):
            ret = func(context, *argi, **argv)
            t = get_template(file_name)
            return t.render(ret, context.request)

        return register.simple_tag(
            takes_context=True, name=getattr(func, "_decorated_function", func).__name__
        )(func2)

    return dec


# row actions


class RowActionNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        if output.replace("\n", ""):
            t = Template(output)
            output2 = t.render(context).replace("\n", ";")
            t = get_template("widgets/row_actions.html")
            d = actions_dict(context, output2)
            return t.render(d, request=d["request"])
        else:
            return ""


@register.tag
def row_actions(parser, token):
    nodelist = parser.parse(("endrow_actions",))
    parser.delete_first_token()
    return RowActionNode(nodelist)


@inclusion_tag("widgets/action.html")
def action(
    context, action, title="", icon_name="", target="", attrs="", tag_class="", url=""
):
    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url)
    return ret


# actions


@inclusion_tag("widgets/view_row.html")
def view_row(
    context,
    object,
    title="",
    icon_name="",
    target="popup_info",
    attrs="",
    tag_class="",
    url="",
):
    if url:
        href = url
    else:
        if "version" in context and context["version"]:
            href = "{tp}%s/%s/view/?version=%s" % (
                context["object"].id,
                context["target"] if context["target"] != "json" else "_",
                context["version"],
            )
        else:
            href = "{tp}%s/%s/view/" % (
                context["object"].id,
                context["target"] if context["target"] != "json" else "_",
            )
    ret = action_fun(
        context, "view_row", title, icon_name, target, attrs, tag_class, href
    )
    # if hasattr(object, "get_derived_object"):
    #    object2 = object.get_derived_object()
    #    if hasattr(object2, "str"):
    #        ret["title2"] = str(object2)
    #    else:
    #        ret["title2"] = ("%s(id=" % type(object2).__name__) + str(title) + ")"
    # else:
    if hasattr(object, "str"):
        ret["title2"] = str(object)
    else:
        ret["title2"] = ("%s(id=" % type(object).__name__) + str(title) + ")"
    return ret


@inclusion_tag("widgets/get_row.html")
def get_row(context, title="", icon_name="", target="", attrs="", tag_class="", url=""):
    ret = action_fun(context, "get", title, icon_name, target, attrs, tag_class, url)
    ret["id"] = context["object"].id
    ret["text"] = str(context["object"])
    return ret


@inclusion_tag("widgets/button.html")
def button(context, title="", icon_name="", target="", attrs="", tag_class="", url=""):
    ret = action_fun(context, "button", title, icon_name, target, attrs, tag_class, url)
    return ret


def new_row_base(
    context,
    action="new_row/-",
    title="",
    icon_name="",
    target="",
    attrs="",
    tag_class="",
    url="",
):
    if url and not url.startswith("+"):
        url2 = url
    else:
        if "vtype" in context and context["vtype"] == "tree":
            url2 = "{tp}%s/this/{x1}/add/" % context["parent_pk"]
        else:
            url2 = "{tp}{x1}/add/"

        if url:
            url2 += url[1:]

        if action == "new_row/-":
            if (
                "base_filter" in context
                and context["base_filter"]
                and context["base_filter"] != "-"
            ):
                action = "new_row/" + context["base_filter"]
            elif "filter" in context and context["filter"] and context["filter"] != "-":
                action = "new_row/" + context["filter"]

    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url2)
    if title and title[0] == "+":
        description = title[1:]
        title = ""
    else:
        description = title
    ret["description"] = description
    return ret


@inclusion_tag("widgets/new_row.html")
def new_row(
    context,
    title="",
    icon_name="",
    target="",
    attrs="",
    tag_class="",
    url="",
    action="new_row/-",
):
    return new_row_base(
        context, action, title, icon_name, target, attrs, tag_class, url
    )


@inclusion_tag("widgets/new_row.html")
def new_row_inline(
    context,
    title="",
    icon_name="",
    target="",
    attrs="",
    tag_class="",
    url="",
    action="new_row-inline/-",
):
    return new_row_base(
        context, action, title, icon_name, target, attrs, tag_class, url
    )


@inclusion_tag("widgets/row_related_list.html")
def row_related_list(
    context,
    table_name,
    title="",
    filter="",
    icon_name="fa fa-lg fa-caret-down",
    target="",
    attrs="",
    tag_class="",
    url="",
    action="field_list",
    app=None,
    version="",
):
    if app:
        table = table_name
    else:
        app, table = table_name.split("/")
    if url and not url.startswith("+"):
        url2 = url
    else:
        if version:
            version = "__" + version
        if filter != "!":
            if filter.startswith("+") or not filter:
                f = "%s__%s__%d" % (
                    context["app_name"],
                    context["table_name"],
                    context["object"].id,
                )
                if filter:
                    filter = f + "__" + filter[1:]
                else:
                    obj = context["object"]
                    if hasattr(obj, "application") and hasattr(obj, "table"):
                        filter = "%s__%s_%s" % (
                            f,
                            obj.application,
                            obj.table,
                        )
                    else:
                        filter = f + "__default"

            url2 = "{bp}" + f"{app}/table/{table}//{filter}/form{version}/sublist/"
        else:
            url2 = (
                "{bp}"
                + f"{app}/table/{table}/{context['object'].id}/-/form{version}/sublist/"
            )
        if url:
            url2 += url[1:]
    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url2)
    return ret


@inclusion_tag("widgets/list_action.html")
def list_action(
    context,
    action,
    title="",
    icon_name="",
    target="_parent",
    attrs="",
    tag_class="",
    url="",
    active=False,
):
    if attrs:
        ret = action_fun(
            context,
            action,
            title,
            icon_name,
            target,
            attrs,
            tag_class,
            url if url else "{tp}action/%s/" % action,
        )
    elif active:
        ret = action_fun(
            context,
            action,
            title,
            icon_name,
            target,
            "data-role='button'",
            "btn btn-light shadow-none no_close no_cancel",
            url if url else "{tp}action/%s/" % action,
        )
    else:
        ret = action_fun(
            context,
            action,
            title,
            icon_name,
            target,
            "data-role='button'",
            "btn btn-light shadow-none no_ok no_cancel",
            url if url else "{tp}action/%s/" % action,
        )
    return ret


@inclusion_tag("widgets/wiki_button.html")
def wiki_button(
    context,
    subject,
    wiki_description,
    icon_name="",
    target="_self",
    attrs="",
    tag_class="",
    url="",
):
    wiki_name = wiki_from_str(wiki_description)
    wiki_url = "/schwiki/%s/%s/view/" % (subject, wiki_name)
    return action_fun(
        context,
        "wiki",
        wiki_description,
        icon_name,
        target,
        attrs,
        tag_class,
        url if url else wiki_url,
    )


@inclusion_tag("widgets/wiki_link.html")
def wiki_link(context, subject, wiki_description, attrs="", target="_self", url=""):
    return wiki_button(context, subject, wiki_description, attrs, target, url)


# form


@inclusion_tag("widgets/field.html")
def field(context, form_field, fieldformat=None, inline=False):
    if type(form_field) in (
        SafeText,
        str,
    ):
        field = context["form"][form_field]
    else:
        field = form_field

    label_class = "control-label float-left"
    offset = ""
    form_group_class = "form-group group_%s" % type(field.field).__name__.lower()
    form_group_size_class = " col-sm-12 col-md-12"
    field_class = "controls float-left %s" % type(field.field).__name__.lower()
    placeholder = ""
    show_label = True

    addon_after = ""
    addon_before = ""
    addon_after_class = ""
    addon_before_class = ""

    ff = None
    if fieldformat:
        ff = fieldformat
    else:
        if "formformat" in context:
            ff = context["formformat"]
        if not ff:
            ff = "12:3:3/12:12:12"
    hidden = False

    if ff == "!":
        hidden = True
    else:
        x = ff.split("/", 2)
        if len(x) < 2:
            return {}

        if x[0] == "^":
            form_group_class += " form-floating"
            field_class += " col-12"
            if not placeholder:
                placeholder = field.label
        elif x[0] == "-":
            form_group_class += " label-over-field"
            field_class += " col-12"
        elif not x[0]:
            placeholder = field.label
            show_label = False
            field_class += " col-12"
        else:
            y = [int(pos) for pos in x[0].split(":")]
            if len(y) == 3:
                label_class += " col-sm-%d col-md-%d col-lg-%d" % (y[0], y[1], y[2])
                field_class += " col-sm-%d col-md-%d col-lg-%d" % (
                    (11 - y[0]) % 12 + 1,
                    (11 - y[1]) % 12 + 1,
                    (11 - y[2]) % 12 + 1,
                )
                offset = " offset-sm-%d offset-md-%d offset-lg-%d" % (
                    y[0] % 12,
                    y[1] % 12,
                    y[2] % 12,
                )
            else:
                label_class += " col-sm-12 col-md-%d" % y[0]
                field_class += " col-sm-12 col-md-%d" % ((11 - y[0]) % 12 + 1)
                offset = "offset-sm-0 offset-md-%d" % (y[0] % 12)

        if not inline:
            form_group_class += " mb-2"

        if x[1]:
            y = x[1].split(":")
            if len(y) == 3:
                form_group_size_class = "col-sm-%s col-md-%s col-lg-%s" % (
                    y[0],
                    y[1],
                    y[2],
                )
            else:
                form_group_size_class = " col-sm-12 col-md-%s" % y[0]
            form_group_class += " " + form_group_size_class

        if len(x) > 2:
            addon = x[2]
            if addon:
                if addon.startswith("(-X)"):
                    addon_after = addon[4:]
                    addon_after_class = "input-group-btn"
                elif addon.startswith("(X-)"):
                    addon_before = addon[4:]
                    addon_before_class = "input-group-btn"
                elif addon.startswith("(-x)"):
                    addon_after = addon[4:]
                    addon_after_class = "input-group-addon"
                elif addon.startswith("(x-)"):
                    addon_before = addon[4:]
                    addon_before_class = "input-group-addon"

        if offset and type(field.field.widget) in (
            CheckboxInput,
            RadioSelect,
            CheckboxSelectMultiple,
            FileInput,
        ):
            field_class += " " + offset

        # if type(field.field.widget) in (CheckboxInput, RadioSelect, CheckboxSelectMultiple):
        #    field.field.widget.attrs["class"] = 'custom-control-input'

    ret = {}
    ret["form"] = context["form"]
    ret["field"] = field
    ret["hidden"] = hidden
    ret["label_class"] = label_class
    ret["form_group_class"] = form_group_class
    ret["form_group_size_class"] = form_group_size_class
    ret["field_class"] = field_class
    ret["placeholder"] = placeholder
    ret["addon_after"] = addon_after
    ret["addon_after_class"] = addon_after_class
    ret["addon_before"] = addon_before
    ret["addon_before_class"] = addon_before_class
    ret["show_label"] = show_label
    ret["standard_web_browser"] = context["standard_web_browser"]
    ret["server_side_validation"] = (
        False
        if "server_side_validation" in context
        and context["server_side_validation"] == False
        else True
    )
    return ret


class Form(Node):
    def __init__(self, nodelist, def_param, param, inline=False):
        self.nodelist = nodelist
        self.def_param = def_param
        self.param = []
        if inline:
            self.inline = 1
        else:
            self.inline = 0
        for pos in param:
            self.param.append(template.Variable(pos))

    def render(self, context):
        output = self.nodelist.render(context).strip()

        form = context["form"]
        fields = []
        if output:
            if "((" in output:
                output_tab = []
                x = output.split("((")
                if x[0]:
                    value = x[0].strip().replace('"', "'").replace(";", "','")
                    if value:
                        output_tab.append(value)
                for item in x[1:]:
                    y = item.split("))")
                    output_tab.append("@" + y[0])
                    if len(y) > 1 and y[1]:
                        value = y[1].strip().replace('"', "'").replace(";", "','")
                        if value:
                            output_tab.append(value)
            else:
                output_tab = (output.replace('"', "'").replace(";", "','"),)

            for item in output_tab:
                if item.startswith("@"):
                    fields.append(item[1:])
                else:
                    for f in item.split(","):
                        x = f.split(":", 1)
                        name = x[0].replace("'", "").strip()
                        if len(x) > 1:
                            p = x[1]
                        elif len(self.param) > 1:
                            p = self.param[1].resolve(context)
                        else:
                            p = self.def_param
                        fields.append([name, p])
        else:
            for field in form:
                if len(self.param) > 1:
                    p = self.param[1].resolve(context)
                else:
                    p = self.def_param
                fields.append([field.name, p])
        if self.def_param == "^/":
            template_str = "{% load exsyntax %}<div class='d-inline-flex flex-wrap'>"
        else:
            template_str = "{% load exsyntax %}<div class='row'>"
        for field in fields:
            if type(field) == str:
                template_str += field
            else:
                template_str += "{%% field '%s' '%s' %d %%}" % (
                    field[0],
                    field[1],
                    self.inline,
                )
        template_str += "</div>"
        t = Template(template_str)
        return t.render(context)


@register.tag
def form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(("endform"))
    parser.delete_first_token()
    return Form(nodelist, "12:3:3/12:12:12", parm)


@register.tag
def vert_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(("endvert_form",))
    parser.delete_first_token()
    return Form(nodelist, "^/12", parm)


@register.tag
def inline_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(("endinline_form",))
    parser.delete_first_token()
    return Form(nodelist, "^/", parm, inline=True)


@register.tag
def col2_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(("endcol2_form",))
    parser.delete_first_token()
    return Form(nodelist, "^/12:6:6", parm)


class FormItemNode(Node):
    def __init__(self, nodelist, field_name, tag):
        self.nodelist = nodelist
        self.field_name = field_name
        self.tag = tag

    def render(self, context):
        x = self.nodelist.render(context)
        if "|" in x:
            pos = x.find("|")
            title = x[:pos].strip()
            content = x[pos + 1 :]
        else:
            title = context["form"][self.field_name].label
            content = x

        if not content:
            content = str(context["form"][self.field_name])

        if self.tag:
            elem0 = """ <%s class="%s form-control" name="%s" id="id_%s"> """ % (
                self.tag,
                self.field_name,
                self.field_name,
                self.field_name,
            )
            elem1 = "</%s>" % self.tag
        else:
            elem0 = ""
            elem1 = ""

        ret = """
            <div id="div_id_%s" class="form-group">
                <label for="id_%s" class="control-label">%s</label>
                <div class="controls">%s%s%s</div>
            </div>
        """ % (
            self.field_name,
            self.field_name,
            title,
            elem0,
            content,
            elem1,
        )

        return ret


@register.tag
def form_item(parser, token):
    field_name = token.contents[10:]
    tag = None
    if "." in field_name:
        tmp = field_name.split(".")
        tag = tmp[1]
        field_name = tmp[0]
    nodelist = parser.parse(("endform_item",))
    parser.delete_first_token()
    return FormItemNode(nodelist, field_name, tag)


# @inclusion_tag('widgets/form2columns.html')
# def form2columns(context, fields):
#    ftab = fields.split(';')
#    it = iter(ftab)
#    fields2 = itertools.zip_longest(it,it)
#    return standard_dict(context, {'fields': ftab, 'fields2': fields2, 'form': context['form']})


@inclusion_tag("widgets/get_table_row.html")
def get_table_row(
    context,
    field_or_name,
    app_name=None,
    table_name=None,
    search_fields=None,
    filter=None,
    label=None,
    initial=None,
    is_get_button=True,
    is_new_button=False,
    get_target="popup_edit",
    new_target="inline",
):
    if type(field_or_name) in (
        SafeText,
        str,
    ):
        model = import_model(app_name, table_name)
        _name = field_or_name
        _app_name = app_name
        _table_name = table_name
        _initial = initial
        _label = label if label else table_name
        _queryset = None
        _search_fields = search_fields
    else:
        _queryset = field_or_name.field.queryset
        model = _queryset.model
        _name = field_or_name.name
        _app_name = app_name if app_name else _queryset.model._meta.app_label
        _table_name = table_name if table_name else _queryset.model._meta.object_name
        _initial = initial if initial else field_or_name.initial
        _label = label if label else field_or_name.label
        if search_fields:
            _search_fields = search_fields
        else:
            if hasattr(field_or_name, "search_fields"):
                _search_fields = field_or_name.search_fields
            else:
                _search_fields = "name__icontains"

    if "formformat" in context:
        formformat = context["formformat"]
    else:
        formformat = "12:3:3/12:12:12"

    if TreeModel in model.__bases__:
        if filter:
            href1 = make_href(
                "/%s/table/%s/%s/0/form/gettree/" % (_app_name, _table_name, filter)
            )
            href2 = make_href("/%s/table/%s/-/add/" % (_app_name, _table_name))
        else:
            href1 = make_href("/%s/table/%s/0/form/gettree/" % (_app_name, _table_name))
            href2 = make_href("/%s/table/%s/-/add/" % (_app_name, _table_name))
    else:
        _filter = filter if filter else "-"
        href1 = make_href(
            "/%s/table/%s/%s/form/get/" % (_app_name, _table_name, _filter)
        )
        href2 = make_href("/%s/table/%s/%s/add/" % (_app_name, _table_name, _filter))

    class _Form(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields[_name] = forms.ChoiceField(
                widget=s2forms.ModelSelect2Widget(
                    model=model,
                    search_fields=[
                        _search_fields,
                    ],
                    queryset=_queryset,
                    attrs={"href1": href1, "href2": href2},
                ),
            )

    form = _Form(initial={_name: _initial})
    return {
        "form": form,
        "field": form[_name],
        "formformat": formformat,
        "href1": href1,
        "href2": href2,
    }


##  include


@inclusion_tag("widgets/frame.html")
def frame(context, href, height):
    return standard_dict(context, {"href": href, "height": height})


@inclusion_tag("widgets/subform.html")
def subform(context, name):
    return standard_dict(
        context,
        {
            "href": name,
        },
    )


@inclusion_tag("widgets/require.html")
def require(context, href):
    return {"href": mark_safe(href)}


@inclusion_tag("widgets/module_link.html")
def module_link(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, "rt", encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except:
            print("file: ", href, "does'nt exists")
        return {"href": mark_safe(href), "content": mark_safe(content)}
    else:
        return {"href": mark_safe(href), "content": None}


@inclusion_tag("widgets/jscript_link.html")
def jscript_link(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, "rt", encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except:
            print("file: ", href, "does'nt exists")
        return {"href": mark_safe(href), "content": mark_safe(content)}
    else:
        return {"href": mark_safe(href), "content": None}


@inclusion_tag("widgets/css_link.html")
def css_link(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, "rt", encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except:
            print("file: ", href, "does'nt exists")
        return standard_dict(context, {"href": href, "content": mark_safe(content)})
    else:
        return standard_dict(context, {"href": href, "content": None})


@inclusion_tag("widgets/link.html")
def link(context, href, rel, typ):
    return standard_dict(
        context,
        {"href": settings.STATIC_URL + href, "rel": rel, "typ": typ, "content": None},
    )


@inclusion_tag("widgets/jscript.html")
def jscript(context, href):
    content_path = os.path.join(settings.STATIC_ROOT, href)
    content = ""
    with open(content_path, "rt", encoding="utf-8") as f:
        content = f.read()
    return {"content": mark_safe(content)}


@inclusion_tag("widgets/component.html")
def component(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, "rt", encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except:
            print("file: ", href, "does'nt exists")
        return {"href": mark_safe(href), "content": mark_safe(content)}
    else:
        return {"href": mark_safe(href), "content": None}

    # return standard_dict(
    #    context,
    #    {
    #        "href": href,
    #    },
    # )


# other tags


@register.simple_tag
def spec(format):
    return (
        format.replace("{", "{{")
        .replace("}", "}}")
        .replace("[", "{%")
        .replace("]", "%}")
    )


@register.simple_tag(takes_context=True)
def include_wiki(context, wiki_str, from_wiki_page, path=None, only_header=True):
    ret = ""
    if "request" in context:
        username = context["request"].user.username
    subpage = from_wiki_page.get_page_for_wiki(wiki_str, username)
    if subpage and subpage.content:
        if only_header:
            content = subpage.content.split("<div class='read_more'")[0]
        else:
            content = subpage.content

        ret += (
            "<div class='article-header'><div class='article-header-title'>"
            + subpage.get_href(path)
            + "</div>"
            + content
            + "</div>\n"
        )
    else:
        ret = wikify("[[" + wiki_str + "]]", path, from_wiki_page.subject)
    return mark_safe(ret)


@register.simple_tag(takes_context=True)
def markdown2html(context, markdown_str, path=None, section=None):
    return mark_safe(wikify(markdown_str, path, section))


@register.simple_tag(takes_context=True)
def subtemplate(context, template_string):
    t = Template(template_string)
    return mark_safe(t.render(context))


def editable_base(context, name, title, url):
    if ":" in name:
        field_name, t = name.split(":")
    else:
        field_name = name
        t = "text"
    date_str = ""
    if "date" in t:
        t = "combodate"
        date_str = """ data-format="YYYY-MM-DD" data-viewformat="YYYY-MM-DD" data-template="YYYY-MM-DD" """
    if title:
        t2 = title
    else:
        t2 = ""
    oid = getattr(context["object"], "id")
    value = getattr(context["object"], field_name)
    return f"<a class='editable autoopen' data-name='{field_name}' data-type='{t}' data-pk='{oid}' data-url='{url.format(**locals())}' data-title='{t2}' href='#' {date_str}> {value} </a>"


@register.simple_tag(takes_context=True)
def editable(context, name, title="", url=None):
    if url and not url.startswith("+"):
        url2 = url
    else:
        url2 = "../../../{oid}/{field_name}/editable/editor/"
        if url:
            url2 += url[1:]

    return mark_safe(editable_base(context, name, title, url2))


@register.simple_tag(takes_context=True)
def td_editable(context, name, title=""):
    if context["standard_web_browser"]:
        url = context["table_path"] + "{oid}/{field_name}/editable/editor/"
        return mark_safe("<td>%s</td>" % editable_base(context, name, title, url))
    else:
        ret = "<td>%s</td>" % getattr(context["object"], name)
        return mark_safe(ret)


@inclusion_tag("widgets/svg_standard_style.html")
def svg_standard_style(
    context,
):
    return {}


@register.simple_tag(takes_context=True)
def id_num(context, name, sorting=False):
    if not context["standard_web_browser"] or (
        "doc_type" in context and context["doc_type"] == "json"
    ):
        if "paginator" in context:
            return (
                name
                + ":"
                + str(context["paginator"].per_page)
                + "/"
                + str(context["paginator"].count)
            )
    if sorting or ("sort" in context and context["sort"]):
        return sorted_column(context, "id", name)
    else:
        return name


@inclusion_tag("widgets/ok_cancel.html")
def ok_cancel(context):
    return standard_dict(context, {})


@inclusion_tag("widgets/paginator.html")
def paginator(context):
    return context.flatten()


@inclusion_tag("widgets/sorted_column.html")
def sorted_column(context, name, description):
    ret = standard_dict(context, {})
    ret["column_name"] = name
    ret["column_description"] = description
    return ret


class ComboSelect(Node):
    def __init__(self, nodelist, field_or_field_name, param):
        self.nodelist = nodelist
        self.field_or_field_name = field_or_field_name
        self.param = param

    def render(self, context):
        output = self.nodelist.render(context).strip()
        field_or_field_name = template.Variable(self.field_or_field_name).resolve(
            context
        )
        label = ""
        if type(field_or_field_name) in (str, SafeString):
            name = field_or_field_name
        else:
            name = field_or_field_name.name
            label = field_or_field_name.label

        values = dict([(key, val.resolve(context)) for key, val in self.param.items()])
        if "label" in values:
            label = values["label"]
        else:
            if not label:
                label = name
        if "data_rel_name" in values:
            data_rel_name = values["data_rel_name"]
        else:
            data_rel_name = ""
        if "src" in values:
            src = values["src"]
        else:
            src = ""

        template_str = """
            {%% load exsyntax %%}
            <div class="form-group group_choicefield form-floating">
                <select class="select_combo form-select" name="%s" data-rel-name="%s" src="%s">
                        <option disabled selected value />
                        %s 
                </select>
                <label class="form-label control-label float-left">
                    %s
                </label>
            </div>
        """ % (
            name,
            data_rel_name,
            src,
            output,
            label,
        )
        t = Template(template_str)
        return t.render(context)


@register.tag
def comboselect(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[2:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    parm = token.split_contents()
    nodelist = parser.parse(("endcomboselect"))
    parser.delete_first_token()
    return ComboSelect(nodelist, bits[1], extra_context)


# @inclusion_tag('widgets/paginator.html')
# def paginator2(context):
#    context['page_range'] = []

#    if 'paginator' in context and 'page_obj' in context:
#        if context['paginator'].page_range[-1] > 15:
#            nr = context['page_obj'].number
#            start = nr - 5
#            end = nr + 5
#            if start < 0:
#                end += -1 * start
#                start = 0
#            if end > context['paginator'].page_range[-1]:
#                start -= end - context['paginator'].page_range[-1]
#                end = context['paginator'].page_range[-1]
#
#            context['page_range'] = context['paginator'].page_range[start + 1:end - 1]
#            context['page_all'] = False
#        else:
#            context['page_range'] = context['paginator'].page_range
#            context['page_all'] = True
#
#        context['page_last'] = context['paginator'].page_range[-1]
#        context['page_number'] = context['page_obj'].number
#    return context.flatten()


# @inclusion_tag('widgets/checkboxselectmultiple.html')
# def checkboxselectmultiple(context, field, only_field=False):
#    field.field.widget = CheckboxSelectMultiple(choices=field.field.choices)
#    field.field.widget.attrs['class'] = "list-group row"
#    return standard_dict(context, {'field': field, 'only_field': only_field})


class HtmlWidgetNode(template.Node):
    def __init__(self, template_name, var, name, nodelist, extra_context=None):
        self.nodelist = nodelist
        self.template_name = template_name
        self.extra_context = extra_context or {}
        if name:
            self.extra_context[name] = var

    def __repr__(self):
        return "<HtmlWidgetNode>"

    def render(self, context):
        values = dict(
            [(key, val.resolve(context)) for key, val in self.extra_context.items()]
        )

        context.update(values)

        data = self.nodelist.render(context)
        data = (
            data.replace("[%]", "%")
            .replace("[{", "{{")
            .replace("}]", "}}")
            .replace("[%", "{%")
            .replace("%]", "%}")
        )
        id = context["id"]
        class_name = context["class"]

        context["template_name"] = "widgets/html_widgets/" + class_name + ".html"
        def_param = ""
        if "width" in context:
            def_param = def_param + "width='%s' " % context["width"]
            try:
                context["width"] = int(context["width"]) - 10
            except:
                pass
        if "height" in context:
            def_param = def_param + "height='%s' " % context["height"]
            try:
                context["height"] = int(context["height"]) - 10
            except:
                pass
        context["def_param"] = def_param

        t = Template(data)
        tdata = t.render(context)

        template = get_template(self.template_name)

        context_dict = {}
        for c in context.dicts:
            context_dict.update(c)
        context_dict["data"] = tdata

        # tdata = t.render(context_dict)

        # output = template.render(context)
        output = template.render(context_dict)

        context.pop()

        return mark_safe(output)


@register.tag("widget")
def do_html_widget(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError(
            "%r expected at least one variable assignment" % bits[0]
        )
    if not "id" in extra_context or not "class" in extra_context:
        raise TemplateSyntaxError("id and class parameters are required")
    if remaining_bits:
        raise TemplateSyntaxError(
            "%r received an invalid token: %r" % (bits[0], remaining_bits[0])
        )
    nodelist = parser.parse(("endwidget",))
    parser.delete_first_token()
    return HtmlWidgetNode(
        "widgets/widget.html", None, None, nodelist, extra_context=extra_context
    )


ICON_CACHE = {}


def _read_icon_file(path):
    tmp = None
    path_tab = path.split("/")
    with open(os.path.join(settings.STATIC_ROOT, *path_tab), "rt") as f:
        tmp = f.read()
    return tmp


def _read_user_icon_file(path):
    tmp = None
    path_tab = path.split("/")
    with open(os.path.join(settings.MEDIA_ROOT, *path_tab), "rt") as f:
        tmp = f.read()
    return tmp


def _to_b64(href):
    content_path = os.path.join(settings.STATIC_ROOT, href)
    bcontent = ""
    try:
        with open(content_path, "rb") as f:
            content = f.read()
            bcontent = b64encode(content).decode("utf-8")
    except:
        print("file: ", content_path, "does'nt exists")
    return bcontent


@register.simple_tag(takes_context=False)
def to_b64(href):
    return _to_b64(href)


@register.simple_tag(takes_context=True)
def icon(context, class_str, width=None, height=None):
    global ICON_CACHE

    if class_str.startswith("fa://"):
        return mark_safe(
            "<i class='fa fa-%s'></i>" % (class_str[5:].replace(".png", ""))
        )
    elif class_str.startswith("fa-"):
        return mark_safe("<i class='fa %s'></i>" % class_str)
    elif class_str.startswith("bi-"):
        x = re.findall("bi-" + r"[\w-]+", class_str)
        if x:
            icon_name = x[0].replace("bi-", "")
            if not icon_name in ICON_CACHE:
                tmp = _read_icon_file(
                    "icons/bootstrap-icons/" + icon_name.replace("--", "/") + ".svg"
                )
                if tmp:
                    ICON_CACHE[icon_name] = tmp
                else:
                    return mark_safe("<i></i>")
            icon = ICON_CACHE[icon_name]
            if width:
                icon = icon.replace('width="16"', ('width="%d"' % width)).replace(
                    'height="16"', 'height="%d"' % (height if height else width)
                )
            return mark_safe("<i>%s</i>" % icon)
    elif class_str.startswith("icon-"):
        x = re.findall("icon-" + r"[\w-]+", class_str)
        if x:
            icon_name = x[0].replace("icon-", "")
            if not icon_name in ICON_CACHE:
                tmp = _read_user_icon_file(
                    "icons/" + icon_name.replace("--", "/") + ".svg"
                )
                if tmp:
                    ICON_CACHE[icon_name] = tmp
                else:
                    return mark_safe("<i></i>")
            icon = ICON_CACHE[icon_name]
            return mark_safe("<i>%s</i>" % icon)
    elif class_str.startswith("svg-"):
        x = re.findall("svg-" + r"[\w-]+", class_str)
        if x:
            icon_name = x[0].replace("svg-", "")
            if not icon_name in ICON_CACHE:
                tmp = _read_icon_file(
                    "icons/scalable/" + icon_name.replace("--", "/") + ".svg"
                )
                if tmp:
                    ICON_CACHE[icon_name] = tmp
                else:
                    return mark_safe("<i></i>")
            icon = ICON_CACHE[icon_name]
            return mark_safe("<i>%s</i>" % icon)
    elif class_str.startswith("png://"):
        x = class_str[6:]
        x2 = x.split(" ", 1)
        src = mhref("/static/icons/22x22/%s" % x2[0])
        if "user_agent" in context and context["user_agent"] == "webviewembeded":
            bcontent = _to_b64(src[8:])
            if len(x2) > 1:
                return mark_safe(
                    "<img src='data:image/png;base64, %s' class='%s'></img>"
                    % (bcontent, x2[1])
                )
            else:
                return mark_safe(
                    "<img src='data:image/png;base64, %s'></img>" % bcontent
                )
        else:
            if len(x2) > 1:
                return mark_safe("<img src='%s' class='%s'></img>" % (src, x2[1]))
            else:
                return mark_safe("<img src='%s'></img>" % src)
    elif class_str.startswith("client://"):
        x = class_str[9:]
        x2 = x.split(" ", 1)
        src = mhref("/static/icons/22x22/%s" % x2[0])
        if "user_agent" in context and context["user_agent"] == "webviewembeded":
            ext = src[8:].split(".")[-1]
            bcontent = _to_b64(src[8:])
            if len(x2) > 1:
                return mark_safe(
                    "<img src='data:image/%s;base64, %s' class='%s'></img>"
                    % (ext, bcontent, x2[1])
                )
            else:
                return mark_safe(
                    "<img src='data:image/%s;base64, %s'></img>" % (ext, bcontent)
                )
        else:
            if len(x2) > 1:
                return mark_safe("<img src='%s' class='%s'></img>" % (src, x2[1]))
            else:
                return mark_safe("<img src='%s'></img>" % src)

    elif class_str.startswith("data:image/svg+xml"):
        x = class_str.split(",", 1)
        svg_code = x[1]
        return mark_safe(svg_code)
    elif "fa-" in class_str:
        return mark_safe("<i class='fa %s'></i>" % class_str)
    else:
        return mark_safe("<i class='fa fa-arrow-circle-right fa-lg'></i>")


class TemplateNameNode(Node):
    def __init__(self, template_name):
        self.name = template_name

    def render(self, context):
        return self.name


@register.tag
def show_template_name(parser, token):
    return TemplateNameNode(parser.template_name)


class TreeNode(Node):
    def __init__(self, nodelist, param):
        self.nodelist = nodelist
        self.tree = param

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def render(self, context):
        if "tree_template" in context:
            nodelist = context["tree_template"]
        else:
            nodelist = self.nodelist

        tree = self.tree.resolve(context)

        if type(tree) == list:
            with context.push(
                {
                    "tree_element": "element_list",
                    "element_list": tree,
                    "tree_template": nodelist,
                }
            ):
                return nodelist.render(context)
        elif type(tree) == dict:
            with context.push(
                {
                    "tree_element": "element",
                    "element": tree,
                    "tree_template": nodelist,
                }
            ):
                return nodelist.render(context)
        else:
            with context.push(
                {
                    "tree_element": "object",
                    "object": tree,
                    "tree_template": nodelist,
                }
            ):
                return nodelist.render(context)


@register.tag("tree")
def do_tree(parser, token):
    """
    {% tree treelist %}
        html
    {% endtree %}

    """
    parm = token.split_contents()
    nodelist = parser.parse(("endtree"))
    parser.delete_first_token()
    return TreeNode(nodelist, parser.compile_filter(parm[1]))


class RowDetailsNode(Node):
    def __init__(self, nodelist, vertical=False):
        self.nodelist = nodelist
        self.vertical = vertical

    def render(self, context):
        output = self.nodelist.render(context).replace("\n", ";")
        title_url_tab = []
        test = False
        for item in output.split(";"):
            item = item.strip()
            if ":" in item:
                title, url = item.split(":", 1)
                default = False
                perm = None
                if title.startswith("*"):
                    title = title[1:]
                    default = True
                if title.startswith("(") and ")" in title:
                    perm, title = title.split(")", 1)
                    perm = perm[1:]

                if perm == None or (
                    "perms" in context
                    and hasattr(context["perms"], "user")
                    and context["perms"].user.has_perm(perm)
                ):
                    if default and not test:
                        title_url_tab.append([title, url, True])
                        test = True
                    else:
                        title_url_tab.append([title, url, False])

        if not test and len(title_url_tab) > 0:
            title_url_tab[0][2] = True

        t = get_template("widgets/row_details.html")

        d = {}
        d.update(context.flatten())
        d["title_url_tab"] = title_url_tab
        if self.vertical:
            d["vertical"] = True
        else:
            d["vertical"] = False
        return t.render(d, request=d["request"])


@register.tag
def row_details(parser, token):
    nodelist = parser.parse(("endrow_details",))
    parser.delete_first_token()
    return RowDetailsNode(nodelist, False)


@register.tag
def v_row_details(parser, token):
    nodelist = parser.parse(("endv_row_details",))
    parser.delete_first_token()
    return RowDetailsNode(nodelist, True)


class ModifyNode(Node):
    def __init__(self, nodelist, arg):
        self.nodelist = nodelist
        self.arg = arg
        print("=================================")
        for key, value in self.arg.items():
            print(key, str(value))
        print("=================================")

    def render(self, context):
        data = self.nodelist.render(context)
        d = pq(data)
        for key, v in self.arg.items():
            value = str(v)[1:-1]
            if key == "addclass":
                for item in value.split(";"):
                    if item:
                        x = item.split("=", 1)
                        p = d(x[0])
                        p.addClass(x[1])
            elif key == "removeclass":
                for item in value.split(";"):
                    if item:
                        x = item.split("=", 1)
                        p = d(x[0])
                        p.removeClass(x[1])
            elif key == "setattr":
                for item in value.split(";"):
                    if item:
                        x = item.split("=", 1)
                        xx = x[0].split(":", 1)
                        p = d(xx[0])
                        p.attr(xx[1], x[1])
            elif key == "remove":
                for item in value.split(";"):
                    if item:
                        d.remove(item)

        txt = d.html()

        for key, v in self.arg.items():
            value = str(v)[1:-1]
            if key == "replace":
                for item in value.split(";"):
                    if item:
                        x = split("/", 1)
                        txt = txt.replace(x[0], x[1])

        return d.html()


@register.tag
def modify(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    arg = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not arg:
        raise TemplateSyntaxError(
            "%r expected at least one variable assignment" % bits[0]
        )
    if remaining_bits:
        raise TemplateSyntaxError(
            "%r received an invalid token: %r" % (bits[0], remaining_bits[0])
        )
    nodelist = parser.parse(("endmodify",))
    parser.delete_first_token()
    return ModifyNode(nodelist, arg=arg)


@register.simple_tag(takes_context=True)
def show_context(context):
    return str(context)
