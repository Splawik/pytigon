# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main')
Title = _('Simple scripts')
Perms = True
Index = ''
Urls  = (
    ('table/Scripts/-/form/list?schtml=shtml',_('Scripts'),'simplescript.change_scripts','client://apps/utilities-terminal.png'),
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
                        ret.append(('run/'+object.name+"/?schtml=1", elements[1], None, elements[2]))
                    else:
                        ret.append(('run/'+object.name+"/?schtml=1", elements[1], None, 'client://apps/utilities-terminal.png'))
    return ret
