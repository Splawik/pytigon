## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('edit/(?P<d>\d{4}-\d{2}-\d{2})/(?P<mg>\w+)/(?P<kar>\d+)/(?P<c>\w+)/(?P<kw>.+)', views.edit_wiek),
    gen_tab_action('Raporty', 'gen', views.gen),
    gen_tab_action('Raporty', 'gen2', views.gen2),
    url('kwerenda/(?P<name>\w+)/$', views.kwerenda, {}),
    url('rep_gen/(?P<rep_id>\d+)/$', views.rep_gen, {}),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    url('form/WiekowanieForm/$', views.view_wiekowanieform, {}),
    url('form/SaldaForm/$', views.view_saldaform, {}),
    url('form/ObrotyTransport/$', views.view_obrotytransport, {}),
    url('form/FakturaWzTest/$', views.view_fakturawztest, {}),
    url('form/SimpleReport/$', views.view_simplereport, {}),
    url('form/Tranformer/$', views.view_tranformer, {}),
]

gen = generic_table_start(urlpatterns, 'raporty', views)


gen.standard('Raporty', _('Raporty'), _('Raporty'))
gen.standard('Kwerendy', _('Kwerendy'), _('Kwerendy'))

