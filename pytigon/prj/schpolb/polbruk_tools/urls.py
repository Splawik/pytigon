## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('../sw.js', views.service_worker, {}),
    
     url(r'^kalkulator_cenowy', TemplateView.as_view(template_name='polbruk_tools/kalkulator_cenowy.html'), {}), 
     url(r'^kalkulator_sync', TemplateView.as_view(template_name='polbruk_tools/kalkulator_sync.html'), {}), 
    
    
]

gen = generic_table_start(urlpatterns, 'polbruk_tools', views)


gen.standard('DelegNag', _('Delegacja'), _('Delegacje'))
gen.standard('DelegLin', _('Linijka delegacji'), _('Linijki delegacji'))

