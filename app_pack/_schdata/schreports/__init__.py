# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Reports')
Title = _('Reports')
Perms = True
Index = 'None'
Urls  = (
    ('table/ReportDef/-/form/list/?schtml=desktop',_('Report definition'),None,'client://actions/document-properties.png'),
    ('table/Report/main_reports/form/list/?schtml=desktop',_('Reports'),None,'client://actions/format-justify-fill.png'),
    ('table/Plot/-/form/list/?schtml=desktop',_('Plots'),None,'fa://pencil-square.png'),
)
UserParam = {}