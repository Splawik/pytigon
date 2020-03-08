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
import io
import re
import itertools
import html

from django.db import models
from django import template
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxSelectMultiple
from django.template.base import token_kwargs, TemplateSyntaxError
from django.template.base import Node


from pytigon_lib.schhtml.parser import Parser
from pytigon_lib.schtools.wiki import wiki_from_str
from pytigon_lib.schtools.href_action import standard_dict, actions_dict, action_fun
from pytigon_lib.schdjangoext.tools import import_model

from pytigon_lib.schdjangoext.tools import make_href
from pytigon_lib.schdjangoext.fields import ForeignKey, ModelSelect2WidgetExt
from pytigon_lib.schdjangoext.models import TreeModel
from pytigon_lib.schtools.wiki import wiki_from_str, wikify



from django.forms import FileInput, CheckboxInput, RadioSelect, CheckboxSelectMultiple
from django.utils.safestring import SafeText
from django import forms



register = template.Library()


def inclusion_tag(file_name):
    def dec(func):
        def func2(context, *argi, **argv):
            ret = func(context, *argi, **argv)
            t = get_template(file_name)
            return t.render(ret, context.request)
        return register.simple_tag(takes_context=True, name=getattr(func, '_decorated_function', func).__name__)(func2)
    return dec


def mark_safe2(x):
    if type(x)==str:
        return mark_safe(x.replace('<', '[').replace('>', ']'))
    else:
        return x


# ROW ACTIONS

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
    ret = action_fun(context, action, title, icon_name, target, attrs, tag_class, url)
    return ret

# Actions

@inclusion_tag('widgets/view_row.html')
def view_row(context, title = "", icon_name = "", target = "popup_info", attrs = "", tag_class = "", url = ""):
    if url:
        href=url
    else:
        href = "{tp}%s/_/view/" % context['object'].id
    ret = action_fun(context, 'view_row', title, icon_name, target, attrs,tag_class, href)
    return ret


@inclusion_tag('widgets/get_row.html')
def get_row(context, title = "", icon_name = "", target = "", attrs = "", tag_class = "", url = ""):
    ret = action_fun(context, 'get_row', title, icon_name, target, attrs, tag_class, url)
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


@inclusion_tag('widgets/list_action.html')
def list_action(context, action, title="", icon_name="", target='_top', attrs='', tag_class="", url="", active=False):
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


class ExprNode(template.Node):
    def __init__(self, expr_string, var_name, safe=True, escape=False):
        self.expr_string = expr_string
        self.var_name = var_name
        self.safe = safe
        self.escape = escape

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                if self.escape:
                    if self.safe:
                        context[self.var_name] = html.escape(mark_safe2(eval(self.expr_string, d)))
                    else:
                        context[self.var_name] = html.escape(eval(self.expr_string, d))
                else:
                    if self.safe:
                        context[self.var_name] = mark_safe2(eval(self.expr_string, d))
                    else:
                        context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                val = eval(self.expr_string, d)
                if val != None:
                    if self.safe:
                        ret =  mark_safe2(str(val))
                    else:
                        ret = str(val)
                    if self.escape:
                        return html.escape(ret)
                    else:
                        return ret
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


def do_expr_escape(parser, token):
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
    return ExprNode(expr_string, var_name, True, True)


do_expr_escape = register.tag('expr_escape', do_expr_escape)


def build_eval(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError('eval takes one argument')
    (tag, val_expr) = bits
    return EvalObject(val_expr)


class GetContext:
    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        if key in self.context:
            return self.context.get(key)
        else:
            return None


class EvalObject(template.Node):
    def __init__(self, val_expr):
        self.val_expr = val_expr

    def render(self, context):
        output = eval(self.val_expr, {'this': GetContext(context)})
        context['eval'] = output
        return ''


register.tag('eval', build_eval)


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
                context[self.var_name] = [0,]*16
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


@register.simple_tag(takes_context=True)
def id_num(context, name):
    if not context['standard_web_browser'] or ('doc_type' in context and context['doc_type'] == 'json' ):
        if 'paginator' in context:
            return name + ':' + str(context['paginator'].per_page) + '/'\
                 + str(context['paginator'].count)
    return name


@inclusion_tag('widgets/ok_cancel.html')
def ok_cancel(context):
    return standard_dict(context, {})


@inclusion_tag('widgets/jscript_link.html')
def jscript_link(context, href):
    return  {'href':  mark_safe(href)}

@inclusion_tag('widgets/require.html')
def require(context, href):
    return  {'href':  mark_safe(href)}

@inclusion_tag('widgets/module_link.html')
def module_link(context, href):
    return  { 'href':  mark_safe(href) }

@inclusion_tag('widgets/css_link.html')
def css_link(context, href):
    return standard_dict(context, {'href': href})


@inclusion_tag('widgets/link.html')
def link(context, href, rel, typ):
    return standard_dict(context, {'href': settings.STATIC_URL + href, 'rel': rel, 'typ': typ})


@inclusion_tag('widgets/component.html')
def component(context, name):
    return standard_dict(context, {'href': name,})


@inclusion_tag('widgets/subform.html')
def subform(context, name):
    return standard_dict(context, {'href': name,})


@inclusion_tag('widgets/paginator.html')
def paginator(context):
    return context.flatten()


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
        context['page_number'] = context['page_obj'].number
    return context.flatten()


@inclusion_tag('widgets/html_widget_js.html')
def htmlwidget_js(context):
    if 'html_widget_dict' in context:
        html_widget_tab = context['html_widget_dict']
    else:
        html_widget_tab = []
    tab2 = []
    
    for pos in html_widget_tab:
        tab2.append('widgets/html_widgets/'+pos+'_js.html') 
        
    return standard_dict(context, {'html_widget_tab': tab2,})


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

        template = get_template(self.template_name)

        context_dict = {}
        for c in context.dicts:
            context_dict.update(c)
        context_dict['data'] = tdata

        #tdata = t.render(context_dict)

        #output = template.render(context)
        output = template.render(context_dict)



        context.pop()
        
        return mark_safe(output)


@register.tag('htmlwidget')
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
    nodelist = parser.parse(('endhtmlwidget',))
    parser.delete_first_token()
    return HtmlWidgetNode("widgets/html_widget.html", None, None, nodelist, extra_context=extra_context)


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


@inclusion_tag('widgets/checkboxselectmultiple.html')
def checkboxselectmultiple(context, field, only_field=False):
    field.field.widget = CheckboxSelectMultiple(choices=field.field.choices)
    field.field.widget.attrs['class'] = "list-group row"

    return standard_dict(context, {'field': field, 'only_field': only_field})


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


@inclusion_tag('widgets/form2columns.html')
def form2columns(context, fields):
    ftab = fields.split(';')
    it = iter(ftab)
    fields2 = itertools.zip_longest(it,it)
    return standard_dict(context, {'fields': ftab, 'fields2': fields2, 'form': context['form']})


@inclusion_tag('widgets/frame.html')
def frame(context, href, height):
    return standard_dict(context, {'href': href, 'height': height })


_collapse_str = """
        <div class="alert alert-warning" role="alert">
            <a class="collapsed" data-toggle="collapse" href="#{id}/" aria-expanded="false">
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
        raise TemplateSyntaxError("%r expected at least one variable assignment" % bits[0])
    if remaining_bits:
        raise TemplateSyntaxError("%r received an invalid token: %r" % (bits[0], remaining_bits[0]))
    nodelist = parser.parse(('endcollapse',))
    parser.delete_first_token()
    return CollapseNode(nodelist, extra_context=extra_context)


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


class RecurseTreeNode(template.Node):
    def __init__(self, template_nodes, queryset_var):
        self.template_nodes = template_nodes
        self.queryset_var = queryset_var

    def _render_node(self, context, node):
        bits = []
        context.push()

        queryset = self.queryset_var.resolve(context)
        children = queryset.filter(parent=node)

        for child in children:
            bits.append(self._render_node(context, child))
        context['node'] = node
        context['children'] = mark_safe(''.join(bits))
        rendered = self.template_nodes.render(context)
        context.pop()
        return rendered

    def render(self, context):
        queryset = self.queryset_var.resolve(context)

        roots = queryset.filter(parent=None)

        bits = [self._render_node(context, node) for node in roots]
        return ''.join(bits)


@register.tag
def recursetree(parser, token):
    """
    Iterates over the nodes in the tree, and renders the contained block for each node.
    This tag will recursively render children into the template variable {{ children }}.
    Only one database query is required (children are cached for the whole tree)

    Usage:
            <ul>
                {% recursetree nodes %}
                    <li>
                        {{ node.name }}
                        {% if not node.is_leaf_node %}
                            <ul>
                                {{ children }}
                            </ul>
                        {% endif %}
                    </li>
                {% endrecursetree %}
            </ul>
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a queryset') % bits[0])

    queryset_var = template.Variable(bits[1])

    template_nodes = parser.parse(('endrecursetree',))
    parser.delete_first_token()

    return RecurseTreeNode(template_nodes, queryset_var)


@register.simple_tag
def spec(format):
    return format.replace('{', '{{').replace('}', '}}').replace('[', '{%').replace(']', '%}')


#@inclusion_tag('widgets/fields.html')
#def fields(context, fieldformat):
#    ret = {}
#    fields = []
#    for pos in fieldformat.strip().split(';'):
#        pos2 = pos.strip()
#        if pos2:
#            if '/' in pos2:
#                x = pos.split('/')
#                fields.append((x[0],int(x[1]),))
#            else:
#                fields.append((pos2,12))
#    ret['fields'] = fields
#    ret['form'] = context['form']
#    return ret

#fieldformat:
#   label_format/input_format/size/addon
#label_format:
#size:size:size - bootstrap size for .col-sm, .col-md, col-lg or:
# ^ - for floating label or
# empty - for label above input field
#input format:
#size:size:size - bootstrap size for .col-sm, .col-md, col-lg

@inclusion_tag('widgets/field.html')
def field(context, form_field, fieldformat=None):
    if type(form_field) in (SafeText, str,):
        field = context['form'][form_field]
    else:
        field = form_field

    label_class = "control-label float-left"
    offset = ""
    form_group_class = "form-group bmd-form-group row group_%s" % type(field.field).__name__.lower()
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
                label_class += " col-sm-%d col-md-%d col-lg-%s" % (y[0], y[1], y[2])
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
                if   addon.startswith('(-X)'):
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


@inclusion_tag('widgets/get_table_row.html')
def get_table_row(context, field_or_name, prj=None, app_name=None, table_name=None, search_fields=None, filter=None, label = None,
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
            href1 = make_href("/%s/%s/table/%s/%s/0/form/gettree/?schtml=1" % (prj, _app_name, _table_name, filter))
            href2 = make_href("/%s/%s/table/%s/-/add/?schtml=1" % (prj, _app_name, _table_name))
        else:
            href1 = make_href("/%s/%s/table/%s/0/form/gettree/?schtml=1" % (prj, _app_name, _table_name))
            href2 = make_href("/%s/%s/table/%s/-/add/?schtml=1" % (prj, _app_name, _table_name))
    else:
        _filter = filter if filter else "-"
        href1 = make_href("/%s/%s/table/%s/%s/form/get/?schtml=1" % (prj, _app_name, _table_name, _filter))
        href2 = make_href("/%s/%s/table/%s/%s/add/?schtml=1" % (prj, _app_name, _table_name, _filter))

    class _Form(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print("X1:", href1, href2)
            self.fields[_name] = forms.ChoiceField(
                label = _label,
                widget=ModelSelect2WidgetExt(href1, href2, is_new_button, is_get_button, _label,
                    model=model,
                    search_fields=[_search_fields, "description__icontains"],
                    queryset = _queryset,
                ),
            )
    form = _Form(initial = { _name: _initial })
    return { 'form': form, 'field': form[_name], "formformat": formformat, }


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
def wiki (context, wiki_str, path=None, section = None,  only_header=True):
    return mark_safe(wikify(wiki_str, path, section))


@register.simple_tag(takes_context=True)
def subtemplate(context, template_string):
    t = Template(template_string)
    return mark_safe(t.render(context))
