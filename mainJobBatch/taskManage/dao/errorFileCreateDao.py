from abc import ABCMeta, abstractmethod

class ErrorFileCreateDao(metaclass=ABCMeta):
    @abstractmethod
    def getJobNum(self, cur, result_file_num):
        pass

    @abstractmethod
    def jadgeQueStock(self, cur, result_file_num):
        pass







