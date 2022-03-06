from mainJobBatch.taskManage.dao.mdScrapingDao import MdScrapingDao
from mainJobBatch.taskManage.dao.daoImple.mdScrapingDaoImple import MdScrapingDaoImple
from logging import getLogger
import traceback
from mainJobBatch.taskManage.serviceBase.mdScrapingLogicService import MeteorologicaldataScrapingService
from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingLogicServiceImpl import MeteorologicaldataScrapingServiceImpl
from mainJobBatch.taskManage.serviceBase.mdScrapingTaskService import MdScrapingTaskService

##気象データ収集タスク基底クラス
class MdScrapingTaskServiceImpl(MdScrapingTaskService):
    def __init__(self, user_id):
        self.user_id = user_id
        self.md_scraping_dao: MdScrapingDao = MdScrapingDaoImple()
        self.conn = self.md_scraping_dao.getConnection()
        self.general_group_key = 'GR000001'
        self.end_general_key = '03'
        self.error_general_key = '04'
        self.logger = getLogger("OnlineBatchLog").getChild("taskService")

    def taskManageRegister(self, task_id):
        self.conn.autocommit = False
        try:
            self.conn.ping(reconnect=True)
            cur = self.conn.cursor()

            self.md_scraping_dao.taskManageRegist(cur, task_id, self.user_id)

            self.conn.commit()
            cur.close()
        except:
            self.conn.rollback()
            cur.close()
            raise

    def getUserTaskStatus(self, task_id):
        try:
            self.conn.ping(reconnect=True)
            cur = self.conn.cursor()

            user_status = self.md_scraping_dao.getUserProcessFlag(cur, task_id, self.user_id)

            cur.close()
            return user_status
        except:
            cur.close()
            raise

    def updateUserTaskStatus(self, task_id, user_process_status):
        self.conn.autocommit = False
        try:
            self.conn.ping(reconnect=True)
            cur = self.conn.cursor()

            self.md_scraping_dao.updateUserProcessFlag(cur, task_id, self.user_id, user_process_status)

            self.conn.commit()
            cur.close()
        except:
            self.conn.rollback()
            cur.close()
            raise

    def updateFileCreateStatus(self, general_group_key, general_key):
        self.conn.autocommit = False
        try:
            self.conn.ping(reconnect=True)
            cur = self.conn.cursor()

            process_param = self.getResultFileNumAndJobNum(cur)
            result_file_num = process_param['result_file_num']
            self.md_scraping_dao.updateFileCreateStatus(cur, result_file_num, general_group_key, general_key)

            self.conn.commit()
            cur.close()
        except:
            self.conn.rollback()
            cur.close()
            raise

    def getResultFileNumAndJobNum(self, cur):
        pass

    def scrapingTask(self):
        self.logger.debug("==GO_MAIN_SCRAPING==")
        self.conn.ping(reconnect=True)
        cur = self.conn.cursor()
        job_non_count = 0

        while True:
            if job_non_count == self.getBatchBreakCount():
                break

            try:
                if self.countJob(cur):
                    job_non_count += 1
                    continue
            except:
                raise

            try:
                self.conn.autocommit = False

                process_param = self.getResultFileNumAndJobNum(cur)
                job_num = process_param['job_num']
                result_file_num = process_param['result_file_num']

                job_param_select_result = self.md_scraping_dao.getJobParamData(cur, job_num)
                job_start_year = job_param_select_result['job_start_year']
                job_end_year = job_param_select_result['job_end_year']
                job_start_month = job_param_select_result['job_start_month']
                job_end_month = job_param_select_result['job_end_month']
                job_ken_list = job_param_select_result['job_ken_list']
                job_md_item_list = job_param_select_result['job_md_item_list']
                job_ken_list = [s for s in job_ken_list if s != '']
                job_md_item_list = [s for s in job_md_item_list if s != '']

                result_ken_param_list = self.md_scraping_dao.getKenUrlParam(cur, job_ken_list)
                ken_no_list = result_ken_param_list['ken_no_list']
                ken_block_list = result_ken_param_list['ken_block_list']

                md_url_list = self.md_scraping_dao.getJMAgencyURL(cur)

                md_scraping_logic_service: MeteorologicaldataScrapingService = MeteorologicaldataScrapingServiceImpl(
                    cur,
                    result_file_num,
                    self.md_scraping_dao,
                    int(job_start_year),
                    int(job_end_year),
                    int(job_start_month),
                    int(job_end_month),
                    job_ken_list,
                    ken_no_list,
                    ken_block_list,
                    md_url_list,
                    job_md_item_list)
                while True:
                    endSign = md_scraping_logic_service.mainSoup()
                    if endSign == '終了':
                        break
                md_scraping_logic_service.MDOutput()

                self.updateFileCreateStatus(self.general_group_key, self.end_general_key)
                self.md_scraping_dao.deleteUserJobData(cur, job_num)

                self.conn.commit()
            except:
                self.logger.debug("==GET_EXCEPTION==")
                traceback.print_exc()
                self.conn.rollback()
                self.updateFileCreateStatus(self.general_group_key, self.error_general_key)
                continue

        cur.close()

    def getBatchBreakCount(self):
        pass

    def countJob(self, cur):
        pass

    def disConnect(self):
        self.logger.debug("==SQL_CONN_END==")
        self.conn.close()



