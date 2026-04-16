from django.urls import reverse_lazy, reverse

# from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels

class UserAccountCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = MainhaForms.CreateUserAccountForm
    template_name = "user_account/create.html"

    def has_permission(self):
        user_account = MainhaModels.UserAccount.objects.filter(
            user=self.request.user,
            account_id=self.kwargs.get("pk")
        ).first()

        if self.request.user.is_staff:
            return True
        elif user_account is not None and user_account.role == "director":
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        form = MainhaForms.CreateUserAccountForm(request.POST)

        if form.is_valid():
            user_form = MainhaForms.UserRegistrationForm({
                "email": form.cleaned_data.get("email"),
                "username": form.cleaned_data.get("email"),
                "password": form.cleaned_data.get("password"),
            })

            if user_form.is_valid():
                new_user = user_form.save()
                account = MainhaModels.Account.objects.get(id=self.kwargs.get("pk"))
                role = form.cleaned_data.get("role")
                MainhaModels.UserAccount.objects.create(user=new_user, account=account, role=role)

                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = MainhaModels.Account.objects.get(id=self.kwargs.get("pk"))
        return context
        
    def get_success_url(self):
        return reverse('account-detail', kwargs=self.kwargs)
    

class UserAccountUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.UserAccount
    form_class = MainhaForms.UpdateUserAccountForm
    template_name = "user_account/update.html"

    def has_permission(self):
        user_account = MainhaModels.UserAccount.objects.filter(
            user=self.request.user,
            account_id=self.kwargs.get("account_id")
        ).first()

        if self.request.user.is_staff:
            return True
        elif user_account is not None and user_account.role == "director":
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('account-detail', kwargs={'pk': self.kwargs['account_id']})
    

class UserAccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.UserAccount
    template_name = "user_account/delete.html"

    def has_permission(self):
        user_account = MainhaModels.UserAccount.objects.filter(
            user=self.request.user,
            account_id=self.kwargs.get("account_id")
        ).first()

        if self.request.user.is_staff:
            return True
        elif user_account is not None and user_account.role == "director":
            return True
        else:
            return False
        
    def form_valid(self, form):
        user = self.object.user
        result = super().form_valid(form)

        user.delete()
        return result

    def get_success_url(self):
        return reverse('account-detail', kwargs={'pk': self.kwargs['account_id']})