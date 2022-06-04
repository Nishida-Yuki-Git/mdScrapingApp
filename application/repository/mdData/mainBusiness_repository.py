from abc import ABCMeta, abstractmethod

class MainBusinessRepository(metaclass=ABCMeta):
    """ 新規ファイル作成レポジトリインターフェース
    """

    @abstractmethod
    def jobQueRegister(self, saiban_job_num, user_id, result_file_num):
        """
        ジョブキュー登録実行

        Parameters
        ----------
        saiban_job_num : str
            ジョブ番号
        user_id : str
            ユーザーID
        result_file_num : str
            ファイル番号
        """

        pass

    @abstractmethod
    def jobParamRegister(self, saiban_job_num, serviceDto):
        """
        ジョブパラメータ登録実行

        Parameters
        ----------
        saiban_job_num : str
            ジョブ番号
        serviceDto : MainBusinessServiceDto
            メインビジネスサービスDTO
        """

        pass

    @abstractmethod
    def userProcessResultRegister(self, result_file_num, first_status_code, serviceDto):
        """
        ユーザー処理結果登録実行

        Parameters
        ----------
        result_file_num : str
            ファイル番号
        first_status_code : str
            ユーザー初期ステータス
        serviceDto : MainBusinessServiceDto
            メインビジネスサービスDTO
        """

        pass

    @abstractmethod
    def fileManageDataRegister(self, result_file_num, serviceDto):
        """
        ファイル管理データ登録実行

        Parameters
        ----------
        result_file_num : str
            ファイル番号
        serviceDto : MainBusinessServiceDto
            メインビジネスサービスDTO
        """

        pass
