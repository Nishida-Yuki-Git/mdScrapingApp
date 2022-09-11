import openpyxl
import os
import calendar
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
from mainJobBatch.taskManage.serviceBase.mdScrapingXlWriteService import MdScrapingXlWriteService

class MdScrapingXlWriteServiceImpl(MdScrapingXlWriteService):
    """
    気象データ中間コミット書き込みサービス基底クラス

    Attributes
    ----------
    wb : openpyxl.workbook.workbook.Workbook
        エクセルオブジェクト
    sheet : openpyxl.worksheet.worksheet.Worksheet
        エクセルシートオブジェクト
    batch_setting : OnlineBatchSetting
        オンライン随時バッチ設定クラスオブジェクト
    middle_save_path : str
        作成ファイル保存パス
    start_year_init : str
        収集開始初期年
    start_month_init : str
        収集開始初期月
    user_select_md_item_list : list
        画面上で選択された抽出対象気象データ項目リスト
    ken_name_list : list
        県名リスト
    end_month : str
        気象データ収集終了月
    end_year : str
        気象データ収集終了年
    init_count : int
        気象データ書き込み時初期動作用カウンター
    xl_count : int
        セル書き込み行数カウンター
    ken_init_count : int
        県名書き込み用カウンター
    ken_list_index : int
        県名取得用インデックス
    year_init_count : int
        年書き込み用カウンター
    write_year : int
        ファイル書き込み年
    write_month : int
        ファイル書き込み月
    write_day : int
        ファイル書き込み日
    """

    def __init__(self, cur, result_file_num, md_scraping_dao, start_year_init, start_month_init, user_select_md_item_list, ken_name_list, end_month, end_year):
        """
        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        result_file_num : str
            ファイル番号
        md_scraping_dao : MdScrapingDao
            気象データ収集バッチDaoインターフェース
        start_year_init : str
            収集開始初期年
        start_month_init : str
            収集開始初期月
        user_select_md_item_list : list
            画面上で選択された抽出対象気象データ項目リスト
        ken_name_list : list
            県名リスト
        end_month : str
            気象データ収集終了月
        end_year : str
            気象データ収集終了年
        """

        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.batch_setting = OnlineBatchSetting.get_instance()
        self.start_year_init = start_year_init
        self.start_month_init = start_month_init
        self.user_select_md_item_list = user_select_md_item_list
        self.ken_name_list = ken_name_list
        self.end_month = end_month
        self.end_year = end_year
        self.init_count = 0
        self.xl_count = 1
        self.ken_init_count = 0
        self.ken_list_index = 0
        self.year_init_count = 0
        self.write_year = int(self.start_year_init)
        self.write_month = int(self.start_month_init)
        self.write_day = 1

        change_cr_dir = self.batch_setting.getMediaRoot()
        os.chdir(change_cr_dir)
        file_path = self.batch_setting.getFileSaveDir()
        file_name = result_file_num + '.xlsx'
        self.middle_save_path = change_cr_dir + file_path + file_name

        self.sheet.title = 'sheet1'
        self.wb.save(self.middle_save_path)
        md_scraping_dao.registFilePath(cur, result_file_num, self.middle_save_path)


    def xlMiddleCommit(self, output_data):
        """
        気象データ中間コミット書き込み実装

        Parameters
        ----------
        outputData : list
            書き込み気象データ
        """

        self.wb = openpyxl.load_workbook(self.middle_save_path)
        self.sheet = self.wb['sheet1']


        output_data_list = [list(x) for x in zip(*output_data)]

        xl_column_alphabet_list = [chr(ord("D")+i) for i in range(23)]
        data_write_column_list = []
        for i in range(len(output_data_list[0])):
            data_write_column_list.append(xl_column_alphabet_list[i])

        for output_data in output_data_list:
            self.init_count += 1
            self.ken_init_count += 1
            self.xl_count += 1
            self.year_init_count += 1

            if self.init_count == 1:
                for (data_write_column, md_item_name) in zip(data_write_column_list, self.user_select_md_item_list):
                    self.sheet[data_write_column + "1"] = md_item_name

            if self.ken_init_count == 1:
                self.sheet['A' + str(self.xl_count)] = self.ken_name_list[self.ken_list_index]

            if self.year_init_count == 1:
                self.sheet['B' + str(self.xl_count)] = str(self.write_year)+'年'

            self.sheet['C' + str(self.xl_count)] = str(self.write_month)+'月'+str(self.write_day)+'日'
            self.write_day += 1
            if self.write_day == (int(calendar.monthrange(self.write_year, self.write_month)[1]) + 1):
                self.write_day = 1
                self.write_month += 1
                if self.write_month == (int(self.end_month) + 1):
                    self.write_month = int(self.start_month_init)
                    self.year_init_count = 0
                    self.write_year += 1
                    if self.write_year == (int(self.end_year) + 1):
                        self.write_year = int(self.start_year_init)
                        self.ken_init_count = 0
                        self.ken_list_index += 1

            for i in range(len(data_write_column_list)):
                self.sheet[data_write_column_list[i] + str(self.xl_count)] = output_data[i]


        self.wb.save(self.middle_save_path)
        output_data.clear()