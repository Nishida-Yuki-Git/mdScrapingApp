from application.domainLayer.account.account_repository import AccountRepository
from scrapingSystem.models import Account, AccountManager

class AccountRepositoryImple(AccountRepository):
    ##ユーザーデータオブジェクトの取得
    def getAccountObj(self):
        return Account

    ##ユーザーアカウント作成
    def createAccount(self, validated_data):
        return Account.objects.create_user(request_data=validated_data)