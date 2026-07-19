"""Inclusion template tags for Pytigon exsyntax library."""

import logging
import os

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from pytigon_lib.schtools.href_action import standard_dict

logger = logging.getLogger(__name__)

register = template.Library()


@register.inclusion_tag("widgets/frame.html")
def frame(context, href, height):
    return standard_dict(context, {"href": href, "height": height})


@register.inclusion_tag("widgets/subform.html")
def subform(context, name):
    return standard_dict(
        context,
        {
            "href": name,
        },
    )


@register.inclusion_tag("widgets/require.html")
def require(context, href):
    return {"href": mark_safe(href)}


@register.inclusion_tag("widgets/module_link.html")
def module_link(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except Exception:
            logger.warning("File not found: %s", href)
        return {"href": mark_safe(href), "content": mark_safe(content)}
    else:
        return {"href": mark_safe(href), "content": None}


@register.inclusion_tag("widgets/jscript_link.html")
def jscript_link(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except Exception:
            logger.warning("File not found: %s", href)
        return {"href": mark_safe(href), "content": mark_safe(content)}
    else:
        return {"href": mark_safe(href), "content": None}


@register.inclusion_tag("widgets/css_link.html")
def css_link(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except Exception:
            logger.warning("File not found: %s", href)
        return standard_dict(context, {"href": href, "content": mark_safe(content)})
    else:
        return standard_dict(context, {"href": href, "content": None})


@register.inclusion_tag("widgets/link.html")
def link(context, href, rel, typ):
    return standard_dict(
        context,
        {"href": settings.STATIC_URL + href, "rel": rel, "typ": typ, "content": None},
    )


@register.inclusion_tag("widgets/jscript.html")
def jscript(context, href):
    content_path = os.path.join(settings.STATIC_ROOT, href)
    content = ""
    with open(content_path, encoding="utf-8") as f:
        content = f.read()
    return {"content": mark_safe(content)}


@register.inclusion_tag("widgets/component.html")
def component(context, href):
    if "user_agent" in context and context["user_agent"] == "webviewembeded":
        content_path = os.path.join(settings.STATIC_ROOT, href)
        content = ""
        try:
            with open(content_path, encoding="utf-8") as f:
                content = (
                    f.read()
                    .replace("<script", "<_script_")
                    .replace("</script>", "</_script_>")
                )
        except Exception:
            logger.warning("File not found: %s", href)
        return {"href": mark_safe(href), "content": mark_safe(content)}
    else:
        return {"href": mark_safe(href), "content": None}
