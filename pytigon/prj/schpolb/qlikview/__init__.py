# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main')
Title = _('QlikView')
Perms = True
Index = ''
Urls  = (
    ('form/QlikTkw/?schtml=desktop',_('Wczytanie TKW'),None,'client://actions/document-properties.png'),
    ('form/QlikRabat/?schtml=desktop',_('Rabaty specjalne'),None,'ART_GO_DOWN'),
)
UserParam = {'icon': 'fa-bullseye'}