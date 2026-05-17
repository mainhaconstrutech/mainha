from django.contrib.auth.models import User

from mainha import models as MainhaModels


class Scopes:
    @staticmethod
    def list_accounts(user: User):
        """
        Load account list which current user has access.

        Args:
            user (User): Current user.
        Returns:
            List: List of accounts which user has access allowed.
        """
        if user.is_staff:
            return MainhaModels.Account.objects.all()
        else:
            user_account = MainhaModels.UserAccount.objects.filter(user=user).first()
            return MainhaModels.Account.objects.filter(id=user_account.account.id).all()

    @staticmethod
    def list_projects(user: User):
        """
        Load project list which current user has access.

        Args:
            user (User): Current user.
        Returns:
            List: List of projects which user has access allowed.
        """
        if user.is_staff:
            return MainhaModels.Project.objects.all()
        else:
            user_account = MainhaModels.UserAccount.objects.filter(user=user).first()

            if user_account.role == 'director':
                return MainhaModels.Project.objects.filter(account=user_account.account).all()
            else:
                user_included_project_ids = MainhaModels.UserProject.objects.filter(user=user).values('project_id')
                return MainhaModels.Project.objects.filter(id__in=user_included_project_ids).all()

    @staticmethod
    def has_director_permission(user: User):
        """
        Check if current user has director permission allowed.

        Args:
            user (User): Current user.
        Returns:
            Boolean: User has permission.
        """
        return Scopes.has_permission(user, 'director')

    @staticmethod
    def has_manager_permission(user: User):
        """
        Check if current user has manager permission allowed.

        Args:
            user (User): Current user.
        Returns:
            Boolean: User has permission.
        """
        return Scopes.has_permission(user, 'manager')

    @staticmethod
    def has_employee_permission(user: User):
        """
        Check if current user has employee permission allowed.

        Args:
            user (User): Current user.
        Returns:
            Boolean: User has permission.
        """
        return Scopes.has_permission(user, 'employee')

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
        if user.is_staff:
            return True

        user_account = MainhaModels.UserAccount.objects.filter(user=user).first()

        for current_role in MainhaModels.UserAccount.ROLE_HIERARCHY:
            if user_account.role == min_account_permission:
                return True
            if current_role == min_account_permission:
                return False

        return False
