from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, email, password=None, **extra_fields):
        if not username:
            raise ValueError('username должно быть установлено')

        if not email:
            raise ValueError('email должно быть установлено')

        if not first_name:
            raise ValueError('first_name должно быть установлено')

        if not last_name:
            raise ValueError('last_name должно быть установлено')

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        return self.create_user(username, first_name, last_name, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Логин')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


