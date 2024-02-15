from django.utils.translation import gettext_lazy as _

ModuleName = "tools"
ModuleTitle = _("Tools")
Name = "schbrowser"
Title = _("Browser")
Perms = False
Index = ""
Urls = (
    (
        "table/bookmarks/0/form/tree?view_in=desktop",
        _("Bookmarks"),
        None,
        """client://actions/bookmark-new.png""",
    ),
    (
        "table/history/-/form/list?view_in=desktop",
        _("History"),
        None,
        """client://emblems/emblem-photos.png""",
    ),
    (
        "form/MultiDownload/?view_in=desktop",
        _("Download"),
        None,
        """client://status/folder-open.png""",
    ),
)
UserParam = {}
