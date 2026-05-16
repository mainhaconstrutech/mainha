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
