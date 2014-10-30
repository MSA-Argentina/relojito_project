from rest_framework import viewsets

from .models import Task, Project, ResolutionType, TaskType
from .serializers import (TaskSerializer, ProjectSerializer,
                          ResolutionSerializer, TaskTypeSerializer)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    model = Task

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    model = Project

    def get_queryset(self):
        return Project.objects.filter(projectcollaborator__user=self.request.user,
                                      is_active=True)


class ResolutionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResolutionSerializer
    model = ResolutionType


class TaskTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskTypeSerializer
    model = TaskType
