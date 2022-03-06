from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingTaskServiceImpl import MdScrapingTaskServiceImpl
from mainJobBatch.taskManage.dao.errorFileCreateDao import ErrorFileCreateDao
from mainJobBatch.taskManage.dao.daoImple.errorFileCreateDaoImple import ErrorFileCreateDaoImple

##エラーファイル再作成サービスクラス
class ErrorFileCreateTaskServiceImpl(MdScrapingTaskServiceImpl):
    def __init__(self, user_id, result_file_num):
        super().__init__(user_id)
        self.result_file_num = result_file_num
        self.batch_break_count = 1
        self.error_file_create_dao: ErrorFileCreateDao = ErrorFileCreateDaoImple()

    def getResultFileNumAndJobNum(self, cur):
        super().getResultFileNumAndJobNum(cur)
        try:
            job_num = self.error_file_create_dao.getJobNum(cur, self.result_file_num)

            process_param = {
                "job_num": job_num,
                "result_file_num": self.result_file_num,
            }
            return process_param
        except:
            raise

    def getBatchBreakCount(self):
        super().getBatchBreakCount()
        return self.batch_break_count

    def countJob(self, cur):
        super().countJob(cur)
        try:
            return True
        except:
            raise

