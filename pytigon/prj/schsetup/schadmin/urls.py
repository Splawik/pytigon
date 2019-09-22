## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
     url(r'^terminal', TemplateView.as_view(template_name='schadmin/terminal.html'), {}), 
     url(r'^administration', TemplateView.as_view(template_name='schadmin/administration.html'), {}), 
     url(r'^filemanager', TemplateView.as_view(template_name='schadmin/filemanager.html'), {}), 
     url(r'^sqlexplore', TemplateView.as_view(template_name='schadmin/sqlexplore.html'), {}), 
    
    
]

gen = generic_table_start(urlpatterns, 'schadmin', views)
from django.conf.urls import include
from django.contrib import admin
from pytigon_lib.schtools.platform_info import platform_name

urlpatterns.append(url(r'^admin/', admin.site.urls))
urlpatterns.append(url(r'^explorer/', include('explorer.urls')))

if platform_name()!='Android':
    urlpatterns.append(url(r'^filer/', include('filer.urls')))



