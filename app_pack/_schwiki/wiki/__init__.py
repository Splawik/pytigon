# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main tools')
Title = _('Wiki')
Perms = True
Index = ''
Urls  = (
    ('table/Page/-/form/list/?schtml=desktop',_('Wiki'),'wiki.change_page','wx.ART_HELP_SIDE_PANEL'),
    ('table/PageObjectsConf/-/form/list/?schtml=desktop',_('Page objects conf.'),None,'client://actions/document-properties.png'),
    ('table/WikiConf/-/form/list/?schtml=desktop',_('Publish options'),None,'png://categories/applications-system.png'),
)
UserParam = {}
from django.utils.translation import ugettext_lazy as _

def AdditionalUrls():
    from .models import Page
    ret = []
    for object in Page.objects.all():
        if object.menu:
            elements = object.menu.split(',')
            menu_path=elements[0].split('/')            
            module_title = menu_path[0]
            app_name = None
            app_title = None
            if len(menu_path)>1:
                app_name = menu_path[1]
            if len(menu_path)>2:
                app_title = menu_path[2]                        
            if len(elements)>1:
                icon = elements[1]
            else:
                icon = 'client://apps/utilities-terminal.png'                    
            ret.append(("wiki/"+object.subject+"/"+object.name+"/view/?schtml=1", object.description, object.rights_group, icon, _(module_title) if module_title else "", app_name, _(app_title) if app_title else ""))
    return ret
