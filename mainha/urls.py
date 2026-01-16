from django.urls import path
from django.views.generic.base import RedirectView

from mainha import views as MainhaViews

urlpatterns = [
    path("", RedirectView.as_view(url="/dashboard/"), name="index"),
    path("dashboard/", MainhaViews.DashboardView.as_view(), name="dashboard"),
    path("projects/", MainhaViews.ProjectListView.as_view(), name="project-list"),
    path("projects/new/", MainhaViews.ProjectCreateView.as_view(), name="project-create"),
    path("projects/<slug:pk>/", MainhaViews.ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<slug:pk>/edit/", MainhaViews.ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<slug:pk>/delete/", MainhaViews.ProjectDeleteView.as_view(), name="project-delete"),
    path("standards/", MainhaViews.StandardListView.as_view(), name="standard-list"),
    path("standards/new/", MainhaViews.StandardCreateView.as_view(), name="standard-create"),
    path("standards/<slug:pk>/", MainhaViews.StandardDetailView.as_view(), name="standard-detail"),
    path("standards/<slug:pk>/edit/", MainhaViews.StandardUpdateView.as_view(), name="standard-update"),
    path("standards/<slug:pk>/delete/", MainhaViews.StandardDeleteView.as_view(), name="standard-delete"),
    path("standards/<slug:standard_id>/standard-rule/new/", MainhaViews.StandardRuleCreateView.as_view(), name="standard-rule-create"),
    path("standards/<slug:standard_id>/standard-rule/<slug:pk>/", MainhaViews.StandardRuleDetailView.as_view(), name="standard-rule-detail"),
    path("standards/<slug:standard_id>/standard-rule/<slug:pk>/edit/", MainhaViews.StandardRuleUpdateView.as_view(), name="standard-rule-update"),
    path("standards/<slug:standard_id>/standard-rule/<slug:pk>/delete/", MainhaViews.StandardRuleDeleteView.as_view(), name="standard-rule-delete"),
]