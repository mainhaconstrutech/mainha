from django.urls import reverse_lazy, reverse

from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import DeleteView, UpdateView, FormView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from mainha import forms as MainhaForms
from mainha import models as MainhaModels
from mainha import scopes as MainhaScopes
from mainha import services as MainhaServices


class AccountListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    template_name = "account/list.html"

    def get_queryset(self):
        return MainhaScopes.Scopes.list_accounts(self.request.user).order_by("name")


class AccountCreateAdminUserView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = MainhaForms.CreateAccountAdminUserForm
    permission_required = 'is_staff'
    template_name = "account/create.html"
    success_url = reverse_lazy("account-list")

    def post(self, request, *args, **kwargs):
        form = MainhaForms.CreateAccountAdminUserForm(request.POST)

        if form.is_valid():
            user_form = UserCreationForm({
                "email": form.cleaned_data.get("user_email"),
                "username": form.cleaned_data.get("user_email"),
                "password1": form.cleaned_data.get("user_password"),
                "password2": form.cleaned_data.get("user_password")
            })

            account_form = MainhaForms.AccountAdminUserForm({
                "name": form.cleaned_data.get("account_name"),
                "cnpj": form.cleaned_data.get("account_cnpj"),
                "email": form.cleaned_data.get("account_email"),
                "phone": form.cleaned_data.get("account_phone"),
                "subscription": form.cleaned_data.get("account_subscription")
            })

            if user_form.is_valid() and account_form.is_valid():
                new_user = user_form.save()
                new_account = account_form.save()
                MainhaModels.UserAccount.objects.create(user=new_user, account=new_account)

                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class AccountDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MainhaModels.Account
    template_name = "account/detail.html"

    def get_queryset(self):
        return MainhaScopes.Scopes.list_accounts(self.request.user).order_by("name")

    def has_permission(self):
        return MainhaScopes.Scopes.has_director_permission(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_users"] = MainhaModels.UserAccount.objects.filter(
            account_id=self.kwargs.get("pk")).order_by("user__username")
        return context


class AccountUpdateAdminUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.Account
    form_class = MainhaForms.AccountAdminUserForm
    permission_required = 'is_staff'
    template_name = "account/update.html"

    def get_success_url(self):
        return reverse('account-detail', kwargs=self.kwargs)


class AccountUpdateRegularUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.Account
    form_class = MainhaForms.AccountRegularUserForm
    template_name = "account/update.html"

    def get_queryset(self):
        return MainhaScopes.Scopes.list_accounts(self.request.user)

    def has_permission(self):
        return MainhaScopes.Scopes.has_director_permission(self.request.user)

    def get_success_url(self):
        return reverse('account-detail', kwargs=self.kwargs)


class AccountUpdateActiveStatusView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, RedirectView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    pattern_name = 'account-detail'

    def dispatch(self, request, *args, **kwargs):
        MainhaServices.AccountService.toggle_account_active(self.get_object())
        return super().dispatch(request, *args, **kwargs)


class AccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    template_name = "account/delete.html"
    success_url = reverse_lazy("account-list")
