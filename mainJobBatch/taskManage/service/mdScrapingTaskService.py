import traceback
import logging
from mainJobBatch.taskManage.dao.mdScrapingDao import MdScrapingDao
from mainJobBatch.taskManage.dao.daoImple.mdScrapingDaoImple import MdScrapingDaoImple
from mainJobBatch.taskManage.service.mdScrapingLogicService import MeteorologicaldataScraping

##気象データ収集タスク(ユーザートリガー)
class MdScrapingTaskService():
    def __init__(self, user_id):
        self.user_id = user_id
        self.logger = logging.getLogger("md_scraping_task")
        self.md_scraping_dao: MdScrapingDao = MdScrapingDaoImple()
        self.conn = self.md_scraping_dao.getConnection()
        self.batch_break_count = 10 ##バッチの処理を止めるカウント
        self.general_group_key = 'GR000001'
        self.end_general_key = '03'
        self.error_general_key = '04'

    def taskManageRegister(self, task_id):
        logging.basicConfig(level=logging.DEBUG)
        self.conn.autocommit = False
        try:
            logging.debug("===TASK_MANAGE_REGISTER_SETUP===")
            self.conn.ping(reconnect=True)
            logging.debug(self.conn.is_connected())
            cur = self.conn.cursor()

            self.md_scraping_dao.taskManageRegist(cur, task_id, self.user_id)

            self.conn.commit()
            cur.close()
        except:
            self.conn.rollback()
            cur.close()
            raise

    def getUserTaskStatus(self, task_id):
        logging.basicConfig(level=logging.DEBUG)
        try:
            logging.debug("===GET_USER_TASK_STATUS_SETUP===")
            self.conn.ping(reconnect=True)
            logging.debug(self.conn.is_connected())
            cur = self.conn.cursor()

            user_status = self.md_scraping_dao.getUserProcessFlag(cur, task_id, self.user_id)

            cur.close()
            return user_status
        except:
            cur.close()
            raise

    def updateUserTaskStatus(self, task_id, user_process_status):
        logging.basicConfig(level=logging.DEBUG)
        self.conn.autocommit = False
        try:
            logging.debug("===USER_PROCESS_UPDATE===")
            self.conn.ping(reconnect=True)
            logging.debug(self.conn.is_connected())
            cur = self.conn.cursor()

            self.md_scraping_dao.updateUserProcessFlag(cur, task_id, self.user_id, user_process_status)

            self.conn.commit()
            cur.close()
        except:
            self.conn.rollback()
            cur.close()
            raise

    def updateFileCreateStatus(self, general_group_key, general_key):
        logging.basicConfig(level=logging.DEBUG)
        self.conn.autocommit = False
        try:
            logging.debug("===UPDATE_FILE＿CREATE_STATUS===")
            self.conn.ping(reconnect=True)
            logging.debug(self.conn.is_connected())
            cur = self.conn.cursor()

            select_job_que_data_result = self.md_scraping_dao.getJobQueData(cur, self.user_id)
            result_file_num = select_job_que_data_result['result_file_num_list'][0]
            self.md_scraping_dao.updateFileCreateStatus(cur, result_file_num, general_group_key, general_key)

            self.conn.commit()
            cur.close()
        except:
            self.conn.rollback()
            cur.close()
            raise

    def scrapingTask(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("===MAIN_LOGIC_START===")
        self.conn.ping(reconnect=True)
        logging.debug(self.conn.is_connected())
        cur = self.conn.cursor()
        job_non_count = 0

        while True:
            if job_non_count == self.batch_break_count:
                logging.debug("===MAIN_BATCH_BREAK===")
                break

            try:
                if self.md_scraping_dao.jadgeJobNumStock(cur, self.user_id):
                    logging.debug("===JOB_NUM_NON===")
                    job_non_count += 1
                    continue
            except:
                raise

            try:
                self.conn.autocommit = False

                select_job_que_data_result = self.md_scraping_dao.getJobQueData(cur, self.user_id)
                job_num = select_job_que_data_result['job_num_list'][0]
                result_file_num = select_job_que_data_result['result_file_num_list'][0]

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

                logging.debug("===MAIN_LOGIC_SERVICE_START===")
                main_logic_service = MeteorologicaldataScraping(
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
                    endSign = main_logic_service.mainSoup()
                    if endSign == '終了':
                        break
                main_logic_service.MDOutput()

                self.updateFileCreateStatus(self.general_group_key, self.end_general_key)
                self.md_scraping_dao.deleteUserJobData(cur, job_num)

                self.conn.commit()
                logging.debug("===FILE_CREATE===")
            except:
                traceback.print_exc()
                self.conn.rollback()
                self.updateFileCreateStatus(self.general_group_key, self.error_general_key)
                continue

        logging.debug("===MAIN_LOGIC_END===")
        cur.close()

    def disConnect(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("===MYSQL-CONNECTION_DISCONNECT===")
        self.conn.close()



