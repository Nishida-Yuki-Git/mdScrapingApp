from mainJobBatch.taskManage.dao.mdScrapingDao import MdScrapingDao
import mysql.connector as mydb
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.mdException import MdQueBizException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils

class MdScrapingDaoImple(MdScrapingDao):
    """
    バッチ共通Daoインターフェース

    Attributes
    ----------
    batch_setting : OnlineBatchSetting
        オンライン随時バッチ設定クラスオブジェクト
    conn : MySQLdb.connections.Connection
        MySQLコネクタ
    """

    def __init__(self):
        self.batch_setting = OnlineBatchSetting()
        self.conn = None
        try:
            self.conn = mydb.connect(host=self.batch_setting.getHostId(),
                        port=self.batch_setting.getPortNum(),
                        user=self.batch_setting.getDbUser(),
                        password=self.batch_setting.getDbPassWord(),
                        database=self.batch_setting.getDatabaseName())
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def getConnection(self):
        """
        MySQLコネクタの返却

        Returns
        ----------
        conn : MySQLdb.connections.Connection
            MySQLコネクタ
        """

        return self.conn

    def taskManageRegist(self, cur, task_id, user_id):
        """
        ユーザーバッチプロセス登録

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        task_id : str
            バッチプロセスタスクID
        user_id : str
            ユーザーID
        """

        select_sql_str = "SELECT * FROM scrapingSystem_taskmanagedata WHERE task_id = '" + task_id + "' AND user_id = '" + user_id + "'"
        insert_sql_id = ("""
        INSERT INTO scrapingSystem_taskmanagedata
         (task_id, user_id, task_thread_num)
        VALUES (%s, %s, %s)
        """)

        try:
            cur.execute(select_sql_str)
            cur.fetchall()

            if cur.rowcount == 0:
                cur.execute(insert_sql_id, (task_id, user_id, '0'))
            else:
                pass
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def getUserTaskThreadNum(self, cur, task_id, user_id):
        """
        ユーザーバッチThread数取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        task_id : str
            バッチプロセスタスクID
        user_id : str
            ユーザーID

        Returns
        ----------
        resulr_str : list
            ユーザーバッチThread数
        """

        select_sql_str = "SELECT TMDATA.task_thread_num FROM scrapingSystem_taskmanagedata AS TMDATA WHERE task_id = '" + task_id + "' AND user_id = '" + user_id + "'"

        try:
            cur.execute(select_sql_str)
            rows = cur.fetchall()
            result = ''
            for row in rows:
                result = row
            result_str = result[0]

            return result_str
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def updateUserProcessThread(self, cur, task_id, user_id, thread_controll_flag, max_thread):
        """
        ユーザーバッチThread更新

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        task_id : str
            バッチプロセスタスクID
        user_id : str
            ユーザーID
        thread_controll_flag : str
            thread増減フラグ
        max_thread : int
            macThread数
        """

        select_sql_str = "SELECT TMDATA.task_thread_num FROM scrapingSystem_taskmanagedata AS TMDATA WHERE task_id = '" + task_id + "' AND user_id = '" + user_id + "'"

        delete_task_manage_record = ("""
        DELETE FROM scrapingSystem_taskmanagedata
        WHERE task_id = '""" + task_id + """' AND user_id = '""" + user_id + """'""")
        insert_task_manage_record = ("""
        INSERT INTO scrapingSystem_taskmanagedata
         (task_id, user_id, task_thread_num)
        VALUES (%s, %s, %s)
        """)

        try:
            cur.execute(select_sql_str)
            rows = cur.fetchall()
            result = ''
            for row in rows:
                result = row
            result_num = int(result[0])

            if thread_controll_flag == '1':
                if result_num < max_thread:
                    cur.execute(delete_task_manage_record)
                    cur.execute(insert_task_manage_record, (task_id, user_id, result_num+1))
            else:
                if result_num > 0:
                    cur.execute(delete_task_manage_record)
                    cur.execute(insert_task_manage_record, (task_id, user_id, result_num-1))
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def getJobParamData(self, cur, job_num):
        """
        ジョブパラメータ取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        job_num : str
            ジョブID

        Returns
        ----------
        job_param_result : dict
            ジョブパラメータ
        """

        select_user_job_param = ("""
        SELECT
          JOB_PARAM_DATA.job_start_year,
          JOB_PARAM_DATA.job_end_year,
          JOB_PARAM_DATA.job_start_month,
          JOB_PARAM_DATA.job_end_month
        FROM
          scrapingSystem_jobparamdata AS JOB_PARAM_DATA
        WHERE
          job_num = '""" + job_num + """'""")
        select_user_job_param_detail = ("""
        SELECT
          JOB_PARAM_DETAIL_DATA.job_ken,
          JOB_PARAM_DETAIL_DATA.job_md_item
        FROM
          scrapingSystem_jobparamdetaildata AS JOB_PARAM_DETAIL_DATA
        WHERE
          job_num = '""" + job_num + """'""")

        try:
            cur.execute(select_user_job_param)
            rows = cur.fetchall()

            job_start_year = ''
            job_end_year = ''
            job_start_month = ''
            job_start_month = ''
            for row in rows:
                job_start_year = row[0]
                job_end_year = row[1]
                job_start_month = row[2]
                job_end_month = row[3]

            cur.execute(select_user_job_param_detail)
            rows_detail = cur.fetchall()

            job_ken_list = []
            job_md_item_list = []
            for row_detail in rows_detail:
                job_ken_list.append(row_detail[0])
                job_md_item_list.append(row_detail[1])

            job_param_result = {
                "job_start_year": job_start_year,
                "job_end_year": job_end_year,
                "job_start_month": job_start_month,
                "job_end_month": job_end_month,
                "job_ken_list": job_ken_list,
                "job_md_item_list": job_md_item_list,
            }
            return job_param_result
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '2')
            raise ex

    def getKenUrlParam(self, cur, ken_list):
        """
        県パラメータ取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        ken_list : list
            県名リスト

        Returns
        ----------
        result_ken_param_list : dict
            県パラメータ
        """

        try:

            ken_no_list = []
            ken_block_list = []
            for ken in ken_list:
                select_ken_param_sql = ("""
                SELECT
                  KEN_PARAM_MT.ken_no,
                  KEN_PARAM_MT.ken_block_no
                FROM
                  scrapingSystem_kenparammt AS KEN_PARAM_MT
                WHERE
                  KEN_PARAM_MT.ken_name = '""" + ken + """'""")
                cur.execute(select_ken_param_sql)
                rows = cur.fetchall()
                for row in rows:
                    ken_no_list.append(row[0])
                    ken_block_list.append(row[1])

            result_ken_param_list = {
                "ken_no_list": ken_no_list,
                "ken_block_list": ken_block_list,
            }
            return result_ken_param_list
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '2')
            raise ex

    def getJMAgencyURL(self, cur):
        """
        気象庁URLパーツ取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル

        Returns
        ----------
        md_url_list : list
            気象庁URLパーツリスト
        """

        select_jm_agency_url = ("""
        SELECT
          URL_MT.md_url
        FROM
          scrapingSystem_mdurlmt AS URL_MT
        ORDER BY
          URL_MT.md_url_seq ASC
        """)

        try:
            cur.execute(select_jm_agency_url)
            rows = cur.fetchall()

            md_url_list = []
            for row in rows:
                md_url_list.append(row[0])

            return md_url_list
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '2')
            raise ex

    def updateFileCreateStatus(self, cur, result_file_num, general_group_key, general_key):
        """
        ファイル作成ステータス更新

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        result_file_num : str
            ファイル番号
        general_group_key : str
            汎用グループキー
        general_key : str
            汎用キー
        """

        select_general_code_MT = ("""
        SELECT
          GENERAL_CODE_MT.general_code
        FROM
          scrapingSystem_generalcodemt AS GENERAL_CODE_MT
        WHERE
          GENERAL_CODE_MT.general_group_key = '""" + general_group_key + """'
          AND GENERAL_CODE_MT.general_key = '""" + general_key + """'
        """)

        try:
            cur.execute(select_general_code_MT)
            rows = cur.fetchall()

            update_file_create_status_sql = ("""
            UPDATE
              scrapingSystem_processresultdata AS PRMT
            SET
              PRMT.file_create_status = '""" + rows[0][0] + """'
            WHERE
              PRMT.result_file_num = '""" + str(result_file_num) + """'
            """)
            cur.execute(update_file_create_status_sql)

        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def deleteUserJobData(self, cur, job_num):
        """
        処理済みジョブキューの削除

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        job_nu, : str
            ジョブ番号
        """

        delete_job_que_data = ("""
        DELETE FROM scrapingSystem_jobquedata
        WHERE job_num = '""" + job_num + """'""")
        delete_job_param_data = ("""
        DELETE FROM scrapingSystem_jobparamdata
        WHERE job_num = '""" + job_num + """'""")
        delete_job_param_detail_data = ("""
        DELETE FROM scrapingSystem_jobparamdetaildata
        WHERE job_num = '""" + job_num + """'""")

        try:
            cur.execute(delete_job_que_data)
            cur.execute(delete_job_param_data)
            cur.execute(delete_job_param_detail_data)
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '2')
            raise ex

    def registFilePath(self, cur, result_file_num, save_path):
        """
        物理ファイル格納パス登録

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        result_file_num : str
            ファイル番号
        save_path : str
            物理ファイル格納パス
        """

        regist_create_file = ("""
        UPDATE
          scrapingSystem_filemanagedata AS FILE_MANAGE_MT
        SET
          FILE_MANAGE_MT.create_file = '""" + save_path + """'
        WHERE
          FILE_MANAGE_MT.result_file_num = '""" + result_file_num + """'
        """)

        try:
            cur.execute(regist_create_file)
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '2')
            raise ex













