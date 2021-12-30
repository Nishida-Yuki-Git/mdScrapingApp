from application.domainLayer.mdData.userInputItem_repository import UserInputItemGetRepository

class UserInputItemGetService():
    def __init__(self, user_input_item_get_repo : UserInputItemGetRepository, user_id='null_user'):
        self.user_input_item_get_repo = user_input_item_get_repo
        self.user_id = user_id

    def getYearManageMTModel(self):
        return self.user_input_item_get_repo.getYearManageMTModel()

    def getYearManageMTObj(self):
        return self.user_input_item_get_repo.getYearManageMTObj()

    def getMonthManageMTModel(self):
        return self.user_input_item_get_repo.getMonthManageMTModel()

    def getMonthManageMTObj(self):
        return self.user_input_item_get_repo.getMonthManageMTObj()

    def getKenParamMTModel(self):
        return self.user_input_item_get_repo.getKenParamMTModel()

    def getKenParamMTObj(self):
        return self.user_input_item_get_repo.getKenParamMTObj()

    def getMDItemMTModel(self):
        return self.user_input_item_get_repo.getMDItemMTModel()

    def getMDItemMTObj(self):
        return self.user_input_item_get_repo.getMDItemMTObj()

    def getProcessResultDataModel(self):
        return self.user_input_item_get_repo.getProcessResultDataModel()

    def getProcessResultDataObj(self):
        return self.user_input_item_get_repo.getProcessResultDataObj(self.user_id)






