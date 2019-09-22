# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Sprzęt')
Title = _('Sprzęt')
Perms = True
Index = ''
Urls  = (
    ('raport_domena_softlab/?schtml=desktop',_('Raport sprzęt: domena - softlab'),'hardware.list_sprzet','client://actions/view-refresh.png'),
)
UserParam = {'icon': 'fa-desktop'}