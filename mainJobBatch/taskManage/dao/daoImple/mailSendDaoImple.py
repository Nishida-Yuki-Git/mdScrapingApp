from mainJobBatch.taskManage.dao.mailSendDao import MailSendDao
from mainJobBatch.taskManage.exception.mdException import MdException

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

    def getFileGyomuData(self, cur, result_file_num):
        """
        ファイル業務データを取得

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        result_file_num : str
            ファイル番号

        Returns
        ----------
        dict
            ファイル関連業務データ
        """

        select_gyomu = ("""
        select
            PRODATA.target_start_year,
            PRODATA.target_end_year,
            PRODATA.target_start_month,
            PRODATA.target_end_month,
            GROUP_CONCAT(PRODETAIL.target_ken),
            GROUP_CONCAT(PRODETAIL.target_md_item)
        from
            mdsystemdb.scrapingSystem_processresultdata PRODATA
            left join mdsystemdb.scrapingSystem_processresultdetaildata PRODETAIL
                ON PRODETAIL.result_file_num = PRODATA.result_file_num
        where
            PRODATA.result_file_num = '""" + str(result_file_num) + """'
        """)

        try:
            cur.execute(select_gyomu)
            rows = cur.fetchall()

            result_gyomu_list = {
                "target_start_year": None,
                "target_end_year": None,
                "target_start_month": None,
                "target_end_month": None,
                "target_ken": None,
                "target_md_item": None,
            }

            result_gyomu_list["target_start_year"] = rows[0][0]
            result_gyomu_list["target_end_year"] = rows[0][1]
            result_gyomu_list["target_start_month"] = rows[0][2]
            result_gyomu_list["target_end_month"] = rows[0][3]
            result_gyomu_list["target_ken"] = rows[0][4]
            result_gyomu_list["target_md_item"] = rows[0][5]
            return result_gyomu_list
        except:
            raise
