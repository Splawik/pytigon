# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main')
Title = _('Simple scripts')
Perms = False
Index = ''
Urls  = (
    ('table/Scripts/-/form/list?schtml=1',_('Scripts'),None,'client://apps/utilities-terminal.png'),
)
UserParam = {}
def AdditionalUrls():
    from .models import Scripts
    ret = []
    for object in Scripts.objects.all():
        if object.menu:
            elements = object.menu.split(',')
            if len(elements)>2:
                if elements[0]=='main':
                    if len(elements)>2:
                        ret.append(('/simplescripts/run/'+object.name+"/?schtml=1", elements[1], None, elements[2]))
                    else:
                        ret.append(('/simplescripts/run/'+object.name+"/?schtml=1", elements[1], None, 'client://apps/utilities-terminal.png'))
    return ret