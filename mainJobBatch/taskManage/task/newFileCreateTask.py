from mainJobBatch.taskManage.task.base.mdScrapingTask import MdScrapingTaskExecute
from mainJobBatch.taskManage.service.Impl.newFileCreateTaskServiceImpl import NewFileCreateTaskServiceImpl
from mainJobBatch.taskManage.serviceBase.mdScrapingTaskService import MdScrapingTaskService
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils
import traceback


class NewFileCreateTaskExecute(MdScrapingTaskExecute):
    """
    新規ファイル作成バッチタスクコントロールクラス

    Attributes
    ----------
    new_create_task_id : str
        新規ファイル作成バッチタスクID
    """

    def __init__(self, user_id):
        """
        Parameters
        ----------
        user_id : str
            ユーザーID
        """

        super().__init__(user_id)
        self.new_create_task_id = '0001'

    def setNewService(self):
        """
        新規ファイル作成バッチサービスインスタンスを設定する

        Returns
        ----------
        service : NewFileCreateTaskServiceImpl
            新規ファイル作成バッチサービス
        """

        super().setNewService()
        service: MdScrapingTaskService = NewFileCreateTaskServiceImpl(self.user_id)
        return service

    def getTaskThreadNum(self, md_scraping_service):
        """
        新規ファイル作成バッチのThread数を取得する

        Parameters
        ----------
        md_scraping_service : NewFileCreateTaskServiceImpl
            新規ファイル作成バッチサービス

        Returns
        ----------
        task_manage_data_thread_num : str
            個別バッチタスクプロセスThread数
        """

        super().getTaskThreadNum(md_scraping_service)
        try:
            md_scraping_service.taskManageRegister(self.new_create_task_id)
            task_manage_data_thread_num = md_scraping_service.getUserTaskThreadNum(self.new_create_task_id)
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
        md_scraping_service : NewFileCreateTaskServiceImpl
            新規ファイル作成バッチサービス
        max_thread : int
            maxThread数
        """

        super().addThread(md_scraping_service, max_thread)
        try:
            md_scraping_service.updateUserTaskThread(self.new_create_task_id, self.thread_add_flag, max_thread)
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
        md_scraping_service : NewFileCreateTaskServiceImpl
            新規ファイル作成バッチサービス
        """

        super().removeThread(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskThread(self.new_create_task_id, self.thread_remove_flag)
        except MdBatchSystemException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '1')
            raise ex