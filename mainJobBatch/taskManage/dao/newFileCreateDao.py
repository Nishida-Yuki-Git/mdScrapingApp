from abc import ABCMeta, abstractmethod

class NewFileCreateDao(metaclass=ABCMeta):
    @abstractmethod
    def jadgeJobNumStock(self, cur, user_id):
        pass

    @abstractmethod
    def getJobQueData(self, cur, user_id):
        pass









