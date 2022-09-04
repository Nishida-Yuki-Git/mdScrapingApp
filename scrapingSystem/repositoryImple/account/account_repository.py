from application.repository.account.account_repository import AccountRepository
from scrapingSystem.models import Account, AccountManager

class AccountRepositoryImple(AccountRepository):
    """ ユーザーデータ取得レポジトリ実装クラス
    """

    def getAccountObj(self):
        """
        ユーザーデータ取得

        Returns
        ----------
        Account
            アカウントテーブルオブジェクト
        """

        return Account

    def createAccount(self, validated_data):
        """
        ユーザーアカウント作成

        Parameters
        ----------
        validated_data : dict
            バリデーション済みユーザーデータ

        Returns
        ----------
        User
            アカウントテーブルオブジェクト
        """

        return Account.objects.create_user(request_data=validated_data)