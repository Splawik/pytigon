"""Custom template tag for rendering HTML widgets.

Provides the {% widget %} template tag that renders content inside
a Bootstrap-styled widget container, with support for width/height
parameters and Django template syntax within the widget body.
"""

from django import template
from django.template.base import token_kwargs, TemplateSyntaxError
from django.template import Template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
import contextlib

register = template.Library()


class HtmlWidgetNode(template.Node):
    """Template node that renders an HTML widget with configurable attributes."""

    def __init__(self, template_name, var, name, nodelist, extra_context=None):
        """Initialize the widget node.

        Args:
            template_name: Path to the wrapper template.
            var: Variable to bind.
            name: Name to assign in context.
            nodelist: The parsed content inside the widget tag.
            extra_context: Additional context variables.
        """
        self.nodelist = nodelist
        self.template_name = template_name
        self.extra_context = extra_context or {}
        if name:
            self.extra_context[name] = var

    def __repr__(self):
        return "<HtmlWidgetNode>"

    def render(self, context):
        """Render the widget content.

        Args:
            context: Django template context.

        Returns:
            str: Rendered HTML widget.
        """
        values = {
            key: val.resolve(context) for key, val in self.extra_context.items()
        }

        context.update(values)

        data = self.nodelist.render(context)
        # Restore template tags that were escaped for safe storage
        data = (
            data.replace("[%]", "%")
            .replace("[{", "{{")
            .replace("}]", "}}")
            .replace("[%", "{%")
            .replace("%]", "%}")
        )

        # Extract widget attributes from context
        class_name = context.get("class", "")

        # Set the template for rendering
        context["template_name"] = "widgets/html_widgets/" + class_name + ".html"

        # Build default parameters
        def_param = ""
        if "width" in context:
            def_param += "width='{}' ".format(context["width"])
            with contextlib.suppress(ValueError, TypeError):
                context["width"] = int(context["width"]) - 10
        if "height" in context:
            def_param += "height='{}' ".format(context["height"])
            with contextlib.suppress(ValueError, TypeError):
                context["height"] = int(context["height"]) - 10
        context["def_param"] = def_param

        # Render the inner template content
        t = Template(data)
        tdata = t.render(context)

        # Render the outer wrapper template
        template = get_template(self.template_name)

        context_dict = {}
        for c in context.dicts:
            context_dict.update(c)
        context_dict["data"] = tdata

        output = template.render(context_dict)

        context.pop()

        return mark_safe(output)


@register.tag("widget")
def do_widget(parser, token):
    """Parse the {% widget %} template tag.

    Required keyword arguments: id, class
    Optional keyword arguments: width, height, and any custom attributes.

    Args:
        parser: Django template parser.
        token: The template tag token.

    Returns:
        HtmlWidgetNode: The compiled template node.

    Raises:
        TemplateSyntaxError: If required parameters are missing or invalid.
    """
    bits = token.split_contents()
    remaining_bits = bits[1:]
    extra_context = token_kwargs(remaining_bits, parser, support_legacy=True)

    if not extra_context:
        raise TemplateSyntaxError(
            f"{bits[0]!r} tag expected at least one variable assignment"
        )
    if "id" not in extra_context or "class" not in extra_context:
        raise TemplateSyntaxError(
            f"{bits[0]!r} tag requires 'id' and 'class' parameters"
        )
    if remaining_bits:
        raise TemplateSyntaxError(
            f"{bits[0]!r} tag received an invalid token: {remaining_bits[0]!r}"
        )

    nodelist = parser.parse(("endwidget",))
    parser.delete_first_token()
    return HtmlWidgetNode(
        "widgets/widget.html", None, None, nodelist, extra_context=extra_context
    )
