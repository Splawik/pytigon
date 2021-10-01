from django.utils.translation import gettext_lazy as _

ModuleTitle = _("Tools")
Title = _("Browser")
Perms = False
Index = "None"
Urls = (
    (
        "table/bookmarks/0/form/tree?schtml=desktop",
        _("Bookmarks"),
        None,
        """client://actions/bookmark-new.png""",
    ),
    (
        "table/history/-/form/list?schtml=desktop",
        _("History"),
        None,
        """client://emblems/emblem-photos.png""",
    ),
    (
        "form/MultiDownload/?schtml=desktop",
        _("Download"),
        None,
        """client://status/folder-open.png""",
    ),
)
UserParam = {}
