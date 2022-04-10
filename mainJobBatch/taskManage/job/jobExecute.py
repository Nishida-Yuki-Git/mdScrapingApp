from mainJobBatch.taskManage.task.newFileCreateTask import NewFileCreateTaskExecute
from mainJobBatch.taskManage.task.errorFileCreateTask import ErrorFileCreateTaskExecute
from application.service.enum.exeBatchType import ExeBatchType
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting

import os
import traceback
import stat

##起動クラス
class JobExecuter():
    def __init__(self, batch_exe_param_json, exe_batch_type):
        self.batch_setting = OnlineBatchSetting()
        self.batch_exe_param_json = batch_exe_param_json
        self.exe_batch_type = exe_batch_type
        self.logger = self.__setLogger()

    def jobExecute(self):
        if self.exe_batch_type == ExeBatchType.NEW_FILE_CREATE_BATCH:
            self.logger.debug("==NEW_FILE_CREATE_BATCH==")
            new_file_create_task = NewFileCreateTaskExecute(self.batch_exe_param_json['user_id'])
            new_file_create_task.jobControl()
        elif self.exe_batch_type == ExeBatchType.ERROR_FILE_CREATE_BATCH:
            self.logger.debug("==ERROR_FILE_CREATE_BATCH==")
            error_file_create_task = ErrorFileCreateTaskExecute(self.batch_exe_param_json['user_id'], self.batch_exe_param_json['result_file_num'])
            error_file_create_task.jobControl()
        else:
            pass

    def __setLogger(self):
        logger = getLogger("OnlineBatchLog")
        logger.setLevel(logging.DEBUG)
        if not logger.hasHandlers():
            handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            stream_handler = StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(handler_format)
            logger.addHandler(stream_handler)

            #file_handler = FileHandler(filename=self.batch_setting.getErrorLogPath())
            #file_handler.setLevel(logging.DEBUG)
            #file_handler.setFormatter(handler_format)
            #logger.addHandler(file_handler)
        return logger

def goBatch(batch_exe_param_json, exe_batch_type):
    executer = JobExecuter(batch_exe_param_json, exe_batch_type)

    error_log_path = '../../../error_log.txt'
    try:
        executer.jobExecute()
    except:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chmod(path=error_log_path, mode=stat.S_IWRITE)
        with open(error_log_path, 'a') as file:
            traceback.print_exc(file=file)
        os.chmod(path=error_log_path, mode=stat.S_IREAD)

