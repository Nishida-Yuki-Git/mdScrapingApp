from application.repository.mdData.errorRequest_repository import ErrorRequestRepository
from scrapingSystem.models import *

class ErrorRequestRepositoryImple(ErrorRequestRepository):
    def getErrorUserId(self, result_file_num):
        user_result_data = ProcessResultData.objects.get(
            result_file_num = result_file_num)
        error_user_id = user_result_data.user_id
        return error_user_id