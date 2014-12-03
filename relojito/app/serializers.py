from rest_framework import serializers

from .models import Project, Task, TaskType


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ('owner',)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project


class TaskTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskType
