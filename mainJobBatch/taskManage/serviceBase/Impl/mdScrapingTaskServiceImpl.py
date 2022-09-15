from mainJobBatch.taskManage.dao.mdScrapingDao import MdScrapingDao
from mainJobBatch.taskManage.dao.daoImple.mdScrapingDaoImple import MdScrapingDaoImple
from logging import getLogger
import traceback
from mainJobBatch.taskManage.serviceBase.mdScrapingLogicService import MeteorologicaldataScrapingService
from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingLogicServiceImpl import MeteorologicaldataScrapingServiceImpl
from mainJobBatch.taskManage.serviceBase.mdScrapingXlWriteService import MdScrapingXlWriteService
from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingXlWriteServiceImpl import MdScrapingXlWriteServiceImpl
from mainJobBatch.taskManage.serviceBase.mdScrapingTaskService import MdScrapingTaskService
from mainJobBatch.taskManage.serviceBase.mdScrapingMailService import MdScrapingMailService
from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingMailServiceImpl import MdScrapingMailServiceImpl
import os
import stat
import time
import datetime


class MdScrapingTaskServiceImpl(MdScrapingTaskService):
    """
    気象データ収集タスクサービス基底実装クラス

    Attributes
    ----------
    user_id : str
        ユーザーID
    md_scraping_dao : MdScrapingDao
        気象データ収集バッチDaoインターフェース
    conn : MySQLdb.connections.Connection
        MySQLコネクタ
    general_group_key : str
        汎用グループキー
    processing_general_key : str
        汎用キー(ファイル作成中)
    end_general_key : str
        汎用キー(ファイル作成済みステータス)
    error_general_key : str
        汎用キー(エラーステータス)
    logger : logging
        ログ出力オブジェクト
    error_log_path : str
        デバッグトレース内容出力用ファイルパス
    logic_middle_commit_year_num : int
        サービスロジック中間コミット年数
    """

    def __init__(self, user_id):
        """
        Parameters
        ----------
        user_id : str
            ユーザーID
        """

        self.user_id = user_id
        self.md_scraping_dao: MdScrapingDao = MdScrapingDaoImple()
        self.conn = self.md_scraping_dao.getConnection()
        self.general_group_key = 'GR000001'
        self.processing_general_key = '02'
        self.end_general_key = '03'
        self.error_general_key = '04'
        self.logger = getLogger("OnlineBatchLog").getChild("taskService")
        self.error_log_path = '../../../../error_log.txt'
        self.logic_middle_commit_year_num = 5

    def taskManageRegister(self, task_id):
        """
        ユーザーのバッチプロセス登録

        Parameters
        ----------
        task_id : str
            バッチタスクID
        """

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
        """
        個別バッチのプロセスステータスを取得する

        Parameters
        ----------
        task_id : str
            バッチタスクID

        Returns
        ----------
        user_status : str
            ユーザーバッチプロセスステータス
        """

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
        """
        個別バッチのプロセスステータスを更新する

        Parameters
        ----------
        task_id : str
            バッチタスクID
        user_process_status : str
            バッチプロセスステータス
        """

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
        """
        ファイル作成ステータスを更新する

        Parameters
        ----------
        general_group_key : str
            汎用グループキー
        general_key : str
            汎用キー
        """

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
        """
        ファイル番号及びジョブIDの取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル

        Returns
        ----------
        process_param : dict
            ファイル番号及びジョブID
        """

        pass

    def scrapingTask(self):
        """ 気象データ収集実行
        """

        self.logger.debug("==GO_MAIN_SCRAPING==")
        self.conn.ping(reconnect=True)
        cur = self.conn.cursor()
        job_non_count = 0

        while True:
            if job_non_count == self.getBatchBreakCount():
                self.logger.debug("==バッチ処理終了==")
                break

            try:
                if self.countJob(cur):
                    job_non_count += 1
                    self.logger.debug("==キュー残0カウント + " + str(job_non_count) + "==")

                    cur.close()
                    self.disConnect()
                    self.md_scraping_dao: MdScrapingDao = MdScrapingDaoImple()
                    self.conn = self.md_scraping_dao.getConnection()
                    cur = self.conn.cursor()

                    time.sleep(5)
                    continue
            except:
                raise

            try:
                self.conn.autocommit = False

                job_non_count = 0
                self.updateFileCreateStatus(self.general_group_key, self.processing_general_key)

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

                md_scrap_xl_write_service: MdScrapingXlWriteService = MdScrapingXlWriteServiceImpl(
                    cur,
                    result_file_num,
                    self.md_scraping_dao,
                    job_start_year,
                    job_start_month,
                    job_md_item_list,
                    job_ken_list,
                    job_end_month,
                    job_end_year)
                now_year_num = 0
                now_year_num += int(job_start_year)
                while now_year_num<int(job_end_year):
                    if (now_year_num+self.logic_middle_commit_year_num)>=int(job_end_year):
                        break
                    else:
                        now_year_end_num = now_year_num+self.logic_middle_commit_year_num
                        md_scraping_logic_service: MeteorologicaldataScrapingService = MeteorologicaldataScrapingServiceImpl(
                            now_year_num,
                            now_year_end_num,
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
                        md_scrap_xl_write_service.xlMiddleCommit(
                            md_scraping_logic_service.MDOutput())
                        del md_scraping_logic_service
                        now_year_num+=(self.logic_middle_commit_year_num+1)
                md_scraping_logic_service: MeteorologicaldataScrapingService = MeteorologicaldataScrapingServiceImpl(
                    now_year_num,
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
                md_scrap_xl_write_service.xlMiddleCommit(
                    md_scraping_logic_service.MDOutput())
                del md_scraping_logic_service,md_scrap_xl_write_service

                mail_send_service: MdScrapingMailService = MdScrapingMailServiceImpl()
                mail_send_service.mailSender(cur, self.user_id, result_file_num)

                self.updateFileCreateStatus(self.general_group_key, self.end_general_key)
                self.md_scraping_dao.deleteUserJobData(cur, job_num)

                self.conn.commit()
            except:
                self.logger.debug("==GET_EXCEPTION==")
                traceback.print_exc()

                os.chdir(os.path.dirname(os.path.abspath(__file__)))
                ##os.chmod(path=self.error_log_path, mode=stat.S_IWRITE) ##本番環境ではコメントアウト
                with open(self.error_log_path, 'a') as file:
                    file.write('\n')
                    file.write('-----------------------------------------------------\n')
                    file.write(str(datetime.datetime.now())+'：'+self.user_id+'：'+'MdScrapingTaskServiceImpl')
                    traceback.print_exc(file=file)
                    file.write('-----------------------------------------------------\n')
                ##os.chmod(path=self.error_log_path, mode=stat.S_IREAD) ##本番環境ではコメントアウト

                self.conn.rollback()
                self.updateFileCreateStatus(self.general_group_key, self.error_general_key)
                continue

        cur.close()

    def getBatchBreakCount(self):
        """
        バッチプロセス終了カウント値の取得

        Returns
        ----------
        int
            バッチプロセス終了カウント値
        """

        pass

    def countJob(self, cur):
        """
        ユーザーIDに紐づくジョブキューの残数の確認

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル

        Returns
        ----------
        bool
            ジョブキュー残数カウント結果(True：0, False：1以上)
        """

        pass

    def disConnect(self):
        """ DBコネクション終了
        """

        self.logger.debug("==SQL_CONN_END==")
        self.conn.close()



