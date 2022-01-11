import traceback
from logging import getLogger

##気象データ収集基底タスク
class MdScrapingTaskExecute():
    def __init__(self, user_id):
        self.process_active_id = '1'
        self.process_rest_id = '0'
        self.general_group_key = 'GR000001'
        self.processing_general_key = '02'
        self.user_id = user_id
        self.logger = getLogger("OnlineBatchLog").getChild("task")
        self.last_user_process_flag = None

    def jobControl(self):
        try:
            md_scraping_service = self.setNewService()
            task_manage_data_flag = self.getTaskManageDataFlag(md_scraping_service)
            if task_manage_data_flag == self.process_rest_id:
                self.logger.debug("==USER_IS_PASSIVE_OK==")
                self.last_user_process_flag = "PASSIVE_OK"
                self.userStatusUpdateActive(md_scraping_service)
                md_scraping_service.updateFileCreateStatus(self.general_group_key, self.processing_general_key)
                md_scraping_service.scrapingTask()
                self.userStatusUpdateRest(md_scraping_service)
            else:
                self.logger.debug("==USER_IS_ACTIVE_NO==")
                self.last_user_process_flag = "ACTIVE_NO"
                pass
            md_scraping_service.disConnect()
        except:
            self.logger.debug("==GET_EXCEPTION==")
            traceback.print_exc()

            if self.last_user_process_flag == "PASSIVE_OK":
                self.userStatusUpdateRest(md_scraping_service)
            elif self.last_user_process_flag == "ACTIVE_NO":
                pass
            else:
                self.userStatusUpdateRest(md_scraping_service)

            md_scraping_service.disConnect()

    def setNewService(self):
        pass

    def getTaskManageDataFlag(self, md_scraping_service):
        pass

    def userStatusUpdateActive(self, md_scraping_service):
        pass

    def userStatusUpdateRest(self, md_scraping_service):
        pass

