from django.utils.translation import gettext_lazy as _

ModuleName = "config"
ModuleTitle = _("Config")
Name = "schbi"
Title = _("BI")
Perms = True
Index = ""
Urls = (
    (
        "table/Project/-/form/list/",
        _("Projects"),
        None,
        """png://mimetypes/x-office-drawing-template.png""",
    ),
)
UserParam = {}

from django.utils.translation import gettext_lazy as _

def AdditionalUrls(prj_name, lang):
    from .models import Project

    ret = []
    ret_buf = []
    for object in Project.objects.all():
        if object.menu:
            if object.base_prj_name and object.base_prj_name != prj_name:
                continue
            menu_path = object.menu.split("/")
            module_title = ""
            app_name = ""
            app_name = menu_path[-1]
            if len(menu_path) > 1:
                module_title = menu_path[0]

            if object.menu_icon:
                icon = object.menu_icon
            else:
                icon = "fa://arrow-circle-right.png"
                        
            if object.menu_position:
                lp = "%02d" % object.menu_position
            else:
                lp = "00"
            ret_buf.append(
                (
                    lp,
                    (
                        "schbi/project_view/" + object.name + "/",
                        object.description,
                        object.rights_group,
                        icon,
                        module_title,
                        _(module_title),
                        app_name,
                        _(app_name),
                    ),
                )
            )
    if ret_buf:
        buf = sorted(ret_buf, key=lambda pos: pos[0])
        for pos in buf:
            ret.append(pos[1])
        return ret
    else:
        return []
