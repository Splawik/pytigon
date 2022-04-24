from django import template

register = template.Library()


@register.filter(name="dochead_prefetch")
def dochead_prefetch(object_list):
    l = object_list
    for related in ['doc_type_parent', 'doc_type_parent__parent', 'doc_type_parent__parent__docregstatus_set']:
        l = l.prefetch_related(related)
    return l

@register.filter(name="dochead_report_prefetch")
def dochead_report_prefetch(object_list):
    l = object_list
    for related in ['doc_type_parent', 'doc_type_parent__parent', 'doc_type_parent__parent__docregstatus_set', 'report_set']:
        l = l.prefetch_related(related)
    return l
