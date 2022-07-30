from mainJobBatch.taskManage.dao.mailSendDao import MailSendDao

class MailSendDaoImple(MailSendDao):
    """ メール送信個別Dao実装
    """

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

        select_mail_address = ("""
        SELECT
          ACCOUNT.email
        FROM
          scrapingSystem_account AS ACCOUNT
        WHERE
          ACCOUNT.userid = '""" + str(user_id) + """'
        """)

        try:
            cur.execute(select_mail_address)
            rows = cur.fetchall()
            return rows[0][0]
        except:
            raise

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

        select_file_path = ("""
        SELECT
          FILEMANAGEDATA.create_file
        FROM
          scrapingSystem_filemanagedata AS FILEMANAGEDATA
        WHERE
          FILEMANAGEDATA.result_file_num = '""" + str(result_file_num) + """'
        """)

        try:
            cur.execute(select_file_path)
            rows = cur.fetchall()
            return rows[0][0]
        except:
            raise
