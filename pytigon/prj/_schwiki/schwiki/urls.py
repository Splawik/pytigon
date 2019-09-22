## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('^(?P<app_or_subject>[^/]*)/(?P<page_path>[^/]*)/view/$', views.view_page),
    url('^(?P<app_or_subject>\w*)/(?P<page_name>\w*)/edit/$', views.edit_page),
    gen_row_action('PageObjectsConf', 'insert_object_to_editor', views.insert_object_to_editor),
    gen_tab_action('PageObjectsConf', 'edit_page_object', views.edit_page_object),
    gen_row_action('WikiConf', 'publish', views.publish),
    url('(?P<q>.*)/search/$', views.search, {}),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
]

gen = generic_table_start(urlpatterns, 'schwiki', views)


gen.standard('PageObjectsConf', _('Page objects configurations'), _('Page objects configurations'))
gen.standard('Page', _('Page'), _('Page'))
gen.standard('WikiConf', _('Wiki config'), _('Wiki config'))

