from abc import ABCMeta, abstractmethod

class AccountService(metaclass=ABCMeta):
    ##ユーザーデータオブジェクトの取得
    @abstractmethod
    def getAccountObj(self):
        pass

    ##ユーザーアカウント作成
    @abstractmethod
    def createAccount(self, validated_data):
        pass