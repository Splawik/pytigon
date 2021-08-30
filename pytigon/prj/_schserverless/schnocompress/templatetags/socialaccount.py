from django import template
from django.template.base import Node

register = template.Library()

class NoneNode(Node):
    def __init__(self):
        pass

    def render(self, context):
        return ""

@register.tag
def provider_login_url(parser, token):
    return NoneNode()
