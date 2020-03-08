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

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

"""Standard python template filters

"""

from base64 import b64encode, b64decode
import datetime
import importlib

from django import template
from django.urls import reverse
from django.forms.widgets import HiddenInput, CheckboxSelectMultiple
from django.template.loader import get_template
from django.template import Context, Template
from django.db.models.query import QuerySet
from django.db.models import Count, Max, Min, Sum, Avg
from django.utils.safestring import mark_safe

import markdown2 as markdown

from pytigon_lib.schdjangoext.tools import make_href as mhref

from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html
from pytigon_lib.schtools.wiki import wiki_from_str, make_href, wikify

from bootstrap4.forms import render_form

register = template.Library()


@register.filter(name='class_name')
def class_name(value):
    """Returns class name of value"""

    ret = ''
    try:
        ret = value.__class__.__name__
    except:
        pass
    return ret


@register.filter(name='class_dir')
def class_dir(value):
    """Returns dir(value)"""

    ret = ''
    try:
        ret = str(dir(value)).replace('\n', '')
    except:
        pass
    return ret


@register.filter(name='is_hidden')
def is_hidden(value):
    """Test if value._is_hidden()"""
    if value._is_hidden():
        return True
    else:
        return False


@register.filter(name='urlencode_shash')
def urlencode_shash(value):
    """return urllib.parse.quote(value, '')"""
    import urllib.request, urllib.parse, urllib.error
    return urllib.parse.quote(value, '')


@register.filter(name='bencode')
def bencode(value):
    """Returns b64encode(value)"""

    if value:
        return b64encode(value.encode('utf-8')).decode('utf-8')
    else:
        return ''


@register.filter(name='bdecode')
def bdecode(value):
    """Returns b64decode(value)"""

    return b64decode(value.encode('utf-8')).decode('utf-8')


@register.filter(name='subtract')
def subtract(value, arg):
    """Returns int(value) - int(arg)"""
    return int(value) - int(arg)


@register.filter(name='multiply')
def multiply(value, arg):
    """Returns int(value) * int(arg)"""
    return int(value) * int(arg)

@register.filter(name='fmultiply')
def fmultiply(value, arg):
    """return fvalue * float"""
    try:
        ret = float(value) * float(arg)
    except:
        ret = ""
    return ret


@register.filter(name='divide')
def divide(value, arg):
    """Return int(value) / int(arg)"""
    return int(value) / int(arg)


@register.filter(name='fdivide')
def fdivide(value, arg):
    """Returns float(value) / float(arg)"""
    if float(arg) != 0:
        return float(value) / float(arg)
    else:
        return ""

@register.filter(name='range')
def frange(value):
    """Returns list(range(int(value)))"""
    return list(range(int(value)))


@register.filter(name='get')
def get(value, argv):
    """Returns value[int(argv)]"""
    return value[int(argv)]


@register.filter(name='getvalue')
def getvalue(value, argv):
    """Returns value[argv]"""
    return value[argv]


@register.filter(name='date_inc')
def date_inc(value, arg):
    """Increment date value by timedelta(int(arg))"""
    try:
        (date, time) = value.split()
        (y, m, d) = date.split('-')
        return datetime.datetime(int(y), int(m), int(d))\
             + datetime.timedelta(int(arg))
    except ValueError:
        return None


@register.filter(name='date_dec')
def date_dec(value, arg):
    """Decrement date value by timedelta(int(arg))"""
    try:
        (y, m, d) = value.split('-')
        return (datetime.datetime(int(y), int(m), int(d))
                 - datetime.timedelta(int(arg))).date()
    except ValueError:
        return None


@register.filter(name='onlyclass')
def onlyclass(value, arg):
    """Filter from list of objects (value) position with arg class"""
    ret = []
    for obj in value:
        if obj.__class__.__name__ == arg:
            ret.append(obj)
    if len(ret) == 0:
        ret = None
    return ret


@register.filter(name='errormessage')
def errormessage(value):
    """Returns True if value.endswith('!')"""
    if value.endswith('!'):
        return True
    else:
        return False


@register.filter(name='feval')
def template_eval(value):
    """Returns eval(value)"""
    return eval(value)


@register.filter(name='one_line_block')
def one_line_block(value):
    """Clean value by removing unnecessary spaces and characters: '\n', '\t' """
    return value.replace('        ', ' ').replace('    ', ' ').replace('  ', ' ').replace('\n', '').replace('\t', '')

@register.filter(name='one_line_code')
def one_line_code(value):
    """Clean value by removing unnecessary spaces and characters: '\n', '\t' """
    return value.replace('\n', '').replace('\r', '').replace('\t', '')

@register.filter(name='arg')
def arg_fun(value, arg):
    """Replace first '%s' in value with arg"""
    return value.replace('%s', arg, 1)


@register.filter(name='dir')
def f_dir(value):
    """Returns dir(value)"""
    return dir(value)


@register.filter(name='getfield')
def getfield(value, attr):
    """Returns getattr(value, attr)"""
    try:
        obj = getattr(value, attr)
    except:
        obj = None
    return obj


@register.filter(name='getfields')
def getfields(value):
    """Returns fields for model (value) without many_to_many fields"""
    ret = []
    if value and hasattr(value, '_meta'):
        for f in value._meta.fields:
            ret.append(f)
    return ret


@register.filter(name='getallparents')
def getparents(parent):
    """Returns fields for model (value) without many_to_many fields"""
    ret = []
    while parent:
        ret.append(parent)
        parent=parent.parent
    return ret

@register.filter(name='getallfields')
def getallfields(value):
    """Returns all fields for model (value)"""
    ret = []
    for f in value._meta.fields + value._meta.many_to_many:
        ret.append(f)
    return ret


@register.filter(name='tostr')
def tostr(value):
    """Converts value to str"""
    return str(value)


@register.filter(name='as_widget')
def as_widget_fun(value, arg):
    d = {}
    l = arg.split(',')
    for x in l:
        x2 = x.split(':')
        d[x2[0]] = x2[1]
    return value.as_widget(attrs=d)


@register.filter(name='sum')
def sum(value, arg):
    value = value + float(arg)
    return ''


@register.filter(name='left')
def left(value, arg):
    return str(value)[:int(arg)]


@register.filter(name='truncate')
def truncate(value, arg):
    try:
        retstr = str(value)
    except:
        retstr = unicode(value)
        
    if len(retstr) > int(arg):
        return retstr[:int(arg) - 3] + '...'
    else:
        return retstr


@register.filter(name='genericfloatformat')
def genericfloatformat(text, arg="{: .2f}"):
    space_convert = False
    try:
        f = float(text)
        if ': ' in arg:
            space_convert = True
            arg2 = arg.replace(': ', ':,')
        else:
            arg2 = arg
        x = arg2.format(f)
        if space_convert:
            return x.replace(',', ' ')
        else:
            return ""
    except ValueError:
        return ''

@register.filter(name='genericfloatnullformat')
def genericfloatnullformat(text, arg="{: .2f}"):
    try:
        f = float(text)
        if not f:
            return "-"
        else:
            return genericfloatformat(text, arg)
    except:
        return "-"

@register.filter(name='floatformat2')
def floatformat2(text):
    return genericfloatformat(text, "{: .2f}")

@register.filter(name='floatformat3')
def floatformat3(text):
    return genericfloatformat(text, "{: .3f}")

@register.filter(name='floatnullformat')
def floatnullformat(text):
    return genericfloatnullformat(text, "{: .2f}")

@register.filter(name='floatnullformat3')
def floatnullformat3(text):
    return genericfloatnullformat(text, "{: .3f}")


@register.filter(name='amount')
def amount(text):
    try:
        f = float(text)
    except ValueError:
        return ''
    if f==0.0:
        return '-  '
    def split_len(seq, length):
        return [seq[i:i+length] for i in range(0, len(seq), length)]

    s = "%.02f" % f
    t = s.split('.')
    return ' '.join(split_len(t[0][::-1], 3))[::-1] + "." + t[1]


@register.filter(name='hide')
def hide(value):
    value.widget = HiddenInput()
    return value


@register.filter(name='query')
def query(value, query):
    tab = str(query).split('=')
    kwargs = {}
    kwargs[tab[0]] = eval(tab[1])
    value.field.queryset = value.field.queryset.filter(**kwargs)
    return value


@register.filter(name='clean')
def clean(value):
    return ' '.join(value.replace('\n', '').replace('\t', '').split())


@register.filter(name='print_info')
def print_info(value):
    print('PRINT_INFO:', value.__class__.__name__, dir(value), value)
    return value

#@register.filter(name='wikify')
#def _wikify(value, path=None):
#    return wikify(value, path)


@register.filter(name='wiki')
def wiki(value):
    return wiki_from_str(value)


@register.filter(name='wiki_href')
def wiki_href(value, section="help"):
    if section.startswith('+'):
        path = section
        section = 'help'
    else:
        path=None
    return make_href(value, section=section, path=path)


@register.filter(name='comma')
def comma(value):
    if value and len(value) > 0 and value != ' ':
        return value + ', '
    else:
        return ''


@register.filter(name='readonly_transform')
def readonly_transform(value, arg):
    if arg == '_':
        return value
    else:
        return value.replace('/_', '/')


@register.filter(name='children')
def children(value):
    set_name = value._meta.model_name
    if hasattr(value, set_name + '_set'):
        o = getattr(value, set_name + '_set')
    else:
        o = getattr(value, 'children')
    l = o.all()
    if len(l) > 0:
        return True
    else:
        return False


@register.filter(name='print')
def print_fun(value):
    print('print_fun:', value.__class__, value)
    return value


@register.filter(name='format')
def format(value, id):
    return value % id


@register.filter(name='replace')
def replace(value, replace_str):
    l = replace_str.split('|')
    if len(l) == 2:
        value2 = value.replace(l[0], l[1])
        return value2
    else:
        return value

@register.filter(name='append_str')
def append_str(value, s):
    if s==None or s=="":
        return value
    else:
        return value + str(s)

@register.filter(name='css_hack', is_safe=True)
def css_hack(value):
    return mark_safe(value+'?'+datetime.datetime.now().isoformat())

@register.filter(name='isoformat')
def isoformat(value):
    if value:
        iso = value.isoformat()[:19].replace('T', ' ')
        return iso
    else:
        return ""

@register.filter(name='isoformat_short')
def isoformat(value):
    if value:
        iso = value.isoformat()[:16].replace('T', ' ')
        return iso
    else:
        return ""


@register.filter(name='d_isoformat')
def d_isoformat(value):
    if value:
        iso = value.isoformat()[:10]
        return iso
    else:
        return ""


@register.filter(name='choices_from_field')
def choices_from_field(obj, field):
    return obj._meta.get_field(field).choices


@register.filter(name='is_')
def is_(value):
    return value.startswith('_')


@register.filter(name='to_int')
def to_int(value):
    try: 
        ret = int(value)
    except:
        ret = 0
    return ret


@register.filter(name='minus')
def to_int(value, arg):
    try:
        ret = int(value) - int(arg)
    except:
        ret = 0
    return ret

@register.filter(name='plus')
def to_int(value, arg):
    try:
        ret = int(value) + int(arg)
    except:
        ret = 0
    return ret


@register.filter(name='addclass')
def addclass(value, arg):
    value.field.widget.attrs['class'] = arg
    return value


@register.filter(name='alternatewidget')
def alternatewidget(value):
    value.field.widget = CheckboxSelectMultiple(choices=value.field.choices)
    return value

@register.filter(name='reverse')
def _reverse(value):
    return reverse(value)


@register.filter(name='textfiel_row_col')
def textfiel_row_col(field, arg):
    row, col = arg.split('x')
    field.field.widget.attrs['rows']=int(row)
    field.field.widget.attrs['cols']=int(col)
    return field


@register.filter(name='set_textfiel_row_col')
def set_textfiel_row_col(field, arg):
    row, col = arg.split('x')
    field.field.widget.attrs['rows']=int(row)
    field.field.widget.attrs['cols']=int(col)
    return ""


def obj_to_date(value):
    if value:
        return str(value)[0:10]
    else:
        return ""

def obj_to_time(value):
    if value:
        return str(value)[0:16]
    else:
        return ""

def obj_to_str(value):
    if value:
        return value
    else:
        return ""

def obj_to_float(value):
    if value:
        return floatformat2(value)
    else:
        return ""

def obj_to_float2(value):
    if value:
        return floatnullformat(value)
    else:
        return "-"

def obj_to_int(value):
    if value:
        return "%d" % int(value)
    else:
        return ""

@register.filter(name='tr_format')
def tr_format(row, format):
    ret = "<tr>"
    i=0
    for f in format:
        pos = row[i]
        if   f=='i':
            ret+="<td align='right'>%s</td>" % obj_to_int(pos)
        elif f=='I':
            ret+="<td align='right'>%s</td>" % obj_to_int(pos)
        elif f=='f':
            ret+="<td align='right'>%s</td>" % obj_to_float(pos)
        elif f=='F':
            ret+="<td align='right'>%s</td>" % obj_to_float2(pos)
        elif f=='s':
            ret+="<td>%s</td>" % obj_to_str(pos)
        elif f=='S':
            ret+="<td>%s</td>" % obj_to_str(pos)
        elif f=='k':
            ret+="<td align='right'>%s</td>" % obj_to_float(pos)
        elif f=='K':
            ret+="<td align='right'>%s</td>" % obj_to_float(pos)
        elif f=='D':
            ret+="<td>%s</td>" % obj_to_date(pos)
        elif f=='d':
            ret+="<td>%s</td>" % obj_to_date(pos)
        elif f=='T':
            ret+="<td>%s</td>" % obj_to_time(pos)
        elif f=='t':
            ret+="<td>%s</td>" % obj_to_time(pos)
        else:
            ret+="<td>%s</td>" % str(pos)
        i+=1
    ret+="</tr>"
    return ret

@register.filter(name='as_title')
def as_title(field):
    t = get_template('widgets/field_title.html')
    d = { 'field': field }
    c = Context(d)
    return t.render(c)

@register.filter(name='translate')
def translate(s, lng):
    return s.replace('.html', "_"+lng+".html")

@register.filter(name='add_label')
def add_label(obj, label):
    obj['label'] = label
    return obj

@register.filter(name='split')
def filter_split(obj, sep=';'):
    return obj.split(sep)

@register.filter(name='hasattr')
def filter_hasattr(obj, attr_name):
    return hasattr(obj, attr_name)


@register.filter(name='module_obj')
def filter_module_obj(obj, obj_name):
    if type(obj) == QuerySet:
        module_name = obj.model.__module__
        return getattr(__import__(module_name).models, obj_name)
    return None

@register.filter(name='ihtml2html')
def ihtml2html(html):
    return ihtml_to_html(None, input_str=html)


@register.filter(name='first_section')
def first_section(html):
    return html.split('$$$')[0]

@register.filter(name='second_section')
def second_section(html):
    x = html.split('$$$')
    if len(x)>1:
        return x[1]
    else:
        return ""


@register.filter(name='is_menu_checked')
def is_menu_checked(url, full_path):
    if url and full_path:
        p = full_path.split('?')[0]
        if len(p)>0 and p[0]=='/': p=p[1:]
        if len(p)>0 and p[-1]=='/': p=p[:-1]

        u = url.split('?')[0]
        if len(u)>0 and u[0]=='/': u=u[1:]
        if len(u)>0 and u[-1]=='/': u=u[:-1]

        if (p in u and 'wiki' in p) or u in p:
            return True
        else:
            return False
    else:
        return False


@register.filter(name='last_elem')
def last_elem(value, sep='/'):
    return value.split(sep)[-1]


@register.filter(name='get_fields_names')
def get_fields_names(obj):
    ret = []
    for field in obj._meta.get_fields():
        if hasattr(obj, field.name):
            if field.name == 'id':
                ret.insert(0,field.name)
            else:
                ret.append(field.name)
    return ret

@register.filter(name='get_fields_verbose_names')
def get_fields_verbose_names(obj):
    ret = []
    if hasattr(obj, "_meta"):
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if hasattr(field, "verbose_name"):
                    if field.name == 'id':
                        ret.insert(0,field.verbose_name)
                    else:
                        ret.append(field.verbose_name)
                else:
                    ret.append(field.name)
    else:
        for i in range(0, len(obj)):
            ret.append("x%d" % i)
    return ret

@register.filter(name='get_fields')
def get_fields(obj):
    if hasattr(obj, "_meta"):
        ret = []
        for field in obj._meta.get_fields():
            if hasattr(obj, field.name):
                if field.name == 'id':
                    ret.insert(0, getattr(obj, field.name))
                else:
                    ret.append(getattr(obj, field.name))
        return ret
    else:
        return obj


@register.filter(name='has_group') 
def has_group(user, group_name): 
    return user.groups.filter(name=group_name).exists()


def callMethod(obj, methodName):
    method = getattr(obj, methodName)
    if hasattr(obj, "__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()
register.filter("call", callMethod)


def args(obj, arg):
    if not hasattr(obj, "__callArg"):
        obj.__callArg = []
    obj.__callArg += [arg]
    return obj
register.filter("args", args)


@register.filter(name='aggregate')
def aggregate(objects, field_name):
    if field_name.startswith('max_'):
        field = field_name[4:]
        x = objects.aggregate(Max(field))
        return x[field+'__max']
    elif field_name.startswith('min_'):
        field = field_name[4:]
        x = objects.aggregate(Min(field))
        return x[field+'__min']
    elif field_name.startswith('sum_'):
        field = field_name[4:]
        x = objects.aggregate(Sum(field))
        return x[field+'__sum']
    elif field_name.startswith('avg_'):
        field = field_name[4:]
        x = objects.aggregate(Avg(field))
        return x[field+'__avg']
    elif field_name.startswith('count_'):
        field = field_name[6:]
        x = objects.aggregate(Count(field))
        return x[field+'__count']
    return 0


@register.filter(name='append_class_to_attrs')
def append_class_to_attrs(obj, arg):
    if obj:
        ret = ""
        test = False
        for pos in [ x.split('=') for x in obj.split(' ') ]:
            if pos[0]=='class':
                test = True
                ret += "%s='%s' " % ('class', pos[1].replace('"',"").replace("'","") +" "+arg+" ")
            else:
                if len(pos)==2:
                    ret += "%s='%s' " % pos
                else:
                    ret += pos[0] + ' '
        if not test:
            ret += "%s='%s' " % ('class', arg + " ")
        return ret[:-1]
    else:
        return "class='%s'" % arg

@register.filter(name='import_var')
def _import_var(obj):
    path = str(obj)
    base_path, item = path.split(':')
    m = importlib.import_module(base_path)
    return getattr(m, item)

@register.filter(name='run_fun')
def _run_fun(obj):
    return obj()
    
    
@register.filter(name='getitem')
def getitem(value, attr):
    """Returns getattr(value, attr)"""
    try:
        obj = value[attr]
    except:
        obj = None
    return obj

@register.filter(name='append_filter')
def append_filter(form_field, filter):
    if hasattr(form_field, "filter"):
        form_field.filter = filter
    return form_field


@register.filter(name='get_or_tree')
def get_or_tree(getattr):
    if getattr:
        return 'gettree'
    else:
        return 'tree'

@register.filter(name='to_html_icon')
def to_html_icon(icon_str, additional_class=""):
    if icon_str.startswith('fa://'):
        return "<i class='fa fa-%s %s'></i>" % (icon_str[5:].replace('.png',''), additional_class)
    elif icon_str.startswith('png://'):
        src = mhref("/static/icons/22x22/%s" % icon_str[6:])
        return "<img src='%s' class='%s'></img>" % (src, additional_class)
    elif icon_str.startswith('client://'):
        src = mhref("/static/icons/22x22/%s" % icon_str[9:])
        return "<img src='%s' class='%s'></img>" % (src, additional_class)
    else:
        return "<i class='fa fa-circle-o'></i>"

@register.filter(name='append_get_param')
def append_get_param(href, parm):
    if '?' in href:
        return href+"&"+str(parm)
    else:
        return href+"?"+str(parm)

@register.filter(name='markdown', is_safe=True)
def _markdown(value):
    return markdown.markdown(value, extras=['tables', 'codehilite'])


@register.filter(name='preferred_enctype')
def _preferred_enctype(form):
    if hasattr(form, 'visible_fields'):
        for field in form.visible_fields():
            if type(field.field).__name__ in ('FileField', 'ImageField'):
                return "multipart/form-data"
    return "application/x-www-form-urlencoded"


class BootstrapForm():
    def __init__(self, form):
        self.form = form

    def as_p(self):
        return render_form(self.form)

@register.filter(name='to_bootstrap')
def to_bootstrap(form):
    return BootstrapForm(form)


@register.filter(name='ooxml')
def ooxml(value):
    if type(value) in (datetime.datetime, datetime.date):
        if value:
            return value.isoformat()
        else:
            return '0'
    elif type(value) in (float, int):
        if value:
            return str(value)
        else:
            return '0'
    else :
        if value:
            return str(value)
        else:
            return ""


@register.filter(name='nbsp')
def nbsp(value):
    return value.replace(' ', '&nbsp;')


@register.filter(name='ext')
def ext(value, arg):
    if value.lower().endswith(arg.lower()):
        return True
    else:
        return False

@register.filter(name='base_name')
def base_name(value):
    return value.split('/')[-1].split('.')[0]
