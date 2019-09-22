## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    gen_row_action('qlik_firmy', 'import_data', views.import_data),
    gen_row_action('qlik_firmy', 'import_data2', views.import_data2),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    url('form/QlikViewUploadForm/$', views.view_qlikviewuploadform, {}),
    url('form/QlikTkw/$', views.view_qliktkw, {}),
    url('form/QlikRabat/$', views.view_qlikrabat, {}),
    url('form/QlikViewTkw2/$', views.view_qlikviewtkw2, {}),
]

gen = generic_table_start(urlpatterns, 'qlikview', views)


gen.standard('qlik_klient', _('qlik_klient'), _('qlik_klient'))
gen.standard('qlik_kar', _('qlik_kar'), _('qlik_kar'))
gen.standard('qlik_handlowiec', _('qlik_handlowiec'), _('qlik_handlowiec'))
gen.standard('qlik_dok', _('qlik_dok'), _('qlik_dok'))
gen.standard('qlik_mm', _('qlik_mm'), _('qlik_mm'))
gen.standard('qlik_lokalizacje', _('qlik_lokalizacje'), _('qlik_lokalizacje'))
gen.standard('qlik_segmentacja', _('qlik_segmentacja'), _('qlik_segmentacja'))
gen.standard('qlik_grupa_asortyment', _('qlik_grupa_asortyment'), _('qlik_grupa_asortyment'))
gen.standard('qlik_firmy', _('qlik_firmy'), _('qlik_firmy'))

