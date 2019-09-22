# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Spisy')
Title = _('Spisy')
Perms = True
Index = ''
Urls  = (
    ('table/UserAD/-/form/list/?schtml=desktop',_('Użytkownicy AD'),None,'wx.ART_TIP'),
    ('table/UserSoftlab/-/form/list/?schtml=desktop',_('Użytkownicy Softlaba'),None,'wx.ART_TIP'),
    ('table/NowyKomputer/-/form/list/?schtml=desktop',_('Komputery'),None,'wx.ART_TIP'),
    ('table/TypKomputera/-/form/list/?schtml=desktop',_('Typy komputerów'),None,'wx.ART_TIP'),
    ('table/NowaDrukarka/-/form/list/?schtml=desktop',_('Drukarki'),None,'wx.ART_TIP'),
    ('table/UserPolbruk/-/form/list/?schtml=desktop',_('Pracownicy'),None,'client://apps/system-users.png'),
    ('form/ImportPracForm/?schtml=desktop',_('Pracownicy - import'),None,'client://actions/mail-reply-all.png'),
    ('form/RaportForm/?schtml=desktop',_('Raporty kontrolne'),None,'wx.ART_TIP'),
)
UserParam = {'icon': 'fa-list'}