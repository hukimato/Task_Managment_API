from django.contrib import admin

from .models import *


class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'weight', 'taskType', 'creation_date', 'dead_line', 'is_done')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title',)
    list_editable = ('is_done',)
    list_filter = ('taskType', 'is_done')


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chief', 'position',)
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user', 'chief', 'position',)
    list_filter = ('position',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'manager', )
    list_display_links = ('id', 'project_name')
    search_fields = ('id', 'project_name')


admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Project, ProjectAdmin)
