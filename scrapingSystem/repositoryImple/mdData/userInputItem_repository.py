from application.repository.mdData.userInputItem_repository import UserInputItemGetRepository
from scrapingSystem.models import *
import os
from pathlib import Path

class UserInputItemGetRepositoryImple(UserInputItemGetRepository):
    """ 画面表示ユーザーデータ取得レポジトリインターフェース
    Attribute
    ----------
    target_file_status_const_process : str
        ファイル作成済みステータス文字列コンスト
    target_file_status_const_end : str
        ファイル作成済みステータス文字列コンスト
    kiro_byte_str : str
        キロバイトコンスト
    rate_str : str
        パーセントコンスト
    sintyokuritsu_str : str
        「進捗率」コンスト
    init_file_size : int
        初期エクセルファイルサイズ(中身なしの状態)
    md_one_item_byte : int
        気象データ１項目時の1回のデータ取得バイト数
    md_two_item_byte : int
        気象データ2項目時の1回のデータ取得バイト数
    md_three_item_byte : int
        気象データ3項目時の1回のデータ取得バイト数
    """
    def __init__(self):
        self.target_file_status_const_process = '作成中'
        self.target_file_status_const_end = '済'
        self.kiro_byte_str = 'KB'
        self.rate_str = '%'
        self.sintyokuritsu_str = '進捗率'
        self.init_file_size = 8058
        self.md_one_item_byte = 2463
        self.md_two_item_byte = 3160
        self.md_three_item_byte = 5152

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
        ユーザー処理結果情報管理データ全レコードセット取得&画面項目処理

        Returns
        ----------
        dict
            ユーザー処理結果情報管理データ全レコード
        """
        process_result_list = ProcessResultData.objects.order_by('result_file_num').reverse().filter(user_id=user_id)

        change_cr_dir = os.path.join(Path(__file__).resolve().parent.parent, 'media')
        os.chdir(change_cr_dir)

        for process_result in process_result_list:
            file_status = process_result.file_create_status
            result_file_num = process_result.result_file_num

            middle_save_path = change_cr_dir + '/file/' + result_file_num + '.xlsx'

            if file_status == self.target_file_status_const_end:
                kiro_byte_num = '{:.1f}'.format(os.path.getsize(middle_save_path)/1000)
                process_result.file_create_status = self.target_file_status_const_end+' ('+str(kiro_byte_num)+' '+self.kiro_byte_str+')'
            elif file_status == self.target_file_status_const_process:
                now_file_size = 0
                change_cr_dir = os.path.join(Path(__file__).resolve().parent.parent, 'media')
                os.chdir(change_cr_dir)
                file_path = '/file/'
                file_name = result_file_num + '.xlsx'
                middle_save_path = change_cr_dir + file_path + file_name
                try:
                    now_file_size = os.path.getsize(middle_save_path)
                except FileNotFoundError:
                    continue

                process_result_detail_list = ProcessResultDetailData.objects.filter(result_file_num=result_file_num)
                ken_item_count = len(process_result_detail_list)
                md_item_count = 0
                for process_result_detail in process_result_detail_list:
                    if process_result_detail.target_md_item != ('' or None):
                        md_item_count += 1
                    if md_item_count==3:
                        break

                target_start_year = process_result.target_start_year
                target_end_year = process_result.target_end_year
                target_start_month = process_result.target_start_month
                target_end_month = process_result.target_end_month
                year_month_ken_calc = (target_end_year-target_start_year)*(target_end_month-target_start_month)*ken_item_count
                now_byte = now_file_size-self.init_file_size
                about_last_size = 0
                if md_item_count==1:
                    about_last_size = (year_month_ken_calc*self.md_one_item_byte)-self.init_file_size
                elif md_item_count==2:
                    about_last_size = (year_month_ken_calc*self.md_two_item_byte)-self.init_file_size
                elif md_item_count==3:
                    about_last_size = (year_month_ken_calc*self.md_three_item_byte)-self.init_file_size
                else:
                    continue
                process_result.file_create_status = self.target_file_status_const_process+' ('+self.sintyokuritsu_str+str(
                    (now_byte/about_last_size)*100)+self.rate_str+')'

        return process_result_list
