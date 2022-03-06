from abc import ABCMeta, abstractmethod

class ErrorRequestService(metaclass=ABCMeta):
    @abstractmethod
    def mainLogic(self):
        pass






