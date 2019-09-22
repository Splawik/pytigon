## -- coding: utf-8 --

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from pytigon_lib.schviews import generic_table_start, gen_tab_action, gen_row_action
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url('put$', views.put, {}),
    url('put_message$', views.put_message, {}),
    url('get_messages$', views.get_messages, {}),
    url('pop_messages$', views.pop_messages, {}),
    url('kill_thread$', views.kill_thread, {}),
    url('remove_thread$', views.remove_thread, {}),
    url('list_threads', views.list_threads, {}),
    url('thread_info$', views.thread_info, {}),
    url('kill_all$', views.kill_all, {}),
    url('wait_for_result$', views.wait_for_result, {}),
    url('form/TaskListForm/(?P<id>\d+)/(edit2__)*task$', views.edit_task, {}),
    url('form/TaskListForm/(?P<id>\d+)/delete2__task$', views.kill_task, {}),
    
    
    
    
    
    url('form/TaskListForm/$', views.view_tasklistform, {}),
]

gen = generic_table_start(urlpatterns, 'schtasks', views)



