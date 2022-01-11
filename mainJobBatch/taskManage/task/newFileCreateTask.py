from mainJobBatch.taskManage.task.base.mdScrapingTask import MdScrapingTaskExecute
from mainJobBatch.taskManage.service.newFileCreateTaskService import NewFileCreateTaskService

##新規ファイル作成タスク
class NewFileCreateTaskExecute(MdScrapingTaskExecute):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.new_create_task_id = '0001'

    def setNewService(self):
        super().setNewService()
        return NewFileCreateTaskService(self.user_id)

    def getTaskManageDataFlag(self, md_scraping_service):
        super().getTaskManageDataFlag(md_scraping_service)
        try:
            md_scraping_service.taskManageRegister(self.new_create_task_id)
            task_manage_data_flag = md_scraping_service.getUserTaskStatus(self.new_create_task_id)
            return task_manage_data_flag
        except:
            raise

    def userStatusUpdateActive(self, md_scraping_service):
        super().userStatusUpdateActive(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.new_create_task_id, self.process_active_id)
        except:
            raise

    def userStatusUpdateRest(self, md_scraping_service):
        super().userStatusUpdateRest(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.new_create_task_id, self.process_rest_id)
        except:
            raise