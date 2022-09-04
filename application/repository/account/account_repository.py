from abc import ABCMeta, abstractmethod

class AccountRepository(metaclass=ABCMeta):
    """ ユーザーデータ取得レポジトリインターフェース
    """

    @abstractmethod
    def getAccountObj(self):
        """
        ユーザーデータ取得

        Returns
        ----------
        Account
            アカウントテーブルオブジェクト
        """

        pass

    @abstractmethod
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

        pass