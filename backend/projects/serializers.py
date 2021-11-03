from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskType
        fields = "__all__"

    def create(self, validated_data):
        task_type = models.TaskType.objects.create(
            title=validated_data.get('title', None),
            project=validated_data.get('project', None)
        )
        return task_type


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskFile
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"

    def create(self, validated_data):
        task = models.Task.objects.create(
            title=validated_data.get('title', None),
            content=validated_data.get('content', None),
            weight=validated_data.get('weight', None),
            taskType=validated_data.get('taskType', None),
            dead_line=validated_data.get('dead_line', None),
            is_done=validated_data.get('is_done', None),
            project=validated_data.get('project', None),
            doers=validated_data.get('doers', None)
        )
        return task


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = "__all__"

    def create(self, validated_data):
        position = models.Position.objects.create(
            title=validated_data.get('title', None),
            project=validated_data.get('project', None)
        )
        return position


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = "__all__"

    def create(self, validated_data):
        position = models.Position.objects.create(
            user=models.User.objects.get(validated_data.get('user_id', None)),
            chief=validated_data.get('chief', None),
            position=validated_data.get('position', None),
            project=validated_data.get('project', None)
        )
        return position


class ProjectSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = (
            "id",
            "project_name",
            "manager"
        )

    def create(self, validated_data):
        project = models.Project.objects.create(
            manager=validated_data.get('manager', None),
            project_name=validated_data.get('project_name', None)
        )
        return project



'''
class ProjectSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    employees = EmployeeSerializer(many=True)
    task_types = TaskTypeSerializer(many=True)
    tasks = TaskSerializer(many=True)
    positions = PositionSerializer(many=True)

    class Meta:
        model = models.Project
        fields = (
            "id",
            "project_name",
            "manager",
            "employees",
            "task_types",
            "tasks",
            "positions"
        )
'''

