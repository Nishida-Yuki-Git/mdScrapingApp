from mainJobBatch.taskManage.dao.newFileCreateDao import NewFileCreateDao
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.mdException import MdException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils

class NewFileCreateDaoImple(NewFileCreateDao):
    """ 新規ファイル作成バッチDaoインターフェース
    """

    def jadgeJobNumStock(self, cur, user_id):
        """
        ジョブキュー残数の確認

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        user_id : str
            ユーザーID

        Returns
        ----------
        bool
            検索結果(0：True, 1 < False)
        """

        select_user_job_num = ("""
        SELECT
          JOB_QUE_DATA.job_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        INNER JOIN scrapingSystem_processresultdata AS PROCESS_RESULT
          ON PROCESS_RESULT.result_file_num = JOB_QUE_DATA.result_file_num
        WHERE
          JOB_QUE_DATA.user_id = '""" + user_id + """'
          AND PROCESS_RESULT.file_create_status = 'ファイル作成処理開始前'
        ORDER BY JOB_QUE_DATA.job_num ASC""")

        try:
            cur.execute(select_user_job_num)
            rows = cur.fetchall()
            if len(rows) == 0:
                return True
            else:
                return False
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def getJobQueData(self, cur, user_id):
        """
        ジョブ番号及びファイル番号を取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        user_id : str
            ユーザーID

        Returns
        ----------
        result_list : dict
            ジョブ番号及びファイル番号
        """

        select_user_job_id = ("""
        SELECT
          JOB_QUE_DATA.job_num,
          JOB_QUE_DATA.result_file_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        INNER JOIN scrapingSystem_processresultdata AS PROCESS_RESULT
          ON PROCESS_RESULT.result_file_num = JOB_QUE_DATA.result_file_num
        WHERE
          JOB_QUE_DATA.user_id = '""" + user_id + """'
          AND PROCESS_RESULT.file_create_status = 'ファイル作成処理開始前'
        ORDER BY JOB_QUE_DATA.job_num ASC""")

        try:
            cur.execute(select_user_job_id)
            rows = cur.fetchall()

            job_num_list = []
            result_file_num_list = []
            for row in rows:
                job_num_list.append(row[0])
                result_file_num_list.append(row[1])

            result_list = {
                "job_num_list": job_num_list,
                "result_file_num_list": result_file_num_list,
            }
            return result_list
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '0')
            raise ex