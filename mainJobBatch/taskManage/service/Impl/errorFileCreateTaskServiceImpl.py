from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingTaskServiceImpl import MdScrapingTaskServiceImpl
from mainJobBatch.taskManage.dao.errorFileCreateDao import ErrorFileCreateDao
from mainJobBatch.taskManage.dao.daoImple.errorFileCreateDaoImple import ErrorFileCreateDaoImple


class ErrorFileCreateTaskServiceImpl(MdScrapingTaskServiceImpl):
    """
    エラーファイル再作成サービスクラス

    Attributes
    ----------
    result_file_num : str
        ファイル番号
    batch_break_count : int
        バッチプロセス終了カウント値
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
        self.batch_break_count = 1
        self.error_file_create_dao: ErrorFileCreateDao = ErrorFileCreateDaoImple()

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

        super().getResultFileNumAndJobNum(cur)
        try:
            job_num = self.error_file_create_dao.getJobNum(cur, self.result_file_num)

            process_param = {
                "job_num": job_num,
                "result_file_num": self.result_file_num,
            }
            return process_param
        except:
            raise

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
            return self.error_file_create_dao.jadgeQueStock(cur, self.user_id)
        except:
            raise

