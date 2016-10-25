## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('set_param/(?P<parm>\d+)/$', views.set_param, {}),
    url('get_param/(?P<parm>\d+)/(?P<id>\d+)/$', views.get_param, {}),
    
    
]

gen = generic_table_start(urlpatterns, 'schsession', views)



