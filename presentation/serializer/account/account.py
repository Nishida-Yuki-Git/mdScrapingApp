from rest_framework import serializers
from application.system_application.account.accountService import AccountService

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        service = AccountService()
        model = service.getAccountObj()
        fields = ('userid', 'username', 'email', 'profile', 'password')

    def create(self, validated_data):
        service = AccountService()
        return service.createAccount(validated_data)








