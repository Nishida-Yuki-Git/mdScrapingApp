from application.domainLayer.account.account_repository import AccountRepository

class AccountService():
    def __init__(self, account_repo : AccountRepository): ##ここに実際はインプルを入れる
        self.account_repo = account_repo

    ##ユーザーデータオブジェクトの取得
    def getAccountObj(self):
        return self.account_repo.getAccountObj()

    ##ユーザーアカウント作成
    def createAccount(self, validated_data):
        return self.account_repo.createAccount(validated_data)