from scrapingSystem.models import *
from django.core.management.base import BaseCommand
import datetime
from django.db import connection

class Command(BaseCommand):
    """ マスタ設定及びトラン初期化オフラインバッチ
    """

    def handle(self, *args, **options):
        print("task-start")

        YearManageMT.objects.all().delete()
        start_year = 1945
        today = datetime.date.today()
        year_list = []
        for i in range(start_year, today.year+1):
            year_list.append(i)
        for year in year_list:
            year_obj = YearManageMT(
                year_param=year)
            year_obj.save()

        MonthManageMT.objects.all().delete()
        month_list = [i + 1 for i in range(12)]
        for month in month_list:
            month_obj = MonthManageMT(
                month_param=month)
            month_obj.save()

        KenParamMT.objects.all().delete()
        Ken_name_list = ['北海道', '青森', '秋田', '岩手', '山形', '宮城', '福島', '新潟', '茨城', '千葉', '栃木', '群馬', '東京', '神奈川', '山梨', '長野', '静岡', '富山', '岐阜', '石川', '愛知', '三重', '京都', '奈良', '大阪', '和歌山', '兵庫', '鳥取', '岡山', '香川', '徳島', '島根', '広島', '高知', '愛媛', '山口', '大分', '宮崎', '熊本', '佐賀', '長崎', '鹿児島', '沖縄', '埼玉', '福井', '滋賀', '福岡']
        no_list = [14, 31, 32, 33, 35, 34, 36, 54, 40, 45, 41, 42, 44, 46, 49, 48, 50, 55, 52, 56, 51, 53, 61, 64, 62, 65, 63, 69, 66, 72, 71, 68, 67, 74, 73, 81, 83, 87, 86, 85, 84, 88, 91, 43, 57, 60, 82]
        block_list = [47412, 47575, 47582, 47584, 47588, 47590, 47595, 47604, 47629, 47682, 47615, 47624, 47662, 47670, 47638, 47610, 47656, 47607, 47632, 47605, 47636, 47651, 47759, 47780, 47772, 47777, 47770, 47746, 47768, 47891, 47895, 47741, 47765, 47893, 47887, 47784, 47815, 47830, 47819, 47813, 47817, 47827, 47936, 47626, 47616, 47761, 47807]
        for (ken, no, block) in zip(Ken_name_list, no_list, block_list):
            ken_param_obj = KenParamMT(
                ken_name=ken,
                ken_no=no,
                ken_block_no=block)
            ken_param_obj.save()

        MdUrlMT.objects.all().delete()
        md_url_seq_list = [1, 2, 3, 4, 5]
        md_url_list = ['https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=',
                       '&block_no=',
                       '&year=',
                       '&month=',
                       '&day=1&view=a2']
        for (url_seq, url) in zip(md_url_seq_list, md_url_list):
            md_url_obj = MdUrlMT(
                md_url_seq=url_seq,
                md_url=url)
            md_url_obj.save()

        MDItemMT.objects.all().delete()
        md_item_list = ['気温(C)',
                        '相対湿度(％)',
                        '絶対湿度(g)',
                        '気圧現地平均(hPa)']
        for md_item in md_item_list:
            md_item_obj = MDItemMT(
                md_item=md_item)
            md_item_obj.save()

        SaibanMT.objects.all().delete()
        key_list = ['jobKey']
        saiban_count_list = [0]
        ketasu_list = [13]
        for (key, saiban_count, ketasu) in zip(key_list, saiban_count_list, ketasu_list):
            saiban_obj = SaibanMT(
                saiban_key=key,
                saiban_count=saiban_count,
                saiban_ketasu=ketasu)
            saiban_obj.save()

        GeneralCodeMT.objects.all().delete()
        group_key_list = ['GR000001',
                          'GR000001',
                          'GR000001',
                          'GR000001']
        general_key_list = ['01',
                            '02',
                            '03',
                            '04']
        general_code_list = ['ファイル作成処理開始前',
                             '作成中',
                             '済',
                             'エラー']
        for (group_key, general_key, general_code) in zip(group_key_list, general_key_list, general_code_list):
            general_code_obj = GeneralCodeMT(
                general_group_key=group_key,
                general_key=general_key,
                general_code=general_code)
            general_code_obj.save()

        JobQueData.objects.all().delete()
        JobParamData.objects.all().delete()
        JobParamDetailData.objects.all().delete()
        ProcessResultData.objects.all().delete()
        ProcessResultDetailData.objects.all().delete()
        FileManageData.objects.all().delete()
        TaskManageData.objects.all().delete()
        Account.objects.all().delete()

        print("task-end")









