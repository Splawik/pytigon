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

from __future__ import unicode_literals

from base64 import b64encode, b64decode

from django import template
from django.utils.translation import gettext_lazy as _
import re
from django.template.loader import get_template
from django.template import Context, Template, RequestContext


from django.conf import settings
from schlib.schtools.wiki import wiki_from_str
from django.utils import six
from django.utils.safestring import mark_safe

from django.forms.widgets import CheckboxSelectMultiple

from django.template.base import token_kwargs, TemplateSyntaxError

from django.template.base import Node


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, MultiField, Field, Hidden
from crispy_forms.bootstrap import (
    PrependedAppendedText, AppendedText, PrependedText, InlineRadios,
    Tab, TabHolder, AccordionGroup, Accordion, Alert, InlineCheckboxes,
    FieldWithButtons, StrictButton
)

#from templatetag_sugar.register import tag
#from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model

import itertools

register = template.Library()


def inclusion_tag(file_name):
    def dec(func):
        def func2(context, *argi, **argv):
            ret = func(context, *argi, **argv)
            t = get_template(file_name)
            c = Context(context)
            c.update(ret)
            return t.render(c)
        return register.simple_tag(takes_context=True, name=getattr(func, '_decorated_function', func).__name__)(func2)
    return dec


def mark_safe2(x):
    if type(x)==str:
        return mark_safe(x.replace('<', '[').replace('>', ']'))
    else:
        return x

STANDARD_DESC = {
    'default': ('Default', "class='btn btn-sm btn-default' data-role='button' data-inline='true' data-mini='true' "),
    'edit': ('Update', "class='popup btn btn-sm btn-primary' data-role='button' data-inline='true' data-mini='true' |class='popup' "),
    'edit2': ('Update', "class='popup btn btn-sm btn-primary' data-role='button' data-inline='true' data-mini='true' |class='popup' "),
    'delete': ('Delete',  "class='popup_delete btn btn-sm btn-danger' data-role='button' data-inline='true' data-mini='true' |class='popup_delete' "),
    'delete2': ('Delete',  "class='popup_delete btn btn-sm btn-danger' data-role='button' data-inline='true' data-mini='true' |class='popup_delete' "),
}


STANDARD_URL = {
    'action': "../../../{id}/action/{action}?childwin=1",
    'edit': "../../../{id}/{action}?childwin=1",
    'edit2': "./{id}/{action}?childwin=1",
    'delete': "../../../{id}/{action}?childwin=1",
    'delete2': "./{id}/{action}?childwin=1",
    'pdf': "../../../{id}/pdf/view/",
    'odf': "../../../{id}/odf/view/",
    'field_list': "{base_path}../{object_name}/{id}/{x1}/-/form/list?childwin=1",
    'field_edit': "{base_path}../{object_name}/{id}/{x1}/py/editor?childwin=1",
}

STANDARD_URL_CHILD_TAB = {
    'action': "{base_path}../{table_name}/{id}/action/{action}?childwin=1",
    'field_list': "{base_path}../{object_name}/{id}/{x1}/-/form/list?childwin=1",
    'field_edit': "{base_path}../{object_name}/{id}/{x1}/py/editor?childwin=1",
}

STANDARD_ICON = {
    'edit':  ['glyphicon-edit', 'edit'],
    'edit2':  ['glyphicon-edit', 'edit'],
    'delete': ['glyphicon-trash', 'delete'],
    'delete2': ['glyphicon-trash', 'delete'],
    'print': ['glyphicon-print', 'arrow-d'],
    'pdf': ['glyphicon-eye-open', 'eye'],
    'odf': ['glyphicon-list', 'bullets'],
    'field_list': ['glyphicon-th', 'grid'],
    'field_edit': ['glyphicon-edit', 'edit'],
}


class Action:
    def __init__(self, actions_str, context, d):
        #actions_str: action,title,name,target,style,url
        self.d = d
        self.context = context
        self.action = ""
        self.title = ""
        self.name = ""
        self.target = ""
        self.style = ""
        self.style_in_menu = ""
        self.url = ""

        self.x1 = ""
        self.x2 = ""
        self.x3 = ""

        pos = actions_str.split(',')
        action = pos[0]

        if '/' in action:
            x = action.split('/')
            self.x1 = x[1]
            if len(x)>2:
                self.x2 = x[2]
                if len(x)>3:
                    self.x3 = x[3]
            self.d['action'] = self.action =  x[0]
        else:
            self.d['action'] = self.action = action

        self.d['x1'] = self.x1
        self.d['x2'] = self.x2
        self.d['x3'] = self.x3

        if len(pos)>1:
            self.title = pos[1].strip()
            if len(pos)>2:
                self.name = pos[2].strip()
                if len(pos)>3:
                    self.target = pos[3].strip()
                    if len(pos)>4:
                        self.style = pos[4].strip()
                        if len(pos)>5:
                            self.url = pos[5].strip()

        action2 = self.action.split('__')[0]

        if not self.title:
            if action2 in STANDARD_DESC:
                self.title = STANDARD_DESC[action2][0]
            else:
                self.title = action.replace('/', '_')

        if not self.name:
            self.name = action.replace('/', '_')

        if not self.target:
            if context['standard_web_browser']:
                #if context['default_template'] == 'template/mobile.html':
                #    self.target = '_self'
                #else:
                self.target = '_top'
            else:
                self.target = '_blank'

        if not self.style :
            if action2 in STANDARD_DESC:
                self.style = STANDARD_DESC[action2][1]
            else:
                self.style = STANDARD_DESC['default'][1]
        else:
            if self.style[0]=='+':
                if action2 in STANDARD_DESC:
                    self.style = STANDARD_DESC[action2][1] + self.style[1:]
                else:
                    self.style = STANDARD_DESC['default'][1] + self.style[1:]


        if '|' in self.style:
            x = self.style.split('|')
            self.style = x[0]
            self.style_in_menu = x[1]

        if not self.url:
            if action == 'field_up':
                pass
            if 'rel_field' in context and context['rel_field']:
                if action2 in STANDARD_URL_CHILD_TAB:
                    self.url = self.format(STANDARD_URL_CHILD_TAB[action2])
                else:
                    if action2 in STANDARD_URL:
                        self.url = self.format(STANDARD_URL[action2])
                    else:
                        self.url = self.format(STANDARD_URL_CHILD_TAB['action'])
            else:
                if action2 in STANDARD_URL:
                    self.url = self.format(STANDARD_URL[action2])
                else:
                    self.url = self.format(STANDARD_URL['action'])
        else:
            self.url = self.format(self.url)
        if action2 in STANDARD_ICON:
            self.icon = STANDARD_ICON[action2]
        else:
            self.icon = None

        if self.icon and context['browser_type']=='mobile':
            self.style = self.style + " data-iconpos='notext' data-icon='%s' " % self.icon[1]


    def format(self, s):
        return s.format(**self.d)

def actions_dict(
    context,
    actions_str, # action,title,name,target,style,url
    ):
    d = standard_dict(context, {})
    if 'object' in context:
        if hasattr(context['object'], '_meta'):
            d['table_name'] = context['object']._meta.object_name
            d['id'] = context['object'].id
            d['object_name'] = context['object']._meta.object_name
        else:
            d['table_name'] = 'user_table'
            d['id'] = context['object']['id']
            d['object_name'] = 'object_name'

    else:
        d['table_name'] = None
        d['id'] = 0
        d['object_name'] = None

    if 'rel_field' in context and context['rel_field']:
        d['child_tab'] = True
    else:
        d['child_tab'] = False

    actions = []
    actions2 = []
    test_actions2 = False
    act = actions
    for pos2 in actions_str.split(';'):
        pos=pos2.strip()
        if not pos:
            continue
        if pos[0]=='|':
            act = actions2
            test_actions2 = True
        else:
            action = Action(pos, context, d)
            act.append(action)

    if not test_actions2 and len(actions)>2 and context['standard_web_browser']:
        actions2=actions[1:]
        actions = actions[:1]

    d['actions'] = actions
    d['actions2'] = actions2

    d['browser_type'] = context['browser_type']

    if len('actions')>0:
        d['action'] = actions[0]
    else:
        d['action'] = actions2[0]
    return d


# ROW ACTIONS

class RowActionNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        t = Template(output)
        output2 = t.render(context).replace('\n',';')
        t = get_template('widgets/row_actions.html')
        d = actions_dict(context, output2)
        c = Context(d)
        return t.render(c)

@register.tag
def row_actions(parser, token):
    nodelist = parser.parse(('endrow_actions',))
    parser.delete_first_token()
    return RowActionNode(nodelist)

@inclusion_tag('widgets/view_row.html')
#@register.simple_tag(takes_context=True)
def view_row(
    context,
    description,
    target='',
    ):
    href = "../../../%s/_/view/" % context['object'].id
    #href = "../../../%s/_/view/" % object_id
    ret = action_fun(context, 'view_row', description, 'view_row', target, "", href)
    return ret
    #t = get_template('widgets/view_row.html')
    #c = RequestContext(context['request'], context)
    #c = Context(context)

    #for (key, value) in ret.items():
    #    c[key] = value
    #x =  t.render(c)
    #return x
    #return ret


    #return standard_dict(context, {
    #    'description': description,
    #    'href': href,
    #    'id': context['object'].id,
    #    })


# ACTIONS

#@inclusion_tag('widgets/action.html')
def action_fun(
    context,
    action,
    title="",
    name="",
    target="",
    style="",
    url=""
    ):
    action_str = "%s,%s,%s,%s,%s,%s" % (action, title, name, target, style, url)
    t = Template(action_str)
    output2 = t.render(context)
    #t = get_template('widgets/action.html')
    d = actions_dict(context, output2)
    return standard_dict(context, d)


@inclusion_tag('widgets/button.html')
def button(
    context,
    url,
    title="",
    name="",
    target="",
    style=''
    ):
    ret = action_fun(context, 'button', title, name, target, style, url)
    return ret


@inclusion_tag('widgets/new_row.html')
def new_row(
    context,
    title="",
    name="",
    target='',
    style='',
    url=""
    ):
    ret = action_fun(context, 'new_row', title, name, target, style, url if url else '../../../-/add?childwin=1')
    if title and title[0] == '+':
        description = title[1:]
        title = ""
    else:
        description = title
    ret['description'] = description
    return ret



@inclusion_tag('widgets/list_action.html')
def list_action(
    context,
    action,
    id,
    title="",
    name="",
    target='_blank',
    style='',
    url=""
    ):
    ret = action_fun(context, action, title, name, target, style, url if url else "../../../action/%s?childwin=1" % action)
    return ret


@inclusion_tag('widgets/wiki_button.html')
def wiki_button(
    context,
    subject,
    wiki_description,
    style="",
    target='_self',
    url=""
    ):
    wiki_name = wiki_from_str(wiki_description)
    wiki_url = "/schwiki/%s/%s/view/?childwin=1" % (subject, wiki_name)
    return action_fun(context, "wiki", wiki_description, wiki_name, target, style, url if url else wiki_url)


@inclusion_tag('widgets/wiki_link.html')
def wiki_link(
    context,
    subject,
    wiki_description,
    style="",
    target='_self',
    url=""
    ):
    return wiki_button(context, subject, wiki_description, style, target, url)


# This tag can be used to calculate a python expression, and save it into a
# template variable which you can reuse later or directly output to template. So
# if the default django tag can not be suit for your need, you can use it. How
# to use it {% expr "1" as var1 %} {% expr [0, 1, 2] as var2 %} {% expr
# _('Menu') as var3 %} {% expr var1 + "abc" as var4 %} ... {{ var1 }} for 0.2
# version {% expr 3 %} {% expr "".join(["a", "b", "c"]) %} Will directly output
# the result to template Syntax {% expr python_expression as variable_name %}
# python_expression can be valid python expression, and you can even use _() to
# translate a string. Expr tag also can used context variables.

class ExprNode(template.Node):

    def __init__(self, expr_string, var_name, safe=True):
        self.expr_string = expr_string
        self.var_name = var_name
        self.safe = safe

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                if self.safe:
                    context[self.var_name] = mark_safe2(eval(self.expr_string, d))
                else:
                    context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                #try:
                val = eval(self.expr_string, d)
                #except:
                #    #val = '!!!' + str(sys.exc_info()[1]) + ": " + self.expr_string
                #    val =self.expr_string
                if val != None:
                    if self.safe:
                        return mark_safe2(str(val))
                    else:
                        return str(val)
                else:
                    return ''
        except:
            print("EXPR ERROR:", self.expr_string)
            raise


r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


def do_expr(parser, token):
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments'\
             % token.contents[0])
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError('%r tag at least require one argument' % tag_name)
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, False)


do_expr = register.tag('expr', do_expr)


def do_expr_safe(parser, token):
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments'\
             % token.contents[0])
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError('%r tag at least require one argument' % tag_name)
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, True)


do_expr_safe = register.tag('expr_safe', do_expr_safe)


#
# You can use this tag to "catch" some template snippets and save it into a
# context variable, then use this variable later.
#
# How to use it
#
# {% catch as var1 %}any tags and html content{% endcatch %} ... {{ var1 }}


class CatchNode(template.Node):

    def __init__(self, nodelist, var_name):
        self.nodelist = nodelist
        self.var_name = var_name

    def render(self, context):
        output = self.nodelist.render(context)
        if 'VAR' in context:
            context['VAR'][self.var_name] = output
        else:
            context['VAR'] = {self.var_name: output}
        return ''


def do_catch(parser, token):
    """Catch the content and save it to var_name
    Example::
    {% catch as var_name %} ... {% endcatch %}
    """

    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires arguments'\
             % token.contents[0])
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError('%r tag should define as "%r as var_name"' % (tag_name, tag_name))
    var_name = m.groups()[0]
    nodelist = parser.parse(('endcatch', ))
    parser.delete_first_token()
    return CatchNode(nodelist, var_name)


do_catch = register.tag('catch', do_catch)


class SumNode(template.Node):

    def __init__(self, var_name, parm):
        if var_name:
            self.var_name = var_name
        else:
            self.var_name = 'sumtab'
        self.parm = parm

    def render(self, context):
        try:
            if not self.parm:
                context[self.var_name] = [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    ]
                return ''
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                d.update(c)
            if len(self.parm[1]) > 0:
                id = int(eval(self.parm[0], d))
                context[self.var_name][id] = context[self.var_name][id]\
                     + eval(self.parm[1], d)
                return ''
            if self.parm[0] == '*':
                tab = context[self.var_name]
                for i in range(16):
                    tab[i] = 0
            else:
                id = int(eval(self.parm[0], d))
                context[self.var_name][id] = 0
            return ''
        except:
            raise


r_sum = re.compile(r'(.*?)\s*as\s+(\w+)', re.DOTALL)


def do_sumtab(parser, token):
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        return SumNode(None, None)
    expr_string = None
    m = r_sum.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        var_name = None
        expr_string = arg
    if expr_string:
        parm = expr_string.split(':')
        if len(parm) > 1:
            return SumNode(var_name, parm)
    return SumNode(var_name, None)


do_sumtab = register.tag('sumtab', do_sumtab)


def standard_dict(context, parm):
    parm['standard_web_browser'] = context['standard_web_browser']
    if 'rel_field' in context and context['rel_field']:
        parm['base_path'] = '../../../../../'
    else:
        parm['base_path'] = '../../../'
    path = context['request'].path
    if not path.endswith('/'):
        path = path+'/'
    parm['request'] = context['request']
    parm['path'] = path
    return parm


@register.simple_tag(takes_context=True)
def id_num(context, name):
    if not context['standard_web_browser']:
        if 'paginator' in context:
            return name + ':' + str(context['paginator'].per_page) + '/'\
                 + str(context['paginator'].count)
    return name


@inclusion_tag('widgets/ok_cancel.html')
def ok_cancel(context):
    return standard_dict(context, {})


@inclusion_tag('widgets/jscript_link.html')
def jscript_link(context, href):
    return standard_dict(context, {'href': settings.STATIC_URL + href})


@inclusion_tag('widgets/css_link.html')
def css_link(context, href):
    return standard_dict(context, {'href': settings.STATIC_URL + href})


@inclusion_tag('widgets/link.html')
def link(context, href, rel, typ):
    return standard_dict(context, {'href': settings.STATIC_URL + href, 'rel': rel, 'typ': typ})



@inclusion_tag('widgets/paginator.html')
def paginator(context):
    return context

@inclusion_tag('widgets/paginator.html')
def paginator2(context):

    context['page_range'] = []

    if 'paginator' in context and 'page_obj' in context:
        if context['paginator'].page_range[-1] > 15:
            nr = context['page_obj'].number
            start = nr - 5
            end = nr + 5
            if start < 0:
                end += -1 * start
                start = 0
            if end > context['paginator'].page_range[-1]:
                start -= end - context['paginator'].page_range[-1]
                end = context['paginator'].page_range[-1]

            context['page_range'] = context['paginator'].page_range[start+1:end-1]
            context['page_all'] = False
        else:
            context['page_range'] = context['paginator'].page_range
            context['page_all'] = True

        context['page_last'] = context['paginator'].page_range[-1]

    return context


@inclusion_tag('widgets/html_widget_js.html')
def htmlwidget_js(context):
    if 'html_widget_dict' in context:
        html_widget_tab = context['html_widget_dict']
    else:
        html_widget_tab = []
    tab2 = []
    
    for pos in html_widget_tab:
        tab2.append('widgets/html_widgets/'+pos+'_js.html') 
        
    return standard_dict(context, {
        'html_widget_tab': tab2,
        })


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
        values = dict([(key, val.resolve(context)) for key, val in
                       six.iteritems(self.extra_context)])
                               
        context.update(values)
        
        data = self.nodelist.render(context)   
        data = data.replace('[[','{{').replace(']]', '}}').replace('[%', '{%').replace('%]', '%}')              
        id = context['id']
        class_name = context['class'] 
        
        context['template_name'] = "widgets/html_widgets/"+class_name+".html"
        def_param = ""
        if 'width' in context:
            def_param = def_param+"width='%s' " % context['width']
            try:
                context['width']=int(context['width'])-10
            except:
                pass
        if 'height' in context:
            def_param = def_param+"height='%s' " % context['height']
            try:
                context['height']=int(context['height'])-10
            except:
                pass
        context['def_param'] = def_param

        t = Template(data)
        tdata = t.render(context)
        
        context['data'] = tdata

        template = get_template(self.template_name)
        output = template.render(context)
        
        context.pop()
        
        return mark_safe(output)


@register.tag('htmlwidget')
def do_html_widget(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError("%r expected at least one variable "
                                  "assignment" % bits[0])
    if not 'id' in extra_context or not 'class' in extra_context:
        raise TemplateSyntaxError("id and class parameters are required")
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0]))
    nodelist = parser.parse(('endhtmlwidget',))
    parser.delete_first_token()
    return HtmlWidgetNode("widgets/html_widget.html", None, None, nodelist, extra_context=extra_context)


@register.tag('widget')
def do_html_widget(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError("%r expected at least one variable "
                                  "assignment" % bits[0])
    if not 'id' in extra_context or not 'class' in extra_context:
        raise TemplateSyntaxError("id and class parameters are required")
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0]))
    nodelist = parser.parse(('endwidget',))
    parser.delete_first_token()
    return HtmlWidgetNode("widgets/widget.html", None, None, nodelist, extra_context=extra_context)


@inclusion_tag('widgets/checkboxselectmultiple.html')
def checkboxselectmultiple(
    context,
    field,
    only_field=False
    ):
    field.field.widget = CheckboxSelectMultiple(choices=field.field.choices)
    field.field.widget.attrs['class'] = "list-group"

    return standard_dict(context, {
        'field': field,
        'only_field': only_field
        })


class Form(Node):
    def __init__(self, nodelist, form_class = None):
        self.nodelist = nodelist
        self.form_class = form_class

    def render(self, context):
        output = self.nodelist.render(context).strip()

        form = context['form']
        form.helper = FormHelper(form)
        form.helper.form_tag = False
        form.helper.disable_csrf = True
        form.helper.label_class = "formitem"

        if not ('vform' in context and context['vform'] == True):
            if self.form_class:
                if self.form_class == 'form-horizontal':
                    form.helper.form_class = self.form_class
                    form.helper.label_class = 'col-lg-3'
                    form.helper.field_class = 'col-lg-9'
                else:
                    form.helper.form_class = 'form-inline'
                    form.helper.field_template = 'bootstrap3/layout/inline_field.html'

        if output:
            form.helper.layout = eval("Layout("+output.replace('[[', '{{').replace(']]', '}}')+")")
        t = Template("""{% load crispy_forms_tags %}{% crispy form %}""")
        return t.render(context)


@register.tag
def form(parser, token):
    nodelist = parser.parse(('endform'))
    parser.delete_first_token()
    return Form(nodelist, 'form-horizontal')


@register.tag
def vert_form(parser, token):
    nodelist = parser.parse(('endvert_form',))
    parser.delete_first_token()
    return Form(nodelist, None)


@register.tag
def inline_form(parser, token):
    nodelist = parser.parse(('endinline_form',))
    parser.delete_first_token()
    return Form(nodelist, 'form-inline')


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
            elem0 = """ <%s class="%s form-control" name="%s" id="id_%s"> """ % (self.tag, self.field_name, self.field_name, self.field_name)
            elem1 = "</%s>" % self.tag
        else:
            elem0 = ""
            elem1 = ""

        ret = """ <div id="div_id_%s" class="form-group">
            <label for="id_%s" class="control-label">%s</label>
            <div class="controls">
            %s%s%s
            </div></div>
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


@inclusion_tag('widgets/form2columns.html')
def form2columns(context, fields):
    ftab = fields.split(';')
    it = iter(ftab)
    fields2 = itertools.zip_longest(it,it)
    return standard_dict(context, {'fields': ftab, 'fields2': fields2, 'form': context['form']})


@inclusion_tag('widgets/frame.html')
def frame(context, id, href, height):
    return standard_dict(context, {'id': id, 'href': href, 'height': height })



_collapse_str = """
        <div class="alert alert-warning" role="alert">
            <a class="collapsed" data-toggle="collapse" href="#{id}" aria-expanded="false">
                {title}
            </a>
        </div>
        <div id="{id}" class="panel-collapse collapse" role="tabpanel" aria-labelledby="{id}_heading">
            {data}
        </div>
"""

_collapse_str_schweb = """
        <CTRLCOLLAPSIBLE_PANEL id="{id}" label='{title}' width='100%'>
            <data>{data}</data>
        </CTRLCOLLAPSIBLE_PANEL>
"""

class CollapseNode(Node):
    def __init__(self, nodelist, extra_context):
        self.nodelist = nodelist
        self.extra_context = extra_context

    def render(self, context):
        data = self.nodelist.render(context)
        var = { 'data': self.nodelist.render(context), 'id': self.extra_context['id'].resolve(context), 'title': self.extra_context['title'].resolve(context) }
        if context['standard_web_browser']:
            var['data'] = data
            return _collapse_str.format(**var)
        var['data'] = b64encode(data.encode('utf-8')).decode('utf-8')
        return _collapse_str_schweb.format(**var)


@register.tag   
def collapse(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError("%r expected at least one variable "
                                  "assignment" % bits[0])
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0                                                                                                                                                                                                                                                                                                                        ]))
    nodelist = parser.parse(('endcollapse',))
    parser.delete_first_token()
    return CollapseNode(nodelist, extra_context=extra_context)


@register.tag('widget')
def do_html_widget(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError("%r expected at least one variable "
                                  "assignment" % bits[0])
    if not 'id' in extra_context or not 'class' in extra_context:
        raise TemplateSyntaxError("id and class parameters are required")
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0]))
    nodelist = parser.parse(('endwidget',))
    parser.delete_first_token()
    return HtmlWidgetNode("widgets/widget.html", None, None, nodelist, extra_context=extra_context)


class ComponentNode(template.Node):
    def __init__(self, template_name, nodelist, extra_context=None):
        self.nodelist = nodelist
        self.template_name = template_name
        self.extra_context = extra_context or {}


    def __repr__(self):
        return "<ComponentNode>"


    def render(self, context):
        values = dict([(key, val.resolve(context)) for key, val in
                       six.iteritems(self.extra_context)])
        context.update(values)

        if not 'create_div' in context:
            context['create_div'] = True
        if not 'param' in context:
            context['param'] = 'null'
        if not 'class' in context:
            context['class'] = None
        if context['class'] and '/' in context['class']:
            x = context['class'].split('/')
            context['class'] = x[1]
            context['module'] = x[0]

        data = self.nodelist.render(context)
        t = Template(data)
        data2 = t.render(context)
        context['data'] = mark_safe(data2)
        t = get_template(self.template_name)
        return mark_safe(t.render(context))


@register.tag('component')
def component(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError("%r expected at least one variable "
                                  "assignment" % bits[0])
    if not 'id' in extra_context:
        raise TemplateSyntaxError("id and class parameters are required")
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" %
                                  (bits[0], remaining_bits[0]))
    nodelist = parser.parse(('endcomponent',))
    parser.delete_first_token()
    return ComponentNode("widgets/component.html", nodelist, extra_context=extra_context)


