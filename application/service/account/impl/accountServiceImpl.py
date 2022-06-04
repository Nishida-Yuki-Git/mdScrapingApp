from application.repository.account.account_repository import AccountRepository
from scrapingSystem.repositoryImple.account.account_repository import AccountRepositoryImple
from application.service.account.accountService import AccountService

class AccountServiceImpl(AccountService):
    """
    ユーザーデータオブジェクトの取得サービス実装クラス

    Attributes
    ----------
    account_repo : AccountRepository
        ユーザーデータ取得レポジトリインターフェース
    """

    def __init__(self):
        self.account_repo: AccountRepository = AccountRepositoryImple()

    def getAccountObj(self):
        """
        ユーザーデータ取得

        Returns
        ----------
        Account
            アカウントテーブルオブジェクト
        """

        try:
            return self.account_repo.getAccountObj()
        except:
            raise

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

        try:
            return self.account_repo.createAccount(validated_data)
        except:
            raise