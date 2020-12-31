from django import template
from django.db.models.query import QuerySet

register = template.Library()

@register.filter(name='module_obj')
def filter_module_obj(obj, obj_name):
    if type(obj) == QuerySet:
        module_name = obj.model.__module__
        return getattr(__import__(module_name).models, obj_name)
    return None
