## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('odf_upload/$', views.odf_upload, {}),
    
    
    
    
    
    url('form/OdfUploadForm/$', views.view_odfuploadform, {}),
]

gen = generic_table_start(urlpatterns, 'schodfupload', views)



