import traceback
from logging import getLogger
import os
import stat
import datetime
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException

class MdScrapingTaskExecute():
    """
    随時バッチタスクコントロール基底クラス

    Attributes
    ----------
    max_thread : int
        最大多重Thread数(各ユーザー,各バッチ)
    thread_add_flag : str
        thread追加フラグ
    thread_remove_flag : str
        thread削除フラグ
    general_group_key : str
        汎用グループキー
    error_general_key : str
        汎用キー(ファイル作成ステータス"エラー"取得用キー)
    user_id = str
        ユーザーID
    logger : logging
        ログ出力オブジェクト
    error_log_path : str
        デバッグトレース内容出力用ファイルパス
    """

    def __init__(self, user_id):
        """
        Parameters
        ----------
        user_id : str
            ユーザーID
        """

        self.max_thread = 5
        self.thread_add_flag = '1'
        self.thread_remove_flag = '0'
        self.general_group_key = 'GR000001'
        self.error_general_key = '04'
        self.user_id = user_id
        self.logger = getLogger("OnlineBatchLog").getChild("task")
        self.error_log_path = '../../../../error_log.txt'

    def jobControl(self):
        """ バッチタスクコントロール実行
        """

        try:
            md_scraping_service = self.setNewService()
            task_manage_thread = self.getTaskThreadNum(md_scraping_service)
            if int(task_manage_thread) < self.max_thread:
                self.logger.debug("==Thread_No_MAX_OK==")
                self.addThread(md_scraping_service, self.max_thread)
                md_scraping_service.scrapingTask()
                self.removeThread(md_scraping_service)
            else:
                self.logger.debug("==Thread_Max_NO==")
                pass
            md_scraping_service.disConnect()
        except Exception as ex:
            md_scraping_service.updateFileCreateStatus(self.general_group_key, self.error_general_key, '0')
            self.removeThread(md_scraping_service)

            self.logger.debug("==GET_EXCEPTION==")
            self.logger.debug(ex.getMessage())
            self.logger.debug(ex.getTrace())

            md_scraping_service.disConnect()

            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            ##os.chmod(path=self.error_log_path, mode=stat.S_IWRITE) ##本番環境ではコメントアウト
            with open(self.error_log_path, 'a') as file:
                file.write('\n')
                file.write('-----------------------------------------------------\n')
                file.write(str(datetime.datetime.now())+'：'+self.user_id+'：'+'MdScrapingTaskExecute'+'\n')
                file.write(ex.getMessage()+'\n')
                file.write(ex.getTrace()+'\n')
                file.write('-----------------------------------------------------\n')
            ##os.chmod(path=self.error_log_path, mode=stat.S_IREAD) ##本番環境ではコメントアウト

    def setNewService(self):
        """
        個別バッチサービスインスタンスを設定する

        Returns
        ----------
        service : ?
            個別バッチサービス
        """

        pass

    def getTaskThreadNum(self, md_scraping_service):
        """
        個別バッチのThread数を取得

        Parameters
        ----------
        md_scraping_service : ?
            個別バッチサービス

        Returns
        ----------
        task_manage_data_thread_num : str
            個別バッチタスクThread数
        """

        pass

    def addThread(self, md_scraping_service, max_thread):
        """
        ユーザーバッチ処理のActiveThread数を追加

        Parameters
        ----------
        md_scraping_service : ?
            個別バッチサービス
        max_thread : int
            maxTread数
        """

        pass

    def removeThread(self, md_scraping_service):
        """
        ユーザーバッチ処理のActiveThread数を1つ削除

        Parameters
        ----------
        md_scraping_service : ?
            個別バッチサービス
        """

        pass

