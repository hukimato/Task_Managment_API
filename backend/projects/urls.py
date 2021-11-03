from django.urls import path
from .import views


urlpatterns = [
    path("projects/", views.ProjectListView.as_view()),
    path("projects/participant/", views.ProjectParticipantListView.as_view()),
    path("projects/<int:pk>/", views.ProjectView.as_view()),
    path("projects/<int:pk>/positions/", views.PositionListView.as_view()),
    path("projects/<int:pk>/positions/<int:pos_pk>/", views.PositionView.as_view()),
    path("projects/<int:pk>/tasktype/", views.TaskTypeListView.as_view()),
    path("projects/<int:pk>/tasktype/<int:pos_pk>/", views.TaskTypeView.as_view()),
    path("projects/<int:pk>/employee/", views.EmployeeListView.as_view()),
    path("projects/<int:pk>/employee/<int:pos_pk>/", views.EmployeeView.as_view()),
]
