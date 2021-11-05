from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models as django_models
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError

from . import models
from . import serializers
from .permissions import IsManagerOfProject, IsParticipantOfProject, IsChiefOfEmployee


class ProjectListView(APIView):

    def get(self, request):  # Работает
        projects = models.Project.objects.filter(manager=self.request.user)
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):  # Работает
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(manager=self.request.user)
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(status=201)
        else:
            return Response(status=400)

    # def delete(self, request):  # Работает
    #     project = models.Project.objects.get(id=request.data.get("id"))
    #     project.delete()
    #     return Response(status=200)


class ProjectParticipantListView(APIView):  # Работает

    def get(self, request):
        projects = [employee.project for employee in models.Employee.objects.filter(user=self.request.user)]
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectView(APIView):
    permission_classes = [IsParticipantOfProject | IsManagerOfProject]

    def get(self, request, pk):
        project = models.Project.objects.get(id=pk)
        self.check_object_permissions(request, project)
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data)

    def patch(self, request, pk):
        project = models.Project.objects.get(id=pk)
        self.check_object_permissions(request, project)
        serializer = serializers.ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(manager=self.request.user)
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(serializer.data, status=201)
        else:
            return Response({'error': 'InvalidSerializer'}, status=400)

    def delete(self, request, pk):
        project = models.Project.objects.get(id=pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=200)


class PositionListView(APIView):
    permission_classes = [IsParticipantOfProject | IsManagerOfProject]

    def get(self, request, pk):
        position = models.Position.objects.filter(project=pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.PositionSerializer(position, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = serializers.PositionSerializer(data=request.data)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk))
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(serializer.data, status=201)
        else:
            return Response({'error': 'IntegrityError'},status=400)


class PositionView(APIView):
    permission_classes = [IsManagerOfProject]

    def get(self, request, pk, pos_pk):
        position = models.Position.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.PositionSerializer(position)
        return Response(serializer.data)

    def patch(self, request, pk, pos_pk):
        position = models.Position.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.PositionSerializer(position, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk))
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(status=201)
        else:
            return Response({'error': 'InvalidSerializer'},status=400)

    def delete(self, request, pk, pos_pk):
        position = models.Position.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        position.delete()
        return Response(status=200)


class TaskTypeListView(APIView):
    permission_classes = [IsParticipantOfProject | IsManagerOfProject]

    def get(self, request, pk):
        task_type = models.TaskType.objects.filter(project=pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.TaskTypeSerializer(task_type, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = serializers.TaskTypeSerializer(data=request.data)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk))
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(status=201)
        else:
            return Response({'error': 'InvalidSerializer'},status=400)


class TaskTypeView(APIView):
    permission_classes = [IsManagerOfProject]

    def get(self, request, pk, pos_pk):
        task_type = models.TaskType.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.TaskTypeSerializer(task_type)
        return Response(serializer.data)

    def patch(self, request, pk, pos_pk):
        task_type = models.TaskType.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.PositionSerializer(task_type, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk))
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(status=201)
        else:
            return Response({'error': 'InvalidSerializer'},status=400)

    def delete(self, request, pk, pos_pk):
        task_type = models.TaskType.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        task_type.delete()
        return Response(status=200)


class EmployeeListView(APIView):
    permission_classes = [IsParticipantOfProject | IsManagerOfProject]

    def get(self, request, pk):
        employee = models.Employee.objects.filter(project=pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.EmployeeSerializer(employee, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        if models.Position.objects.get(id=request.data.get('position')).project != models.Project.objects.get(id=pk):
            return Response({'error': 'Invalid position'}, status=400)
        serializer = serializers.EmployeeSerializer(data=request.data)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk))
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(serializer.data, status=201)
        else:
            return Response({'error': 'InvalidSerializer'}, status=400)


class EmployeeView(APIView):
    permission_classes = [IsParticipantOfProject | IsManagerOfProject]

    def get(self, request, pk, pos_pk):
        employee = models.Employee.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.EmployeeSerializer(employee)
        return Response(serializer.data)


    def patch(self, request, pk, pos_pk):
        if request.data.get('position') and models.Position.objects.get(id=request.data.get('position')).project != models.Project.objects.get(id=pk):
            return Response({'error': 'Invalid position'}, status=400)
        employee = models.Employee.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk))
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(serializer.data, status=201)
        else:
            return Response({'error': 'InvalidSerializer'},status=400)

    def delete(self, request, pk, pos_pk):
        employee = models.Employee.objects.get(project=pk, id=pos_pk)
        employee.delete()
        return Response(status=200)


class TaskListView(APIView):
    permission_classes = [IsParticipantOfProject | IsManagerOfProject]

    def get(self, request, pk):
        tasks = models.Task.objects.filter(project=pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        if models.TaskType.objects.get(id=request.data.get('taskType')).project != models.Project.objects.get(id=pk):
            return Response({'error': 'Invalid position'}, status=400)
        serializer = serializers.TaskSerializer(data=request.data)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        doers_ids_str = request.data.get('doers_ids')
        doers_ids = [int(s) for s in doers_ids_str.split(',')]
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk),
                            doers=models.Employee.objects.filter(id__in=doers_ids)
                            )
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(serializer.data, status=201)
            #return Response(doers_ids)
        else:
            return Response({'error': 'InvalidSerializer'}, status=400)


class TaskView(APIView):
    permission_classes = [IsParticipantOfProject | IsManagerOfProject]

    def get(self, request, pk, pos_pk):
        task = models.Task.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.TaskSerializer(task)
        return Response(serializer.data)

    def patch(self, request, pk, pos_pk):
        if request.data.get('taskType') and models.TaskType.objects.get(id=request.data.get('taskType')).project != models.Project.objects.get(id=pk):
            return Response({'error': 'Invalid position'}, status=400)
        task = models.Task.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
        if request.data.get('doers_ids'):
            doers_ids_str = request.data.get('doers_ids')
            doers_ids = [int(s) for s in doers_ids_str.split(',')]
            if serializer.is_valid():
                try:
                    serializer.save(project=models.Project.objects.get(id=pk),
                                    doers=models.Employee.objects.filter(id__in=doers_ids)
                                    )
                except IntegrityError:
                    return Response({'error': 'IntegrityError'}, status=400)
                return Response(serializer.data, status=201)
            # return Response(doers_ids)
            else:
                return Response({'error': 'InvalidSerializer'},status=400)
        else:
            if serializer.is_valid():
                try:
                    serializer.save(project=models.Project.objects.get(id=pk))
                except IntegrityError:
                    return Response({'error': 'IntegrityError'}, status=400)
                return Response(serializer.data, status=201)
            # return Response(doers_ids)
            else:
                return Response({'error': 'InvalidSerializer'}, status=400)

    def delete(self, request, pk, pos_pk):
        task = models.Task.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk))
        task.delete()
        return Response(status=200)


class SetEmployeeOnTask(APIView):
    permission_classes = [IsChiefOfEmployee]

    def check_object_permissions(self, request, obj1, obj2):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj1, obj2):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def patch(self, request, pk, pos_pk):
        if not request.data.get('doer_id', None):
            return Response({'error': 'Invalid data'}, status=400)
        if models.Employee.objects.get(id=request.data.get('doer_id', None)).project != models.Project.objects.get(id=pk):
            return Response({'error': 'Invalid data'}, status=400)
        task = models.Task.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk),
                                      models.Employee.objects.get(id=request.data.get('doer_id', None)))
        task.doers.add(models.Employee.objects.get(id=request.data.get('doer_id', None)))
        serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save(project=models.Project.objects.get(id=pk))
            except IntegrityError:
                return Response({'error': 'IntegrityError'}, status=400)
            return Response(serializer.data, status=201)
        # return Response(doers_ids)
        else:
            return Response({'error': 'InvalidSerializer'},status=400)

    def delete(self, request, pk, pos_pk):
        if not request.data.get('doer_id', None):
            return Response(status=400)
        if models.Employee.objects.get(id=request.data.get('doer_id', None)).project != models.Project.objects.get(id=pk):
            return Response(status=400)
        task = models.Task.objects.get(project=pk, id=pos_pk)
        self.check_object_permissions(request, models.Project.objects.get(id=pk),
                                      models.Employee.objects.get(id=request.data.get('doer_id', None)))
        task.doers.remove(models.Employee.objects.get(id=request.data.get('doer_id', None)))
        serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(project=models.Project.objects.get(id=pk))
            return Response(serializer.data, status=201)
        # return Response(doers_ids)
        else:
            return Response({'error': 'InvalidSerializer'}, status=400)

        # if request.data.get('doers_ids'):
        #     doers_ids_str = request.data.get('doers_ids')
        #     doers_ids = [int(s) for s in doers_ids_str.split(',')]
        #     self.check_object_permissions(request, models.Project.objects.get(id=pk),
        #                                   models.Employee.objects.filter(id__in=doers_ids))
        #     if serializer.is_valid():
        #         serializer.save(project=models.Project.objects.get(id=pk),
        #                         doers=models.Employee.objects.filter(id__in=doers_ids)
        #                         )
        #         return Response(status=201)
        #     # return Response(doers_ids)
        #     else:
        #         return Response(status=400)
        # else:
        #     if serializer.is_valid():
        #         serializer.save(project=models.Project.objects.get(id=pk))
        #         return Response(status=201)
        #     # return Response(doers_ids)
        #     else:
        #         return Response(status=400)
















