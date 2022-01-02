from mainJobBatch.taskManage.service.mdScrapingTaskService import MdScrapingTaskService
import traceback
import logging

##気象データ収集タスク(オンラインバッチ)
class MdScrapingTaskExecute():
    def __init__(self, user_id):
        self.task_id = '0001' ##気象データ収集バッチタスクID
        self.process_active_id = '1' ##プロセスフラグ：稼働中
        self.process_rest_id = '0' ##プロセスフラグ：待機中
        self.general_group_key = 'GR000001'
        self.processing_general_key = '02'
        self.user_id = user_id

    def jobControl(self):
        try:
            md_scraping_service = MdScrapingTaskService(self.user_id)
            md_scraping_service.taskManageRegister(self.task_id)
            task_manage_data_flag = md_scraping_service.getUserTaskStatus(self.task_id)
            if task_manage_data_flag == self.process_rest_id:
                logging.debug("===CURENT_USER_" + self.user_id + "_RESTED===")
                md_scraping_service.updateUserTaskStatus(self.task_id, self.process_active_id)
                md_scraping_service.updateFileCreateStatus(self.general_group_key, self.processing_general_key)
                md_scraping_service.scrapingTask()
                md_scraping_service.updateUserTaskStatus(self.task_id, self.process_rest_id)
            else:
                logging.debug("===CURENT_USER_" + self.user_id + "_IS_PROCESSING===")
            md_scraping_service.disConnect()
        except:
            traceback.print_exc()
            md_scraping_service.updateUserTaskStatus(self.task_id, self.process_rest_id)
