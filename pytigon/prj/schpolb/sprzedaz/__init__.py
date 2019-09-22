# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Sprzedaż')
Title = _('Sprzedaz')
Perms = True
Index = ''
Urls  = (
    ('table/CastoramaKli/-/form/list/?schtml=desktop',_('Castorama - mapowanie lokalizacji'),'sprzedaz','client://apps/system-users.png'),
    ('table/CastoramaKar/-/form/list/?schtml=desktop',_('Castorama - mapowanie kartotek'),'sprzedaz','client://apps/preferences-desktop-theme.png'),
    ('table/CastoramaLog/-/form/list/?schtml=desktop',_('Castorama - log'),'sprzedaz','wx.ART_GO_DIR_UP'),
    ('table/Nag/-/form/list/?schtml=desktop',_('Dokumenty'),'sprzedaz','wx.ART_NORMAL_FILE'),
    ('kalkulator1/?schtml=desktop',_('Kalkulator cenowy'),None,'client://apps/accessories-calculator.png'),
    ('kalkulator2/?schtml=desktop',_('Kalkulator MM'),None,'fa://truck.png'),
    ('kalkulator3/?schtml=desktop',_('Kontrakt wirtualny'),None,'client://apps/accessories-text-editor.png'),
    ('kalkulator_sync/?schtml=desktop',_('Kalkulator - synchronizacja'),None,'client://actions/view-refresh.png'),
    ('kalkulator_zmieniony/?schtml=desktop',_('Zmienione dane kalkulatora'),None,'client://devices/network-wireless.png'),
    ('table/CastoramaRegion/-/form/list/?schtml=desktop',_('Regiony Castoramy'),None,'client://places/start-here.png'),
    ('table/CastoramaStanMag/-/form/list/?schtml=desktop',_('Stany mag. Castoramy'),None,'client://apps/accessories-text-editor.png'),
)
UserParam = {'icon': 'fa-shopping-cart'}