from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models as django_models

from . import models
from . import serializers


class ProjectListView(APIView):

    def get(self, request):
        projects = models.Project.objects.filter(manager=self.request.user)
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(manager=self.request.user)
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        project = models.Project.objects.get(id=request.data.get("id"))
        project.delete()
        return Response(status=200)


class ProjectParticipantListView(APIView):  # Работает

    def get(self, request):

        projects = [employee.project for employee in models.Employee.objects.filter(user=self.request.user)]

        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectView(APIView):

    def get(self, request, pk):
        project = models.Project.objects.get(id=pk)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data)

    def patch(self, request, pk):
        project = models.Project.objects.get(id=pk)
        serializer = serializers.ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(manager=self.request.user)
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, pk):
        project = models.Project.objects.get(id=pk)
        project.delete()
        return Response(status=200)


class PositionListView(APIView):

    def get(self, request, pk):
        position = models.Position.objects.filter(project=pk)
        serializer = serializers.PositionSerializer(position, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = serializers.PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)


class PositionView(APIView):

    def get(self, request, pk, pos_pk):
        position = models.Position.objects.get(project=pk, id=pos_pk)
        serializer = serializers.PositionSerializer(position)
        return Response(serializer.data)

    def patch(self, request, pk, pos_pk):
        position = models.Position.objects.get(project=pk, id=pos_pk)
        serializer = serializers.PositionSerializer(position, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, pk, pos_pk):
        position = models.Position.objects.get(project=pk, id=pos_pk)
        position.delete()
        return Response(status=200)


class TaskTypeListView(APIView):

    def get(self, request, pk):
        task_type = models.TaskType.objects.filter(project=pk)
        serializer = serializers.TaskTypeSerializer(task_type, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = serializers.TaskTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)


class TaskTypeView(APIView):

    def get(self, request, pk, pos_pk):
        task_type = models.TaskType.objects.get(project=pk, id=pos_pk)
        serializer = serializers.TaskTypeSerializer(task_type)
        return Response(serializer.data)

    def patch(self, request, pk, pos_pk):
        task_type = models.TaskType.objects.get(project=pk, id=pos_pk)
        serializer = serializers.PositionSerializer(task_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, pk, pos_pk):
        task_type = models.TaskType.objects.get(project=pk, id=pos_pk)
        task_type.delete()
        return Response(status=200)


class EmployeeListView(APIView):

    def get(self, request, pk):
        employee = models.Employee.objects.filter(project=pk)
        serializer = serializers.EmployeeSerializer(employee, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = serializers.EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)


class EmployeeView(APIView):

    def get(self, request, pk, pos_pk):
        employee = models.Employee.objects.get(project=pk, id=pos_pk)
        serializer = serializers.EmployeeSerializer(employee)
        return Response(serializer.data)


    def patch(self, request, pk, pos_pk):
        employee = models.Employee.objects.get(project=pk, id=pos_pk)
        serializer = serializers.EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, pk, pos_pk):
        employee = models.Employee.objects.get(project=pk, id=pos_pk)
        employee.delete()
        return Response(status=200)


class TaskListView(APIView):

    def get(self, request, pk):
        tasks = models.Task.objects.filter(project=pk)
        serializer = serializers.TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = serializers.TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)

class TaskView(APIView):

    def get(self, requset, pk, pos_pk):
        task = models.Task.objects.get(project=pk, id=pos_pk)
        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk, pos_pk):
        task = models.Task.objects.get(project=pk, id=pos_pk)
        serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request, pk, pos_pk):
        task = models.Task.objects.get(project=pk, id=pos_pk)
        task.delete()
        return Response(status=200)


















