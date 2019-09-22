# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Prawa')
Title = _('Prawa')
Perms = True
Index = ''
Urls  = (
    ('table/Operator/-/form/list/?schtml=desktop',_('Operatorzy'),'prawa.list_operator','client://apps/system-users.png'),
    ('table/DokPrzydzielenia/-/form/list/?schtml=desktop',_('Dok. przydz.'),'prawa.list_dokprzydzielenia','client://actions/list-add.png'),
    ('table/DokPrzydzielenia/niezatwierdzone/form/list/?schtml=desktop',_('Dok. niezatwierdzone'),'prawa.list_dokprzydzielenia','client://mimetypes/text-x-script.png'),
    ('table/DokOdebrania/-/form/list/?schtml=desktop',_('Dok. odebr.'),'prawa.list_dokodebrania','client://actions/list-remove.png'),
    ('table/Lokalizacja/-/form/list/?schtml=desktop',_('Lokalizacje'),'prawa.list_lokalizacja','client://apps/preferences-desktop-remote-desktop.png'),
    ('table/Dzial/-/form/list/?schtml=desktop',_('Działy'),'prawa.list_dzial','client://apps/system-file-manager.png'),
    ('table/GrupaPraw/-/form/list/?schtml=desktop',_('Grupy praw'),'prawa.list_grupapraw','client://places/folder.png'),
    ('table/LogZmian/-/form/list/?schtml=desktop',_('Logi'),'prawa.list_logzmian','client://devices/camera-video.png'),
    ('form/FunkcjePrawForm/?schtml=desktop',_('Funkcje praw'),None,'client://actions/format-justify-fill.png'),
    ('form/GrupyFunkcjeForm/?schtml=desktop',_('Grupy z funkcjami'),None,'client://actions/contact-new.png'),
    ('form/KartyPrawForm/?schtml=desktop',_('Karty uprawnień'),None,'client://mimetypes/application-certificate.png'),
    ('form/PrawaWyklucz/?schtml=desktop',_('Grupy zakazane'),None,'client://status/dialog-error.png'),
    ('form/AkceptacjeDP/?schtml=desktop',_('Akceptacje - zakupy'),None,'fa://check.png'),
    ('form/GrupyZOperatorami/?schtml=desktop',_('Grupy z operatorami'),None,'client://apps/preferences-desktop-theme.png'),
    ('form/LogZmian/?schtml=desktop',_('Log zmian uprawnień'),None,'client://mimetypes/text-x-generic-template.png'),
)
UserParam = {'icon': 'fa-lock'}