from rest_framework import serializers
from application.service.account.accountService import AccountService
from application.service.account.impl.accountServiceImpl import AccountServiceImpl

class AccountSerializer(serializers.ModelSerializer):
    """ ユーザーアカウント用セリアライズクラス
    """

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        """ ユーザーアカウント用メタクラス
        """

        service: AccountService = AccountServiceImpl()
        model = service.getAccountObj()
        fields = ('userid', 'username', 'email', 'profile', 'password')

    def create(self, validated_data):
        """
        ユーザーアカウント作成

        Parameters
        ----------
        validated_data : dict
            バリデーション済みアカウントデータ

        Returns
        ----------
        User
            アカウントテーブルオブジェクト
        """

        try:
            service: AccountService = AccountServiceImpl()
            return service.createAccount(validated_data)
        except:
            raise








