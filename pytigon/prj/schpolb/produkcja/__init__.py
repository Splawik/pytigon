# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Produkcja')
Title = _('Produkcja')
Perms = True
Index = ''
Urls  = (
    ('form/ProdukcjaForm/?schtml=desktop',_('Premie'),'produkcja.list_config','client://categories/applications-development.png'),
    ('table/Config/-/form/list/?schtml=desktop',_('Premie - ustawienia'),'produkcja.list_config','client://categories/preferences-system.png'),
    ('form/ConfigUploadForm/?schtml=desktop',_('Premie - importuj ustawienia'),'produkcja.list_config','ART_EXECUTABLE_FILE'),
)
UserParam = {'icon': 'fa-building-o'}