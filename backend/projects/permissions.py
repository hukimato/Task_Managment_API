from rest_framework.permissions import BasePermission
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class IsParticipantOfProject(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if models.Employee.objects.filter(user=request.user, project=obj).exists() and request.method == 'GET':
            return True
        return False


class IsManagerOfProject(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.manager == request.user:
            return True
        return False


class IsChiefOfEmployee(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj1, obj2):  # obj1 - проект, obj2 - работники
        if models.Employee.objects.filter(user=request.user, project=obj1).exists():
            chief = obj2.chief
            while chief:
                if chief == models.Employee.objects.get(user=request.user, project=obj1):
                    return True
                chief = chief.chief
                return False
        elif obj1.manager == request.user:
            return True
        return False




        # if models.Employee.objects.filter(user=request.user, project=obj1).exists():
        #     if not obj2:
        #         return True
        #     for obj in obj2:
        #         chief = obj.chief
        #         while chief:
        #             if chief == models.Employee.objects.get(user=request.user, project=obj1):
        #                 return True
        #             chief = chief.chief
        #         return False
        # elif obj1.manager == request.user:
        #     return True
        # return False
