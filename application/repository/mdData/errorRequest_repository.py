from abc import ABCMeta, abstractmethod

class ErrorRequestRepository(metaclass=ABCMeta):
    @abstractmethod
    def getErrorUserId(self, result_file_num):
        pass
