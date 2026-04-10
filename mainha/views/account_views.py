from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels


class AccountListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    template_name = "account/list.html"

    def get_queryset(self):
        return MainhaModels.Account.objects.all().order_by("name")


class AccountCreateAdminUserView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MainhaModels.Account
    form_class = MainhaForms.AccountAdminUserForm
    permission_required = 'is_staff'
    template_name = "account/create.html"
    success_url = reverse_lazy("account-list")


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = MainhaModels.Account
    template_name = "account/detail.html"


class AccountUpdateAdminUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.Account
    form_class = MainhaForms.AccountAdminUserForm
    permission_required = 'is_staff'
    template_name = "account/update.html"

    def get_success_url(self):
        return reverse('account-detail', kwargs=self.kwargs)


class AccountUpdateRegularUserView(LoginRequiredMixin, UpdateView):
    model = MainhaModels.Account
    form_class = MainhaForms.AccountRegularUserForm
    template_name = "account/update.html"

    def get_success_url(self):
        return reverse('account-detail', kwargs=self.kwargs)


class AccountUpdateActiveStatusView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = "account/detail.html"

    def dispatch(self, request, *args, **kwargs):
        account = MainhaModels.Account.objects.get(id=self.kwargs["pk"])
        account.active = not(account.active)
        account.save()
        return redirect('account-detail', pk=account.id)


class AccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    template_name = "account/delete.html"
    success_url = reverse_lazy("account-list")
