from django.utils.translation import gettext_lazy as _

ModuleTitle = _("main tools")
Title = _("Wiki")
Perms = True
Index = "None"
Urls = (
    ("table/Page/-/form/list/?view_in=desktop", _("Wiki"), "wiki.change_page", """"""),
    (
        "table/PageObjectsConf/-/form/list/?view_in=desktop",
        _("Page objects conf."),
        None,
        """client://actions/document-properties.png""",
    ),
    (
        "table/WikiConf/-/form/list/?view_in=desktop",
        _("Publish options"),
        None,
        """png://categories/applications-system.png""",
    ),
)
UserParam = {}

from django.utils.translation import gettext_lazy as _

def AdditionalUrls(prj_name, lang):
    from .models import Page
    ret = []
    ret_buf = []
    for object in Page.objects.filter(published=True):        
        if object.menu:
            if object.prj_name and object.prj_name != prj_name:
                continue
            menu_path=object.menu.split('/')            
            module_title = ""
            app_name = ""
            app_name = menu_path[-1]
            if len(menu_path)>1:
                module_title = menu_path[0]
            if object.menu_icon:
                icon = object.menu_icon
            else:
                icon = 'client://apps/utilities-terminal.png'                    
            if object.menu_position:
                lp = "%02d" % object.menu_position
            else:
                lp = '00'
            ret_buf.append((lp, ("schwiki/"+object.subject+"/"+object.name+"/view/", object.description, object.rights_group, icon, module_title, _(module_title), app_name, _(app_name))))
    if ret_buf:        
        buf = sorted(ret_buf, key=lambda pos: pos[0])  
        for pos in buf:
            ret.append(pos[1])
        return ret
    else:
        return []
        