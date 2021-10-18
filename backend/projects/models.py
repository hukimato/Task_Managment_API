from django.db import models


class TaskType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    project = models.ForeignKey('Project',default=None, on_delete=models.CASCADE, blank=False, verbose_name='Проект',
                                related_name='task_types')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'
        ordering = ['title']


class TaskFile(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d/', verbose_name='Файл', blank=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, blank=False, verbose_name='Проект')

    def __str__(self):
        return f"{self.file} {self.task}"

    class Meta:
        verbose_name = 'Файл задачи'
        verbose_name_plural = 'Файлы задачи'
        ordering = ['task']


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    content = models.TextField(verbose_name='Описание задания', default=None)
    weight = models.IntegerField(verbose_name='Сложность')
    taskType = models.ForeignKey('TaskType', default=None, on_delete=models.PROTECT, blank=True, verbose_name='Тип задания')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    dead_line = models.DateTimeField(blank=True, verbose_name='Срок сдачи')
    is_done = models.BooleanField(default=False)
    project = models.ForeignKey('Project',default=None, on_delete=models.CASCADE, blank=False, verbose_name='Проект',
                                related_name='tasks')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['project', '-creation_date']


class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    project = models.ForeignKey('Project', default=None, on_delete=models.CASCADE, blank=False, verbose_name='Проект',
                                related_name='positions')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['project', 'title']


class Employee(models.Model):  # Employee сильно связанный с проектом. Создается в момент добавления юзера в проект
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    chief = models.ForeignKey(
        'self', on_delete=models.SET_DEFAULT, blank=True, default=None, verbose_name='Начальник', null=True
    )
    position = models.ForeignKey('Position', on_delete=models.PROTECT, blank=True, verbose_name='Роль')
    project = models.ForeignKey('Project', default=None, on_delete=models.CASCADE, blank=False, verbose_name='Проект',
                                related_name='employees')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['project', 'id']


class Project(models.Model):
    project_name = models.CharField(max_length=100, verbose_name='Наименование')
    manager = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='manager', verbose_name='Менеджер проекта')

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['project_name']
