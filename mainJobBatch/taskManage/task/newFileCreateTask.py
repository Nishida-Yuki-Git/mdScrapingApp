from mainJobBatch.taskManage.task.base.mdScrapingTask import MdScrapingTaskExecute
from mainJobBatch.taskManage.service.Impl.newFileCreateTaskServiceImpl import NewFileCreateTaskServiceImpl
from mainJobBatch.taskManage.serviceBase.mdScrapingTaskService import MdScrapingTaskService


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

    def getTaskManageDataFlag(self, md_scraping_service):
        """
        新規ファイル作成バッチのプロセスステータスを取得する

        Parameters
        ----------
        md_scraping_service : NewFileCreateTaskServiceImpl
            新規ファイル作成バッチサービス

        Returns
        ----------
        task_manage_data_flag : str
            個別バッチタスクプロセスフラグ
        """

        super().getTaskManageDataFlag(md_scraping_service)
        try:
            md_scraping_service.taskManageRegister(self.new_create_task_id)
            task_manage_data_flag = md_scraping_service.getUserTaskStatus(self.new_create_task_id)
            return task_manage_data_flag
        except:
            raise

    def userStatusUpdateActive(self, md_scraping_service):
        """
        ユーザーバッチ処理ステータスをActiveに設定

        Parameters
        ----------
        md_scraping_service : NewFileCreateTaskServiceImpl
            新規ファイル作成バッチサービス
        """

        super().userStatusUpdateActive(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.new_create_task_id, self.process_active_id)
        except:
            raise

    def userStatusUpdateRest(self, md_scraping_service):
        """
        ユーザーバッチ処理ステータスをRest状態に設定

        Parameters
        ----------
        md_scraping_service : NewFileCreateTaskServiceImpl
            新規ファイル作成バッチサービス
        """

        super().userStatusUpdateRest(md_scraping_service)
        try:
            md_scraping_service.updateUserTaskStatus(self.new_create_task_id, self.process_rest_id)
        except:
            raise