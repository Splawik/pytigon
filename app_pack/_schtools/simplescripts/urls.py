## -- coding: utf-8 --

from django.conf.urls import patterns, url
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
    gen_row_action('Scripts', 'run', views.run),
    ('run/(?P<script_name>\w+)/$', views.run_script_by_name, {}),
    
    
    
    
)

gen = generic_table_start(urlpatterns, 'simplescripts', views)


gen.standard('Scripts', 'Scripts')
