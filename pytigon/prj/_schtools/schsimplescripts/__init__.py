from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schsimplescripts"
Title = _("Simple scripts")
Perms = True
Index = ""
Urls = (
    (
        "table/Script/-/form/list/?view_in=desktop",
        _("Scripts"),
        "simplescripts.admin_script",
        """client://apps/utilities-terminal.png""",
    ),
)
UserParam = {}

from django.utils.translation import gettext_lazy as _

def AdditionalUrls(app_pack, lang):
    from .models import Script
    ret = []
    ret_buf = []
    for object in Script.objects.all():
        if object.menu:
            elements = object.menu.split(',')

            menu_path=elements[0].split('/')            
            app_pack_name = menu_path[0]
            if app_pack and app_pack_name and app_pack != app_pack_name:
                continue
            module_title = ""
            app_name = ""
            if len(menu_path)>1:
                module_title = menu_path[1]
            if len(menu_path)>2:
                app_name = menu_path[2]
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
            if len(elements)>3:
                if elements[3] and lang != elements[3]:
                    continue
                    
            ret_buf.append((lp, ("schsimplescripts/run/"+object.name+"/", object.title, object.rights_group, icon, module_title, _(module_title), app_name, _(app_name))))

    if ret_buf:        
        buf = sorted(ret_buf, key=lambda pos: pos[0])  
        for pos in buf:
            ret.append(pos[1])
        return ret
    else:
        return []
            