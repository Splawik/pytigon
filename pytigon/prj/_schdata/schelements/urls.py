## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('table/DocHead/(?P<filter>[\w=_,;-]*)/(?P<target>[\w_-]*)/[_]?(?P<vtype>)docheadlist/', views.view_doc_heads, {}),
    url('table/DocItem/(?P<parent_id>\d+)/docitemlist/', views.view_doc_items, {}),
    url('table/DocHead/(?P<id>\d+)/edit_head/', views.edit_head, {}),
    url('table/DocItem/(?P<id>\d+)/edit_item/', views.edit_item, {}),
    gen_row_action('DocHead', 'approve', views.approve),
    gen_row_action('DocHead', 'discard', views.discard),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
]

gen = generic_table_start(urlpatterns, 'schelements', views)
gen.for_field('DocType', 'dochead_set', 'Documents', prefix="doc", template_name="schelements/dochead2.html")


gen.standard('Element', _('Element'), _('Element'))
gen.standard('OrgChartElem', _('Organizational chart'), _('Organizational chart'))
gen.standard('Classifier', _('Classifier'), _('Classifier'))
gen.standard('DocReg', _('Document register'), _('Document registers'))
gen.standard('DocType', _('Type of document'), _('Types of documents'))
gen.standard('DocHead', _('Document header'), _('Document headers'))
gen.standard('DocItem', _('Document item'), _('Document items'))
gen.standard('DocRegStatus', _('Document status'), _('Document status'))
gen.standard('DocHeadStatus', _('Document head status'), _('Documents head status'))
gen.standard('Account', _('Account'), _('Account'))
gen.standard('AccountState', _('State of account'), _('States of account'))
gen.standard('AccountOperation', _('Account operation'), _('Account operations'))



gen.for_field('DocReg', 'doctype_set', _('Type of document'), _('Types of documents'))
gen.for_field('DocType', 'dochead_set', _('Document header'), _('Document headers'))
gen.for_field('OrgChartElem', 'dochead_set', _('Document header'), _('Document headers'))
gen.for_field('DocHead', 'docitem_set', _('Document item'), _('Document items'))
gen.for_field('DocItem', 'docitem_set', _('Document item'), _('Document items'))
gen.for_field('DocReg', 'docregstatus_set', _('Document status'), _('Document status'))
gen.for_field('DocHead', 'docheadstatus_set', _('Document head status'), _('Documents head status'))

gen.for_field('Classifier', 'baseaccount_rc1_set', _('Account'), _('Account'))
gen.for_field('Classifier', 'baseaccount_rc2_set', _('Account'), _('Account'))
gen.for_field('Classifier', 'baseaccount_rc3_set', _('Account'), _('Account'))
gen.for_field('DocItem', 'accountoperation_set', _('Account operation'), _('Account operations'))
gen.for_field('AccountState', 'accountoper_set', _('Account operation'), _('Account operations'))
