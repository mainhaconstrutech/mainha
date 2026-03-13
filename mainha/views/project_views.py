from django.urls import reverse_lazy, reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels

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

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('project-detail', kwargs=self.kwargs)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = MainhaModels.Project
    template_name = "project/delete.html"
    success_url = reverse_lazy("project-list")

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)