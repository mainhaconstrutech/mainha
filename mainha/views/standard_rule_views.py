from django.urls import reverse_lazy, reverse

from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mainha import forms as MainhaForms
from mainha import models as MainhaModels

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