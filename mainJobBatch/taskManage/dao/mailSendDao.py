from abc import ABCMeta, abstractmethod

class MailSendDao(metaclass=ABCMeta):
    """ メール送信個別Daoインターフェース
    """

    @abstractmethod
    def getMailAddress(self, cur, user_id):
        """
        メールアドレスの取得

        Parameters
        ----------
        conn : MySQLdb.connections.Connection
            MySQLコネクタ
        user_id : str
            ユーザーID

        Returns
        ----------
        str
            メールアドレス
        """

        pass

    @abstractmethod
    def getFilePath(self, cur, result_file_num):
        """
        送信ファイルパスを取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        result_file_num : str
            ファイル番号

        Returns
        ----------
        str
            ファイルパス
        """

        pass







