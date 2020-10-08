## -- coding: utf-8 --

from django.urls import path, re_path, include
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    
    
    
    path('form/upload_ptig/', views.view_upload_ptig, {}),
    path('form/download_ptig/', views.view_download_ptig, {}),
]

gen = generic_table_start(urlpatterns, 'schinstall', views)



