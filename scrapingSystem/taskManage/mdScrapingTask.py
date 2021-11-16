from prefect import Flow, task
from scrapingSystem.models import *
import time
from scrapingSystem.MeteorologicalDataModule import meteorologicalDataModule


##気象データ収集タスク(ユーザートリガー)
@task
def scrapingTask():
    task_manage_data = TaskManageMt.objects.get(task_id='0001')
    task_manage_data.task_process_flag = '1'
    task_manage_data.save()

    error_count = 0
    while True:
        JobQueData.objects.all().order_by('job_num')
        if error_count == 10:
            print('scraping_break')
            break

        time.sleep(2)
        print('scraping_start')
        try:
            ##ジョブデータの取得
            job_data = JobQueData.objects.filter().order_by('job_num')[0]
            ##ジョブパラメータデータの取得
            job_param_data = JobParamData.objects.filter(
                job_num=job_data.job_num)
            job_param_dict = {}
            for job_param_obj in job_param_data:
                if job_param_obj.param_name == 'select_start_year':
                    job_param_dict['select_start_year'] = job_param_obj.param
                elif job_param_obj.param_name == 'select_end_year':
                    job_param_dict['select_end_year'] = job_param_obj.param
                elif job_param_obj.param_name == 'select_start_month':
                    job_param_dict['select_start_month'] = job_param_obj.param
                elif job_param_obj.param_name == 'select_end_month':
                    job_param_dict['select_end_month'] = job_param_obj.param
                elif job_param_obj.param_name == 'select_ken':
                    job_param_dict['select_ken'] = job_param_obj.param
                elif job_param_obj.param_name == 'select_md_item':
                    job_param_dict['select_md_item'] = job_param_obj.param
                else:
                    pass

            ##気象データファイル作成サービスの起動
            file_num = job_data.result_file_num
            select_start_year = job_param_dict['select_start_year']
            select_end_year = job_param_dict['select_end_year']
            select_start_month = job_param_dict['select_start_month']
            select_end_month = job_param_dict['select_end_month']
            select_md_item = job_param_dict['select_md_item']

            ##select_kenで気象庁URLにあて当てはめる情報を取得
            ken_object = KenParamMT.objects.get(ken_name = job_param_dict['select_ken'])
            ken_no = ken_object.ken_no
            ken_block = ken_object.ken_block_no

            ##県のURL情報を、一時的に無理矢理リスト化する
            ken_no_list = []
            ken_block_list = []
            ken_no_list.append(ken_no)
            ken_block_list.append(ken_block)

            ##気象庁のURL部品を取得
            MD_url = MdUrlMT.objects.all()
            md_url_str_list = []
            for i in MD_url:
                md_url_str_list.append(str(i))

            ##一旦ここでステータスを更新する
            middle_status_obj = GeneralCodeMT.objects.get(
                general_group_key = 'GR000001',
                general_key = '02')
            middle_status = middle_status_obj.general_code

            user_process = ProcessResultData.objects.get(result_file_num=job_data.result_file_num)
            user_process.file_create_status = middle_status
            user_process.save()

            mainScraping = meteorologicalDataModule.MeteorologicaldataScraping(
                file_num,
                int(select_start_year),
                int(select_end_year),
                int(select_start_month),
                int(select_end_month),
                job_param_dict['select_ken'],
                ken_no_list,
                ken_block_list,
                md_url_str_list,
                select_md_item)
            while True:
                endSign = mainScraping.mainSoup()
                if endSign == '終了':
                    break
            mainScraping.MDOutput()

            ##レコードの削除
            job_data.delete()
            job_param_data.delete()
            print('scraping_end')
        except:
            error_count += 1
            print('scraping_error' + str(error_count))
            continue

    task_manage_data = TaskManageMt.objects.get(task_id='0001')
    task_manage_data.task_process_flag = '0'
    task_manage_data.save()

def goFlow():
    with Flow("GoScraping") as flow:
        task_manage_data = TaskManageMt.objects.get(task_id='0001')
        if task_manage_data.task_process_flag == '0':
            scrapingTask()
        else:
            pass
    flow.run()





