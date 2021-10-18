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


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskFile
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = "__all__"


class ProjectListSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()

    class Meta:
        model = models.Project
        fields = "__all__"


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


