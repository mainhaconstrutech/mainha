from django.urls import reverse_lazy, reverse

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_projects = MainhaModels.Project.objects.filter(
            user=self.request.user).order_by("-updated_at")
        projects_all_total = all_projects.count()
        projects_success_total = all_projects.filter(status="success").count()
        projects_success_rate = projects_success_total / \
            projects_all_total * 100 if projects_all_total != 0 else 0
        context["projects"] = all_projects
        context["projects_all_total"] = projects_all_total
        context["projects_success_total"] = projects_success_total
        context["projects_failed_total"] = all_projects.filter(
            status="failed").count()
        context["projects_success_rate"] = projects_success_rate
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = MainhaModels.Project
    template_name = "project/list.html"

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = MainhaModels.Project
    form_class = MainhaForms.ProjectForm
    template_name = "project/create.html"
    success_url = reverse_lazy("project-list")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        self.object.user = request.user
        self.object.save()
        return response


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = MainhaModels.Project
    template_name = "project/detail.html"

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = MainhaModels.Project
    form_class = MainhaForms.ProjectForm
    template_name = "project/update.html"

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('project-detail', kwargs=self.kwargs)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = MainhaModels.Project
    template_name = "project/delete.html"
    success_url = reverse_lazy("project-list")

    def get_queryset(self):
        return MainhaModels.Project.objects.filter(user=self.request.user)


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
        print(groups)
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


class StandardRuleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MainhaModels.StandardRule
    form_class = MainhaForms.StandardRuleForm
    permission_required = 'is_staff'
    template_name = "standard_rule/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["standard_id"] = self.kwargs["standard_id"]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        standard = MainhaModels.Standard.objects.get(
            pk=self.kwargs["standard_id"])
        kwargs["initial"].update({"standard": standard.id})
        return kwargs

    def get_success_url(self):
        return reverse('standard-detail', kwargs={'pk': self.kwargs['standard_id']})


class StandardRuleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MainhaModels.StandardRule
    permission_required = 'is_staff'
    template_name = "standard_rule/detail.html"


class StandardRuleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MainhaModels.StandardRule
    form_class = MainhaForms.StandardRuleForm
    permission_required = 'is_staff'
    template_name = "standard_rule/update.html"

    def get_success_url(self):
        return reverse('standard-rule-detail', kwargs=self.kwargs)


class StandardRuleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MainhaModels.StandardRule
    permission_required = 'is_staff'
    template_name = "standard_rule/delete.html"

    def get_success_url(self):
        return reverse('standard-detail', kwargs={'pk': self.kwargs['standard_id']})
