from django import template
from django.template.base import Node

register = template.Library()

class TransparentNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return self.nodelist.render(context).strip()

@register.tag
def compress(parser, token):
    nodelist = parser.parse(('endcompress',))
    parser.delete_first_token()
    return TransparentNode(nodelist)
