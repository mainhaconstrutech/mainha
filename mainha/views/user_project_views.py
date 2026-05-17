from django.urls import reverse

from django.views.generic.edit import DeleteView, CreateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels
from mainha import scopes as MainhaScopes


class UserProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MainhaModels.UserProject
    form_class = MainhaForms.UserProjectForm
    template_name = 'user_project/create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'].update({'user': None})
        kwargs['initial'].update({'project': self.kwargs.get('pk')})
        kwargs['user'] = self.request.user
        return kwargs

    def has_permission(self):
        return MainhaScopes.Scopes.has_manager_permission(self.request.user) and \
            MainhaScopes.Scopes.list_projects(self.request.user).filter(id=self.kwargs.get('pk')).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = MainhaModels.Project.objects.get(id=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse('project-detail', kwargs=self.kwargs)


class UserProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.UserProject
    template_name = 'user_project/delete.html'

    def has_permission(self):
        return MainhaScopes.Scopes.has_manager_permission(self.request.user)

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['project_id']})
