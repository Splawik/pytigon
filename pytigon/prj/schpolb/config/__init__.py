# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('Config')
Title = _('Config')
Perms = True
Index = 'None'
Urls  = (
    ('table/Employee/-/form/list/?schtml=desktop',_('Employees'),None,'png://actions/contact-new.png'),
    ('form/employee_import/?schtml=desktop',_('Import employees'),None,'png://actions/document-open.png'),
    ('../schreports/table/ReportDef/-/form/list/?schtml=desktop',_('Definitions of reports'),None,'png://actions/document-properties.png'),
    ('../schreports/table/CommonGroupDef/-/form/list/?schtml=desktop',_('Definitions of common groups'),None,'png://status/folder-visiting.png'),
    ('../schreports/table/CommonGroup/0/form/tree/?schtml=desktop',_('Common groups'),None,'png://places/user-home.png'),
)
UserParam = {}