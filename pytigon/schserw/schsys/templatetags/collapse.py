from django import template
from base64 import b64encode
from django.template.base import token_kwargs, TemplateSyntaxError
from django.template.base import Node


register = template.Library()

# Template strings for collapse functionality
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
    """Node for rendering collapse content in templates."""

    def __init__(self, nodelist, extra_context):
        self.nodelist = nodelist
        self.extra_context = extra_context

    def render(self, context):
        """Render the collapse content based on the context."""
        try:
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
        except Exception as e:
            raise TemplateSyntaxError(f"Error rendering collapse node: {e}")


@register.tag
def collapse(parser, token):
    """Template tag for creating a collapse section."""
    try:
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
    except Exception as e:
        raise TemplateSyntaxError(f"Error parsing collapse tag: {e}")
