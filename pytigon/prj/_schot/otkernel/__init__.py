from django.utils.translation import gettext_lazy as _

ModuleTitle = _("OT kernel")
Title = _("OT kernel")
Perms = True
Index = "None"
Urls = (
    (
        "table/Feature/-/form/list/",
        _("Features"),
        None,
        """png://apps/internet-group-chat.png""",
    ),
    (
        "table/Location/-/form/list/",
        _("Locations"),
        None,
        """png://categories/applications-internet.png""",
    ),
    (
        "table/MeasurementPoint/-/form/list/",
        _("Measurement points"),
        None,
        """png://actions/edit-find-replace.png""",
    ),
    (
        "table/MeasurementPointState/-/form/list/",
        _("Measurement point states"),
        None,
        """png://places/user-desktop.png""",
    ),
    (
        "table/Product/-/form/list/",
        _("Products"),
        None,
        """png://apps/system-file-manager.png""",
    ),
    (
        "table/Inventory/-/form/list/",
        _("Inventory"),
        None,
        """png://actions/format-justify-fill.png""",
    ),
    (
        "table/Operation/-/form/list/",
        _("Operations"),
        None,
        """png://places/start-here.png""",
    ),
    (
        "table/Log/-/form/list/",
        _("Logs"),
        None,
        """png://actions/document-properties.png""",
    ),
    (
        "table/ExtendedLog/-/form/list/",
        _("Extended logs"),
        None,
        """png://status/image-loading.png""",
    ),
)
UserParam = {}
