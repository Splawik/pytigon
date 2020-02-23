# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main tools')
Title = _('Simple controls')
Perms = False
Index = 'None'
Urls  = (
    ('standardcontrols?schtml=desktop',_('Standard controls'),None,'client://mimetypes/x-office-document-template.png'),
    ('htmlcontrols?schtml=desktop',_('Html controls'),None,'client://apps/internet-web-browser.png'),
    ('extendedcontrols?schtml=desktop',_('Extended controls'),None,'client://categories/applications-other.png'),
    ('../schwiki/simplecontrols/userwiki/view/?schtml=desktop',_('Wiki'),None,'client://status/weather-clear.png'),
    ('form/TestForm/?schtml=desktop',_('Form'),None,'client://categories/preferences-desktop.png'),
    ('sum/2/3/?schtml=desktop',_('Json'),None,'client://mimetypes/x-office-spreadsheet.png'),
    ('markdeep?schtml=desktop',_('Markdeep'),None,'png://apps/preferences-desktop-multimedia.png'),
)
UserParam = {}