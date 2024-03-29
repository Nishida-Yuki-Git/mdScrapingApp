from mainJobBatch.taskManage.dao.errorFileCreateDao import ErrorFileCreateDao
from mainJobBatch.taskManage.exception.mdException import MdException
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils

class ErrorFileCreateDaoImple(ErrorFileCreateDao):
    """ エラーファイル再作成バッチ個別Daoインターフェース
    """

    def getJobNum(self, cur, result_file_num):
        """
        ジョブ番号の取得

        Parameters
        ----------
        conn : MySQLdb.connections.Connection
            MySQLコネクタ
        result_file_num : str
            ファイル番号

        Returns
        ----------
        str
            ジョブ番号
        """

        select_user_job_num = ("""
        SELECT
          JOB_QUE_DATA.job_num
        FROM
          scrapingSystem_jobquedata AS JOB_QUE_DATA
        WHERE
          JOB_QUE_DATA.result_file_num = '""" + str(result_file_num) + """'
        """)

        try:
            cur.execute(select_user_job_num)
            rows = cur.fetchall()
            return rows[0][0]
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '0')
            raise ex

    def jadgeQueStock(self, cur, result_file_num):
        """
        ジョブキュー残数の確認

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        result_file_num : str
            ファイル番号

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
        WHERE
          JOB_QUE_DATA.result_file_num = '""" + result_file_num + """'
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