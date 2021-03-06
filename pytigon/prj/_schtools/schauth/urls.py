## -- coding: utf-8 --

from django.urls import path, re_path, include
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    re_path('auth/(?P<key>[\w-]+)/(?P<path>.*)$', views.auth, {}),
    
    
    
]

gen = generic_table_start(urlpatterns, 'schauth', views)


gen.standard('UrlWithAuth', _('Url with authorization'), _('Urls with authorization'))

