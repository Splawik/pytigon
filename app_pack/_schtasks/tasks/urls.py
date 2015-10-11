## -- coding: utf-8 --

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from schlib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = patterns('',
    ('put$', views.put, {}),
    ('put_message$', views.put_message, {}),
    ('get_messages$', views.get_messages, {}),
    ('pop_messages$', views.pop_messages, {}),
    ('kill_thread$', views.kill_thread, {}),
    ('remove_thread$', views.remove_thread, {}),
    ('list_threads', views.list_threads, {}),
    ('thread_info$', views.thread_info, {}),
    ('kill_all$', views.kill_all, {}),
    ('wait_for_result$', views.wait_for_result, {}),
    ('form/TaskListForm/(?P<id>\d+)/(edit2__)*task$', views.edit_task, {}),
    ('form/TaskListForm/(?P<id>\d+)/delete2__task$', views.kill_task, {}),
    
    
    
    
    
    ('form/TaskListForm/$', views.view_tasklistform, {}),
)

gen = generic_table_start(urlpatterns, 'tasks', views)



