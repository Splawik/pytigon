## -- coding: utf-8 --

from django.conf.urls import patterns, url
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
    ('(?P<subject>.*)/(?P<page_name>.*)/view/$', views.view_page),
    ('^(?P<subject>\w*)/(?P<page_name>\w*)/edit/$', views.edit_page),
    
    
    
    
)

gen = generic_table_start(urlpatterns, 'wiki', views)


gen.standard('Page', 'Page')
