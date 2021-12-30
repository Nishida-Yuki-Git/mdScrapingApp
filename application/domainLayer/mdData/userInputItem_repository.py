from abc import ABCMeta, abstractmethod

class UserInputItemGetRepository(metaclass=ABCMeta):
    @abstractmethod
    def getYearManageMTModel(self):
        pass

    @abstractmethod
    def getYearManageMTObj(self):
        pass

    @abstractmethod
    def getMonthManageMTModel(self):
        pass

    @abstractmethod
    def getMonthManageMTObj(self):
        pass

    @abstractmethod
    def getKenParamMTModel(self):
        pass

    @abstractmethod
    def getKenParamMTObj(self):
        pass

    @abstractmethod
    def getMDItemMTModel(self):
        pass

    @abstractmethod
    def getMDItemMTObj(self):
        pass

    @abstractmethod
    def getProcessResultDataModel(self):
        pass

    @abstractmethod
    def getProcessResultDataObj(self, user_id):
        pass



