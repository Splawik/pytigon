from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("form/", views.form, {}, name="schcomponents_demo_form"),
    path(
        "codeeditor",
        TemplateView.as_view(template_name="schcomponents_demo/code_editor.html"),
        {},
    ),
    path("d3", TemplateView.as_view(template_name="schcomponents_demo/d3.html"), {}),
    path(
        "spreadsheet",
        TemplateView.as_view(template_name="schcomponents_demo/spreadsheet.html"),
        {},
    ),
    path(
        "pivottable",
        TemplateView.as_view(template_name="schcomponents_demo/pivottable.html"),
        {},
    ),
    path(
        "plotly",
        TemplateView.as_view(template_name="schcomponents_demo/plotly.html"),
        {},
    ),
    path(
        "leaflet",
        TemplateView.as_view(template_name="schcomponents_demo/leaflet.html"),
        {},
    ),
    path(
        "video", TemplateView.as_view(template_name="schcomponents_demo/video.html"), {}
    ),
    path(
        "wysiwyg",
        TemplateView.as_view(template_name="schcomponents_demo/wysiwygeditor.html"),
        {},
    ),
    path(
        "xterm", TemplateView.as_view(template_name="schcomponents_demo/xterm.html"), {}
    ),
    path(
        "calendar",
        TemplateView.as_view(template_name="schcomponents_demo/calendar.html"),
        {},
    ),
    path(
        "mask", TemplateView.as_view(template_name="schcomponents_demo/mask.html"), {}
    ),
    path(
        "webrtc",
        TemplateView.as_view(template_name="schcomponents_demo/webrtc.html"),
        {},
    ),
    path(
        "time", TemplateView.as_view(template_name="schcomponents_demo/time.html"), {}
    ),
    path(
        "scrollaction",
        TemplateView.as_view(template_name="schcomponents_demo/scrollaction.html"),
        {},
    ),
    path(
        "test", TemplateView.as_view(template_name="schcomponents_demo/test.html"), {}
    ),
    path("svg", TemplateView.as_view(template_name="schcomponents_demo/svg.html"), {}),
    path(
        "select2",
        TemplateView.as_view(template_name="schcomponents_demo/select2.html"),
        {},
    ),
    path("db", TemplateView.as_view(template_name="schcomponents_demo/db.html"), {}),
    path(
        "form", TemplateView.as_view(template_name="schcomponents_demo/form.html"), {}
    ),
    path(
        "event-calendar",
        TemplateView.as_view(template_name="schcomponents_demo/event-calendar.html"),
        {},
    ),
    path(
        "test_inline_content",
        TemplateView.as_view(template_name="schcomponents_demo/testinlinecontent.html"),
        {},
    ),
]

gen = generic_table_start(urlpatterns, "schcomponents_demo", views)
