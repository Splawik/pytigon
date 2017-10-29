## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('search/(?P<type>.+)/', views.autocomplete_search, {}),
    url('set_user_param/$', views.set_user_param, {}),
    url('get_user_param/$', views.get_user_param, {}),
    
    
]

gen = generic_table_start(urlpatterns, 'tools', views)


gen.standard('Parameter', _('Parameter'), _('Parameter'))

