from abc import ABCMeta, abstractmethod

##気象データ収集タスク基底インターフェース
class MdScrapingTaskService(metaclass=ABCMeta):
    @abstractmethod
    def taskManageRegister(self, task_id):
        pass

    @abstractmethod
    def getUserTaskStatus(self, task_id):
        pass

    @abstractmethod
    def updateUserTaskStatus(self, task_id, user_process_status):
        pass

    @abstractmethod
    def updateFileCreateStatus(self, general_group_key, general_key):
        pass

    @abstractmethod
    def getResultFileNumAndJobNum(self, cur):
        pass

    @abstractmethod
    def scrapingTask(self):
        pass

    @abstractmethod
    def getBatchBreakCount(self):
        pass

    @abstractmethod
    def countJob(self, cur):
        pass

    @abstractmethod
    def disConnect(self):
        pass



