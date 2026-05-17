from django.urls import reverse

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView, UpdateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from mainha import forms as MainhaForms
from mainha import models as MainhaModels
from mainha import scopes as MainhaScopes


class UserAccountCreateView(LoginRequiredMixin, PermissionRequiredMixin, SingleObjectMixin, FormView):
    model = MainhaModels.Account
    form_class = MainhaForms.CreateUserAccountForm
    template_name = 'user_account/create.html'

    def get_queryset(self):
        return MainhaScopes.Scopes.list_accounts(self.request.user)

    def has_permission(self):
        return MainhaScopes.Scopes.has_director_permission(self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MainhaForms.CreateUserAccountForm(request.POST)

        if form.is_valid():
            user_form = UserCreationForm({
                'email': form.cleaned_data.get('email'),
                'username': form.cleaned_data.get('email'),
                'password1': form.cleaned_data.get('password1'),
                'password2': form.cleaned_data.get('password2')
            })

            if user_form.is_valid():
                new_user = user_form.save()
                new_user.email = new_user.username
                new_user.save()

                role = form.cleaned_data.get('role')
                account = self.object

                if not self.request.user.is_staff:
                    account = self.request.user.useraccount_set.first().account
                MainhaModels.UserAccount.objects.create(user=new_user, account=account, role=role)

                return self.form_valid(form)
            else:
                for field, errors in user_form.errors.items():
                    for error in errors:
                        field_name = field.replace('username', 'email')
                        form.add_error(field_name, error)
                form.error_messages = user_form.error_messages

                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('account-detail', kwargs=self.kwargs)


class UserAccountUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.UserAccount
    form_class = MainhaForms.UpdateUserAccountForm
    template_name = 'user_account/update.html'

    def has_permission(self):
        return MainhaScopes.Scopes.has_director_permission(self.request.user)

    def get_success_url(self):
        return reverse('account-detail', kwargs={'pk': self.kwargs.get('account_id')})


class UserAccountDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.UserAccount
    template_name = 'user_account/delete.html'

    def has_permission(self):
        return MainhaScopes.Scopes.has_director_permission(self.request.user)

    def form_valid(self, form):
        user = self.object.user
        result = super().form_valid(form)

        user.delete()
        return result

    def get_success_url(self):
        return reverse('account-detail', kwargs={'pk': self.kwargs.get('account_id')})
