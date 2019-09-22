# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Audyty')
Title = _('Audyty')
Perms = True
Index = ''
Urls  = (
    ('table/Audyt/-/form/list/?schtml=desktop',_('Audyty'),None,'client://apps/utilities-system-monitor.png'),
    ('table/TypAudytu/-/form/list/?schtml=desktop',_('Typy audytow'),None,'client://categories/applications-system.png'),
    ('table/Change/-/form/list/?schtml=desktop',_('Zmiany'),None,'png://actions/view-refresh.png'),
    ('table/Test/-/form/list/?schtml=desktop',_('Testy'),None,'png://mimetypes/text-x-generic.png'),
    ('../schreports/list_group_by_tag/riskregister/?schtml=desktop',_('Risk register'),None,'png://actions/window-new.png'),
    ('../schreports/list_group_by_tag/controls/?schtml=desktop',_('Controls'),None,'png://apps/accessories-text-editor.png'),
    ('../schreports/list_group_by_tag/checks/?schtml=desktop',_('Checks'),None,'png://actions/appointment-new.png'),
)
UserParam = {'icon': 'fa-check'}