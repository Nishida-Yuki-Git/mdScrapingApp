from rest_framework import serializers
from application.service.account.accountService import AccountService
from application.service.account.impl.accountServiceImpl import AccountServiceImpl

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        service: AccountService = AccountServiceImpl()
        model = service.getAccountObj()
        fields = ('userid', 'username', 'email', 'profile', 'password')

    def create(self, validated_data):
        try:
            service: AccountService = AccountServiceImpl()
            return service.createAccount(validated_data)
        except:
            raise








