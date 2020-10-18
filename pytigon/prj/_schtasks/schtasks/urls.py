## -- coding: utf-8 --

from django.urls import path, re_path, include
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('put', views.put, {}),
    path('put_message', views.put_message, {}),
    path('get_messages', views.get_messages, {}),
    path('pop_messages', views.pop_messages, {}),
    path('kill_thread', views.kill_thread, {}),
    path('remove_thread', views.remove_thread, {}),
    path('list_thread', views.list_threads, {}),
    path('thread_info', views.thread_info, {}),
    path('kill_all', views.kill_all, {}),
    path('wait_for_result', views.wait_for_result, {}),
    re_path('form/TaskListForm/(?P<id>\d+)/(edit2__)*task', views.edit_task, {}),
    re_path('form/TaskListForm/(?P<id>\d+)/delete2__task', views.kill_task, {}),
    
    
    
    
    
    path('form/TaskListForm/', views.view_tasklistform, {}),
]

gen = generic_table_start(urlpatterns, 'schtasks', views)



