# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

ModuleTitle = _('main tools')
Title = _('Wiki')
Perms = True
Index = 'None'
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
    ret_buf = []
    for object in Page.objects.filter(published=True):
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
                if elements[1]:
                    icon = elements[1]
                else:
                    icon = 'client://apps/utilities-terminal.png'                    
            else:
                icon = 'client://apps/utilities-terminal.png'                    
            if len(elements)>2:
                lp = elements[2]
            else:
                lp = '00'
                
            ret_buf.append((lp, ("schwiki/"+object.subject+"/"+object.name+"/view/?schtml=1", object.description, object.rights_group, icon, _(module_title) if module_title else "", app_name, _(app_title) if app_title else "")))
    if ret_buf:        
        buf = sorted(ret_buf, key=lambda pos: pos[0])  
        for pos in buf:
            ret.append(pos[1])
        return ret
    else:
        return []
        