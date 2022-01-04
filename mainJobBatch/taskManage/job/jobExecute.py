from mainJobBatch.taskManage.task.mdScrapingTask import MdScrapingTaskExecute
from application.system_application.enum.exeBatchType import ExeBatchType

class JobExecuter():
    def __init__(self, batch_exe_param_json, exe_batch_type):
        self.batch_exe_param_json = batch_exe_param_json
        self.exe_batch_type = exe_batch_type

    def jobExecute(self):
        if self.exe_batch_type == ExeBatchType.NEW_FILE_CREATE_BATCH:
            md_scraping_job_batch = MdScrapingTaskExecute(self.batch_exe_param_json['user_id'])
            md_scraping_job_batch.jobControl()
        elif self.exe_batch_type == ExeBatchType.ERROR_FILE_CREATE_BATCH:
            pass
        else:
            print('起動バッチがありませんでした')
            pass

def goBatch(batch_exe_param_json, exe_batch_type):
    executer = JobExecuter(batch_exe_param_json, exe_batch_type)
    executer.jobExecute()

