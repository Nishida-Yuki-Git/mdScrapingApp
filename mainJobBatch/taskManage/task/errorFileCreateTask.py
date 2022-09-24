from mainJobBatch.taskManage.task.base.mdScrapingTask import MdScrapingTaskExecute
from mainJobBatch.taskManage.service.Impl.errorFileCreateTaskServiceImpl import ErrorFileCreateTaskServiceImpl
from mainJobBatch.taskManage.serviceBase.mdScrapingTaskService import MdScrapingTaskService
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils
import traceback


class ErrorFileCreateTaskExecute(MdScrapingTaskExecute):
    """
    エラーファイル再作成バッチタスクコントロールクラス

    Attributes
    ----------
    result_file_num : str
        ファイル番号
    error_create_task_id : str
        エラーファイル作成バッチタスクID
    """

    def __init__(self, user_id, result_file_num):
        """
        Parameters
        ----------
        user_id : str
            ユーザーID
        """

        super().__init__(user_id)
        self.result_file_num = result_file_num
        self.error_create_task_id = '0002'

    def setNewService(self):
        """
        エラーファイル再作成バッチサービスインスタンスを設定する

        Returns
        ----------
        service : ErrorFileCreateTaskServiceImpl
            エラーファイル再作成バッチサービス
        """

        super().setNewService()
        service: MdScrapingTaskService = ErrorFileCreateTaskServiceImpl(self.user_id, self.result_file_num)
        return service

    def getTaskManageDataFlag(self, md_scraping_service):
        """
        エラーファイル再作成バッチのプロセスステータスを取得する

        Parameters
        ----------
        md_scraping_service : ErrorFileCreateTaskServiceImpl
            エラーファイル再作成バッチサービス

        Returns
        ----------
        task_manage_data_flag : str
            個別バッチタスクプロセスフラグ
        """

        super().getTaskManageDataFlag(md_scraping_service)
        try:
            md_scraping_service.taskManageRegister(self.error_create_task_id)
            task_manage_data_flag = md_scraping_service.getUserTaskStatus(self.error_create_task_id)
            return task_manage_data_flag
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def userStatusUpdateActive(self, md_scraping_service):
        """
        ユーザーバッチ処理ステータスをActiveに設定

        Parameters
        ----------
        md_scraping_service : ErrorFileCreateTaskServiceImpl
            エラーファイル再作成バッチサービス
        """

        super().userStatusUpdateActive(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.error_create_task_id, self.process_active_id)
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def userStatusUpdateRest(self, md_scraping_service):
        """
        ユーザーバッチ処理ステータスをRest状態に設定

        Parameters
        ----------
        md_scraping_service : ErrorFileCreateTaskServiceImpl
            エラーファイル再作成バッチサービス
        """

        super().userStatusUpdateRest(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.error_create_task_id, self.process_rest_id)
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex
