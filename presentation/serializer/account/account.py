from rest_framework import serializers
from application.system_application.account.accountService import AccountService
from scrapingSystem.repositoryImple.account.account_repository import AccountRepositoryImple
from application.domainLayer.account.account_repository import AccountRepository

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        repository: AccountRepository = AccountRepositoryImple()
        service = AccountService(repository)
        model = service.getAccountObj()
        fields = ('userid', 'username', 'email', 'profile', 'password')

    def create(self, validated_data):
        repository: AccountRepository = AccountRepositoryImple()
        service = AccountService(repository)
        return service.createAccount(validated_data)








