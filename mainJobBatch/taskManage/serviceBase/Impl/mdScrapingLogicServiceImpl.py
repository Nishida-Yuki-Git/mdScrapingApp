import requests
from bs4 import BeautifulSoup
import re
import openpyxl
import calendar
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
import os
from logging import getLogger
from mainJobBatch.taskManage.serviceBase.mdScrapingLogicService import MeteorologicaldataScrapingService

##気象データ収集&ファイル作成ビジネスロジッククラス
class MeteorologicaldataScrapingServiceImpl(MeteorologicaldataScrapingService):
    def __init__(self, cur, file_num, md_scraping_dao, start_year, end_year, start_month, end_month, ken_name_list, ken_no_list, ken_block_list, md_url_list, md_item_list):
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

        self.temp_list = [] # 平均気温
        self.rh_list = [] # 相対湿度
        self.ab_hu_list = [] # 絶対湿度

        self.user_select_md_item_list = md_item_list

        self.end = None
        self.batch_setting = OnlineBatchSetting()
        self.logger = getLogger("OnlineBatchLog").getChild("logicService")

    def mainSoup(self): ##メイン処理
        ##ループ用の初期化
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
        self.logger.debug('県：'+self.ken_name_list[self.Ken_count]+' 年：'+str(self.start_year)+' 月：'+str(self.start_month))

    def __DateNumCount(self):
        self.day_num_list.append(calendar.monthrange(self.start_year, self.start_month)[1])

    def MDOutput(self):
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
        response = requests.get(self.main_clowling_url)
        response.encoding = response.apparent_encoding
        return response

    def __HtmlParser(self):
        bs = BeautifulSoup(self.__UrlRequest().text, 'html.parser')
        self.temp_datasets = bs.select('td.data_0_0') #気温
        self.rh_datasets = bs.select('td.data_0_0') # 相対湿度

    def __TempDataScraping(self):
        first_data = 0 # 欠損補完データ
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
        first_data = 0 # 欠損補完データ
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
        for (temp, rh) in zip(self.temp_list, self.rh_list):
            ab_hu = 217 * (6.1078 * (10 ** (7.5 * float(temp) / (float(temp) + 237.3)))) / (float(temp) + 273.15) * (int(rh) / 100)
            self.ab_hu_list.append(ab_hu)

    def __OutputData(self):
        for (temp, rh, ab_hu) in zip(self.temp_list, self.rh_list, self.ab_hu_list):
            self.temp_output_list.append(temp)
            self.rh_output_list.append(rh)
            self.ab_hu_output_list.append(ab_hu)

    def __YearMonthMethod(self):
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
        #実データリストの行列の入れ替え
        output_data_list = [list(x) for x in zip(*output)]

        xl_column_alphabet_list = [chr(ord("D")+i) for i in range(23)]
        data_write_column_list = [] #column名リスト
        for i in range(len(self.user_select_md_item_list)):
            data_write_column_list.append(xl_column_alphabet_list[i])

        #データ書き込みロジック
        init_count = 0 #最初のループでのみ使用する
        xl_count = 1 #セルカウント(リセットなし)
        ken_init_count = 0 #対象の県名ごとに1になる値
        ken_list_index = 0 #フィールドの「県」リストのインデックス番号リスト
        year_init_count = 0 #1の時に、年を書き込む
        write_year = int(self.start_year_init) #書き込み年
        write_month = int(self.start_month_init) #書き込み月
        write_day = 1 #書き込み日
        for output_data in output_data_list:
            init_count += 1
            ken_init_count += 1
            xl_count += 1
            year_init_count += 1

            #1行目に気象データ項目のカラム書き込み処理
            if init_count == 1:
                for (data_write_column, md_item_name) in zip(data_write_column_list, self.user_select_md_item_list):
                    sheet[data_write_column + "1"] = md_item_name

            #「県」の書き込み処理
            if ken_init_count == 1:
                sheet['A' + str(xl_count)] = self.ken_name_list[ken_list_index]

            #「年」の書き込み処理
            if year_init_count == 1:
                sheet['B' + str(xl_count)] = str(write_year)+'年'

            #「月」と「日」の書き込み処理
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

            #実データ書き込み処理
            for i in range(len(data_write_column_list)):
                sheet[data_write_column_list[i] + str(xl_count)] = output_data[i]






