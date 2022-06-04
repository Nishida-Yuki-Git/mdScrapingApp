from abc import ABCMeta, abstractmethod


class MdScrapingTaskService(metaclass=ABCMeta):
    """ 気象データ収集タスクサービス基底インターフェース
    """

    @abstractmethod
    def taskManageRegister(self, task_id):
        """
        ユーザーのバッチプロセス登録

        Parameters
        ----------
        task_id : str
            バッチタスクID
        """

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

    @abstractmethod
    def scrapingTask(self):
        """ 気象データ収集実行
        """

        pass

    @abstractmethod
    def getBatchBreakCount(self):
        """
        バッチプロセス終了カウント値の取得

        Returns
        ----------
        int
            バッチプロセス終了カウント値
        """

        pass

    @abstractmethod
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

    @abstractmethod
    def disConnect(self):
        """ DBコネクションの終了
        """

        pass



