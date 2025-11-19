from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from mainha.forms import ProjectForm

from mainha.models import Project

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_projects = Project.objects.filter(user=self.request.user).order_by("-updated_at")
        projects_all_total = all_projects.count()
        projects_success_total = all_projects.filter(status="success").count()
        projects_success_rate = projects_success_total / projects_all_total * 100 if projects_all_total != 0 else 0
        context["projects"] = all_projects
        context["projects_all_total"] = projects_all_total
        context["projects_success_total"] = projects_success_total
        context["projects_failed_total"] = all_projects.filter(status="failed").count()
        context["projects_success_rate"] = projects_success_rate
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "project/list.html"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project/create.html"
    success_url = reverse_lazy("project-list")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        self.object.user = request.user
        self.object.save()
        return response

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "project/detail.html"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project/update.html"
    success_url = reverse_lazy("project-list")

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "project/delete.html"
    success_url = reverse_lazy("project-list")

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
