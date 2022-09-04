from abc import ABCMeta, abstractmethod

class MdScrapingDao(metaclass=ABCMeta):
    """ バッチ共通Daoインターフェース
    """

    @abstractmethod
    def getConnection(self):
        """
        MySQLコネクタの返却

        Returns
        ----------
        conn : MySQLdb.connections.Connection
            MySQLコネクタ
        """

        pass

    @abstractmethod
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

        pass

    @abstractmethod
    def getUserProcessFlag(self, cur, task_id, user_id):
        """
        ユーザーバッチプロセス取得

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
            ユーザーバッチプロセス
        """

        pass

    @abstractmethod
    def updateUserProcessFlag(self, cur, task_id, user_id, user_process_status):
        """
        ユーザーバッチプロセス更新

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        task_id : str
            バッチプロセスタスクID
        user_id : str
            ユーザーID
        user_process_status : str
            ユーザーバッチプロセスステータス
        """

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass









