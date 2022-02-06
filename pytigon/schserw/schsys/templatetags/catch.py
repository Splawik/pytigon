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

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

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
        if "VAR" in context:
            context["VAR"][self.var_name] = mark_safe(output)
        else:
            context["VAR"] = {self.var_name: mark_safe(output)}
        return ""


def do_catch(parser, token):
    """Catch the content and save it to var_name
    Example::
    {% catch as var_name %} ... {% endcatch %}
    """

    try:
        (tag_name, arg) = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents[0]
        )
    m = re.search(r"as (\w+)", arg)
    if not m:
        raise template.TemplateSyntaxError(
            '%r tag should define as "%r as var_name"' % (tag_name, tag_name)
        )
    var_name = m.groups()[0]
    nodelist = parser.parse(("endcatch",))
    parser.delete_first_token()
    return CatchNode(nodelist, var_name)


do_catch = register.tag("catch", do_catch)
