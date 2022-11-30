import requests
from bs4 import BeautifulSoup
import re
import calendar
from logging import getLogger
from mainJobBatch.taskManage.serviceBase.mdScrapingLogicService import MeteorologicaldataScrapingService
from mainJobBatch.taskManage.exception.mdException import MdQueBizException
from mainJobBatch.taskManage.exception.exceptionUtils import ExceptionUtils
import os
from pathlib import Path
import time


class MeteorologicaldataScrapingServiceImpl(MeteorologicaldataScrapingService):
    """
    気象データ収集ビジネスサービス基底クラス

    Attributes
    ----------
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
    atmospheric_pressure_local_ave_output_list : list
        ファイル出力用気圧.現地.平均リスト
    pressure_sea_level_ave_output_list : list
        ファイル出力用気圧海面平均リスト
    total_precipitation_output_list : list
        ファイル出力用降水量合計リスト
    precipitation_up_to_one_hour_output_list : list
        ファイル出力用降水量最大1時間リスト
    precipitation_up_to_ten_min_output_list : list
        ファイル出力用降水量最大10分間リスト
    highest_temperature_output_list : list
        ファイル出力用最高気温リスト
    lowest_temperature_output_list : list
        ファイル出力用最低気温リスト
    min_relative_humidity_output_list : list
        ファイル出力用最小相対湿度リスト
    average_wind_speed_output_list : list
        ファイル出力用平均風速リスト
    maximum_wind_speed_output_list : list
        ファイル出力用最大風速リスト
    maximum_wind_direction_output_list : list
        ファイル出力用最大風向リスト
    maximum_instantaneous_wind_speed_output_list : list
        ファイル出力用最大瞬間風速リスト
    maximum_instantaneous_wind_direction_output_list : list
        ファイル出力用最大瞬間風向リスト
    sunshine_hours_output_list : list
        ファイル出力用日照時間リスト
    total_snowfall_output_list : list
        ファイル出力用合計降雪リスト
    deepest_snow_output_list : list
        ファイル出力用最深積雪リスト
    weather_forecast_noon_output_list : list
        ファイル出力用天気概況昼リスト
    weather_forecast_night_output_list : list
        ファイル出力用天気概況夜リスト
    temp_datasets : list
        気象庁の1画面から抽出する全データ(気温解析用)
    rh_datasets : list
        気象庁の1画面から抽出する全データ(相対湿度解析用)
    atmospheric_pressure_local_ave_output_datasets : list
        気象庁の1画面から抽出する全データ(気圧.現地.平均解析用)
    pressure_sea_level_ave_datasets : list
        気象庁の1画面から抽出する全データ(気圧海面平均解析用)
    total_precipitation_datasets : list
        気象庁の1画面から出力する全データ(降水量合計解析用)
    precipitation_up_to_one_hour_datasets : list
        気象庁の1画面から出力する全データ(降水量最大1時間解析用)
    precipitation_up_to_ten_min_datasets : list
        気象庁の1画面から出力する全データ(降水量最大10分間解析用)
    highest_temperature_datasets : list
        気象庁の1画面から出力する全データ(最高気温解析用)
    lowest_temperature_datasets : list
        気象庁の1画面から出力する全データ(最低気温解析用)
    min_relative_humidity_datasets : list
        気象庁の1画面から出力する全データ(最小相対湿度解析用)
    average_wind_speed_datasets : list
        気象庁の1画面から出力する全データ(平均風速解析用)
    maximum_wind_speed_datasets : list
        気象庁の1画面から出力する全データ(最大風速解析用)
    maximum_wind_direction_datasets : list
        気象庁の1画面から出力する全データ(最大風向解析用)
    maximum_instantaneous_wind_speed_datasets : list
        気象庁の1画面から出力する全データ(最大瞬間風速解析用)
    maximum_instantaneous_wind_direction_datasets : list
        気象庁の1画面から出力する全データ(最大瞬間風向解析用)
    sunshine_hours_datasets : list
        気象庁の1画面から出力する全データ(日照時間解析用)
    total_snowfall_datasets : list
        気象庁の1画面から出力する全データ(合計降雪解析用)
    deepest_snow_datasets : list
        気象庁の1画面から出力する全データ(最深積雪解析用)
    weather_forecast_noon_datasets : list
        気象庁の1画面から出力する全データ(天気概況昼解析用)
    weather_forecast_night_datasets : list
        気象庁の1画面から出力する全データ(天気概況夜解析用)
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
    atmospheric_pressure_local_ave_list : list
        抽出した気圧.現地.平均データの退避リスト
    pressure_sea_level_ave_list : list
        抽出した気圧海面平均データの退避リスト
    total_precipitation_list : list
        抽出した降水量合計データの退避リスト
    precipitation_up_to_one_hour_list : list
        抽出した降水量最大1時間データの退避リスト
    precipitation_up_to_ten_min_list : list
        抽出した降水量最大10分間データの退避リスト
    highest_temperature_list : list
        抽出した最高気温データの退避リスト
    lowest_temperature_list : list
        抽出した最低気温データの退避リスト
    min_relative_humidity_list : list
        抽出した最小相対湿度データの退避リスト
    average_wind_speed_list : list
        抽出した平均風速データの退避リスト
    maximum_wind_speed_list : list
        抽出した最大風速データの退避リスト
    maximum_wind_direction_list : list
        抽出した最大風向データの退避リスト
    maximum_instantaneous_wind_speed_list : list
        抽出した最大瞬間風速データの退避リスト
    maximum_instantaneous_wind_direction_list : list
        抽出した最大瞬間風向データの退避リスト
    sunshine_hours_list : list
        抽出した日照時間データの退避リスト
    total_snowfall_list : list
        抽出した合計降雪データの退避リスト
    deepest_snow_list : list
        抽出した最深積雪データの退避リスト
    weather_forecast_noon_list : list
        抽出した天気概況昼データの退避リスト
    weather_forecast_night_list : list
        抽出した天気概況夜データの退避リスト
    user_select_md_item_list : list
        画面上で選択された抽出対象気象データ項目リスト
    end : str
        ビジネスロジック処理終了サイン
    batch_setting : OnlineBatchSetting
        オンライン随時バッチ設定クラスオブジェクト
    logger : logging
        ログ出力オブジェクト
    result_file_num : str
        ファイル番号
    """

    def __init__(self, start_year, end_year, start_month, end_month, ken_name_list, ken_no_list, ken_block_list, md_url_list, md_item_list, result_file_num):
        """
        Parameters
        ----------
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
        result_file_num : str
            ファイル番号
        """

        self.start_year_init = start_year
        self.start_year = start_year
        self.end_year = end_year
        self.start_month_init = start_month
        self.start_month = start_month
        self.end_month = end_month
        self.Ken_count = 0

        self.ken_name_list = ken_name_list
        self.no_list = ken_no_list
        self.block_list = ken_block_list

        self.temp_output_list = []
        self.rh_output_list = []
        self.ab_hu_output_list = []
        self.atmospheric_pressure_local_ave_output_list = []
        self.pressure_sea_level_ave_output_list = []
        self.total_precipitation_output_list = []
        self.precipitation_up_to_one_hour_output_list = []
        self.precipitation_up_to_ten_min_output_list = []
        self.highest_temperature_output_list = []
        self.lowest_temperature_output_list = []
        self.min_relative_humidity_output_list = []
        self.average_wind_speed_output_list = []
        self.maximum_wind_speed_output_list = []
        self.maximum_wind_direction_output_list = []
        self.maximum_instantaneous_wind_speed_output_list = []
        self.maximum_instantaneous_wind_direction_output_list = []
        self.sunshine_hours_output_list = []
        self.total_snowfall_output_list = []
        self.deepest_snow_output_list = []
        self.weather_forecast_noon_output_list = []
        self.weather_forecast_night_output_list = []

        self.temp_datasets = None
        self.rh_datasets = None
        self.atmospheric_pressure_local_ave_datasets = None
        self.pressure_sea_level_ave_datasets = None
        self.total_precipitation_datasets = None
        self.precipitation_up_to_one_hour_datasets = None
        self.precipitation_up_to_ten_min_datasets = None
        self.highest_temperature_datasets = None
        self.lowest_temperature_datasets = None
        self.min_relative_humidity_datasets = None
        self.average_wind_speed_datasets = None
        self.maximum_wind_speed_datasets = None
        self.maximum_wind_direction_datasets = None
        self.maximum_instantaneous_wind_speed_datasets = None
        self.maximum_instantaneous_wind_direction_datasets = None
        self.sunshine_hours_datasets = None
        self.total_snowfall_datasets = None
        self.deepest_snow_datasets = None
        self.weather_forecast_noon_datasets = None
        self.weather_forecast_night_datasets = None

        self.main_clowling_url_list = md_url_list
        self.main_clowling_url = ''

        self.temp_list = []
        self.rh_list = []
        self.ab_hu_list = []
        self.atmospheric_pressure_local_ave_list = []
        self.pressure_sea_level_ave_list = []
        self.total_precipitation_list = []
        self.precipitation_up_to_one_hour_list = []
        self.precipitation_up_to_ten_min_list = []
        self.highest_temperature_list = []
        self.lowest_temperature_list = []
        self.min_relative_humidity_list = []
        self.average_wind_speed_list = []
        self.maximum_wind_speed_list = []
        self.maximum_wind_direction_list = []
        self.maximum_instantaneous_wind_speed_list = []
        self.maximum_instantaneous_wind_direction_list = []
        self.sunshine_hours_list = []
        self.total_snowfall_list = []
        self.deepest_snow_list = []
        self.weather_forecast_noon_list = []
        self.weather_forecast_night_list = []

        self.user_select_md_item_list = md_item_list

        self.end = None
        self.logger = getLogger("OnlineBatchLog").getChild("logicService")

        self.result_file_num = result_file_num

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
        self.atmospheric_pressure_local_ave_datasets = None
        self.pressure_sea_level_ave_datasets = None
        self.total_precipitation_datasets = None
        self.precipitation_up_to_one_hour_datasets = None
        self.precipitation_up_to_ten_min_datasets = None
        self.highest_temperature_datasets = None
        self.lowest_temperature_datasets = None
        self.min_relative_humidity_datasets = None
        self.average_wind_speed_datasets = None
        self.maximum_wind_speed_datasets = None
        self.maximum_wind_direction_datasets = None
        self.maximum_instantaneous_wind_speed_datasets = None
        self.maximum_instantaneous_wind_direction_datasets = None
        self.sunshine_hours_datasets = None
        self.total_snowfall_datasets = None
        self.deepest_snow_datasets = None
        self.weather_forecast_noon_datasets = None
        self.weather_forecast_night_datasets = None
        self.temp_list = []
        self.rh_list = []
        self.ab_hu_list = []
        self.atmospheric_pressure_local_ave_list = []
        self.pressure_sea_level_ave_list = []
        self.total_precipitation_list = []
        self.precipitation_up_to_one_hour_list = []
        self.precipitation_up_to_ten_min_list = []
        self.highest_temperature_list = []
        self.lowest_temperature_list = []
        self.min_relative_humidity_list = []
        self.average_wind_speed_list = []
        self.maximum_wind_speed_list = []
        self.maximum_wind_direction_list = []
        self.maximum_instantaneous_wind_speed_list = []
        self.maximum_instantaneous_wind_direction_list = []
        self.sunshine_hours_list = []
        self.total_snowfall_list = []
        self.deepest_snow_list = []
        self.weather_forecast_noon_list = []
        self.weather_forecast_night_list = []

        try:
            self.__logBackPrint()
            self.__MdUrlCreate()
            self.__HtmlParser()
            self.__TempDataScraping()
            self.__RhDataScraping()
            self.__AtmosphericPressureLocalAveScraping()
            self.__PressureSeaLevelAveScraping()
            self.__TotalPrecipitationScraping()
            self.__PrecipitationUpToOneHourScraping()
            self.__PrecipitationUpToTenMinScraping()
            self.__HighestTemperatureScraping()
            self.__LowestTemperatureScraping()
            self.__MinRelativeHumidityScraping()
            self.__AverageWindSpeedScraping()
            self.__MaximumWindSpeedScraping()
            self.__MaximumWindDirectionScraping()
            self.__MaximumInstantaneousWindSpeedScraping()
            self.__MaximumInstantaneousWindDirectionScraping()
            self.__SunshineHoursScraping()
            self.__TotalSnowfallScraping()
            self.__DeepestSnowScraping()
            self.__WeatherForecastNoonScraping()
            self.__WeatherForecastNightScraping()
            self.__AbHumidCalc()
            self.__OutputData()
            self.__YearMonthMethod()
            self.__scrapingProgressCommit()
            return self.end
        except MdQueBizException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '2')
            raise ex

    def __logBackPrint(self):
        """ スクレイピング中の県、年、月、のログを出力
        """

        self.logger.debug('県：'+self.ken_name_list[self.Ken_count]+' 年：'+str(self.start_year)+' 月：'+str(self.start_month))

    def MDOutput(self):
        """ ファイル作成用データの返却
        """

        try:
            output = []
            for md_item in self.user_select_md_item_list:
                if md_item == '平均気温(C)':
                    output.append(self.temp_output_list)
                elif md_item == '平均相対湿度(％)':
                    output.append(self.rh_output_list)
                elif md_item == '絶対湿度(g)':
                    output.append(self.ab_hu_output_list)
                elif md_item == '気圧現地平均(hPa)':
                    output.append(self.atmospheric_pressure_local_ave_output_list)
                elif md_item == '気圧海面平均(hPa)':
                    output.append(self.pressure_sea_level_ave_output_list)
                elif md_item == '降水量合計(mm)':
                    output.append(self.total_precipitation_output_list)
                elif md_item == '降水量最大1時間(mm)':
                    output.append(self.precipitation_up_to_one_hour_output_list)
                elif md_item == '降水量最大10分間(mm)':
                    output.append(self.precipitation_up_to_ten_min_output_list)
                elif md_item == '最高気温(C)':
                    output.append(self.highest_temperature_output_list)
                elif md_item == '最低気温(C)':
                    output.append(self.lowest_temperature_output_list)
                elif md_item == '最小相対湿度(%)':
                    output.append(self.min_relative_humidity_output_list)
                elif md_item == '平均風速(m/s)':
                    output.append(self.average_wind_speed_output_list)
                elif md_item == '最大風速(m/s)':
                    output.append(self.maximum_wind_speed_output_list)
                elif md_item == '最大風向':
                    output.append(self.maximum_wind_direction_output_list)
                elif md_item == '最大瞬間風速(m/s)':
                    output.append(self.maximum_instantaneous_wind_speed_output_list)
                elif md_item == '最大瞬間風向':
                    output.append(self.maximum_instantaneous_wind_direction_output_list)
                elif md_item == '日照時間(h)':
                    output.append(self.sunshine_hours_output_list)
                elif md_item == '合計降雪(cm)':
                    output.append(self.total_snowfall_output_list)
                elif md_item == '最深積雪(cm)':
                    output.append(self.deepest_snow_output_list)
                elif md_item == '天気概況昼(06:00-18:00)':
                    output.append(self.weather_forecast_noon_output_list)
                elif md_item == '天気概況夜(18:00-翌日06:00)':
                    output.append(self.weather_forecast_night_output_list)
                else:
                    pass
            return output
        except MdQueBizException as ex:
            raise
        except Exception as ex:
            ex_util = ExceptionUtils.get_instance()
            ex = ex_util.commonHandling(ex, '2')
            raise ex

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
        self.atmospheric_pressure_local_ave_datasets = bs.select('td.data_0_0')
        self.pressure_sea_level_ave_datasets = bs.select('td.data_0_0')
        self.total_precipitation_datasets = bs.select('td.data_0_0')
        self.precipitation_up_to_one_hour_datasets = bs.select('td.data_0_0')
        self.precipitation_up_to_ten_min_datasets = bs.select('td.data_0_0')
        self.highest_temperature_datasets = bs.select('td.data_0_0')
        self.lowest_temperature_datasets = bs.select('td.data_0_0')
        self.min_relative_humidity_datasets = bs.select('td.data_0_0')
        self.average_wind_speed_datasets = bs.select('td.data_0_0')
        self.maximum_wind_speed_datasets = bs.select('td.data_0_0')
        self.maximum_wind_direction_datasets = bs.select('td.data_0_0')
        self.maximum_instantaneous_wind_speed_datasets = bs.select('td.data_0_0')
        self.maximum_instantaneous_wind_direction_datasets = bs.select('td.data_0_0')
        self.sunshine_hours_datasets = bs.select('td.data_0_0')
        self.total_snowfall_datasets = bs.select('td.data_0_0')
        self.deepest_snow_datasets = bs.select('td.data_0_0')
        self.weather_forecast_noon_datasets = bs.select('td.data_0_0')
        self.weather_forecast_night_datasets = bs.select('td.data_0_0')

    def __TempDataScraping(self):
        """ 気温データスクレイピング
        """

        first_data = 0
        first_count = 0
        count = 0
        test_count = 0
        for temp_data in self.temp_datasets:
            test = re.search('.*\d+.\d', temp_data.text)
            if test is not None and test.group == '8.6':
                print(temp_data)
                print(test_count)
            test_count += 1
            time.sleep(1)
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

    def __AtmosphericPressureLocalAveScraping(self):
        """ 気圧.現地.平均データスクレイピング
        """

        count = 0
        for atmospheric_pressure_local_ave_data in self.atmospheric_pressure_local_ave_datasets:
            count += 1
            count -= 19
            if count == 0 or count % 18 == 0:
                data = re.search('.*', atmospheric_pressure_local_ave_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.atmospheric_pressure_local_ave_list.append(data)
            else:
                pass
            count += 19

    def __PressureSeaLevelAveScraping(self):
        """ 気圧海面平均データスクレイピング
        """

        count = 0
        for pressure_sea_level_ave_data in self.pressure_sea_level_ave_datasets:
            count += 1
            count -= 20
            if count == 0 or count % 18 == 0:
                data = re.search('.*', pressure_sea_level_ave_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.pressure_sea_level_ave_list.append(data)
            else:
                pass
            count += 20

    def __TotalPrecipitationScraping(self):
        """ 降水量合計データスクレイピング
        """

        count = 0
        for total_precipitation_data in self.total_precipitation_datasets:
            count += 1
            count -= 5
            if count == 0 or count % 18 == 0:
                data = re.search('.*', total_precipitation_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.total_precipitation_list.append(data)
            else:
                pass
            count += 5

    def __PrecipitationUpToOneHourScraping(self):
        """ 降水量最大1時間データスクレイピング
        """

        count = 0
        for precipitation_up_to_one_hour_data in self.precipitation_up_to_one_hour_datasets:
            count += 1
            count -= 6
            if count == 0 or count % 18 == 0:
                data = re.search('.*', precipitation_up_to_one_hour_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.precipitation_up_to_one_hour_list.append(data)
            else:
                pass
            count += 6

    def __PrecipitationUpToTenMinScraping(self):
        """ 降水量最大10分間データスクレイピング
        """

        count = 0
        for precipitation_up_to_ten_min_data in self.precipitation_up_to_ten_min_datasets:
            count += 1
            count -= 8
            if count == 0 or count % 18 == 0:
                data = re.search('.*', precipitation_up_to_ten_min_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.precipitation_up_to_ten_min_list.append(data)
            else:
                pass
            count += 8

    def __HighestTemperatureScraping(self):
        """ 最高気温データスクレイピング
        """

        count = 0
        for highest_temperature_data in self.highest_temperature_datasets:
            count += 1
            count -= 11
            if count == 0 or count % 18 == 0:
                data = re.search('.*', highest_temperature_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.highest_temperature_list.append(data)
            else:
                pass
            count += 11

    def __LowestTemperatureScraping(self):
        """ 最低気温データスクレイピング
        """

        count = 0
        for lowest_temperature_data in self.lowest_temperature_datasets:
            count += 1
            count -= 13
            if count == 0 or count % 18 == 0:
                data = re.search('.*', lowest_temperature_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.lowest_temperature_list.append(data)
            else:
                pass
            count += 13

    def __MinRelativeHumidityScraping(self):
        """ 最小相対湿度データスクレイピング
        """

        count = 0
        for min_relative_humidity_data in self.min_relative_humidity_datasets:
            count += 1
            count -= 17
            if count == 0 or count % 18 == 0:
                data = re.search('.*', min_relative_humidity_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.min_relative_humidity_list.append(data)
            else:
                pass
            count += 17

    def __AverageWindSpeedScraping(self):
        """ 平均風速データスクレイピング
        """

        count = 0
        for average_wind_speed_data in self.average_wind_speed_datasets:
            count += 1
            count -= 16
            if count == 0 or count % 18 == 0:
                data = re.search('.*', average_wind_speed_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.average_wind_speed_list.append(data)
            else:
                pass
            count += 16

    def __MaximumWindSpeedScraping(self):
        """ 最大風速データスクレイピング
        """

        count = 0
        for maximum_wind_speed_data in self.maximum_wind_speed_datasets:
            count += 1
            count -= 22
            if count == 0 or count % 18 == 0:
                data = re.search('.*', maximum_wind_speed_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.maximum_wind_speed_list.append(data)
            else:
                pass
            count += 22

    def __MaximumWindDirectionScraping(self):
        """ 最大風向データスクレイピング
        """

        count = 0
        for maximum_wind_direction_data in self.maximum_wind_direction_datasets:
            count += 1
            count -= 23
            if count == 0 or count % 18 == 0:
                data = re.search('.*', maximum_wind_direction_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.maximum_wind_direction_list.append(data)
            else:
                pass
            count += 23

    def __MaximumInstantaneousWindSpeedScraping(self):
        """ 最大瞬間風速データスクレイピング
        """

        count = 0
        for maximum_instantaneous_wind_speed_data in self.maximum_instantaneous_wind_speed_datasets:
            count += 1
            count -= 24
            if count == 0 or count % 18 == 0:
                data = re.search('.*', maximum_instantaneous_wind_speed_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.maximum_instantaneous_wind_speed_list.append(data)
            else:
                pass
            count += 24

    def __MaximumInstantaneousWindDirectionScraping(self):
        """ 最大瞬間風向データスクレイピング
        """

        count = 0
        for maximum_instantaneous_wind_direction_data in self.maximum_instantaneous_wind_direction_datasets:
            count += 1
            count -= 25
            if count == 0 or count % 18 == 0:
                data = re.search('.*', maximum_instantaneous_wind_direction_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.maximum_instantaneous_wind_direction_list.append(data)
            else:
                pass
            count += 25

    def __SunshineHoursScraping(self):
        """ 日照時間データスクレイピング
        """

        count = 0
        for sunshine_hours_data in self.sunshine_hours_datasets:
            count += 1
            count -= 26
            if count == 0 or count % 18 == 0:
                data = re.search('.*', sunshine_hours_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.sunshine_hours_list.append(data)
            else:
                pass
            count += 26

    def __TotalSnowfallScraping(self):
        """ 合計降雪データスクレイピング
        """

        count = 0
        for total_snowfall_data in self.total_snowfall_datasets:
            count += 1
            count -= 27
            if count == 0 or count % 18 == 0:
                data = re.search('.*', total_snowfall_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.total_snowfall_list.append(data)
            else:
                pass
            count += 27

    def __DeepestSnowScraping(self):
        """ 最深積雪データスクレイピング
        """

        count = 0
        for deepest_snow_data in self.deepest_snow_datasets:
            count += 1
            count -= 28
            if count == 0 or count % 18 == 0:
                data = re.search('.*', deepest_snow_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.deepest_snow_list.append(data)
            else:
                pass
            count += 28

    def __WeatherForecastNoonScraping(self):
        """ 天気概況昼データスクレイピング
        """

        count = 0
        for weather_forecast_noon_data in self.weather_forecast_noon_datasets:
            count += 1
            count -= 29
            if count == 0 or count % 18 == 0:
                data = re.search('.*', weather_forecast_noon_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.weather_forecast_noon_list.append(data)
            else:
                pass
            count += 29

    def __WeatherForecastNightScraping(self):
        """ 天気概況夜データスクレイピング
        """

        count = 0
        for weather_forecast_night_data in self.weather_forecast_night_datasets:
            count += 1
            count -= 30
            if count == 0 or count % 18 == 0:
                data = re.search('.*', weather_forecast_night_data.text)
                if data is not None:
                    data = data.group()
                elif data is None:
                    data = '-'
                self.weather_forecast_night_list.append(data)
            else:
                pass
            count += 30

    def __AbHumidCalc(self):
        """ 絶対湿度の計算処理
        """

        for (temp, rh) in zip(self.temp_list, self.rh_list):
            ab_hu = 217 * (6.1078 * (10 ** (7.5 * float(temp) / (float(temp) + 237.3)))) / (float(temp) + 273.15) * (int(rh) / 100)
            self.ab_hu_list.append(ab_hu)

    def __OutputData(self):
        """ ファイル出力用データリストへの解析データの追加
        """

        for temp in self.temp_list:
            self.temp_output_list.append(temp)
        for rh in self.rh_list:
            self.rh_output_list.append(rh)
        for ab_hu in self.ab_hu_list:
            self.ab_hu_output_list.append(ab_hu)
        for atmospheric_pressure_local_ave in self.atmospheric_pressure_local_ave_list:
            self.atmospheric_pressure_local_ave_output_list.append(atmospheric_pressure_local_ave)
        for pressure_sea_level_ave in self.pressure_sea_level_ave_list:
            self.pressure_sea_level_ave_output_list.append(pressure_sea_level_ave)
        for total_precipitation in self.total_precipitation_list:
            self.total_precipitation_output_list.append(total_precipitation)
        for precipitation_up_to_one_hour in self.precipitation_up_to_one_hour_list:
            self.precipitation_up_to_one_hour_output_list.append(precipitation_up_to_one_hour)
        for precipitation_up_to_ten_min in self.precipitation_up_to_ten_min_list:
            self.precipitation_up_to_ten_min_output_list.append(precipitation_up_to_ten_min)
        for highest_temperature in self.highest_temperature_list:
            self.highest_temperature_output_list.append(highest_temperature)
        for lowest_temperature in self.lowest_temperature_list:
            self.lowest_temperature_output_list.append(lowest_temperature)
        for min_relative_humidity in self.min_relative_humidity_list:
            self.min_relative_humidity_output_list.append(min_relative_humidity)
        for average_wind_speed in self.average_wind_speed_list:
            self.average_wind_speed_output_list.append(average_wind_speed)
        for maximum_wind_speed in self.maximum_wind_speed_list:
            self.maximum_wind_speed_output_list.append(maximum_wind_speed)
        for maximum_wind_direction in self.maximum_wind_direction_list:
            self.maximum_wind_direction_output_list.append(maximum_wind_direction)
        for maximum_instantaneous_wind_speed in self.maximum_instantaneous_wind_speed_list:
            self.maximum_instantaneous_wind_speed_output_list.append(maximum_instantaneous_wind_speed)
        for maximum_instantaneous_wind_direction in self.maximum_instantaneous_wind_direction_list:
            self.maximum_instantaneous_wind_direction_output_list.append(maximum_instantaneous_wind_direction)
        for sunshine_hours in self.sunshine_hours_list:
            self.sunshine_hours_output_list.append(sunshine_hours)
        for total_snowfall in self.total_snowfall_list:
            self.total_snowfall_output_list.append(total_snowfall)
        for deepest_snow in self.deepest_snow_list:
            self.deepest_snow_output_list.append(deepest_snow)
        for weather_forecast_noon in self.weather_forecast_noon_list:
            self.weather_forecast_noon_output_list.append(weather_forecast_noon)
        for weather_forecast_night in self.weather_forecast_night_list:
            self.weather_forecast_night_output_list.append(weather_forecast_night)

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

    def __scrapingProgressCommit(self):
        """ スクレイピング進捗率書き込み
        """

        progress_file_path = os.path.join(Path(__file__).resolve().parent.parent.parent.parent.parent, 'media')+'/file/'+self.result_file_num+'_tmp.txt'
        try:
            progress_file_read = open(progress_file_path, 'r')
            last_progress = 0
            for num in progress_file_read.readlines():
                last_progress = int(num)
            progress_file_read.close()
            progress_file_write = open(progress_file_path, 'w')
            progress_file_write.write(str(last_progress+1))
            progress_file_write.close()
        except FileNotFoundError:
            progress_file_write = open(progress_file_path, 'w')
            progress_file_write.write('1')
            progress_file_write.close()