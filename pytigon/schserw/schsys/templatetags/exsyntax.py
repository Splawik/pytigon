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

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

from base64 import b64encode
import re
import itertools
import html
import os

from django import template
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.template import Template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.base import token_kwargs, TemplateSyntaxError, Node

from pytigon_lib.schtools.href_action import standard_dict, actions_dict, action_fun
from pytigon_lib.schdjangoext.tools import import_model, make_href

from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schdjangoext.fields import ModelSelect2WidgetExt
from pytigon_lib.schdjangoext.models import TreeModel
from pytigon_lib.schtools.wiki import wiki_from_str, wikify
from pytigon_lib.schdjangoext.tools import make_href as mhref

from django.forms import FileInput, CheckboxInput, RadioSelect, CheckboxSelectMultiple
from django.utils.safestring import SafeText
from django import forms

register = template.Library()

## tools

def inclusion_tag(file_name):
    def dec(func):
        def func2(context, *argi, **argv):
            ret = func(context, *argi, **argv)
            t = get_template(file_name)
            return t.render(ret, context.request)
        return register.simple_tag(takes_context=True, name=getattr(func, '_decorated_function', func).__name__)(func2)
    return dec


# row actions

class RowActionNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        if output.replace('\n',''):
            t = Template(output)
            output2 = t.render(context).replace('\n',';')
            t = get_template('widgets/row_actions.html')
            d = actions_dict(context, output2)
            return t.render(d, request = d['request'])
        else:
            return ""

@register.tag
def row_actions(parser, token):
    nodelist = parser.parse(('endrow_actions',))
    parser.delete_first_token()
    return RowActionNode(nodelist)

@inclusion_tag('widgets/action.html')
def action(context, action, title = "", icon_name = "", target = "", attrs = "", tag_class = "", url = ""):
    print("====>>", action, target)
    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url)
    return ret

# actions

@inclusion_tag('widgets/view_row.html')
def view_row(context, object, title = "", icon_name = "", target = "popup_info", attrs = "", tag_class = "", url = ""):
    if url:
        href=url
    else:
        href = "{tp}%s/_/view/" % context['object'].id
    ret = action_fun(context, 'view_row', title, icon_name, target, attrs,tag_class, href)
    if hasattr(object, 'get_derived_object'):
        object2 = object.get_derived_object()
        if hasattr(object2, 'str'):
            ret['title2'] = str(object2)
        else:
            ret['title2'] = ("%s(id=" % type(object2).__name__) + str(title) + ")"
    else:
        if hasattr(object, 'str'):
            ret['title2'] = str(object)
        else:
            ret['title2'] = ("%s(id=" % type(object).__name__ )+ str(title) + ")"
    return ret


@inclusion_tag('widgets/get_row.html')
def get_row(context, title = "", icon_name = "", target = "", attrs = "", tag_class = "", url = ""):
    ret = action_fun(context, 'get', title, icon_name, target, attrs, tag_class, url)
    ret['id'] = context['object'].id
    ret['text'] = str(context['object'])
    return ret


@inclusion_tag('widgets/button.html')
def button(context, title = "", icon_name = "", target = "", attrs = "", tag_class = "", url = ""):
    ret = action_fun(context, 'button', title, icon_name, target, attrs, tag_class, url)
    return ret


def new_row_base(context, action="new_row/-", title="", icon_name="", target='', attrs='', tag_class="", url=""):
    if url:
        url2=url
    else:
        url2='{tp}{x1}/add/'
    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url2)
    if title and title[0] == '+':
        description = title[1:]
        title = ""
    else:
        description = title
    ret['description'] = description
    return ret


@inclusion_tag('widgets/new_row.html')
def new_row(context, title="", icon_name="", target='', attrs='', tag_class='', url="", action="new_row/-"):
    return new_row_base(context, action, title, icon_name, target, attrs, tag_class, url)


@inclusion_tag('widgets/new_row.html')
def new_row_inline(context, title="", icon_name="", target='', attrs='', tag_class='', url="", action="new_row-inline/-"):
    return new_row_base(context, action, title, icon_name, target, attrs, tag_class, url)


@inclusion_tag('widgets/list_sublist.html')
def list_sublist(context, app="", table_name="", filter="", title="", icon_name="fa fa-lg fa-caret-down", target="", attrs="", tag_class="", url="", action="field_list"):
    if url:
        url2 = url
    else:
        if filter:
            url2 = "{bp}" + f"{app}/table/{table_name}//{filter}/form/sublist/"
        else:
            url2 = "{bp}" + f"{app}/table/{table_name}/{context['object'].id}/-/form/sublist/"

    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url2)
    return ret

@inclusion_tag('widgets/list_action.html')
def list_action(context, action, title="", icon_name="", target='_parent', attrs='', tag_class="", url="", active=False):
    if attrs:
        ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url if url else "{tp}action/%s/" % action)
    elif active:
        ret = action_fun(context, action, title, icon_name, target, "data-role='button'", "btn btn-outline-secondary no_close no_cancel", url if url else "{tp}action/%s/" % action)
    else:
        ret = action_fun(context, action, title, icon_name, target, "data-role='button'", "btn btn-outline-secondary no_ok no_cancel", url if url else "{tp}action/%s/" % action)
    return ret


@inclusion_tag('widgets/wiki_button.html')
def wiki_button(context, subject, wiki_description, icon_name="", target='_self',  attrs="", tag_class="", url=""):
    wiki_name = wiki_from_str(wiki_description)
    wiki_url = "/schwiki/%s/%s/view/" % (subject, wiki_name)
    return action_fun(context, "wiki", wiki_description, icon_name, target, attrs, tag_class, url if url else wiki_url)


@inclusion_tag('widgets/wiki_link.html')
def wiki_link(context, subject, wiki_description, attrs="", target='_self', url=""):
    return wiki_button(context, subject, wiki_description, attrs, target, url)

# form

@inclusion_tag('widgets/field.html')
def field(context, form_field, fieldformat=None):
    if type(form_field) in (SafeText, str,):
        field = context['form'][form_field]
    else:
        field = form_field

    label_class = "control-label float-left"
    offset = ""
    form_group_class = "form-group group_%s" % type(field.field).__name__.lower()
    field_class = "controls float-left %s" % type(field.field).__name__.lower()
    placeholder = False
    show_label = True

    addon_after=""
    addon_before=""
    addon_after_class=""
    addon_before_class=""

    ff = None
    if fieldformat:
        ff = fieldformat
    else:
        if 'formformat' in context:
            ff = context['formformat']
        if not ff:
            ff = "12:3:3/12:12:12"
    hidden = False

    if ff=='!':
        hidden=True
    else:
        x = ff.split('/',2)
        if len(x) < 2:
            return {}

        if x[0]=='^':
            form_group_class += " label-floating"
            field_class += " col-12"
        elif x[0]=='-':
            form_group_class += " label-over-field"
            field_class += " col-12"
        elif not x[0]:
            placeholder=field.label
            show_label=False
            field_class += " col-12"
        else:
            y = [int(pos) for pos in x[0].split(':')]
            if len(y)==3:
                label_class += " col-sm-%d col-md-%d col-lg-%d" % (y[0], y[1], y[2])
                field_class += " col-sm-%d col-md-%d col-lg-%d" % ((11-y[0])%12+1, (11-y[1])%12+1, (11-y[2])%12+1)
                offset = " offset-sm-%d offset-md-%d offset-lg-%d" % (y[0]%12, y[1]%12, y[2]%12)
            else:
                label_class += " col-sm-12 col-md-%d" % y[0]
                field_class += " col-sm-12 col-md-%d" % ((11-y[0])%12+1)
                offset = "offset-sm-0 offset-md-%d" % (y[0] % 12)

        if x[1]:
            y = x[1].split(':')
            if len(y)==3:
                form_group_class += " col-sm-%s col-md-%s col-lg-%s" % (y[0], y[1], y[2])
            else:
                form_group_class += " col-sm-12 col-md-%s" % y[0]

        if len(x)>2:
            addon = x[2]
            if addon:
                if  addon.startswith('(-X)'):
                    addon_after=addon[4:]
                    addon_after_class = "input-group-btn"
                elif addon.startswith('(X-)'):
                    addon_before=addon[4:]
                    addon_before_class = "input-group-btn"
                elif addon.startswith('(-x)'):
                    addon_after = addon[4:]
                    addon_after_class = "input-group-addon"
                elif addon.startswith('(x-)'):
                    addon_before=addon[4:]
                    addon_before_class = "input-group-addon"

        if offset and type(field.field.widget) in (CheckboxInput, RadioSelect, CheckboxSelectMultiple, FileInput):
            field_class += " " + offset

        #if type(field.field.widget) in (CheckboxInput, RadioSelect, CheckboxSelectMultiple):
        #    field.field.widget.attrs["class"] = 'custom-control-input'

    ret = {}
    ret['form'] = context['form']
    ret['field'] = field
    ret['hidden'] = hidden
    ret['label_class'] = label_class
    ret['form_group_class'] = form_group_class
    ret['field_class'] = field_class
    ret['placeholder'] = placeholder
    ret['addon_after'] = addon_after
    ret['addon_after_class'] = addon_after_class
    ret['addon_before'] = addon_before
    ret['addon_before_class'] = addon_before_class
    ret['show_label'] = show_label
    ret['standard_web_browser'] = context['standard_web_browser']
    return ret

class Form(Node):
    def __init__(self, nodelist, def_param, param):
        self.nodelist = nodelist
        self.def_param=def_param
        self.param = []
        for pos in param:
            self.param.append(template.Variable(pos))

    def render(self, context):
        output = self.nodelist.render(context).strip().replace('\"',"'").replace(";","','")
        form = context['form']
        fields = []
        if output:
            for f in output.split(','):
                x = f.split(':', 1)
                name = x[0].replace("'", "").strip()
                if len(x)>1:
                    p=x[1]
                elif len(self.param)>1:
                    p=self.param[1].resolve(context)
                else:
                    p=self.def_param
                fields.append([name,p])
        else:
            for field in form:
                if len(self.param)>1:
                    p=self.param[1].resolve(context)
                else:
                    p=self.def_param
                fields.append([field.name,p])

        template_str = "{% load exsyntax %}<div class='row'>"
        for field in fields:
            template_str += "{%% field '%s' '%s' %%}" % ( field[0], field[1])
        template_str += "</div>"
        t = Template(template_str)
        return t.render(context)

@register.tag
def form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(('endform'))
    parser.delete_first_token()
    return Form(nodelist, "12:3:3/12:12:12", parm)


@register.tag
def vert_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(('endvert_form',))
    parser.delete_first_token()
    return Form(nodelist, "^/12", parm)

@register.tag
def inline_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(('endinline_form',))
    parser.delete_first_token()
    return Form(nodelist, "^/", parm)

@register.tag
def col2_form(parser, token):
    parm = token.split_contents()
    nodelist = parser.parse(('endcol2_form',))
    parser.delete_first_token()
    return Form(nodelist, "^/12:6:6", parm)

class FormItemNode(Node):
    def __init__(self, nodelist, field_name, tag):
        self.nodelist = nodelist
        self.field_name = field_name
        self.tag = tag

    def render(self, context):
        x = self.nodelist.render(context)
        if '|' in x:
            pos=x.find('|')
            title = x[:pos].strip()
            content = x[pos+1:]
        else:
            title = context['form'][self.field_name].label
            content = x

        if not content:
            content = str(context['form'][self.field_name])

        if self.tag:
            elem0 = """ <%s class="%s form-control" name="%s" id="id_%s"> """ % \
                    (self.tag, self.field_name, self.field_name, self.field_name)
            elem1 = "</%s>" % self.tag
        else:
            elem0 = ""
            elem1 = ""

        ret = """
            <div id="div_id_%s" class="form-group">
                <label for="id_%s" class="control-label">%s</label>
                <div class="controls">%s%s%s</div>
            </div>
        """ % (self.field_name, self.field_name, title, elem0, content, elem1)

        return ret


@register.tag
def form_item(parser, token):
    field_name = token.contents[10:]
    tag = None
    if '.' in field_name:
        tmp = field_name.split('.')
        tag = tmp[1]
        field_name = tmp[0]
    nodelist = parser.parse(('endform_item',))
    parser.delete_first_token()
    return FormItemNode(nodelist, field_name, tag)


#@inclusion_tag('widgets/form2columns.html')
#def form2columns(context, fields):
#    ftab = fields.split(';')
#    it = iter(ftab)
#    fields2 = itertools.zip_longest(it,it)
#    return standard_dict(context, {'fields': ftab, 'fields2': fields2, 'form': context['form']})


@inclusion_tag('widgets/get_table_row.html')
def get_table_row(context, field_or_name, app_name=None, table_name=None, search_fields=None, filter=None, label = None,
                   initial = None, is_get_button=True, is_new_button=False, get_target="popup_edit", new_target="inline"):
    if type(field_or_name) in (SafeText, str,):
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
            if hasattr(field_or_name, 'search_fields'):
                _search_fields = field_or_name.search_fields
            else:
                _search_fields = "name__icontains"

    if 'formformat' in context:
        formformat = context['formformat']
    else:
        formformat = "12:3:3/12:12:12"

    if TreeModel in model.__bases__:
        if filter:
            href1 = make_href("/%s/table/%s/%s/0/form/gettree/?schtml=1" % (_app_name, _table_name, filter))
            href2 = make_href("/%s/table/%s/-/add/?schtml=1" % (_app_name, _table_name))
        else:
            href1 = make_href("/%s/table/%s/0/form/gettree/?schtml=1" % (_app_name, _table_name))
            href2 = make_href("/%s/table/%s/-/add/?schtml=1" % (_app_name, _table_name))
    else:
        _filter = filter if filter else "-"
        href1 = make_href("/%s/table/%s/%s/form/get/?schtml=1" % (_app_name, _table_name, _filter))
        href2 = make_href("/%s/table/%s/%s/add/?schtml=1" % (_app_name, _table_name, _filter))

    class _Form(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print("X1:", href1, href2)
            self.fields[_name] = forms.ChoiceField(
                label = _label,
                widget=ModelSelect2WidgetExt(href1, href2, is_new_button, is_get_button, _label,
                    model=model,
                    #search_fields=[_search_fields, "description__icontains"],
                    search_fields=[_search_fields, ],
                    queryset = _queryset,
                ),
            )
    form = _Form(initial = { _name: _initial })
    return { 'form': form, 'field': form[_name], "formformat": formformat, }

##  include

@inclusion_tag('widgets/frame.html')
def frame(context, href, height):
    return standard_dict(context, {'href': href, 'height': height })

@inclusion_tag('widgets/subform.html')
def subform(context, name):
    return standard_dict(context, {'href': name, })

@inclusion_tag('widgets/require.html')
def require(context, href):
    return {'href': mark_safe(href)}

@inclusion_tag('widgets/module_link.html')
def module_link(context, href):
    return {'href': mark_safe(href)}

@inclusion_tag('widgets/jscript_link.html')
def jscript_link(context, href):
    return {'href': mark_safe(href)}

@inclusion_tag('widgets/css_link.html')
def css_link(context, href):
    return standard_dict(context, {'href': href})

@inclusion_tag('widgets/link.html')
def link(context, href, rel, typ):
    return standard_dict(context, {'href': settings.STATIC_URL + href, 'rel': rel, 'typ': typ})

@inclusion_tag('widgets/component.html')
def component(context, href):
    return standard_dict(context, {'href': href, })

# other tags

@register.simple_tag
def spec(format):
    return format.replace('{', '{{').replace('}', '}}').replace('[', '{%').replace(']', '%}')

@register.simple_tag(takes_context=True)
def include_wiki(context, wiki_str, from_wiki_page, path=None, only_header=True):
    ret = ""
    if 'request' in context:
        username = context['request'].user.username
    subpage = from_wiki_page.get_page_for_wiki(wiki_str, username)
    if subpage and subpage.content:
        if only_header:
            content = subpage.content.split("<div class='read_more'")[0]
        else:
            content = subpage.content

        ret += "<div class='article-header'><div class='article-header-title'>" + subpage.get_href(path) + \
               "</div>" + content + "</div>\n"
    else:
        ret = wikify("[[" + wiki_str + "]]", path, from_wiki_page.subject)
    return mark_safe(ret)

@register.simple_tag(takes_context=True)
def markdown2html (context, markdown_str, path=None, section = None):
    return mark_safe(wikify(markdown_str, path, section))

@register.simple_tag(takes_context=True)
def subtemplate(context, template_string):
    t = Template(template_string)
    return mark_safe(t.render(context))

def editable_base(context, name, title, url):
    if ':' in name:
        field_name, t = name.split(':')
    else:
        field_name = name
        t = 'text'
    date_str = ""
    if "date" in t:
        t = "combodate"
        date_str = """ data-format="YYYY-MM-DD" data-viewformat="YYYY-MM-DD" data-template="YYYY-MM-DD" """
    if title:
        t2 = title
    else:
        t2 = ""
    oid = getattr(context['object'], 'id')
    value = getattr(context['object'], field_name)
    return f"<a class='editable autoopen' data-name='{field_name}' data-type='{t}' data-pk='{oid}' data-url='{url.format(**locals())}' data-title='{t2}' href='#' {date_str}> {value} </a>"

@register.simple_tag(takes_context=True)
def editable(context, name, title="", url=None):
    if url:
        url2 = url
    else:
        url2 = '../../../{oid}/{field_name}/editable/editor/'
    return mark_safe(editable_base(context, name, title, url2))

@register.simple_tag(takes_context=True)
def td_editable(context, name, title=""):
    if context['standard_web_browser']:
        url = '../../../{oid}/{field_name}/editable/editor/'
        return mark_safe("<td>%s</td>" % editable_base(context, name, title, url))
    else:
        #if ':' in name:
        #    field_name, t = name.split(':')
        #else:
        #   field_name = name
        ret = "<td>%s</td>" % getattr(context['object'], name)
        return mark_safe(ret)

@inclusion_tag('widgets/svg_standard_style.html')
def svg_standard_style(context,):
    return {}

@register.simple_tag(takes_context=True)
def id_num(context, name):
    if not context['standard_web_browser'] or ('doc_type' in context and context['doc_type'] == 'json'):
        if 'paginator' in context:
            return name + ':' + str(context['paginator'].per_page) + '/' \
                   + str(context['paginator'].count)
    return name

@inclusion_tag('widgets/ok_cancel.html')
def ok_cancel(context):
    return standard_dict(context, {})

@inclusion_tag('widgets/paginator.html')
def paginator(context):
    return context.flatten()

#@inclusion_tag('widgets/paginator.html')
#def paginator2(context):
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


#@inclusion_tag('widgets/checkboxselectmultiple.html')
#def checkboxselectmultiple(context, field, only_field=False):
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
        values = dict([(key, val.resolve(context)) for key, val in self.extra_context.items()])

        context.update(values)

        data = self.nodelist.render(context)
        data = data.replace('[[', '{{').replace(']]', '}}').replace('[%', '{%').replace('%]', '%}')
        id = context['id']
        class_name = context['class']

        context['template_name'] = "widgets/html_widgets/" + class_name + ".html"
        def_param = ""
        if 'width' in context:
            def_param = def_param + "width='%s' " % context['width']
            try:
                context['width'] = int(context['width']) - 10
            except:
                pass
        if 'height' in context:
            def_param = def_param + "height='%s' " % context['height']
            try:
                context['height'] = int(context['height']) - 10
            except:
                pass
        context['def_param'] = def_param

        t = Template(data)
        tdata = t.render(context)

        template = get_template(self.template_name)

        context_dict = {}
        for c in context.dicts:
            context_dict.update(c)
        context_dict['data'] = tdata

        # tdata = t.render(context_dict)

        # output = template.render(context)
        output = template.render(context_dict)

        context.pop()

        return mark_safe(output)


@register.tag('widget')
def do_html_widget(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError("%r expected at least one variable assignment" % bits[0])
    if not 'id' in extra_context or not 'class' in extra_context:
        raise TemplateSyntaxError("id and class parameters are required")
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" % (bits[0], remaining_bits[0]))
    nodelist = parser.parse(('endwidget',))
    parser.delete_first_token()
    return HtmlWidgetNode("widgets/widget.html", None, None, nodelist, extra_context=extra_context)


ICON_CACHE = {}

def _read_icon_file(path):
    tmp = None
    path_tab = path.split('/')
    with open(os.path.join(settings.STATIC_ROOT, *path_tab), "rt") as f:
        tmp = f.read()
    return tmp

def _read_user_icon_file(path):
    tmp = None
    path_tab = path.split('/')
    with open(os.path.join(settings.MEDIA_ROOT, *path_tab), "rt") as f:
        tmp = f.read()
    return tmp

@register.simple_tag(takes_context=False)
def icon(class_str, width=None, height=None):
    global ICON_CACHE

    if class_str.startswith('fa://'):
        return mark_safe("<i class='fa fa-%s'></i>" % (class_str[5:].replace('.png','')))
    elif class_str.startswith('fa-') :
        return mark_safe("<i class='fa %s'></i>" % class_str)
    elif class_str.startswith('bi-'):
        x = re.findall('bi-' + r'[\w-]+', class_str)
        if x:
            icon_name = x[0].replace('bi-','')
            if not icon_name in ICON_CACHE:
                tmp = _read_icon_file("icons/bootstrap-icons/"+icon_name.replace('--','/')+".svg")
                if tmp:
                    ICON_CACHE[icon_name] = tmp
                else:
                    return mark_safe("<i></i>")
            icon = ICON_CACHE[icon_name]
            if width:
                icon = icon.replace('width="16"', ('width="%d"' % width)).replace('height="16"', 'height="%d"' % (height if height else width))
            return mark_safe("<i>%s</i>" % icon)
    elif class_str.startswith('icon-'):
        x = re.findall('icon-' + r'[\w-]+', class_str)
        if x:
            icon_name = x[0].replace('icon-','')
            if not icon_name in ICON_CACHE:
                tmp = _read_user_icon_file("icons/"+icon_name.replace('--','/')+".svg")
                if tmp:
                    ICON_CACHE[icon_name] = tmp
                else:
                    return mark_safe("<i></i>")
            icon = ICON_CACHE[icon_name]
            return mark_safe("<i>%s</i>" % icon)
    elif class_str.startswith('svg-'):
        x = re.findall('svg-' + r'[\w-]+', class_str)
        if x:
            icon_name = x[0].replace('svg-','')
            if not icon_name in ICON_CACHE:
                tmp = _read_icon_file("icons/scalable/"+icon_name.replace('--','/')+".svg")
                if tmp:
                    ICON_CACHE[icon_name] = tmp
                else:
                    return mark_safe("<i></i>")
            icon = ICON_CACHE[icon_name]
            return mark_safe("<i>%s</i>" % icon)
    elif class_str.startswith('png://'):
        x = class_str[6:]
        x2 = x.split(' ',1)
        src = mhref("/static/icons/22x22/%s" % x2[0])
        if len(x2)>1:
            return mark_safe("<img src='%s' class='%s'></img>" % (src, x2[1]))
        else:
            return mark_safe("<img src='%s'></img>" % src)
    elif class_str.startswith('client://'):
        x = class_str[9:]
        x2 = x.split(' ', 1)
        src = mhref("/static/icons/22x22/%s" % x2[0])
        if len(x2)>1:
            return mark_safe("<img src='%s' class='%s'></img>" % (src, x2[1]))
        else:
            return mark_safe("<img src='%s'></img>" % src)
    elif class_str.startswith('data:image/svg+xml'):
        x = class_str.split(',',1)
        svg_code = x[1]
        return mark_safe(svg_code)
    elif 'fa-' in class_str:
        return mark_safe("<i class='fa %s'></i>" % class_str)
    else:
        return mark_safe("<i class='fa fa-circle-o fa-lg'></i>")
