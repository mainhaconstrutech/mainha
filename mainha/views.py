from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_projects = MainhaModels.Project.objects.filter(user=self.request.user).order_by("-updated_at")
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
    model = MainhaModels.Project
    template_name = "project/list.html"

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = MainhaModels.Project
    form_class = MainhaForms.ProjectForm
    template_name = "project/create.html"
    success_url = reverse_lazy("project-list")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        self.object.user = request.user
        self.object.save()
        return response

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = MainhaModels.Project
    template_name = "project/detail.html"

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = MainhaModels.Project
    form_class = MainhaForms.ProjectForm
    template_name = "project/update.html"
    success_url = reverse_lazy("project-list")

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = MainhaModels.Project
    template_name = "project/delete.html"
    success_url = reverse_lazy("project-list")

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)
    
class StandardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MainhaModels.Standard
    permission_required = 'is_staff'
    template_name = "standard/list.html"

    def get_queryset(self):
        return MainhaModels.Standard.objects.all().order_by("-id")
    
class StandardCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MainhaModels.Standard
    form_class = MainhaForms.StandardForm
    permission_required = 'is_staff'
    template_name = "standard/create.html"
    success_url = reverse_lazy("standard-list")

class StandardDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MainhaModels.Standard
    permission_required = 'is_staff'
    template_name = "standard/detail.html"

class StandardUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.Standard
    form_class = MainhaForms.StandardForm
    permission_required = 'is_staff'
    template_name = "standard/update.html"
    success_url = reverse_lazy("standard-list")

class StandardDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.Standard
    permission_required = 'is_staff'
    template_name = "standard/delete.html"
    success_url = reverse_lazy("standard-list")
