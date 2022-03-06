from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingTaskServiceImpl import MdScrapingTaskServiceImpl
from mainJobBatch.taskManage.dao.newFileCreateDao import NewFileCreateDao
from mainJobBatch.taskManage.dao.daoImple.newFileCreateDaoImple import NewFileCreateDaoImple

##新規作成サービスクラス
class NewFileCreateTaskServiceImpl(MdScrapingTaskServiceImpl):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.batch_break_count = 10
        self.new_file_create_dao: NewFileCreateDao = NewFileCreateDaoImple()

    def getResultFileNumAndJobNum(self, cur):
        super().getResultFileNumAndJobNum(cur)
        try:
            select_job_que_data_result = self.new_file_create_dao.getJobQueData(cur, self.user_id)
            job_num = select_job_que_data_result['job_num_list'][0]
            result_file_num = select_job_que_data_result['result_file_num_list'][0]
            process_param = {
                "job_num": job_num,
                "result_file_num": result_file_num,
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
            return self.new_file_create_dao.jadgeJobNumStock(cur, self.user_id)
        except:
            raise

