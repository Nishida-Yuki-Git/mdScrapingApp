import requests
from bs4 import BeautifulSoup
import re
import openpyxl
import calendar
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
import os
from logging import getLogger
from mainJobBatch.taskManage.serviceBase.mdScrapingLogicService import MeteorologicaldataScrapingService


class MeteorologicaldataScrapingServiceImpl(MeteorologicaldataScrapingService):
    """
    気象データ収集&ファイル作成ビジネスサービスクラス

    Attributes
    ----------
    cur : MySQLdb.connections.Connection
        DBカーソル
    file_num : str
        ファイル番号
    md_scraping_dao : MdScrapingDao
        気象データ収集バッチDaoインターフェース
    start_year_init : str
        気象データ収集開始年(初期値)
    start_year : str
        気象データ収集開始年
    end_year : str
        気象データ収集終了年
    start_month_init : str
        気象データ収集開始月(初期値)
    start_month : str
        気象データ収集開始月
    end_month : str
        気象データ収集終了月
    day_num_list : list
        月ごとの日数リスト
    Ken_count : int
        県名リストインデックス
    ken_name_list : list
        県名リスト
    no_list : list
        県番号リスト
    block_list : list
        県ブロック番号リスト
    temp_output_list : list
        ファイル出力用気温リスト
    rh_output_list : list
        ファイル出力用相対湿度リスト
    ab_hu_output_list : list
        ファイル出力用絶対湿度リスト
    temp_datasets : list
        気象庁の1画面から抽出する全データ(気温解析用)
    rh_datasets : list
        気象庁の1画面から抽出する全データ(相対湿度解析用)
    main_clowling_url_list : list
        気象庁URLパーツリスト
    main_clowling_url : list
        組み立て後の気象庁URL
    temp_list : list
        抽出した気温データの退避リスト
    rh_list : list
        抽出した相対湿度データの退避リスト
    ab_hu_list : list
        抽出した絶対湿度データの退避リスト
    user_select_md_item_list : list
        画面上で選択された抽出対象気象データ項目リスト
    end : str
        ビジネスロジック処理終了サイン
    batch_setting : OnlineBatchSetting
        オンライン随時バッチ設定クラスオブジェクト
    logger : logging
        ログ出力オブジェクト
    """

    def __init__(self, cur, file_num, md_scraping_dao, start_year, end_year, start_month, end_month, ken_name_list, ken_no_list, ken_block_list, md_url_list, md_item_list):
        """
        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        file_num : list
            ファイル番号
        md_scraping_dao : MdScrapingDao
            気象データ収集バッチDaoインターフェース
        start_year : str
            気象データ収集開始年
        end_year : str
            気象データ収集終了年
        start_month : str
            気象データ収集開始月
        end_month : str
            気象データ収集終了月
        ken_name_list : list
            県名リスト
        ken_no_list : list
            県番号リスト
        ken_block_list : list
            県ブロック番号リスト
        md_url_list : list
            気象庁URLパーツリスト
        md_item_list : list
            画面上で選択された抽出対象気象データ項目リスト
        """

        self.cur = cur
        self.file_num = file_num
        self.md_scraping_dao = md_scraping_dao

        self.start_year_init = start_year
        self.start_year = start_year
        self.end_year = end_year
        self.start_month_init = start_month
        self.start_month = start_month
        self.end_month = end_month
        self.day_num_list = []
        self.Ken_count = 0

        self.ken_name_list = ken_name_list
        self.no_list = ken_no_list
        self.block_list = ken_block_list

        self.temp_output_list = []
        self.rh_output_list = []
        self.ab_hu_output_list = []

        self.temp_datasets = None
        self.rh_datasets = None

        self.main_clowling_url_list = md_url_list
        self.main_clowling_url = ''

        self.temp_list = []
        self.rh_list = []
        self.ab_hu_list = []

        self.user_select_md_item_list = md_item_list

        self.end = None
        self.batch_setting = OnlineBatchSetting()
        self.logger = getLogger("OnlineBatchLog").getChild("logicService")

    def mainSoup(self):
        """
        Webスクレイピング及びファイル出力処理

        Returns
        ----------
        end : str
            ビジネスロジック処理終了サイン
        """

        self.temp_datasets = None
        self.rh_datasets = None
        self.temp_list = []
        self.rh_list = []
        self.ab_hu_list = []

        try:
            self.__logBackPrint()
            self.__DateNumCount()
            self.__MdUrlCreate()
            self.__HtmlParser()
            self.__TempDataScraping()
            self.__RhDataScraping()
            self.__AbHumidCalc()
            self.__OutputData()
            self.__YearMonthMethod()

            return self.end
        except:
            raise

    def __logBackPrint(self):
        """ スクレイピング中の県、年、月、のログを出力
        """

        self.logger.debug('県：'+self.ken_name_list[self.Ken_count]+' 年：'+str(self.start_year)+' 月：'+str(self.start_month))

    def __DateNumCount(self):
        """ 対象の年・月の1ヶ月の日数を解析してフィールドに退避
        """

        self.day_num_list.append(calendar.monthrange(self.start_year, self.start_month)[1])

    def MDOutput(self):
        """ 気象データ収集後のファイル作成処理
        """

        try:
            output = []
            for md_item in self.user_select_md_item_list:
                if md_item == '気温':
                    output.append(self.temp_output_list)
                elif md_item == '相対湿度':
                    output.append(self.rh_output_list)
                elif md_item == '絶対湿度':
                    output.append(self.ab_hu_output_list)
                else:
                    pass
            self.__createXl(output)
        except:
            raise

    def __MdUrlCreate(self):
        """ 気象庁URLの組み立て処理
        """

        self.main_clowling_url = ''
        url_count = 0
        for url in self.main_clowling_url_list:
            if url_count == 0:
                self.main_clowling_url += url
            elif url_count == 1:
                self.main_clowling_url += str(self.no_list[self.Ken_count])
                self.main_clowling_url += url
            elif url_count == 2:
                self.main_clowling_url += str(self.block_list[self.Ken_count])
                self.main_clowling_url += url
            elif url_count == 3:
                self.main_clowling_url += str(self.start_year)
                self.main_clowling_url += url
            elif url_count == 4:
                self.main_clowling_url += str(self.start_month)
                self.main_clowling_url += url
            else:
                pass
            url_count += 1

    def __UrlRequest(self):
        """
        レスポンスHTMLの返却

        Returns
        ----------
        response : HttpRespose
            気象庁のResponseオブジェクト
        """

        response = requests.get(self.main_clowling_url)
        response.encoding = response.apparent_encoding
        return response

    def __HtmlParser(self):
        """ 気象庁HTMLの解析
        """

        bs = BeautifulSoup(self.__UrlRequest().text, 'html.parser')
        self.temp_datasets = bs.select('td.data_0_0')
        self.rh_datasets = bs.select('td.data_0_0')

    def __TempDataScraping(self):
        """ 気象データスクレイピング
        """

        first_data = 0
        first_count = 0
        count = 0
        for temp_data in self.temp_datasets:
            count += 1
            count -= 10
            if count == 0 or count % 18 == 0:
                temp = re.search('.*\d+.\d', temp_data.text)
                if temp is not None:
                    temp = temp.group()
                    first_count += 1
                    if first_count == 1:
                        first_data += float(temp)
                    else:
                        pass
                elif temp is None:
                    temp = first_data
                self.temp_list.append(temp)
            else:
                pass
            count += 10

    def __RhDataScraping(self):
        """ 相対湿度データスクレイピング
        """

        first_data = 0
        first_count = 0
        count = 0
        for rh_data in self.rh_datasets:
            count += 1
            count -= 16
            if count == 0 or count % 18 == 0 and rh_data is not None:
                rh = re.search('\d+', rh_data.text)
                if rh is not None:
                    rh = rh.group()
                    first_count += 1
                    if first_count == 1:
                        first_data += float(rh)
                    else:
                        pass
                elif rh is None:
                    rh = first_data
                self.rh_list.append(rh)
            else:
                pass
            count += 16

    def __AbHumidCalc(self):
        """ 絶対湿度の計算処理
        """

        for (temp, rh) in zip(self.temp_list, self.rh_list):
            ab_hu = 217 * (6.1078 * (10 ** (7.5 * float(temp) / (float(temp) + 237.3)))) / (float(temp) + 273.15) * (int(rh) / 100)
            self.ab_hu_list.append(ab_hu)

    def __OutputData(self):
        """ ファイル出力用データリストへの解析データの追加
        """

        for (temp, rh, ab_hu) in zip(self.temp_list, self.rh_list, self.ab_hu_list):
            self.temp_output_list.append(temp)
            self.rh_output_list.append(rh)
            self.ab_hu_output_list.append(ab_hu)

    def __YearMonthMethod(self):
        """ 年・月の制御メソッド
        """

        self.start_month += 1
        if self.Ken_count == (len(self.no_list) - 1) and self.start_year == self.end_year and self.start_month == (self.end_month + 1):
            self.end = '終了'
        elif self.start_year == self.end_year and self.start_month == (self.end_month + 1):
            self.Ken_count += 1
            self.start_year = self.start_year_init
            self.start_month = self.start_month_init
        elif self.start_month == (self.end_month + 1):
            self.start_year += 1
            self.start_month = self.start_month_init
        else:
            pass

    def __createXl(self, output):
        """
        エクセルファイル作成及びプロジェクトフォルダへのファイルオブジェクトの格納

        Parameters
        ----------
        output : list
            書き込みデータリスト
        """

        try:
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.title = 'sheet1'

            self.__xlWriting(output, sheet)

            change_cr_dir = self.batch_setting.getMediaRoot()
            os.chdir(change_cr_dir)
            file_path = self.batch_setting.getFileSaveDir()
            file_name = self.file_num + '.xlsx'
            middle_save_path = change_cr_dir + file_path + file_name
            wb.save(middle_save_path)

            self.md_scraping_dao.registFilePath(self.cur, self.file_num, middle_save_path)
        except:
            raise

    def __xlWriting(self, output, sheet):
        """
        気象データ書き込み処理

        Parameters
        ----------
        output : list
            書き込みデータリスト
        sheet : list
            アクティブシート
        """

        output_data_list = [list(x) for x in zip(*output)]

        xl_column_alphabet_list = [chr(ord("D")+i) for i in range(23)]
        data_write_column_list = []
        for i in range(len(self.user_select_md_item_list)):
            data_write_column_list.append(xl_column_alphabet_list[i])

        init_count = 0
        xl_count = 1
        ken_init_count = 0
        ken_list_index = 0
        year_init_count = 0
        write_year = int(self.start_year_init)
        write_month = int(self.start_month_init)
        write_day = 1
        for output_data in output_data_list:
            init_count += 1
            ken_init_count += 1
            xl_count += 1
            year_init_count += 1

            if init_count == 1:
                for (data_write_column, md_item_name) in zip(data_write_column_list, self.user_select_md_item_list):
                    sheet[data_write_column + "1"] = md_item_name

            if ken_init_count == 1:
                sheet['A' + str(xl_count)] = self.ken_name_list[ken_list_index]

            if year_init_count == 1:
                sheet['B' + str(xl_count)] = str(write_year)+'年'

            sheet['C' + str(xl_count)] = str(write_month)+'月'+str(write_day)+'日'
            write_day += 1
            if write_day == (int(calendar.monthrange(write_year, write_month)[1]) + 1):
                write_day = 1
                write_month += 1
                if write_month == (int(self.end_month) + 1):
                    write_month = int(self.start_month_init)
                    year_init_count = 0
                    write_year += 1
                    if write_year == (int(self.end_year) + 1):
                        write_year = int(self.start_year_init)
                        ken_init_count = 0
                        ken_list_index += 1

            for i in range(len(data_write_column_list)):
                sheet[data_write_column_list[i] + str(xl_count)] = output_data[i]






