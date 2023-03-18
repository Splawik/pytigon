from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = []

gen = generic_table_start(urlpatterns, "otkernel", views)


gen.standard("Feature", _("Feature"), _("Features"))
gen.standard("Location", _("Location"), _("Locations"))
gen.standard("MeasurementPoint", _("Measurement point"), _("Measurement points"))
gen.standard(
    "MeasurementPointState", _("Measurement point state"), _("Measurement point state")
)
gen.standard("Product", _("Product"), _("Products"))
gen.standard("RawMaterial", _("Raw material"), _("Raw materials"))
gen.standard("Operation", _("Operation"), _("Operations"))
gen.standard("Inventory", _("Inventory"), _("Inventories"))
gen.standard("Log", _("Log"), _("Logs"))
gen.standard("ExtendedLog", _("Extended log"), _("Extended log"))
gen.standard(
    "MPointInputQueue",
    _("Measurement point input queue"),
    _("Measurement point input queue"),
)
gen.standard(
    "MPointInputQueueStatus",
    _("Measurement point input queue status"),
    _("Measurement point input queue statuses"),
)
gen.standard(
    "MPointOutputQueue",
    _("Measurement point output queue"),
    _("Measurement point output queue"),
)
gen.standard(
    "MPointOutputQueueStatus",
    _("Measurement point output queue status"),
    _("Measurement point output queue status"),
)
gen.standard(
    "MPointControlQueue",
    _("Measurement point control queue"),
    _("Measurement point control queue"),
)
gen.standard(
    "MPointControlQueueStatus",
    _("Measurement point control queue status"),
    _("Measurement point control queue status"),
)


gen.for_field("Feature", "inventory_set", _("Inventory"), _("Inventories"))
gen.for_field("Product", "inventory_set", _("Inventory"), _("Inventories"))
gen.for_field("Location", "inventory_set", _("Inventory"), _("Inventories"))
gen.for_field("Operation", "inventory_set", _("Inventory"), _("Inventories"))
gen.for_field("MeasurementPoint", "log_set", _("Log"), _("Logs"))
gen.for_field(
    "MeasurementPoint", "extendedlog_set", _("Extended log"), _("Extended log")
)
gen.for_field(
    "MeasurementPoint",
    "mpointinputqueue_set",
    _("Measurement point input queue"),
    _("Measurement point input queue"),
)
gen.for_field(
    "MeasurementPoint",
    "mpointoutputqueue_set",
    _("Measurement point output queue"),
    _("Measurement point output queue"),
)
gen.for_field(
    "MeasurementPoint",
    "mpointcontrolqueue_set",
    _("Measurement point control queue"),
    _("Measurement point control queue"),
)
