from app.views import (CreateProject, CreateTask, EditProject, EditTask,
                       GetToken, IndexView, login_user, logout_user,
                       ProjectDetail, TaskAjaxDetail, TaskAjaxList,
                       TaskDelete, TaskDetail, TaskMonthlyView,
                       total_tasks)
from axes.decorators import watch_login
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='root'),

                       url(r'^login/$',
                           watch_login(login_user), name='login'),
                       url(r'^logout/$',
                           logout_user, name='logout'),

                       url(r'^change_password/$',
                           'django.contrib.auth.views.password_change',
                           {'post_change_redirect': '/',
                            'template_name': 'password_change.html'},
                           name="password_change"),

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

                       url(r'^task/delete/(?P<pk>\d+)/$',
                           TaskDelete.as_view(),
                           name="task_delete"),

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

                       url(r'^get_token/$',
                           GetToken.as_view(),
                           name="get_token"),
                       )
