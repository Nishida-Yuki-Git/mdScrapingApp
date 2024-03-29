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
from mainJobBatch.taskManage.exception.mdException import MdException
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.mdException import MdQueBizException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils
import os
import stat
import time
import datetime
from pathlib import Path


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
    call_ex_kbn_batch_sys : str
        呼び刺しもと例外区分：バッチシステム基盤例外
    call_ex_kbn_que_biz : str
        呼び刺しもと例外区分：キュービジネス例外
    field_file_num : str
        ファイル番号フィールド保存
    field_job_num : str
        ジョブ番号フィールド保存
    begin_transaction_query : str
        トランザクション開始クエリー
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
        self.call_ex_kbn_batch_sys = '0'
        self.call_ex_kbn_que_biz = '1'
        self.field_file_num = None
        self.field_job_num = None
        self.begin_transaction_query = 'START TRANSACTION'
        self.conn.cmd_query('SET innodb_lock_wait_timeout=1')##最大値=1073741824

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
            self.conn.cmd_query(self.begin_transaction_query)
            cur = self.conn.cursor()

            self.md_scraping_dao.taskManageRegist(cur, task_id, self.user_id)

            self.conn.commit()
            cur.close()
        except MdBatchSystemException as ex:
            self.conn.rollback()
            cur.close()
            raise
        except Exception as ex:
            self.conn.rollback()
            cur.close()
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def getUserTaskThreadNum(self, task_id):
        """
        個別バッチのThread数を取得する

        Parameters
        ----------
        task_id : str
            バッチタスクID

        Returns
        ----------
        user_thread_num : str
            ユーザーバッチThread数
        """

        try:
            self.conn.ping(reconnect=True)
            cur = self.conn.cursor()

            user_thread_num = self.md_scraping_dao.getUserTaskThreadNum(cur, task_id, self.user_id)

            cur.close()
            return user_thread_num
        except MdBatchSystemException as ex:
            cur.close()
            raise
        except Exception as ex:
            cur.close()
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def updateUserTaskThread(self, task_id, thread_controll_flag, max_thread=None):
        """
        個別バッチの稼働Thread数を更新する

        Parameters
        ----------
        task_id : str
            バッチタスクID
        thread_controll_flag : str
            thread増減フラグ
        max_thread : int
            maxThread数
        """

        self.conn.autocommit = False
        try:
            self.conn.ping(reconnect=True)
            self.conn.cmd_query(self.begin_transaction_query)
            cur = self.conn.cursor()

            self.md_scraping_dao.updateUserProcessThread(cur, task_id, self.user_id, thread_controll_flag, max_thread)

            self.conn.commit()
            cur.close()
        except MdBatchSystemException as ex:
            self.conn.rollback()
            cur.close()
            raise
        except Exception as ex:
            self.conn.rollback()
            cur.close()
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def updateFileCreateStatus(self, general_group_key, general_key, call_ex_kbn):
        """
        ファイル作成ステータスを更新する(この時ファイル番号とジョブ番号をフィールドに一時保存する)

        Parameters
        ----------
        general_group_key : str
            汎用グループキー
        general_key : str
            汎用キー
        call_ex_kbn : str
            呼び出し区分
        """

        self.conn.autocommit = False
        try:
            self.conn.ping(reconnect=True)
            self.conn.cmd_query(self.begin_transaction_query)
            cur = self.conn.cursor()

            if (self.field_file_num==None) and (self.field_job_num==None):
                process_param = self.getResultFileNumAndJobNum(cur, call_ex_kbn)
                self.field_file_num = process_param['result_file_num']
                self.field_job_num = process_param['job_num']

            self.md_scraping_dao.updateFileCreateStatus(cur, self.field_file_num, general_group_key, general_key)

            self.conn.commit()
            cur.close()
        except MdBatchSystemException as ex:
            self.conn.rollback()
            cur.close()
            raise
        except Exception as ex:
            self.conn.rollback()
            cur.close()
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def getResultFileNumAndJobNum(self, cur, call_ex_kbn):
        """
        ファイル番号及びジョブIDの取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        call_ex_kbn : str
            呼び出し元処理例外区分

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
        self.conn.autocommit = False
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
            except MdBatchSystemException as ex:
                raise
            except Exception as ex:
                ex_util = ExceptionUtils.get_instance()
                ex = ex_util.commonHandling(ex, '1')
                raise ex

            try:
                job_non_count = 0

                self.updateFileCreateStatus(self.general_group_key, self.processing_general_key, self.call_ex_kbn_que_biz)

                job_param_select_result = self.md_scraping_dao.getJobParamData(cur, self.field_job_num)
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
                    self.field_file_num,
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
                            job_md_item_list,
                            self.field_file_num)
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
                    job_md_item_list,
                    self.field_file_num)
                while True:
                    endSign = md_scraping_logic_service.mainSoup()
                    if endSign == '終了':
                        break
                md_scrap_xl_write_service.xlMiddleCommit(
                    md_scraping_logic_service.MDOutput())
                del md_scraping_logic_service,md_scrap_xl_write_service
            except (MdException,MdBatchSystemException,MdQueBizException,) as ex:
                self.__deleteProgress(self.field_file_num)
                if self.__taskServiceMainExceptionLogic(ex):
                    continue
                else:
                    raise
            except Exception as ex:
                ex_util = ExceptionUtils.get_instance()
                ex = ex_util.commonHandling(ex, '1')
                raise ex

            try:
                self.conn.cmd_query(self.begin_transaction_query)

                middle_save_path = os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent, 'media')+'/file/'+self.field_file_num+'.xlsx'
                self.md_scraping_dao.registFilePath(cur, self.field_file_num, middle_save_path)

                self.updateFileCreateStatus(self.general_group_key, self.end_general_key, self.call_ex_kbn_que_biz)
                self.md_scraping_dao.deleteUserJobData(cur, self.field_job_num)

                mail_send_service: MdScrapingMailService = MdScrapingMailServiceImpl()
                mail_send_service.mailSender(cur, self.user_id, self.field_file_num)

                self.conn.commit()

                self.__deleteProgress(self.field_file_num)
                self.field_file_num = None
                self.field_job_num = None
            except (MdException,MdBatchSystemException,MdQueBizException,) as ex:
                self.conn.rollback()
                self.__deleteProgress(self.field_file_num)
                if self.__taskServiceMainExceptionLogic(ex):
                    self.field_file_num = None
                    self.field_job_num = None
                    continue
                else:
                    raise
            except Exception as ex:
                self.conn.rollback()
                ex_util = ExceptionUtils.get_instance()
                ex = ex_util.commonHandling(ex, '1')
                raise ex
        cur.close()

    def __taskServiceMainExceptionLogic(self, ex):
        """
        scrapingTaskメソッド共通例外ロジック

        Parameters
        ----------
        ex : ?
            例外インスタンス(システム独自例外いずれかのインスタンス)

        Returns
        ----------
        boolean
            True:continue, False:raise
        """

        if isinstance(ex, MdQueBizException):
            self.updateFileCreateStatus(self.general_group_key, self.error_general_key,  self.call_ex_kbn_batch_sys)

            self.logger.debug("==GET_EXCEPTION==")
            self.logger.debug(ex.getMessage())
            self.logger.debug(ex.getTrace())

            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            ##os.chmod(path=self.error_log_path, mode=stat.S_IWRITE) ##本番環境ではコメントアウト
            with open(self.error_log_path, 'a') as file:
                file.write('\n')
                file.write('-----------------------------------------------------\n')
                file.write(str(datetime.datetime.now())+'：'+self.user_id+'：'+'MdScrapingTaskServiceImpl'+'\n')
                file.write(ex.getMessage()+'\n')
                file.write(ex.getTrace()+'\n')
                file.write('-----------------------------------------------------\n')
            ##os.chmod(path=self.error_log_path, mode=stat.S_IREAD) ##本番環境ではコメントアウト
            return True
        elif isinstance(ex, MdBatchSystemException):
            return False
        elif isinstance(ex, MdException):
            return False

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

    def __deleteProgress(self, field_file_num):
        """
        進捗ファイル削除

        Parameters
        ----------
        field_file_num : フィールドに一時保存したファイル番号
        """
        try:
            os.remove(os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent, 'media')+'/file/'+field_file_num+'_tmp.txt')
        except:
            pass



