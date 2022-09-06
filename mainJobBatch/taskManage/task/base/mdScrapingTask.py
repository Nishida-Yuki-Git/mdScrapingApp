import traceback
from logging import getLogger
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
import os
import stat
import datetime


class MdScrapingTaskExecute():
    """
    随時バッチタスクコントロール基底クラス

    Attributes
    ----------
    process_active_id : str
        バッチプロセス処理中フラグ
    process_rest_id : str
        バッチプロセス待機中フラグ
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

        self.process_active_id = '1'
        self.process_rest_id = '0'
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
            task_manage_data_flag = self.getTaskManageDataFlag(md_scraping_service)
            if task_manage_data_flag == self.process_rest_id:
                self.logger.debug("==USER_IS_PASSIVE_OK==")
                self.userStatusUpdateActive(md_scraping_service)
                md_scraping_service.scrapingTask()
                self.userStatusUpdateRest(md_scraping_service)
            else:
                self.logger.debug("==USER_IS_ACTIVE_NO==")
                pass
            md_scraping_service.disConnect()
        except:
            self.logger.debug("==GET_EXCEPTION==")
            traceback.print_exc()

            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            ##os.chmod(path=self.error_log_path, mode=stat.S_IWRITE) ##本番環境ではコメントアウト
            with open(self.error_log_path, 'a') as file:
                file.write('\n')
                file.write('-----------------------------------------------------\n')
                file.write(str(datetime.datetime.now())+'：'+self.user_id+'：'+'MdScrapingTaskExecute')
                traceback.print_exc(file=file)
                file.write('-----------------------------------------------------\n')
            ##os.chmod(path=self.error_log_path, mode=stat.S_IREAD) ##本番環境ではコメントアウト

            md_scraping_service.updateFileCreateStatus(self.general_group_key, self.error_general_key)
            self.userStatusUpdateRest(md_scraping_service)
            md_scraping_service.disConnect()

    def setNewService(self):
        """
        個別バッチサービスインスタンスを設定する

        Returns
        ----------
        service : ?
            個別バッチサービス
        """

        pass

    def getTaskManageDataFlag(self, md_scraping_service):
        """
        個別バッチのプロセスステータスを取得する

        Parameters
        ----------
        md_scraping_service : ?
            個別バッチサービス

        Returns
        ----------
        task_manage_data_flag : str
            個別バッチタスクプロセスフラグ
        """

        pass

    def userStatusUpdateActive(self, md_scraping_service):
        """
        ユーザーバッチ処理ステータスをActiveに設定

        Parameters
        ----------
        md_scraping_service : ?
            個別バッチサービス
        """

        pass

    def userStatusUpdateRest(self, md_scraping_service):
        """
        ユーザーバッチ処理ステータスをRest状態に設定

        Parameters
        ----------
        md_scraping_service : ?
            個別バッチサービス
        """

        pass

