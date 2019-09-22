# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Raporty')
Title = _('Raporty')
Perms = True
Index = ''
Urls  = (
    ('form/WiekowanieForm/?schtml=desktop',_('Wiekowanie'),'raporty.list_raporty','client://actions/appointment-new.png'),
    ('form/SaldaForm/?schtml=desktop',_('Salda - SAP'),'raporty.list_raporty','client://actions/edit-find-replace.png'),
    ('form/ObrotyTransport/?schtml=desktop',_('Transport surowców'),None,'client://places/start-here.png'),
    ('form/FakturaWzTest/?schtml=desktop',_('Kontrola WZ - Faktury'),None,'wx.ART_HELP_BOOK'),
    ('table/Raporty/-/form/list/?schtml=desktop',_('Definiowanie raportów (old)'),None,'client://actions/document-properties.png'),
    ('../schreports/list_group_by_tag/reports/?schtml=desktop',_('Definiowanie raportów'),None,'png://actions/format-justify-fill.png'),
    ('table/Kwerendy/-/form/list/?schtml=desktop',_('Definiowanie kwerend'),None,'client://apps/internet-news-reader.png'),
    ('form/SimpleReport/?schtml=desktop',_('Generator raportów'),None,'client://actions/document-properties.png'),
    ('form/Tranformer/?schtml=desktop',_('Transformer'),None,'client://status/network-transmit-receive.png'),
)
UserParam = {'icon': 'fa-file-pdf-o '}