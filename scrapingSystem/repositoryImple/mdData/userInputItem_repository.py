from application.repository.mdData.userInputItem_repository import UserInputItemGetRepository
from scrapingSystem.models import *

class UserInputItemGetRepositoryImple(UserInputItemGetRepository):
    """ 画面表示ユーザーデータ取得レポジトリインターフェース
    Attribute
    ----------
    target_file_status_const : str
        ファイル作成済みステータス文字列コンスト
    kiro_byte_str : str
        キロバイトコンスト
    """
    def __init__(self):
        self.target_file_status_const = '済'
        self.kiro_byte_str = 'KB'

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

        return YearManageMT.objects.order_by('year_param').reverse().all()

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
        """
        ユーザー処理結果情報管理データ全レコードセット取得

        Returns
        ----------
        dict
            ユーザー処理結果情報管理データ全レコード
        """
        process_result_list = ProcessResultData.objects.order_by('result_file_num').reverse().filter(user_id=user_id)
        for process_result in process_result_list:
            if process_result.file_create_status == self.target_file_status_const:
                user_file_obj = FileManageData.objects.get(
                    result_file_num = process_result.result_file_num)
                user_file = user_file_obj.create_file.name
                with open(user_file, "rb") as f:
                    xl_byte_data = f.read()
                kiro_byte_num = '{:.1f}'.format(len(xl_byte_data)/1000)
                process_result.file_create_status = self.target_file_status_const+' ('+str(kiro_byte_num)+' '+self.kiro_byte_str+')'
        return process_result_list
















