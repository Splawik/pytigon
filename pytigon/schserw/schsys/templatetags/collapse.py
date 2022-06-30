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
from base64 import b64encode
from django.template.base import token_kwargs, TemplateSyntaxError
from django.template.base import Node


register = template.Library()


_collapse_str = """
        <div class="alert alert-warning" role="alert">
            <a class="collapsed" data-bs-toggle="collapse" href="#{id}/" aria-expanded="false">
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
        var = {
            "data": self.nodelist.render(context),
            "id": self.extra_context["id"].resolve(context),
            "title": self.extra_context["title"].resolve(context),
        }
        if context["standard_web_browser"]:
            var["data"] = data
            return _collapse_str.format(**var)
        var["data"] = b64encode(data.encode("utf-8")).decode("utf-8")
        return _collapse_str_schweb.format(**var)


@register.tag
def collapse(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)
    if not extra_context:
        raise TemplateSyntaxError(
            "%r expected at least one variable assignment" % bits[0]
        )
    if remaining_bits:
        raise TemplateSyntaxError(
            "%r received an invalid token: %r" % (bits[0], remaining_bits[0])
        )
    nodelist = parser.parse(("endcollapse",))
    parser.delete_first_token()
    return CollapseNode(nodelist, extra_context=extra_context)
