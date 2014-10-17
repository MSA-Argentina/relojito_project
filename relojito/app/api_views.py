from rest_framework import viewsets

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    model = Task

    def get_queryset(self):
            return Task.objects.filter(owner=self.request.user)
