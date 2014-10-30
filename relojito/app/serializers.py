from rest_framework import serializers

from .models import Task, Project, ResolutionType, TaskType


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('owner',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project


class ResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResolutionType


class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
