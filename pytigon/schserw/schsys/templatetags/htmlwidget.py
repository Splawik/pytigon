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


from django import template
from django.template.base import token_kwargs, TemplateSyntaxError


register = template.Library()


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
def do_widget(parser, token):
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
