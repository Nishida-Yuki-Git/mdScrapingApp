from application.repository.mdData.userInputItem_repository import UserInputItemGetRepository
from scrapingSystem.models import *

class UserInputItemGetRepositoryImple(UserInputItemGetRepository):
    """ 画面表示ユーザーデータ取得レポジトリインターフェース
    """

    def getYearManageMTModel(self):
        """
        気象データ収集対象年管理マスタモデル取得

        Returns
        ----------
        YearManageMT
            気象データ収集対象年管理マスタモデル
        """

        return YearManageMT

    def getYearManageMTObj(self):
        """
        気象データ収集対象年管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ収集対象年管理マスタ全レコード
        """

        return YearManageMT.objects.all()

    def getMonthManageMTModel(self):
        """
        気象データ収集対象月管理マスタモデル取得

        Returns
        ----------
        MonthManageMT
            気象データ収集対象月管理マスタモデル
        """

        return MonthManageMT

    def getMonthManageMTObj(self):
        """
        気象データ収集対象月管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ収集対象月管理マスタ全レコード
        """

        return MonthManageMT.objects.all()

    def getKenParamMTModel(self):
        """
        県管理マスタモデル取得

        Returns
        ----------
        KenParamMT
            県管理マスタモデル
        """

        return KenParamMT

    def getKenParamMTObj(self):
        """
        県管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            県管理マスタ全レコード
        """

        return KenParamMT.objects.all()

    def getMDItemMTModel(self):
        """
        気象データ項目名称管理マスタモデル取得

        Returns
        ----------
        MDItemMT
            気象データ項目名称管理マスタモデル
        """

        return MDItemMT

    def getMDItemMTObj(self):
        """
        気象データ項目名称管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ項目名称管理マスタ全レコード
        """

        return MDItemMT.objects.all()

    def getProcessResultDataModel(self):
        """
        ユーザー処理結果情報管理データモデル取得

        Returns
        ----------
        ProcessResultData
            ユーザー処理結果情報管理データモデル
        """

        return ProcessResultData

    def getProcessResultDataObj(self, user_id):
        return ProcessResultData.objects.filter(user_id=user_id)
















