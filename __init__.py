# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _

# from .models import Scripts

ModuleTitle = _("main")
Title = _("Simple scripts")
Perms = False
Index = ""
Urls = [
    (
        "table/Scripts/-/form/list",
        _("Scripts"),
        None,
        "client://apps/utilities-terminal.png",
    ),
]

UserParam = {}


def AdditionalUrls():
    from .models import Scripts

    ret = []
    for object in Scripts.objects.all():
        if object.menu:
            elements = object.menu.split(",")
            if len(elements) > 2:
                if elements[0] == "main":
                    if len(elements) > 3:
                        ret.append(
                            (
                                "/simplescripts/run/" + object.name,
                                elements[1],
                                None,
                                elements[2],
                            )
                        )
                    else:
                        ret.append(
                            (
                                "/simplescripts/run/" + object.name,
                                elements[1],
                                None,
                                "client://apps/utilities-terminal.png",
                            )
                        )
    return ret
