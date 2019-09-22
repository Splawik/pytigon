## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_tab_action('Ad', 'sync', views.sync),
    gen_tab_action('Ad', 'errors', views.errors),
    url('fun/(?P<parm>\d+)/$', views.confirm, {}),
    
    
    
    
    
    
    
]

gen = generic_table_start(urlpatterns, 'crh', views)


gen.standard('Ad', _('AD'), _('AD'))
gen.standard('AgreementDoc', _('Agreement document'), _('Agreement documents'))
gen.standard('Agreement', _('Agreement'), _('Agreements'))

gen.for_field('Ad', 'agreement_set', _('Agreement'), _('Agreements'))
gen.for_field('AgreementDoc', 'agreement_set', _('Agreement'), _('Agreements'))
