from django.urls import reverse_lazy, reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels


class AccountListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    template_name = "account/list.html"

    def get_queryset(self):
        return MainhaModels.Account.objects.all().order_by("name")


class AccountCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MainhaModels.Account
    form_class = MainhaForms.AccountAdminCreateForm
    permission_required = 'is_staff'
    template_name = "account/create.html"
    success_url = reverse_lazy("account-list")


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = MainhaModels.Account
    template_name = "account/detail.html"


# class AccountUpdateView(LoginRequiredMixin, UpdateView):
#     model = MainhaModels.Account
#     form_class = MainhaForms.AccountForm
#     template_name = "project/update.html"

#     def get_queryset(self):
#         return MainhaModels.Project.objects.filter(user=self.request.user)

#     def get_success_url(self):
#         return reverse('project-detail', kwargs=self.kwargs)


class AccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    template_name = "account/delete.html"
    success_url = reverse_lazy("account-list")
