
from django.utils.translation import ugettext_lazy as _

def AdditionalUrls():
    from .models import Scripts
    ret = []
    for object in Scripts.objects.all():
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
            ret.append(("simplescripts/run/"+object.name+"/?schtml=1", object.title, object.rights_group, icon, _(module_title) if module_title else "", app_name, _(app_title) if app_title else ""))    
            
    return ret

from django.utils.translation import ugettext_lazy as _

def AdditionalUrls():
    from .models import Scripts
    ret = []
    for object in Scripts.objects.all():
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
            ret.append(("simplescripts/run/"+object.name+"/?schtml=1", object.title, object.rights_group, icon, _(module_title) if module_title else "", app_name, _(app_title) if app_title else ""))    
            
    return ret

from django.utils.translation import ugettext_lazy as _

def AdditionalUrls():
    from .models import Scripts
    ret = []
    for object in Scripts.objects.all():
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
            ret.append(("simplescripts/run/"+object.name+"/?schtml=1", object.title, object.rights_group, icon, _(module_title) if module_title else "", app_name, _(app_title) if app_title else ""))    
            
    return ret
