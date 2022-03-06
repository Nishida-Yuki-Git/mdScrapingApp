from rest_framework import serializers
from application.service.mdData.userInputItemService import UserInputItemGetService
from application.service.mdData.Impl.userInputItemServiceImpl import UserInputItemGetServiceImpl

class YearManageMTSerializer(serializers.ModelSerializer):
    class Meta:
        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getYearManageMTModel()
        fields = ('year_param',)

class MonthManageMTSerializer(serializers.ModelSerializer):
    class Meta:
        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getMonthManageMTModel()
        fields = ('month_param',)

class KenParamMTSerializer(serializers.ModelSerializer):
    class Meta:
        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getKenParamMTModel()
        fields = ('ken_name',)

class MDItemMTSerializer(serializers.ModelSerializer):
    class Meta:
        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getMDItemMTModel()
        fields = ('md_item',)

class ProcessResultDataSerializer(serializers.ModelSerializer):
    class Meta:
        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getProcessResultDataModel()
        fields = ('result_file_num','user_id','file_create_status','create_date_time',)

class UserInputItemCommunicater():
    def __init__(self, user_id):
        self.user_id = user_id

    def getYearManageMTObj(self):
        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getYearManageMTObj()
        except:
            raise

    def getMonthManageMTObj(self):
        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getMonthManageMTObj()
        except:
            raise

    def getKenParamMTObj(self):
        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getKenParamMTObj()
        except:
            raise

    def getMDItemMTObj(self):
        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getMDItemMTObj()
        except:
            raise

    def getProcessResultDataObj(self):
        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl(self.user_id)
            return service.getProcessResultDataObj()
        except:
            raise

    def getFileManageDataObj(self):
        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl(self.user_id)
            return service.getFileManageDataObj()
        except:
            raise




