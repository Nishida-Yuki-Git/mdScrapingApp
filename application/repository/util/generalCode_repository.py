from abc import ABCMeta, abstractmethod

class generalCodeRepository(metaclass=ABCMeta):
    @abstractmethod
    def getGeneralCode(self, general_group_key, general_key):
        pass



