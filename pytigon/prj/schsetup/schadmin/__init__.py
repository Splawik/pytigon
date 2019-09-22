# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('administration')
Title = _('Administration')
Perms = True
Index = 'None'
Urls  = (
    ('terminal?schtml=desktop',_('Terminal'),None,'png://apps/utilities-terminal.png'),
    ('administration?schtml=desktop',_('Administration'),None,'png://apps/utilities-system-monitor.png'),
    ('filemanager?schtml=desktop',_('File manager'),None,'png://apps/system-file-manager.png'),
    ('sqlexplore?schtml=desktop',_('SQL explorer'),None,'png://mimetypes/x-office-spreadsheet.png'),
)
UserParam = {}