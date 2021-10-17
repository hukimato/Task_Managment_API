from django.shortcuts import render
from djoser.views import UserViewSet
from djoser import signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser


class CustomUserViewSet(UserViewSet):

    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user, "password": serializer.initial_data.get('password')}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)

