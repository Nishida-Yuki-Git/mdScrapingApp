from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingTaskServiceImpl import MdScrapingTaskServiceImpl
from mainJobBatch.taskManage.dao.errorFileCreateDao import ErrorFileCreateDao
from mainJobBatch.taskManage.dao.daoImple.errorFileCreateDaoImple import ErrorFileCreateDaoImple
from mainJobBatch.taskManage.exception.mdException import MdException
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.mdException import MdQueBizException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils


class ErrorFileCreateTaskServiceImpl(MdScrapingTaskServiceImpl):
    """
    エラーファイル再作成サービスクラス

    Attributes
    ----------
    result_file_num : str
        ファイル番号
    batch_break_count : int
        バッチプロセス終了カウント値
    batch_process_flag : boolean
        バッチプロセスフラグ
    error_file_create_dao : ErrorFileCreateDao
        エラーファイル再作成バッチDaoインターフェース
    """

    def __init__(self, user_id, result_file_num):
        """
        Parameters
        ----------
        user_id : str
            ユーザーID
        result_file_num : str
            ファイル番号
        """

        super().__init__(user_id)
        self.result_file_num = result_file_num
        self.batch_break_count = 2
        self.batch_process_flag = False
        self.error_file_create_dao: ErrorFileCreateDao = ErrorFileCreateDaoImple()

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

        super().getResultFileNumAndJobNum(cur, call_ex_kbn)
        try:
            job_num = self.error_file_create_dao.getJobNum(cur, self.result_file_num)

            process_param = {
                "job_num": job_num,
                "result_file_num": self.result_file_num,
            }
            return process_param
        except MdException as ex:
            if call_ex_kbn=='0':
                raise MdBatchSystemException
            else:
                raise MdQueBizException
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            if call_ex_kbn=='0':
                ex = ex_util.commonHandling(ex, '1')
            else:
                ex = ex_util.commonHandling(ex, '2')
            raise ex

    def getBatchBreakCount(self):
        """
        バッチプロセス終了カウント値の取得

        Returns
        ----------
        int
            バッチプロセス終了カウント値
        """

        super().getBatchBreakCount()
        return self.batch_break_count

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

        super().countJob(cur)
        try:
            if self.batch_process_flag:
                return True
            else:
                self.batch_process_flag = True
                return self.error_file_create_dao.jadgeQueStock(cur, self.result_file_num)
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

