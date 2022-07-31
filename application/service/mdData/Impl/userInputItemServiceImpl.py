from application.repository.mdData.userInputItem_repository import UserInputItemGetRepository
from scrapingSystem.repositoryImple.mdData.userInputItem_repository import UserInputItemGetRepositoryImple
from application.service.mdData.userInputItemService import UserInputItemGetService

class UserInputItemGetServiceImpl(UserInputItemGetService):
    """
    画面表示ユーザーデータ取得サービス実装クラス

    Attributes
    ----------
    user_inpuit_item_get_repo : UserInputItemGetRepository
        画面表示ユーザーデータ取得レポジトリインターフェース
    user_id : str
        ユーザーID
    """

    def __init__(self, user_id='null_user'):
        """
        Parameters
        ----------
        userid : str
            ユーザーID
        """

        self.user_input_item_get_repo : UserInputItemGetRepository = UserInputItemGetRepositoryImple()
        self.user_id = user_id

    def getYearManageMTModel(self):
        """
        気象データ収集対象年管理マスタモデル取得

        Returns
        ----------
        YearManageMT
            気象データ収集対象年管理マスタモデル
        """

        try:
            return self.user_input_item_get_repo.getYearManageMTModel()
        except:
            raise

    def getYearManageMTObj(self):
        """
        気象データ収集対象年管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ収集対象年管理マスタ全レコード
        """

        try:
            year_list = self.user_input_item_get_repo.getYearManageMTObj()
            year_list = sorted(year_list, reverse=True)
            return year_list
        except:
            raise

    def getMonthManageMTModel(self):
        """
        気象データ収集対象月管理マスタモデル取得

        Returns
        ----------
        MonthManageMT
            気象データ収集対象月管理マスタモデル
        """

        try:
            return self.user_input_item_get_repo.getMonthManageMTModel()
        except:
            raise

    def getMonthManageMTObj(self):
        """
        気象データ収集対象月管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ収集対象月管理マスタ全レコード
        """

        try:
            return self.user_input_item_get_repo.getMonthManageMTObj()
        except:
            raise

    def getKenParamMTModel(self):
        """
        県管理マスタモデル取得

        Returns
        ----------
        KenParamMT
            県管理マスタモデル
        """

        try:
            return self.user_input_item_get_repo.getKenParamMTModel()
        except:
            raise

    def getKenParamMTObj(self):
        """
        県管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            県管理マスタ全レコード
        """

        try:
            return self.user_input_item_get_repo.getKenParamMTObj()
        except:
            raise

    def getMDItemMTModel(self):
        """
        気象データ項目名称管理マスタモデル取得

        Returns
        ----------
        MDItemMT
            気象データ項目名称管理マスタモデル
        """

        try:
            return self.user_input_item_get_repo.getMDItemMTModel()
        except:
            raise

    def getMDItemMTObj(self):
        """
        気象データ項目名称管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ項目名称管理マスタ全レコード
        """

        try:
            return self.user_input_item_get_repo.getMDItemMTObj()
        except:
            raise

    def getProcessResultDataModel(self):
        """
        ユーザー処理結果情報管理データモデル取得

        Returns
        ----------
        ProcessResultData
            ユーザー処理結果情報管理データモデル
        """

        try:
            return self.user_input_item_get_repo.getProcessResultDataModel()
        except:
            raise

    def getProcessResultDataObj(self):
        """
        ユーザー処理結果情報管理データ全レコードセット取得

        Returns
        ----------
        dict
            ユーザー処理結果情報管理データ全レコード
        """

        try:
            return self.user_input_item_get_repo.getProcessResultDataObj(self.user_id)
        except:
            raise






