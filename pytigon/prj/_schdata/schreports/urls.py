## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('new_rep/(?P<rep_type>\w+)/(?P<doc_type_name>\w+)/$', views.new_rep, {}),
    url('table/Report/(?P<rep_id>\d+)/edit__rep/$', views.edit__rep, {}),
    url('new_subrep/(?P<parent_rep_id>\d+)/(?P<rep_type>\w+)/$', views.new_subrep, {}),
    url('edit_subrep/(?P<parent_rep_id>\d+)/(?P<rep_type>\w+)/(?P<view_type>\w+)/$', views.edit_subrep, {}),
    gen_row_action('Report', 'move_up', views.move_up),
    gen_row_action('Report', 'move_down', views.move_down),
    url('table/Report/(?P<dochead_id>\d+)/edit__rep2/$', views.edit__rep2, {}),
    url('table/Report/(?P<dochead_id>\d+)/repaction/(?P<rep_action>\w+)/$', views.repaction, {}),
    url('table/Report/(?P<rep_id>\d+)/(?P<to_pos>\d+)/action/move_to/$', views.move_to, {}),
    url('plot_service/(?P<name>\w+)/$', views.plot_service, {}),
    url('new_group/(?P<group_type>\w+)/(?P<parent_id>\d+)/$', views.new_group, {}),
    url('table/CommonGroup/(?P<group_id>\d+)/edit__group/$', views.edit__group, {}),
    url('list_group_by_tag/(?P<group_tag>\w+)/$', views.list_group_by_tag, {}),
    
    
    
    
    
    
    
    
    
    
    
    
]

gen = generic_table_start(urlpatterns, 'schreports', views)


gen.standard('ReportDef', _('Report definition'), _('Reports definitions'))
gen.standard('Report', _('Report'), _('Reports'))
gen.standard('CommonGroupDef', _('Common group definition'), _('Common groups definition'))
gen.standard('CommonGroup', _('Common group'), _('Common groups'))
gen.standard('Plot', _('Plot'), _('Polts'))



