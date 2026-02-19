from django.urls import reverse_lazy, reverse
from django.forms import formset_factory
from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView, FormView

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        standard = MainhaModels.Standard.objects.get(
            pk=self.kwargs["standard_id"])
        kwargs["initial"].update({"standard": standard.id})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["standard_id"] = self.kwargs["standard_id"]
        return context

    def get_success_url(self):
        return reverse('standard-detail', kwargs={'pk': self.kwargs['standard_id']})


class StandardRuleBulkCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = MainhaForms.StandardRuleBulkForm
    permission_required = 'is_staff'
    template_name = "standard_rule/bulk_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"].update({"standard": self.kwargs["standard_id"]})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["standard_id"] = self.kwargs["standard_id"]
        return context

    def form_valid(self, form):
        standard = form.cleaned_data["standard"]
        standard_rules = []
        for standard_rule_data in form.cleaned_data["standard_rules"]:
            standard_rules.append(MainhaModels.StandardRule(
                name=standard_rule_data.get("name"),
                description=standard_rule_data.get("description", ""),
                group=standard_rule_data.get("group", ""),
                standard=standard
            ))
        MainhaModels.StandardRule.objects.bulk_create(standard_rules)
        return super().form_valid(form)

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


class ValidationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MainhaModels.Validation
    permission_required = 'is_staff'
    template_name = "validation/list.html"

    def get_queryset(self):
        return MainhaModels.Validation.objects.filter(analyzed=False, analyzed_by=None).order_by("id")


class ValidationInProgressListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MainhaModels.Validation
    permission_required = 'is_staff'
    template_name = "validation/in_progress_list.html"

    def get_queryset(self):
        return MainhaModels.Validation.objects.filter(analyzed=False, analyzed_by=self.request.user).order_by("id")


class ValidationCreateView(LoginRequiredMixin, CreateView):
    model = MainhaModels.Validation
    form_class = MainhaForms.ValidationForm
    template_name = "validation/create.html"
    success_url = reverse_lazy("project-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"].update({"user": self.request.user})
        return kwargs


class ValidationCreateForProjectView(LoginRequiredMixin, CreateView):
    model = MainhaModels.Validation
    form_class = MainhaForms.ValidationForm
    template_name = "validation/create_for_project.html"
    success_url = reverse_lazy("project-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"].update({"user": self.request.user})
        kwargs["initial"].update({"project": self.kwargs["pk"]})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = MainhaModels.Project.objects.get(pk=self.kwargs["pk"])
        return context


class ValidationSetOperatorView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request, *args, **kwargs):
        validation = MainhaModels.Validation.objects.get(pk=self.kwargs["pk"])
        validation.analyzed_by = request.user
        validation.save()

        return redirect('validation-analysis', pk=validation.id)


class ValidationAnalysisView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = MainhaForms.ValidationRuleForm
    permission_required = 'is_staff'
    template_name = "validation/analysis.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        validation = MainhaModels.Validation.objects.get(pk=self.kwargs["pk"])
        standard_rules = MainhaModels.StandardRule.objects.filter(standard_id=validation.standard.id)

        initial_values = []
        for standard_rule in standard_rules:
            validation_rule = MainhaModels.ValidationRule.objects.filter(
                validation_id=validation.id,
                standard_rule_id=standard_rule.id
            ).first()

            initial_value = {
                "validation": validation,
                "standard_rule": standard_rule,
                "fulfilled": False
            }

            if validation_rule is not None:
                initial_value["fulfilled"] = validation_rule.fulfilled
                initial_value["note"] = validation_rule.note

            initial_values.append(initial_value)

        ValidationRuleFormSet = formset_factory(MainhaForms.ValidationRuleForm, extra=0)
        formset = ValidationRuleFormSet(initial=initial_values)

        context["standard_rules"] = standard_rules
        context["project"] = validation.project
        context["standard"] = validation.standard
        context["formset"] = formset

        return context

    def post(self, request, *args, **kwargs):
        validation = MainhaModels.Validation.objects.get(pk=kwargs["pk"])

        ValidationRuleFormSet = formset_factory(MainhaForms.ValidationRuleForm, extra=0)
        formset = ValidationRuleFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                form_data = form.cleaned_data
                validation_rule = MainhaModels.ValidationRule.objects.filter(
                    validation_id=form_data["validation"],
                    standard_rule_id=form_data["standard_rule"]
                ).first()

                if form_data:
                    if validation_rule is not None:
                        new_form = MainhaForms.ValidationRuleForm(form_data, instance=validation_rule)
                        new_form.save()
                    else:
                        form.save()

            if request.POST.get('submit') == 'save-end':
                # validation.analyzed_by = request.user
                validation.analyzed = True
                validation.set_analysis_result()
                validation.save()

            return redirect('index')
        else:
            standard_rules = MainhaModels.StandardRule.objects.filter(standard_id=validation.standard.id)

            return render(request, "validation/analysis.html", {
                "standard_rules": standard_rules,
                "project": validation.project,
                "standard": validation.standard,
                "formset": formset
            })
