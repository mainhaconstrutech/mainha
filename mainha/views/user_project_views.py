from django.urls import reverse_lazy, reverse

# from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels

class UserProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MainhaModels.UserProject
    form_class = MainhaForms.UserProjectForm
    template_name = "user_project/create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"].update({"user": None})
        kwargs["initial"].update({"project": self.kwargs.get("pk")})
        return kwargs

    def has_permission(self):
        user_account = MainhaModels.UserAccount.objects.filter(
            user=self.request.user
        ).first()

        if self.request.user.is_staff:
            return True
        elif user_account is not None and user_account.role in ["director", "manager"]:
            return True
        else:
            return False
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = MainhaModels.Project.objects.get(id=self.kwargs.get("pk"))
        return context
        
    def get_success_url(self):
        return reverse('project-detail', kwargs=self.kwargs)
    
    

class UserProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.UserProject
    template_name = "user_project/delete.html"

    def has_permission(self):
        user_account = MainhaModels.UserAccount.objects.filter(
            user=self.request.user,
            account_id=self.kwargs.get("account_id")
        ).first()

        if self.request.user.is_staff:
            return True
        elif user_account is not None and user_account.role in ["director", "manager"]:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.kwargs['project_id']})