## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('grid/(?P<folder>.*)/(?P<value>[\w=]*)/$', views.grid, {}),
    url('open/(?P<file_name>.*)/$', views.open, {}),
    url('save/(?P<file_name>.*)/$', views.save, {}),
    url('open_page/(?P<file_name>.*)/(?P<page>\d+)/$', views.open_page, {}),
    
    
    
    
    
    
    
    
    
    url('form/FileManager/$', views.view_filemanager, {}),
    url('form/Move/$', views.view_move, {}),
    url('form/Copy/$', views.view_copy, {}),
    url('form/MkDir/$', views.view_mkdir, {}),
    url('form/Rename/$', views.view_rename, {}),
    url('form/NewFile/$', views.view_newfile, {}),
    url('form/Delete/$', views.view_delete, {}),
    url('form/Setup/$', views.view_setup, {}),
]

gen = generic_table_start(urlpatterns, 'schcommander', views)



