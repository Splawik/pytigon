# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Projekty')
Title = _('Projekty')
Perms = True
Index = ''
Urls  = (
    ('table/ProjektInw/-/form/list/?schtml=desktop',_('Inwestycje'),'projekty.list_projektinw','client://status/image-loading.png'),
    ('table/ProjektNawierzchni/-/form/list/?schtml=desktop',_('Projekty nawierzchni'),'projekty.list_projektnawierzchni','client://mimetypes/x-office-drawing.png'),
    ('table/Hurtownia/-/form/list/?schtml=desktop',_('Hurtownie'),None,'client://mimetypes/package-x-generic.png'),
    ('table/BiuroProjekt/-/form/list/?schtml=desktop',_('Biura projektowe'),None,'client://apps/system-users.png'),
    ('table/Asortyment/-/form/list/?schtml=desktop',_('Asortyment'),None,'client://apps/system-file-manager.png'),
    ('form/Raporty/?schtml=desktop',_('Raporty'),None,'client://mimetypes/text-x-generic.png'),
)
UserParam = {'icon': 'fa-tasks'}