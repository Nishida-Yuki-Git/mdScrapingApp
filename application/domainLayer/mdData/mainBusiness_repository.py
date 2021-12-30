from abc import ABCMeta, abstractmethod

class MainBusinessRepository(metaclass=ABCMeta):
    @abstractmethod
    def jobQueRegister(self, saiban_job_num, user_id, result_file_num):
        pass

    @abstractmethod
    def jobParamRegister(self, saiban_job_num, serviceDto):
        pass

    @abstractmethod
    def userProcessResultRegister(self, result_file_num, first_status_code, serviceDto):
        pass

    @abstractmethod
    def fileManageDataRegister(self, result_file_num, serviceDto):
        pass
