from base64 import b64encode
import io
import re
import itertools
import html

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
from pytigon_lib.schdjangoext.tools import make_href

register = template.Library()

def inclusion_tag(file_name):
    def dec(func):
        def func2(context, *argi, **argv):
            ret = func(context, *argi, **argv)
            t = get_template(file_name)
            return t.render(ret, context.request)
        return register.simple_tag(takes_context=True, name=getattr(func, '_decorated_function', func).__name__)(func2)
    return dec

@inclusion_tag('schdoc/subdoc.html')
def subdoc(context, name, type):
    doc = context['doc']
    doc_def = context['doc_def']
    url = make_href("/schdoc/edit_subdoc/%d/%s/%s/" % (doc.id, name, type))
    return { 'href':  url }

@inclusion_tag('schdoc/check.html')
def check(context, is_checked, title=""):
    return { 'is_checked':  is_checked, 'title': title }
