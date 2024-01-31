#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

"""Standard python template filters

"""

from base64 import b64encode, b64decode
import datetime
import importlib
import uuid

from django import template
from django.urls import reverse
from django.db.models import Count, Max, Min, Sum, Avg

import markdown


from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schtools.wiki import wiki_from_str, make_href, wikify
from pytigon_lib.schtools.schjson import json_dumps


from django_bootstrap5.forms import render_form

register = template.Library()


# tools


@register.filter(name="class_name")
def class_name(value):
    """Returns class name of value"""
    ret = ""
    try:
        ret = value.__class__.__name__
    except:
        pass
    return ret


@register.filter(name="to_console")
def to_console(value):
    """Returns class name of value"""
    print(value)
    return ""


@register.filter(name="is_private")
def is_private(value):
    """Check if function is private"""
    return value.startswith("_")


@register.filter(name="get_value")
def getvalue(value, argv):
    """Returns value[argv]"""
    return value[argv]


@register.filter(name="get_attr")
def get_attr(value, attr):
    """Returns getattr(value, attr)"""
    try:
        obj = getattr(value, attr)
    except:
        obj = None
    return obj


@register.filter(name="range")
def _range(value):
    """Returns list(range(int(value)))"""
    return list(range(int(value)))


@register.filter(name="dir")
def f_dir(value):
    """Returns dir(value)"""
    return dir(value)


@register.filter(name="split")
def filter_split(obj, sep=";"):
    "split obj and return result"
    return obj.split(sep)


@register.filter(name="feval")
def _eval(value):
    """Returns eval(value)"""
    return eval(value)


@register.filter(name="left")
def left(value, arg):
    return str(value)[: int(arg)]


@register.filter(name="truncate")
def truncate(value, arg):
    """truncate result"""
    try:
        retstr = str(value)
    except:
        retstr = unicode(value)

    if len(retstr) > int(arg):
        return retstr[: int(arg) - 3] + "..."
    else:
        return retstr


@register.filter(name="first_elem")
def first_elem(value, sep="/"):
    """split value and return first element"""
    return value.split(sep)[0]


@register.filter(name="last_elem")
def last_elem(value, sep="/"):
    """split value and return last element"""
    return value.split(sep)[-1]


@register.filter(name="penultimate_elem")
def penultimate_elem(value, sep="/"):
    """split value and return penultimate element"""
    x = value.split(sep)
    if len(x) > 1:
        return x[-2]
    else:
        return ""


@register.filter(name="first_section")
def first_section(html):
    """part of string before $$$"""
    if html:
        return html.split("$$$")[0]
    else:
        return ""


@register.filter(name="second_section")
def second_section(html):
    """part of string after $$$"""
    if html:
        x = html.split("$$$")
        if len(x) > 1:
            return x[1]
        else:
            return ""
    else:
        return ""


@register.filter(name="replace")
def replace(value, replace_str):
    """replace_str: 'old_value|new_value'"""
    l = replace_str.split("|")
    if len(l) == 2:
        value2 = value.replace(l[0], l[1])
        return value2
    else:
        return value


@register.filter(name="nbsp")
def nbsp(value):
    """replace_str: 'old_value|new_value'"""
    return value.replace(" ", "&nbsp;")


@register.filter(name="hasattr")
def filter_hasattr(obj, attr_name):
    return hasattr(obj, attr_name)


@register.filter(name="has_ext")
def has_ext(value, arg):
    if value.lower().endswith(arg.lower()):
        return True
    else:
        return False


@register.filter(name="append_get_param")
def append_get_param(href, parm):
    if "?" in href:
        return href + "&" + str(parm)
    else:
        return href + "?" + str(parm)


@register.filter(name="call")
def _call(obj, methodName):
    if hasattr(obj, methodName):
        method = getattr(obj, methodName)
        if hasattr(obj, "__callArg"):
            param = obj.__callArg
            del obj.__callArg
            return method(*param)
        return method()
    return ""


@register.filter(name="args")
def args(obj, arg):
    if not hasattr(obj, "__callArg"):
        obj.__callArg = []
    obj.__callArg += [arg]
    return obj


@register.filter(name="call_with")
def call_with(proxy, arg):
    return proxy.call(arg)


# conversion functions
@register.filter(name="bencode")
def bencode(value):
    """Returns b64encode(value)"""

    if value:
        return b64encode(value.encode("utf-8")).decode("utf-8")
    else:
        return b64encode(b"").decode("utf-8")


@register.filter(name="bdecode")
def bdecode(value):
    """Returns b64decode(value)"""

    return b64decode(value.encode("utf-8")).decode("utf-8")


@register.filter(name="to_str")
def to_str(value):
    """Converts value to str"""
    try:
        ret = str(value)
    except:
        ret = ""
    return ret


@register.filter(name="none_to_empty")
def none_to_empty(value):
    """Converts value to str, None to ''"""
    if value:
        try:
            ret = str(value)
        except:
            ret = ""
    else:
        ret = ""
    return ret


@register.filter(name="to_int")
def to_int(value):
    try:
        ret = int(value)
    except:
        ret = 0
    return ret


@register.filter(name="to_float")
def to_float(value):
    try:
        ret = float(value)
    except:
        ret = 0.0
    return ret


@register.filter(name="num2str")
def num2str(value):
    buf = str(value)
    return buf.replace(",", ".").replace(" ", "")


@register.filter(name="format")
def format(value, id):
    return value % id


@register.filter(name="genericfloatformat")
def genericfloatformat(text, arg="{: .2f}"):
    space_convert = False
    try:
        f = float(text)
        if ": " in arg:
            space_convert = True
            arg2 = arg.replace(": ", ":,")
        else:
            arg2 = arg
        x = arg2.format(f)
        if space_convert:
            return x.replace(",", " ")
        else:
            return ""
    except ValueError:
        return ""


@register.filter(name="genericfloatnullformat")
def genericfloatnullformat(text, arg="{: .2f}"):
    try:
        f = float(text)
        if not f:
            return "-"
        else:
            return genericfloatformat(text, arg)
    except:
        return "-"


@register.filter(name="floatformat2")
def floatformat2(text):
    return genericfloatformat(text, "{: .2f}")


@register.filter(name="floatformat3")
def floatformat3(text):
    return genericfloatformat(text, "{: .3f}")


@register.filter(name="floatnullformat")
def floatnullformat(text):
    return genericfloatnullformat(text, "{: .2f}")


@register.filter(name="floatnullformat3")
def floatnullformat3(text):
    return genericfloatnullformat(text, "{: .3f}")


@register.filter(name="amount")
def amount(text):
    try:
        f = float(text)
    except ValueError:
        return ""
    if f == 0.0:
        return "-  "

    def split_len(seq, length):
        return [seq[i : i + length] for i in range(0, len(seq), length)]

    s = "%.02f" % f
    t = s.split(".")
    return " ".join(split_len(t[0][::-1], 3))[::-1] + "." + t[1]


@register.filter(name="isoformat")
def isoformat(value):
    if value:
        try:
            iso = value.isoformat()[:19].replace("T", " ")
            return iso
        except:
            return value
    else:
        return ""


@register.filter(name="sysisoformat")
def sysisoformat(value):
    if value:
        try:
            if type(value) == str:
                x = value[:10].replace("-", " ").replace(".", " ").split(" ")
                if len(x[0]) == 4:
                    x2 = value[:10]
                elif len(x[2]) == 4:
                    x2 = x[2] + "-" + x[1] + "-" + x[0]
                else:
                    x2 = value[:10]
                iso = x2 + value[10:].replace(" ", "T")
            else:
                value2 = value
                iso = value2.isoformat()[:19].replace(" ", "T")
            return iso
        except:
            return value.replace(" ", "T")
    else:
        return ""


@register.filter(name="isoformat_short")
def isoformat_short(value):
    if value:
        iso = value.isoformat()[:16].replace("T", " ")
        return iso
    else:
        return ""


@register.filter(name="d_isoformat")
def d_isoformat(value):
    if value:
        iso = value.isoformat()[:10]
        return iso
    else:
        return ""


@register.filter(name="one_line_block")
def one_line_block(value):
    """Clean value by removing unnecessary spaces and characters: '\n', '\t'"""
    return (
        value.replace("        ", " ")
        .replace("    ", " ")
        .replace("  ", " ")
        .replace("\n", "")
        .replace("\t", "")
    )


@register.filter(name="one_line_code")
def one_line_code(value):
    """Clean value by removing unnecessary spaces and characters: '\n', '\t'"""
    return value.replace("\n", "").replace("\r", "").replace("\t", "")


@register.filter(name="clean")
def clean(value):
    return " ".join(value.replace("\n", "").replace("\t", "").split())


# + - / *


@register.filter(name="fadd")
def fadd(value, arg):
    """Returns int(value) - int(arg)"""
    return float(value) + float(arg)


@register.filter(name="subtract")
def subtract(value, arg):
    """Returns int(value) - int(arg)"""
    return int(value) - int(arg)


@register.filter(name="fsubtract")
def fsubtract(value, arg):
    """Returns int(value) - int(arg)"""
    return float(value) - float(arg)


@register.filter(name="multiply")
def multiply(value, arg):
    """Returns int(value) * int(arg)"""
    return int(value) * int(arg)


@register.filter(name="fmultiply")
def fmultiply(value, arg):
    """return fvalue * float"""
    try:
        ret = float(value) * float(arg)
    except:
        ret = ""
    return ret


@register.filter(name="divide")
def divide(value, arg):
    """Return int(value) / int(arg)"""
    return int(value) / int(arg)


@register.filter(name="fdivide")
def fdivide(value, arg):
    """Returns float(value) / float(arg)"""
    if float(arg) != 0:
        return float(value) / float(arg)
    else:
        return ""


@register.filter(name="append_str")
def append_str(value, s):
    if s == None or s == "":
        return value
    else:
        return value + str(s)


@register.filter(name="date_inc")
def date_inc(value, arg):
    """Increment date value by timedelta(int(arg))"""
    try:
        (date, time) = value.split()
        (y, m, d) = date.split("-")
        return datetime.datetime(int(y), int(m), int(d)) + datetime.timedelta(int(arg))
    except ValueError:
        return None


@register.filter(name="date_dec")
def date_dec(value, arg):
    """Decrement date value by timedelta(int(arg))"""
    try:
        (y, m, d) = value.split("-")
        return (
            datetime.datetime(int(y), int(m), int(d)) - datetime.timedelta(int(arg))
        ).date()
    except ValueError:
        return None


# models and fields


@register.filter(name="get_model_fields")
def get_model_fields(value):
    """Returns fields for model (value) without many_to_many fields"""
    ret = []
    if value and hasattr(value, "_meta"):
        for f in value._meta.fields:
            if f.name == "id":
                ret.insert(0, f)
            else:
                ret.append(f)
    return ret


@register.filter(name="get_model_meta")
def get_model_meta(value):
    """Returns model _meta"""
    ret = []
    if value and hasattr(value, "_meta"):
        return value._meta
    return None


@register.filter(name="get_model_app")
def get_model_app(value):
    """Returns model app"""
    ret = []
    if value and hasattr(value, "_meta"):
        return value._meta.app_label
    return "x"


@register.filter(name="get_model_row")
def get_model_row(obj):
    if hasattr(obj, "_meta"):
        ret = []
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if field.name == "id":
                    ret.insert(0, getattr(obj, field.name))
                else:
                    ret.append(getattr(obj, field.name))
        return ret
    else:
        return []


@register.filter(name="get_model_ooxml_row")
def get_model_ooxml_row(obj):
    if hasattr(obj, "_meta"):
        ret = []
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if field.name == "id":
                    ret.insert(0, ooxml(getattr(obj, field.name)))
                else:
                    ret.append(ooxml(getattr(obj, field.name)))
        return ret
    else:
        return []


@register.filter(name="get_all_model_fields")
def get_all_model_fields(value):
    """Returns all fields for model (value)"""
    ret = []
    for f in value._meta.fields + value._meta.many_to_many:
        ret.append(f)
    return ret


@register.filter(name="get_all_model_parents")
def get_all_model_parents(parent):
    """Returns fields for model (value) without many_to_many fields"""
    ret = []
    while parent:
        ret.append(parent)
        parent = parent.parent
    return ret


@register.filter(name="get_model_fields_names")
def get_model_fields_names(obj):
    ret = []
    for field in obj._meta.get_fields():
        if hasattr(obj, field.name):
            if field.name == "id":
                ret.insert(0, field.name)
            else:
                ret.append(field.name)
    return ret


@register.filter(name="get_model_fields_verbose_names")
def get_model_fields_verbose_names(obj):
    ret = []
    if hasattr(obj, "_meta"):
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if hasattr(field, "verbose_name"):
                    if field.name == "id":
                        ret.insert(0, field.verbose_name)
                    else:
                        ret.append(field.verbose_name)
                else:
                    ret.append(field.name)
    else:
        for i in range(0, len(obj)):
            ret.append("x%d" % i)
    return ret


@register.filter(name="user_in_group")
def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name="field_as_widget")
def field_as_widget(value, arg):
    d = {}
    l = arg.split(",")
    for x in l:
        x2 = x.split(":")
        d[x2[0]] = x2[1]
    return value.as_widget(attrs=d)


# TODO - zmiana nazwy


@register.filter(name="model_has_children")
def model_has_children(value):
    if hasattr(value, "has_children"):
        return value.has_children
    set_name = value._meta.model_name
    if hasattr(value, set_name + "_set"):
        o = getattr(value, set_name + "_set")
    else:
        o = getattr(value, "children")
    l = o.all()
    if len(l) > 0:
        return True
    else:
        return False


@register.filter(name="model_can_have_children")
def model_can_have_children(value):
    if hasattr(value, "can_have_children"):
        if value.can_have_children == False:
            return False
    return True


@register.filter(name="choices_from_field")
def choices_from_field(obj, field):
    return obj._meta.get_field(field).choices


# html


@register.filter(name="reverse")
def _reverse(value):
    return reverse(value)


@register.filter(name="errormessage")
def errormessage(value):
    """Returns True if value.endswith('!')"""
    if value.endswith("!"):
        return True
    else:
        return False


# @register.filter(name='to_html_icon')
# def to_html_icon(icon_str, additional_class=""):
#    if icon_str.startswith('fa://'):
#        return "<i class='fa fa-%s %s'></i>" % (icon_str[5:].replace('.png',''), additional_class)
#    elif icon_str.startswith('png://'):
#        src = mhref("/static/icons/22x22/%s" % icon_str[6:])
#        return "<img src='%s' class='%s'></img>" % (src, additional_class)
#     elif icon_str.startswith('client://'):
#         src = mhref("/static/icons/22x22/%s" % icon_str[9:])
#         return "<img src='%s' class='%s'></img>" % (src, additional_class)
#     elif icon_str.startswith('data:image/svg+xml'):
#         x = icon_str.split(',',1)
#         svg_code = x[1]
#         return svg_code
#     else:
#         return "<i class='fa fa-circle-o fa-lg'></i>"


@register.filter(name="aggregate")
def aggregate(objects, field_name):
    if field_name.startswith("max_"):
        field = field_name[4:]
        x = objects.aggregate(Max(field))
        return x[field + "__max"]
    elif field_name.startswith("min_"):
        field = field_name[4:]
        x = objects.aggregate(Min(field))
        return x[field + "__min"]
    elif field_name.startswith("sum_"):
        field = field_name[4:]
        x = objects.aggregate(Sum(field))
        return x[field + "__sum"]
    elif field_name.startswith("avg_"):
        field = field_name[4:]
        x = objects.aggregate(Avg(field))
        return x[field + "__avg"]
    elif field_name.startswith("count_"):
        field = field_name[6:]
        x = objects.aggregate(Count(field))
        return x[field + "__count"]
    return 0


# wiki, markdown


@register.filter(name="wikify")
def _wikify(value, path=None):
    return wikify(value, path)


@register.filter(name="wiki")
def wiki(value):
    return wiki_from_str(value)


@register.filter(name="wiki_href")
def wiki_href(value, section="help"):
    if section.startswith("+"):
        path = section
        section = "help"
    else:
        path = None
    return make_href(value, section=section, path=path)


@register.filter(name="markdown", is_safe=True)
def _markdown(value):
    if value:
        return markdown.markdown(
            value,
            extensions=[
                "abbr",
                "attr_list",
                "def_list",
                "fenced_code",
                "footnotes",
                "md_in_html",
                "tables",
                "admonition",
                "codehilite",
            ],
        )
    else:
        return ""


# forms


@register.filter(name="preferred_enctype")
def _preferred_enctype(form):
    if hasattr(form, "visible_fields"):
        for field in form.visible_fields():
            if type(field.field).__name__ in ("FileField", "ImageField"):
                return "multipart/form-data"
    return "application/x-www-form-urlencoded"


class BootstrapForm:
    def __init__(self, form):
        self.form = form

    def as_p(self):
        return render_form(self.form)


@register.filter(name="to_bootstrap")
def to_bootstrap(form):
    return BootstrapForm(form)


@register.filter(name="textfiel_row_col")
def textfiel_row_col(field, arg):
    row, col = arg.split("x")
    field.field.widget.attrs["rows"] = int(row)
    field.field.widget.attrs["cols"] = int(col)
    return field


# other


def ooxml(value):
    if type(value) in (datetime.datetime, datetime.date):
        if value:
            return value.isoformat()
        else:
            return "0"
    elif type(value) in (float, int):
        if value:
            return str(value)
        else:
            return "0"
    else:
        if value:
            return str(value)
        else:
            return ""


@register.filter(name="ooxml")
def _ooxml(value):
    return ooxml(value)


@register.filter(name="ihtml2html")
def ihtml2html(html):
    return ihtml_to_html(None, input_str=html)


@register.filter(name="get_or_tree")
def get_or_tree(getattr):
    if getattr:
        return "gettree"
    else:
        return "tree"


@register.filter(name="append_class_to_attrs")
def append_class_to_attrs(obj, arg):
    if obj:
        ret = ""
        test = False
        for pos in [x.split("=") for x in obj.split(" ")]:
            if pos[0] == "class":
                test = True
                ret += "%s='%s' " % (
                    "class",
                    pos[1].replace('"', "").replace("'", "") + " " + arg + " ",
                )
            else:
                if len(pos) == 2:
                    ret += "%s=%s " % (pos[0], pos[1])
                else:
                    ret += pos[0] + " "
        if not test:
            ret += "%s='%s' " % ("class", arg + " ")
        return ret[:-1]
    else:
        return "class='%s'" % arg


@register.filter(name="is_menu_checked")
def is_menu_checked(url, full_path):
    if url and full_path:
        p = full_path.split("?")[0]
        if len(p) > 0 and p[0] == "/":
            p = p[1:]
        if len(p) > 0 and p[-1] == "/":
            p = p[:-1]

        u = url.split("?")[0]
        if len(u) > 0 and u[0] == "/":
            u = u[1:]
        if len(u) > 0 and u[-1] == "/":
            u = u[:-1]

        if (p in u and "wiki" in p) or u in p:
            return True
        else:
            return False
    else:
        return False


@register.filter(name="import_var")
def _import_var(obj):
    path = str(obj)
    base_path, item = path.split(":")
    m = importlib.import_module(base_path)
    return getattr(m, item)


@register.filter(name="json_dumps", is_safe=True)
def _json_dumps(obj):
    ret = json_dumps(obj)
    return ret


@register.filter(name="only_items_containing")
def only_items_containing(select_field, mask):
    """Remove frem select field items not in line with mask"""
    if mask:
        to_delete = []
        for item in select_field.field.widget.choices:
            if not mask in item[0]:
                to_delete.append(item)
        for item in to_delete:
            select_field.field.widget.choices.remove(item)
    return ""


@register.filter(name="user_can_change_password")
def user_can_change_password(user):
    try:
        from allauth.account.models import EmailAddress
    except:
        return True

    object_list = EmailAddress.objects.filter(user=user)
    if len(object_list) > 0:
        return False
    else:
        return True


@register.filter(name="prefetch_related")
def prefetch_related(object_list, param):
    l = object_list
    for related in param.replace(",", ";").split(";"):
        if related:
            l = l.prefetch_related(related)
    return l


@register.filter(name="append_uuid")
def append_uuid(var):
    return str(var) + str(uuid.uuid4())


@register.filter(name="append_suffix")
def append_suffix(value, s):
    if s == None or s == "":
        return value
    else:
        if value.endswith(s):
            return value
        else:
            return value + str(s)


@register.filter(name="remove_suffix")
def remove_suffix(value, s):
    if s == None or s == "":
        return value
    else:
        if value.endswith(s):
            return value[: -len(s)]
        else:
            return value
