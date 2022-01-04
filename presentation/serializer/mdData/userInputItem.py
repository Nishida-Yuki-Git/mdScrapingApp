from rest_framework import serializers
from application.system_application.mdData.userInputItemService import UserInputItemGetService
from application.domainLayer.mdData.userInputItem_repository import UserInputItemGetRepository
from scrapingSystem.repositoryImple.mdData.userInputItem_repository import UserInputItemGetRepositoryImple

class YearManageMTSerializer(serializers.ModelSerializer):
    class Meta:
        repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
        service = UserInputItemGetService(repository)
        model = service.getYearManageMTModel()
        fields = ('year_param',)

class MonthManageMTSerializer(serializers.ModelSerializer):
    class Meta:
        repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
        service = UserInputItemGetService(repository)
        model = service.getMonthManageMTModel()
        fields = ('month_param',)

class KenParamMTSerializer(serializers.ModelSerializer):
    class Meta:
        repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
        service = UserInputItemGetService(repository)
        model = service.getKenParamMTModel()
        fields = ('ken_name',)

class MDItemMTSerializer(serializers.ModelSerializer):
    class Meta:
        repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
        service = UserInputItemGetService(repository)
        model = service.getMDItemMTModel()
        fields = ('md_item',)

class ProcessResultDataSerializer(serializers.ModelSerializer):
    class Meta:
        repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
        service = UserInputItemGetService(repository)
        model = service.getProcessResultDataModel()
        fields = ('result_file_num','user_id','file_create_status','create_date_time',)

class UserInputItemCommunicater():
    def __init__(self, user_id):
        self.user_id = user_id

    def getYearManageMTObj(self):
        try:
            repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
            service = UserInputItemGetService(repository)
            return service.getYearManageMTObj()
        except:
            raise

    def getMonthManageMTObj(self):
        try:
            repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
            service = UserInputItemGetService(repository)
            return service.getMonthManageMTObj()
        except:
            raise

    def getKenParamMTObj(self):
        try:
            repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
            service = UserInputItemGetService(repository)
            return service.getKenParamMTObj()
        except:
            raise

    def getMDItemMTObj(self):
        try:
            repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
            service = UserInputItemGetService(repository)
            return service.getMDItemMTObj()
        except:
            raise

    def getProcessResultDataObj(self):
        try:
            repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
            service = UserInputItemGetService(repository, self.user_id)
            return service.getProcessResultDataObj()
        except:
            raise

    def getFileManageDataObj(self):
        try:
            repository: UserInputItemGetRepository = UserInputItemGetRepositoryImple()
            service = UserInputItemGetService(repository, self.user_id)
            return service.getFileManageDataObj()
        except:
            raise




