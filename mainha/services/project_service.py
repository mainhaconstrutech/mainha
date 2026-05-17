from django.contrib.auth.models import User

from mainha import models as MainhaModels


class ProjectService:
    @staticmethod
    def set_project_context(user: User, project: MainhaModels.Project):
        """
        Set project some data as account, creator and user with access (if necessary).

        Args:
            user (User): Current user.
            project (MainhaModels.Project): Project.
        Returns:
            MainhaModels.Project: Project updated.
        """
        user_account = MainhaModels.UserAccount.objects.filter(user=user).first()

        project.account = user_account.account
        project.created_by = user_account.user
        project.save()

        if user_account.role in ['manager', 'employee']:
            MainhaModels.UserProject.objects.create(user=user_account.user, project=project)

        return project

    @staticmethod
    def list_user_project_in_project(project: MainhaModels.Project):
        """
        Return list of user_project in a project.

        Args:
            project (MainhaModels.Project): Project.
        Returns:
            List: List of UserProject in project.
        """
        return MainhaModels.UserProject.objects.filter(project=project)

    @staticmethod
    def list_users_in_projec(project: MainhaModels.Project):
        """
        Return list of users in a account.

        Args:
            account (MainhaModels.Account): Account.
        Returns:
            List: List of User in account.
        """
        project_user_ids_in_project = ProjectService.list_user_project_in_project(
            project
        ).values_list('user__id', flat=True)

        return User.objects.filter(id__in=project_user_ids_in_project)
