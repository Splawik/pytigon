## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('grid/(?P<folder>.*)/(?P<value>[\w=]*)/$', views.grid, {}),
    url('open/(?P<file_name>.*)/$', views.open, {}),
    url('save/(?P<file_name>.*)/$', views.save, {}),
    url('open_page/(?P<file_name>.*)/(?P<page>\d+)/$', views.open_page, {}),
     url(r'^copy', TemplateView.as_view(template_name='commander/copy.html'), {}), 
     url(r'^move', TemplateView.as_view(template_name='commander/move.html'), {}), 
     url(r'^mkdir', TemplateView.as_view(template_name='commander/mkdir.html'), {}), 
     url(r'^mkdir', TemplateView.as_view(template_name='commander/rename.html'), {}), 
    
    
    
    
    url('form/FileManager/$', views.view_filemanager, {}),
]

gen = generic_table_start(urlpatterns, 'commander', views)



