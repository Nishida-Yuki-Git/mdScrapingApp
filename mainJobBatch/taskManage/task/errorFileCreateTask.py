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

    def getTaskThreadNum(self, md_scraping_service):
        """
        エラーファイル再作成バッチのThread数を取得する

        Parameters
        ----------
        md_scraping_service : ErrorFileCreateTaskServiceImpl
            エラーファイル再作成バッチサービス

        Returns
        ----------
        task_manage_data_thread_num : str
            個別バッチタスクThread数
        """

        super().getTaskThreadNum(md_scraping_service)
        try:
            md_scraping_service.taskManageRegister(self.error_create_task_id)
            task_manage_data_thread_num = md_scraping_service.getUserTaskThreadNum(self.error_create_task_id)
            return task_manage_data_thread_num
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def addThread(self, md_scraping_service, max_thread):
        """
        ユーザーバッチ処理のActiveThread数を追加

        Parameters
        ----------
        md_scraping_service : ErrorFileCreateTaskServiceImpl
            エラーファイル再作成バッチサービス
        max_thread : int
            maxThread数
        """

        super().addThread(md_scraping_service, max_thread)
        try:
            md_scraping_service.updateUserTaskThread(self.error_create_task_id, self.thread_add_flag, max_thread)
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex

    def removeThread(self, md_scraping_service):
        """
        ユーザーバッチ処理のActiveThread数を1つ削除

        Parameters
        ----------
        md_scraping_service : ErrorFileCreateTaskServiceImpl
            エラーファイル再作成バッチサービス
        """

        super().removeThread(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskThread(self.error_create_task_id, self.thread_remove_flag)
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex
