from application.domainLayer.mdData.userInputItem_repository import UserInputItemGetRepository
from scrapingSystem.models import *

class UserInputItemGetRepositoryImple(UserInputItemGetRepository):
    def getYearManageMTModel(self):
        return YearManageMT

    def getYearManageMTObj(self):
        return YearManageMT.objects.all()

    def getMonthManageMTModel(self):
        return MonthManageMT

    def getMonthManageMTObj(self):
        return MonthManageMT.objects.all()

    def getKenParamMTModel(self):
        return KenParamMT

    def getKenParamMTObj(self):
        return KenParamMT.objects.all()

    def getMDItemMTModel(self):
        return MDItemMT

    def getMDItemMTObj(self):
        return MDItemMT.objects.all()

    def getProcessResultDataModel(self):
        return ProcessResultData

    def getProcessResultDataObj(self, user_id):
        return ProcessResultData.objects.filter(user_id=user_id)
















