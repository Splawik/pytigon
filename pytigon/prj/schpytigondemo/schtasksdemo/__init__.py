# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('tasks_demo')
Title = _('Tasks')
Perms = False
Index = 'None'
Urls  = (
    ('gen_task1?schtml=desktop',_('Gen task 1'),None,'client://actions/edit-redo.png'),
    ('gen_task2?schtml=desktop',_('Gen task 2'),None,'client://actions/tab-new.png'),
    ('gen_task3?schtml=desktop',_('Gen task 3'),None,'client://actions/go-home.png'),
)
UserParam = {}