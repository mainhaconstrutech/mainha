from django.contrib.auth.models import User

from mainha import models as MainhaModels


class AccountService:
    @staticmethod
    def toggle_account_active(account: MainhaModels.Account):
        """
        Toogle account active.

        Args:
            account (MainhaModels.Account): Account.
        Returns:
            MainhaModels.Account: Account updated.
        """
        account.active = not (account.active)
        account.save()

        return account

    @staticmethod
    def list_user_account_in_account(account: MainhaModels.Account):
        """
        Return list of user_account in a account.

        Args:
            account (MainhaModels.Account): Account.
        Returns:
            List: List of UserAccount in account.
        """
        return MainhaModels.UserAccount.objects.filter(account=account)

    @staticmethod
    def list_users_in_account(account: MainhaModels.Account):
        """
        Return list of users in a account.

        Args:
            account (MainhaModels.Account): Account.
        Returns:
            List: List of User in account.
        """
        account_user_ids_in_account = AccountService.list_user_account_in_account(
            account
        ).values_list('user__id', flat=True)

        return User.objects.filter(id__in=account_user_ids_in_account)
