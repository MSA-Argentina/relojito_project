from rest_framework import serializers

from .models import Task, Project, ResolutionType


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project


class ResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResolutionType
