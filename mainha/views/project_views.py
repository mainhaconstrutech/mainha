from django.urls import reverse_lazy, reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectTemplateResponseMixin
from django.views.generic.edit import DeleteView, UpdateView, ModelFormMixin, ProcessFormView

from django.contrib.auth.mixins import LoginRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels
from mainha import scopes as MainhaScopes
from mainha import services as MainhaServices


class ProjectListView(LoginRequiredMixin, ListView):
    model = MainhaModels.Project
    template_name = 'project/list.html'

    def get_queryset(self):
        return MainhaScopes.Scopes.list_projects(self.request.user)


class ProjectCreateView(LoginRequiredMixin, SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = MainhaModels.Project
    form_class = MainhaForms.ProjectForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('project-list')

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = self.model.objects.create(name=form.cleaned_data.get('name'))

        response = super().post(request, *args, **kwargs)
        self.object = MainhaServices.ProjectService.set_project_context(self.request.user, self.object)
        return response


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = MainhaModels.Project
    template_name = 'project/detail.html'

    def get_queryset(self):
        return MainhaScopes.Scopes.list_projects(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_users'] = MainhaModels.UserProject.objects.filter(project_id=self.kwargs.get('pk'))
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = MainhaModels.Project
    form_class = MainhaForms.ProjectForm
    template_name = 'project/update.html'

    def get_queryset(self):
        return MainhaScopes.Scopes.list_projects(self.request.user)

    def get_success_url(self):
        return reverse('project-detail', kwargs=self.kwargs)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = MainhaModels.Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('project-list')

    def get_queryset(self):
        return MainhaScopes.Scopes.list_projects(self.request.user)
