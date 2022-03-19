from application.service.enum.exeBatchType import ExeBatchType
import threading
from mainJobBatch.taskManage.job import jobExecute
from application.service.mdData.errorRequestService import ErrorRequestService
from application.repository.mdData.errorRequest_repository import ErrorRequestRepository
from scrapingSystem.repositoryImple.mdData.errorRequest_repository import ErrorRequestRepositoryImple

class ErrorRequestServiceImpl(ErrorRequestService):
    def __init__(self, result_file_num):
        self.result_file_num = result_file_num

    def mainLogic(self):
        try:
            error_request_repository: ErrorRequestRepository = ErrorRequestRepositoryImple()
            user_id = error_request_repository.getErrorUserId(self.result_file_num)

            exe_batch_type = ExeBatchType.ERROR_FILE_CREATE_BATCH
            batch_exe_param_json = {
                "user_id": user_id,
                "result_file_num": self.result_file_num
            }
            thread = threading.Thread(target=jobExecute.goBatch, args=(batch_exe_param_json,exe_batch_type,))
            thread.start()

            return user_id
        except:
            raise






