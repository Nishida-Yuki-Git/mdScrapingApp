from application.domainLayer.mdData.mainBusiness_repository import MainBusinessRepository
from scrapingSystem.models import *

class MainBusinessRepositoryImple(MainBusinessRepository):
    def jobQueRegister(self, saiban_job_num, user_id, result_file_num):
        user_job_data = JobQueData(
            job_num=saiban_job_num,
            user_id=user_id,
            result_file_num=result_file_num)
        user_job_data.save()

    def jobParamRegister(self, saiban_job_num, serviceDto):
        job_param_obj = JobParamData(
            job_num=saiban_job_num,
            job_start_year=serviceDto.getStartYear(),
            job_end_year=serviceDto.getEndYear(),
            job_start_month=serviceDto.getStartMonth(),
            job_end_month=serviceDto.getEndMonth())
        job_param_obj.save()

        ken_list = serviceDto.getKenList()
        md_item_list = serviceDto.getMdItemList()
        detail_regist_range = max(len(ken_list), len(md_item_list))

        for i in range(detail_regist_range):
            ken_name = ""
            md_item_name = ""
            if i < len(ken_list):
                ken_name = ken_list[i]
            if i < len(md_item_list):
                md_item_name = md_item_list[i]
            job_param_detail_obj = JobParamDetailData(
                job_num=saiban_job_num,
                job_item_id=(i + 1),
                job_ken=ken_name,
                job_md_item=md_item_name)
            job_param_detail_obj.save()

    def userProcessResultRegister(self, result_file_num, first_status_code, serviceDto):
        process_result_obj = ProcessResultData(
            result_file_num=result_file_num,
            user_id=serviceDto.getUserId(),
            file_create_status=first_status_code,
            target_start_year=serviceDto.getStartYear(),
            target_end_year=serviceDto.getEndYear(),
            target_start_month=serviceDto.getStartMonth(),
            target_end_month=serviceDto.getEndMonth())
        process_result_obj.save()

        ken_list = serviceDto.getKenList()
        md_item_list = serviceDto.getMdItemList()
        detail_regist_range = max(len(ken_list), len(md_item_list))

        for i in range(detail_regist_range):
            ken_name = ""
            md_item_name = ""
            if i < len(ken_list):
                ken_name = ken_list[i]
            if i < len(md_item_list):
                md_item_name = md_item_list[i]
            process_result_detail_obj = ProcessResultDetailData(
                result_file_num=result_file_num,
                result_item_id=(i + 1),
                target_ken=ken_name,
                target_md_item=md_item_name)
            process_result_detail_obj.save()

    def fileManageDataRegister(self, result_file_num, serviceDto):
        file_manage_data_obj = FileManageData(
            result_file_num=result_file_num,
            user_id=serviceDto.getUserId())
        file_manage_data_obj.save()


















