from application.service.enum.exeBatchType import ExeBatchType
import threading
from mainJobBatch.taskManage.job import jobExecute
from application.service.mdData.errorRequestService import ErrorRequestService

class ErrorRequestServiceImpl(ErrorRequestService):
    def __init__(self, user_id, result_file_num):
        self.user_id = user_id
        self.result_file_num = result_file_num

    def mainLogic(self):
        try:
            exe_batch_type = ExeBatchType.ERROR_FILE_CREATE_BATCH
            batch_exe_param_json = {
                "user_id": self.user_id,
                "result_file_num": self.result_file_num
            }
            thread = threading.Thread(target=jobExecute.goBatch, args=(batch_exe_param_json,exe_batch_type,))
            thread.start()
        except:
            raise






