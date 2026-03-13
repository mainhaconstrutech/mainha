from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin

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