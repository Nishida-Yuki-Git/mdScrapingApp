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

        pass

    @abstractmethod
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

        pass

    @abstractmethod
    def updateFileCreateStatus(self, general_group_key, general_key, call_ex_kbn):
        """
        ファイル作成ステータスを更新する(この時ファイル番号とジョブ番号をフィールドに一時保存する)

        Parameters
        ----------
        general_group_key : str
            汎用グループキー
        general_key : str
            汎用キー
        call_ex_kbn : 呼び出し区分
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



