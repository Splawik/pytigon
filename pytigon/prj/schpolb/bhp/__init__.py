# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('bhp')
Title = _('BHP')
Perms = True
Index = ''
Urls  = (
    ('../schelements/table/DocHead/rep_safety/form/docheadlist/?schtml=desktop',_('Generator procedur'),None,'client://categories/applications-development.png'),
    ('table/EventType/-/form/list/?schtml=desktop',_('Event types'),'bhp.list_eventtype','png://actions/folder-new.png'),
    ('table/Event/-/form/list/?schtml=desktop',_('Events'),'bhp.list_event','png://apps/office-calendar.png'),
)
UserParam = {}