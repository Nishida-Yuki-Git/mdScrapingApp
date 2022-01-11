from abc import ABCMeta, abstractmethod

class MdScrapingDao(metaclass=ABCMeta):
    @abstractmethod
    def getConnection(self):
        pass

    @abstractmethod
    def taskManageRegist(self, cur, task_id, user_id):
        pass

    @abstractmethod
    def getUserProcessFlag(self, cur, task_id, user_id):
        pass

    @abstractmethod
    def updateUserProcessFlag(self, cur, task_id, user_id, user_process_status):
        pass

    @abstractmethod
    def getJobParamData(self, cur, job_num):
        pass

    @abstractmethod
    def getKenUrlParam(self, cur, ken_list):
        pass

    @abstractmethod
    def getJMAgencyURL(self, cur):
        pass

    @abstractmethod
    def updateFileCreateStatus(self, cur, result_file_num, general_group_key, general_key):
        pass

    @abstractmethod
    def deleteUserJobData(self, cur, job_num):
        pass

    @abstractmethod
    def registFilePath(self, cur, result_file_num, save_path):
        pass









