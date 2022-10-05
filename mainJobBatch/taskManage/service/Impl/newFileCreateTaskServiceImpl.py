from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingTaskServiceImpl import MdScrapingTaskServiceImpl
from mainJobBatch.taskManage.dao.newFileCreateDao import NewFileCreateDao
from mainJobBatch.taskManage.dao.daoImple.newFileCreateDaoImple import NewFileCreateDaoImple
from mainJobBatch.taskManage.exception.mdException import MdException
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.mdException import MdQueBizException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils


class NewFileCreateTaskServiceImpl(MdScrapingTaskServiceImpl):
    """
    新規ファイル作成サービスクラス

    Attributes
    ----------
    batch_break_count : int
        バッチプロセス終了カウント値
    new_file_create_dao : NewFileCreateDao
        新規ファイル作成バッチDaoインターフェース
    """

    def __init__(self, user_id):
        """
        Parameters
        ----------
        user_id : str
            ユーザーID
        """

        super().__init__(user_id)
        self.batch_break_count = 50
        self.new_file_create_dao: NewFileCreateDao = NewFileCreateDaoImple()

    def getResultFileNumAndJobNum(self, cur, call_ex_kbn):
        """
        ファイル番号及びジョブIDの取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        call_ex_kbn ; str
            呼び出し元処理例外区分

        Returns
        ----------
        process_param : dict
            ファイル番号及びジョブID
        """

        super().getResultFileNumAndJobNum(cur, call_ex_kbn)
        try:
            select_job_que_data_result = self.new_file_create_dao.getJobQueData(cur, self.user_id)
            job_num = select_job_que_data_result['job_num_list'][0]
            result_file_num = select_job_que_data_result['result_file_num_list'][0]
            process_param = {
                "job_num": job_num,
                "result_file_num": result_file_num,
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
            return self.new_file_create_dao.jadgeJobNumStock(cur, self.user_id)
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

