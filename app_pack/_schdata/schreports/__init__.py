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
    ('table/CommonGroupDef/-/form/list/?schtml=desktop',_('Common group definitons'),None,'png://apps/system-file-manager.png'),
    ('table/CommonGroup/0/form/tree/?schtml=desktop',_('Common groups'),None,'png://apps/system-file-manager.png'),
)
UserParam = {}