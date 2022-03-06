from abc import ABCMeta, abstractmethod

class saibanRepository(metaclass=ABCMeta):
    @abstractmethod
    def getSaibanCode(self, saibanKey):
        pass



