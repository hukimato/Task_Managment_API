from django.db import models

# from Managment_System.users.models import User


class TaskType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'
        ordering = ['title']


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    # content = models.Fil сделать класс для файлов
    weight = models.IntegerField(verbose_name='Сложность')
    taskType = models.ForeignKey('TaskType', on_delete=models.PROTECT, blank=True, verbose_name='Тип')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    dead_line = models.DateTimeField(blank=True, verbose_name='Дэдлайн')
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-creation_date']


class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['title']


class Employee(models.Model):  # Employee сильно связанный с проектом. Создается в момент добавления юзера в проект
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, verbose_name='Пользователь')
    chief = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, default=None, verbose_name='Начальник', null=True)
    position = models.ForeignKey('Position', on_delete=models.PROTECT, blank=True, verbose_name='Роль')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['id']


class Project(models.Model):
    project_name = models.CharField(max_length=100, verbose_name='Наименование')
    manager = models.ForeignKey('Employee', on_delete=models.PROTECT, related_name='manager', verbose_name='Менеджер')
    task_types = models.ManyToManyField('TaskType', verbose_name='Тип')
    tasks = models.ManyToManyField('Task', verbose_name='Задания')
    workers = models.ManyToManyField('Employee', verbose_name='Работники')
    worker_types = models.ManyToManyField('Position', verbose_name='Роли')

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['project_name']
