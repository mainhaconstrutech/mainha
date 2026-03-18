from django.urls import reverse_lazy
from django.forms import formset_factory
from django.shortcuts import render, redirect

from django.views.generic.base import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from django.views.generic.edit import CreateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels


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


class ValidationReportOfProjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = "validation/report_of_project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = MainhaModels.Project.objects.get(id=self.kwargs["pk"])
        validation = MainhaModels.Validation.objects.filter(project_id=project.id).order_by("id").first()
        validation_rules = MainhaModels.ValidationRule.objects.filter(validation_id=validation.id) if validation else []

        context["project"] = project
        context["validation"] = validation
        context["validation_rule_list"] = validation_rules

        return context
