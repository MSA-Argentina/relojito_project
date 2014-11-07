from rest_framework import viewsets
from rest_framework.response import Response

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

    def list(self, request, *args, **kwargs):
        instance = self.filter_queryset(self.get_queryset().order_by('-created_at')[:15])
        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(instance, many=True)

        return Response(serializer.data)


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
