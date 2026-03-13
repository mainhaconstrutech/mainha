from django.urls import reverse_lazy, reverse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels

class StandardListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MainhaModels.Standard
    permission_required = 'is_staff'
    template_name = "standard/list.html"

    def get_queryset(self):
        return MainhaModels.Standard.objects.all().order_by("-id")


class StandardCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MainhaModels.Standard
    form_class = MainhaForms.StandardForm
    permission_required = 'is_staff'
    template_name = "standard/create.html"
    success_url = reverse_lazy("standard-list")


class StandardDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MainhaModels.Standard
    permission_required = 'is_staff'
    template_name = "standard/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standard_rules = MainhaModels.StandardRule.objects.filter(
            standard_id=self.kwargs["pk"]).order_by("group", "name").all()
        groups = set()

        for group in standard_rules.values("group").all():
            groups.add(group["group"])

        context["standard_rules"] = standard_rules
        context["groups"] = groups
        return context


class StandardUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.Standard
    form_class = MainhaForms.StandardForm
    permission_required = 'is_staff'
    template_name = "standard/update.html"

    def get_success_url(self):
        return reverse('standard-detail', kwargs=self.kwargs)


class StandardDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.Standard
    permission_required = 'is_staff'
    template_name = "standard/delete.html"
    success_url = reverse_lazy("standard-list")