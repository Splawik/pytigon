# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main tools')
Title = _('Pytigon builder')
Perms = True
Index = 'None'
Urls  = (
    ('table/SChAppSet/-/form/list/?schtml=desktop',_('Projects'),'schbuilder.change_schappset','client://status/folder-open.png'),
    ('form/Installer/',_('Make installer'),None,'client://categories/applications-internet.png'),
    ('form/Install/',_('Install app'),None,'client://devices/drive-optical.png'),
)
UserParam = {}