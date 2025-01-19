from django.urls import path, re_path, include, reverse
from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("clock/", views.clock, {}, name="channels_demo_clock"),
    path("ai/", views.openai, {}, name="channels_demo_openai"),
    path("ollamaai/", views.ollama_ai, {}, name="channels_demo_ollama_ai"),
]

gen = generic_table_start(urlpatterns, "channels_demo", views)
