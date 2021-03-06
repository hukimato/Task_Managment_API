from django.urls import path
from .import views


urlpatterns = [
    path("projects/", views.ProjectListView.as_view(), name="list_my_projects"),
    path("projects/participant/", views.ProjectParticipantListView.as_view(), name="list_part_projects"),
    path("projects/<int:pk>/", views.ProjectView.as_view(), name="project_id"),
    path("projects/<int:pk>/positions/", views.PositionListView.as_view(), name="project_positions_list"),
    path("projects/<int:pk>/positions/<int:pos_pk>/", views.PositionView.as_view(), name="project_positions_id"),
    path("projects/<int:pk>/tasktype/", views.TaskTypeListView.as_view(), name="project_taskType_list"),
    path("projects/<int:pk>/tasktype/<int:pos_pk>/", views.TaskTypeView.as_view(), name="project_taskType_id"),
    path("projects/<int:pk>/employee/", views.EmployeeListView.as_view(), name="project_employee_list"),
    path("projects/<int:pk>/employee/<int:pos_pk>/", views.EmployeeView.as_view(), name="project_employee_id"),
    path("projects/<int:pk>/task/<int:pos_pk>/", views.TaskView.as_view(), name="project_task_id"),
    path("projects/<int:pk>/task/", views.TaskListView.as_view(), name="project_task_list"),
    path("projects/<int:pk>/employee_set/<int:pos_pk>/", views.SetEmployeeOnTask.as_view(), name="project_set_employee"),
]
