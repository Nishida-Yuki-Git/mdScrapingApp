from application.domainLayer.mdData.userInputItem_repository import UserInputItemGetRepository

class UserInputItemGetService():
    def __init__(self, user_input_item_get_repo : UserInputItemGetRepository, user_id='null_user'):
        self.user_input_item_get_repo = user_input_item_get_repo
        self.user_id = user_id

    def getYearManageMTModel(self):
        try:
            return self.user_input_item_get_repo.getYearManageMTModel()
        except:
            raise

    def getYearManageMTObj(self):
        try:
            return self.user_input_item_get_repo.getYearManageMTObj()
        except:
            raise

    def getMonthManageMTModel(self):
        try:
            return self.user_input_item_get_repo.getMonthManageMTModel()
        except:
            raise

    def getMonthManageMTObj(self):
        try:
            return self.user_input_item_get_repo.getMonthManageMTObj()
        except:
            raise

    def getKenParamMTModel(self):
        try:
            return self.user_input_item_get_repo.getKenParamMTModel()
        except:
            raise

    def getKenParamMTObj(self):
        try:
            return self.user_input_item_get_repo.getKenParamMTObj()
        except:
            raise

    def getMDItemMTModel(self):
        try:
            return self.user_input_item_get_repo.getMDItemMTModel()
        except:
            raise

    def getMDItemMTObj(self):
        try:
            return self.user_input_item_get_repo.getMDItemMTObj()
        except:
            raise

    def getProcessResultDataModel(self):
        try:
            return self.user_input_item_get_repo.getProcessResultDataModel()
        except:
            raise

    def getProcessResultDataObj(self):
        try:
            return self.user_input_item_get_repo.getProcessResultDataObj(self.user_id)
        except:
            raise






