from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


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
            color=validated_data.get('color', None),
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
        doers = validated_data.get('doers')

        task = models.Task.objects.create(
            title=validated_data.get('title', None),
            content=validated_data.get('content', None),
            weight=validated_data.get('weight', None),
            taskType=validated_data.get('taskType', None),
            dead_line=validated_data.get('dead_line', None),
            is_done=validated_data.get('is_done', None),
            project=validated_data.get('project', None),
            #doers=validated_data.get('doers', None)
        )
        task.doers.set(validated_data.get('doers', None))
         #
         # if doers:
         #     for doer in doers:
         #         task.doers.add(doer)

        return task


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = "__all__"

    def create(self, validated_data):
        position = models.Position.objects.create(
            title=validated_data.get('title', None),
            color=validated_data.get('color', None),
            project=validated_data.get('project', None)
        )
        return position


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = "__all__"

    def create(self, validated_data):
        employee = models.Employee.objects.create(
            user=validated_data.get('user', None),
            chief=validated_data.get('chief', None),
            position=validated_data.get('position', None),
            project=validated_data.get('project', None)
        )
        return employee


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

