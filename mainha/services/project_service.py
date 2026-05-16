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
