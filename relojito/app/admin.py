from django.contrib import admin

from .models import (Client, Project, ProjectCollaborator, Holiday,
                     Task, TaskType)


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'description')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'email', 'phone')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'client', 'color', 'is_active')
    list_filter = ('client', 'is_active', 'owner')


class ProjectCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('project', 'user')
    list_filter = ('project', 'user')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'date', 'owner', 'task_type',
                    'total_hours')
    list_filter = ('project', 'task_type', 'owner')

admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCollaborator, ProjectCollaboratorAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(TaskType)
