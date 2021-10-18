from django.urls import path
from .import views


urlpatterns = [
    path("projects/", views.ProjectListView.as_view()),
    path("projects/<int:pk>/", views.ProjectView.as_view())
]
