from django.contrib.auth.models import User

from mainha import models as MainhaModels


class ScopeService:
    @staticmethod
    def list_projects(user: User):
        """
        Load project list which current user has access.

        Args:
            user (User): Current user.
        Returns:
            List: List of projects which user has access permitted.
        """
        if user.is_superuser or user.is_staff:
            return MainhaModels.Project.objects.all()
        else:
            user_account = MainhaModels.UserAccount.objects.filter(user=user).first()

            if user_account.role == 'director':
                return MainhaModels.Project.objects.filter(account=user_account.account).all()
            else:
                user_included_project_ids = MainhaModels.UserProject.objects.filter(user=user).values("project_id")
                return MainhaModels.Project.objects.filter(id__in=user_included_project_ids).all()

    @staticmethod
    def has_permission(user: User, min_account_permission: str):
        """
        Check if current user has minimum permission allowed.

        Args:
            user (User): Current user.
            min_account_permission (string): Minimum account permission allowed.
        Returns:
            Boolean: User has permission.
        """
        if user.is_superuser or user.is_staff:
            return True

        user_account = MainhaModels.UserAccount.objects.filter(user=user).first()
        has_account_permission = False

        for current_role in MainhaModels.UserAccount.ROLE_HIERARCHY:
            if user_account.role == min_account_permission:
                has_account_permission == True
                break
            if current_role == min_account_permission:
                break
        
        return has_account_permission
