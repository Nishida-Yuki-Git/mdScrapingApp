from mainJobBatch.taskManage.task.base.mdScrapingTask import MdScrapingTaskExecute
from mainJobBatch.taskManage.service.errorFileCreateTaskService import ErrorFileCreateTaskService

##エラーファイル再作成タスク
class ErrorFileCreateTaskExecute(MdScrapingTaskExecute):
    def __init__(self, user_id, result_file_num):
        super().__init__(user_id)
        self.result_file_num = result_file_num
        self.error_create_task_id = '0002'

    def setNewService(self):
        super().setNewService()
        return ErrorFileCreateTaskService(self.user_id, self.result_file_num)

    def getTaskManageDataFlag(self, md_scraping_service):
        super().getTaskManageDataFlag(md_scraping_service)
        try:
            md_scraping_service.taskManageRegister(self.error_create_task_id)
            task_manage_data_flag = md_scraping_service.getUserTaskStatus(self.error_create_task_id)
            return task_manage_data_flag
        except:
            raise

    def userStatusUpdateActive(self, md_scraping_service):
        super().userStatusUpdateActive(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.error_create_task_id, self.process_active_id)
        except:
            raise

    def userStatusUpdateRest(self, md_scraping_service):
        super().userStatusUpdateRest(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.error_create_task_id, self.process_rest_id)
        except:
            raise
