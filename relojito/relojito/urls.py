from app.api_views import (ProjectViewSet, TaskDayView, TaskTypeViewSet,
                           TaskViewSet)
from app.views import (CreateProject, CreateProjectCollaborator, CreateTask,
                       EditProfile, EditProject, EditTask, GetToken, IndexView,
                       PersonalStats, ProjectDetail, ProjectList,
                       TaskAjaxDetail, TaskAjaxList, TaskDelete, TaskDetail,
                       ViewProfile, ajax_stats, login_user, logout_user,
                       reset_token, total_tasks)
from django.conf.urls import include, patterns, url
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'task_types', TaskTypeViewSet)

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='root'),

                       url(r'^login/$',
                           login_user, name='login'),
                       url(r'^logout/$',
                           logout_user, name='logout'),

                       url(r'^captcha/', include('captcha.urls')),

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

                       url(r'^ajax_stats/$',
                           ajax_stats, name='ajax_stats'),

                       url(r'^personal_stats/$',
                           PersonalStats.as_view(), name='personal_stats'),

                       url(r'^projects/$',
                           ProjectList.as_view(), name='project_list'),

                       url(r'^profile/edit$',
                           EditProfile.as_view(), name='edit_profile'),

                       url(r'^profile/(?P<pk>\d+)/$',
                           ViewProfile.as_view(), name='view_profile'),

                       url(r'^project/new/$',
                           CreateProject.as_view(),
                           name="create_project"),

                       url(r'^projectcollaborator/new/$',
                           CreateProjectCollaborator.as_view(),
                           name="create_projectcollaborator"),

                       url(r'^project/edit/(?P<pk>\d+)/$',
                           EditProject.as_view(),
                           name='edit_project'),

                       url(r'^task/(?P<pk>\d+)/$',
                           TaskDetail.as_view(),
                           name="task_detail"),

                       url(r'^task/delete/(?P<pk>\d+)/$',
                           TaskDelete.as_view(),
                           name="task_delete"),

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
                       url(r'^reset_token/$',
                           reset_token,
                           name="reset_token"),

                       url(r'^api/tasks_day/(?P<date>[0-9-]+)/$',
                           TaskDayView.as_view(),
                           name='api_tasks_day'),

                       url(r'^api/', include(router.urls)),
                       )
