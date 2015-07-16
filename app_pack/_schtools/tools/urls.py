## -- coding: utf-8 --

from django.conf.urls import patterns, url
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
    ('search/(?P<type>.+)/', views.autocomplete_search, {}),
    
    
)

gen = generic_table_start(urlpatterns, 'tools', views)


gen.standard('Parameter', 'Parameter')

