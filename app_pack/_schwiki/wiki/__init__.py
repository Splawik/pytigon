# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main')
Title = _('Wiki')
Perms = False
Index = ''
Urls  = (
    ('table/Page/-/form/list?schtml=1',_('Wiki'),None,'wx.ART_HELP_SIDE_PANEL'),
    ('../wiki/pytigon_doc/pytigon/view/?schtml=1',_('Pytigon doc'),None,'wx.ART_INFORMATION'),
)
UserParam = {}
def AdditionalUrls():
    from .models import Page
    ret = []
    for object in Page.objects.all():
        if object.menu:
            elements = object.menu.split(',')
            if len(elements)>2:
                if elements[0]=='main':
                    if len(elements)>2:
                        ret.append((object.subject+"/"+object.name+"/view/?schtml=1", elements[1], None, elements[2]))
                    else:
                        ret.append((object.subject+"/"+object.name+"/view/?schtml=1", elements[1], None, 'client://apps/utilities-terminal.png'))
    return ret
