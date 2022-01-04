from application.domainLayer.account.account_repository import AccountRepository
from scrapingSystem.repositoryImple.account.account_repository import AccountRepositoryImple

class AccountService():
    def __init__(self):
        self.account_repo: AccountRepository = AccountRepositoryImple()

    ##ユーザーデータオブジェクトの取得
    def getAccountObj(self):
        try:
            return self.account_repo.getAccountObj()
        except:
            raise

    ##ユーザーアカウント作成
    def createAccount(self, validated_data):
        try:
            return self.account_repo.createAccount(validated_data)
        except:
            raise