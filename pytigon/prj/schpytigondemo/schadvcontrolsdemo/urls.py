## -- coding: utf-8 --

from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path("form/", views.form, {}, name="schadvcontrolsdemo_form"),
    path(
        "codeeditor",
        TemplateView.as_view(template_name="schadvcontrolsdemo/code_editor.html"),
        {},
    ),
    path("d3", TemplateView.as_view(template_name="schadvcontrolsdemo/d3.html"), {}),
    path(
        "spreadsheet",
        TemplateView.as_view(template_name="schadvcontrolsdemo/spreadsheet.html"),
        {},
    ),
    path(
        "pivottable",
        TemplateView.as_view(template_name="schadvcontrolsdemo/pivottable.html"),
        {},
    ),
    path(
        "plotly",
        TemplateView.as_view(template_name="schadvcontrolsdemo/plotly.html"),
        {},
    ),
    path(
        "leaflet",
        TemplateView.as_view(template_name="schadvcontrolsdemo/leaflet.html"),
        {},
    ),
    path(
        "video", TemplateView.as_view(template_name="schadvcontrolsdemo/video.html"), {}
    ),
    path(
        "wysiwyg",
        TemplateView.as_view(template_name="schadvcontrolsdemo/wysiwygeditor.html"),
        {},
    ),
    path(
        "xterm", TemplateView.as_view(template_name="schadvcontrolsdemo/xterm.html"), {}
    ),
    path(
        "calendar",
        TemplateView.as_view(template_name="schadvcontrolsdemo/calendar.html"),
        {},
    ),
    path(
        "mask", TemplateView.as_view(template_name="schadvcontrolsdemo/mask.html"), {}
    ),
    path(
        "markdeep",
        TemplateView.as_view(template_name="schadvcontrolsdemo/markdeep.html"),
        {},
    ),
    path(
        "webrtc",
        TemplateView.as_view(template_name="schadvcontrolsdemo/webrtc.html"),
        {},
    ),
    path(
        "time", TemplateView.as_view(template_name="schadvcontrolsdemo/time.html"), {}
    ),
    path(
        "scrollaction",
        TemplateView.as_view(template_name="schadvcontrolsdemo/scrollaction.html"),
        {},
    ),
    path(
        "test", TemplateView.as_view(template_name="schadvcontrolsdemo/test.html"), {}
    ),
    path("svg", TemplateView.as_view(template_name="schadvcontrolsdemo/svg.html"), {}),
    path(
        "select2",
        TemplateView.as_view(template_name="schadvcontrolsdemo/select2.html"),
        {},
    ),
    path("db", TemplateView.as_view(template_name="schadvcontrolsdemo/db.html"), {}),
    path(
        "form", TemplateView.as_view(template_name="schadvcontrolsdemo/form.html"), {}
    ),
]

gen = generic_table_start(urlpatterns, "schadvcontrolsdemo", views)
