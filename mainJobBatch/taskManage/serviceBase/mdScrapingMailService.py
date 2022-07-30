from abc import ABCMeta, abstractmethod

class MdScrapingMailService(metaclass=ABCMeta):
    """ 気象データ収集メール送信サービス基底インターフェース
    """

    @abstractmethod
    def mailSender(self, cur, user_id, result_file_num):
        """
        添付ファイル付きメール送信の実行

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        user_id : str
            ユーザーID
        result_file_num : str
            ファイル番号
        """

        pass