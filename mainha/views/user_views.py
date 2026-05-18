from django.urls import reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from mainha import forms as MainhaForms
from mainha import models as MainhaModels
from mainha import scopes as MainhaScopes


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'user/detail.html'
    context_object_name = 'user_data'

    def has_permission(self):
        authenticated_user = self.request.user
        user_data = User.objects.get(pk=self.kwargs.get('pk'))

        if authenticated_user == user_data:
            return True
        elif authenticated_user.is_superuser:
            return not(user_data.is_superuser)
        elif authenticated_user.is_staff:
            return not(user_data.is_staff)

        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_user'] = MainhaModels.UserAccount.objects.filter(user_id=self.kwargs.get('pk')).first()
        return context
    

class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = MainhaForms.UserForm
    template_name = 'user/update.html'
    context_object_name = 'user_data'

    def has_permission(self):
        return self.request.user ==User.objects.get(pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('user-detail', kwargs=self.kwargs)


# class UserUpdatePasswordView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = MainhaModels.UserAccount
#     template_name = 'user/delete.html'

#     def has_permission(self):
#         return MainhaScopes.Scopes.has_director_permission(self.request.user)

#     def form_valid(self, form):
#         user = self.object.user
#         result = super().form_valid(form)

#         user.delete()
#         return result

#     def get_success_url(self):
#         return reverse('account-detail', kwargs={'pk': self.kwargs.get('account_id')})
