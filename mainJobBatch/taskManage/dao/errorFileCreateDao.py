from abc import ABCMeta, abstractmethod

class ErrorFileCreateDao(metaclass=ABCMeta):
    """ エラーファイル再作成バッチ個別Daoインターフェース
    """

    @abstractmethod
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

        pass

    @abstractmethod
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

        pass







