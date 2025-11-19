from django.urls import path
from django.views.generic.base import RedirectView
from mainha.views import DashboardView, ProjectListView, ProjectCreateView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path("", RedirectView.as_view(url="/dashboard"), name="index"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/new/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<slug:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<slug:pk>/edit/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<slug:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
]