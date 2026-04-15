from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, FormView
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


class AccountCreateAdminUserView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = MainhaForms.CreateAccountAdminUserForm
    permission_required = 'is_staff'
    template_name = "account/create.html"
    success_url = reverse_lazy("account-list")

    def post(self, request, *args, **kwargs):
        form = MainhaForms.CreateAccountAdminUserForm(request.POST)

        if form.is_valid():
            user_form = MainhaForms.UserRegistrationForm({
                "email": form.cleaned_data.get("user_email"),
                "username": form.cleaned_data.get("user_email"),
                "password": form.cleaned_data.get("user_password"),
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


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = MainhaModels.Account
    template_name = "account/detail.html"

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
        account.active = not (account.active)
        account.save()
        return redirect('account-detail', pk=account.id)


class AccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.Account
    permission_required = 'is_staff'
    template_name = "account/delete.html"
    success_url = reverse_lazy("account-list")
