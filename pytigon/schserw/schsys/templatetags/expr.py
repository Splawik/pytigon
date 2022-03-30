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

import re
import html

from django import template
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

register = template.Library()


def mark_safe2(x):
    if type(x) == str:
        return mark_safe(x.replace("<", "[").replace(">", "]"))
    else:
        return x


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
            d["_"] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                if self.escape:
                    if self.safe:
                        context[self.var_name] = html.escape(
                            mark_safe2(eval(self.expr_string, d))
                        )
                    else:
                        context[self.var_name] = html.escape(eval(self.expr_string, d))
                else:
                    if self.safe:
                        context[self.var_name] = mark_safe2(eval(self.expr_string, d))
                    else:
                        context[self.var_name] = eval(self.expr_string, d)
                return ""
            else:
                try:
                    val = eval(self.expr_string, d)
                except:
                    print("ERROR:")
                    print(self.expr_string)
                    print(d)
                    print("------------------------------")
                    val = None
                if val != None:
                    if self.safe:
                        ret = mark_safe2(str(val))
                    else:
                        ret = str(val)
                    if self.escape:
                        return html.escape(ret)
                    else:
                        return ret
                else:
                    return ""
        except:
            print("EXPR ERROR:", self.expr_string)
            raise


r_expr = re.compile(r"(.*?)\s+as\s+(\w+)", re.DOTALL)


def do_expr(parser, token):
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0]
        )
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name
            )
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, False)


do_expr = register.tag("expr", do_expr)


def do_expr_safe(parser, token):
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0]
        )
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name
            )
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, True)


do_expr_safe = register.tag("expr_safe", do_expr_safe)


def do_expr_escape(parser, token):
    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0]
        )
    m = r_expr.search(arg)
    if m:
        (expr_string, var_name) = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError(
                "%r tag at least require one argument" % tag_name
            )
        (expr_string, var_name) = (arg, None)
    return ExprNode(expr_string, var_name, True, True)


do_expr_escape = register.tag("expr_escape", do_expr_escape)


def build_eval(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("eval takes one argument")
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
        output = eval(self.val_expr, {"this": GetContext(context)})
        context["eval"] = output
        return ""


register.tag("eval", build_eval)
