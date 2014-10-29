from rest_framework import viewsets

from .models import Task, Project, ResolutionType
from .serializers import (TaskSerializer, ProjectSerializer,
                          ResolutionSerializer)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    model = Task

    def pre_save(self, obj):
        obj.owner = self.request.user
        obj.description = ""

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
