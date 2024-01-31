
from django import template
from django.template.loader import get_template

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

@inclusion_tag('schreports/subreport.html')
def subrep(context, name, type):
    rep = context['rep']
    rep_def = context['rep_def']
    url = make_href("/schreports/edit_subrep/%d/%s/%s/" % (rep.id, name, type))
    return { 'href':  url }

@inclusion_tag('schreports/check.html')
def check(context, is_checked, title=""):
    return { 'is_checked':  is_checked, 'title': title }
