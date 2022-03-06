from abc import ABCMeta, abstractmethod

class FileDownloadService(metaclass=ABCMeta):
    @abstractmethod
    def mainLogic(self):
        pass


