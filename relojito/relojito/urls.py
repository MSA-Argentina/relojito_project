from app.views import (CreateProject, CreateTask, EditProject, EditTask,
                       IndexView, login_user, logout_user, ProjectDetail,
                       TaskAjaxDetail, TaskAjaxList, TaskDetail,
                       TaskMonthlyView, total_tasks)
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='root'),

                       url(r'^login/$',
                           login_user, name='login'),
                       url(r'^logout/$',
                           logout_user, name='logout'),

                       url(r'^project/(?P<pk>\d+)/$',
                           ProjectDetail.as_view(),
                           name="project_detail"),

                       url(r'^total_tasks/$',
                           total_tasks, name='total_tasks'),

                       url(r'^project/new/$',
                           CreateProject.as_view(),
                           name="create_project"),

                       url(r'^project/edit/(?P<pk>\d+)/$',
                           EditProject.as_view(),
                           name='edit_project'),

                       url(r'^task/(?P<pk>\d+)/$',
                           TaskDetail.as_view(),
                           name="task_detail"),

                       url(r'^(?P<year>\d{4})/(?P<month>\d+)/$',
                           TaskMonthlyView.as_view(month_format='%m'),
                           name="monthly_tasks"),

                       url(r'^task/edit/(?P<pk>\d+)/$',
                           EditTask.as_view(),
                           name='edit_task'),

                       url(r'^task/json/(?P<pk>\d+)/$',
                           TaskAjaxDetail.as_view(),
                           name='ajax_task_detail'),

                       url(r'^tasks/json/$',
                           TaskAjaxList.as_view(),
                           name='edit_task'),

                       url(r'^task/new/$',
                           CreateTask.as_view(),
                           name="create_task"),

                       url(r'^admin/', include(admin.site.urls)),
                       )
