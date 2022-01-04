from abc import ABCMeta, abstractmethod

class FileDownloadRepository(metaclass=ABCMeta):
    @abstractmethod
    def getUserFileObject(self, result_file_num):
        pass
