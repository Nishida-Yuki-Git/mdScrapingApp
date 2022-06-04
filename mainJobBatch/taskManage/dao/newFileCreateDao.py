from abc import ABCMeta, abstractmethod

class NewFileCreateDao(metaclass=ABCMeta):
    """ 新規ファイル作成バッチDaoインターフェース
    """

    @abstractmethod
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

        pass

    @abstractmethod
    def getJobQueData(self, cur, user_id):
        """
        ジョブ番号及びファイル番号の一覧を取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        user_id : str
            ユーザーID

        Returns
        ----------
        result_list : dict
            ジョブ番号及びファイル番号一覧
        """

        pass









