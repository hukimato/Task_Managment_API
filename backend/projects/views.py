from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models as django_models

from . import models
from . import serializers


class ProjectListView(APIView):

    def get(self, request):
        projects = models.Project.objects.all()
        serializer = serializers.ProjectListSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectView(APIView):

    def get(self, request, pk):
        project = models.Project.objects.get(id=pk)
        '''.annotate(
            employees='employee_project__id'
            )'''
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data)
