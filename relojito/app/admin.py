from django.contrib import admin

from .models import (Client, Project, ProjectCollaborator,
                     ResolutionType, Task, TaskType)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'email', 'phone')



class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client')
    list_filter = ('client',)


class ProjectCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('project', 'user')
    list_filter = ('project',)


class ResolutionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_finished')
    list_filter = ('is_finished', )


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'date', 'owner', 'task_type',
                    'total_hours')
    list_filter = ('project', 'task_type')

admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCollaborator, ProjectCollaboratorAdmin)
admin.site.register(ResolutionType, ResolutionTypeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskType)
