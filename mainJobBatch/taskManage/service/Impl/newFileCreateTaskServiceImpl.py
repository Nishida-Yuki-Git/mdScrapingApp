from mainJobBatch.taskManage.serviceBase.Impl.mdScrapingTaskServiceImpl import MdScrapingTaskServiceImpl
from mainJobBatch.taskManage.dao.newFileCreateDao import NewFileCreateDao
from mainJobBatch.taskManage.dao.daoImple.newFileCreateDaoImple import NewFileCreateDaoImple


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
        self.batch_break_count = 20
        self.new_file_create_dao: NewFileCreateDao = NewFileCreateDaoImple()

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
            select_job_que_data_result = self.new_file_create_dao.getJobQueData(cur, self.user_id)
            job_num = select_job_que_data_result['job_num_list'][0]
            result_file_num = select_job_que_data_result['result_file_num_list'][0]
            process_param = {
                "job_num": job_num,
                "result_file_num": result_file_num,
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
            return self.new_file_create_dao.jadgeJobNumStock(cur, self.user_id)
        except:
            raise

