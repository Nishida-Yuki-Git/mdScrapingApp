from mainJobBatch.taskManage.task.newFileCreateTask import NewFileCreateTaskExecute
from mainJobBatch.taskManage.task.errorFileCreateTask import ErrorFileCreateTaskExecute
from application.service.enum.exeBatchType import ExeBatchType
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
import os
import traceback
import stat


class JobExecuter():
    """
    オンライン随時バッチ起動クラス

    Attributes
    ----------
    batch_setting : OnlineBatchSetting
        バッチ用設定ファイル
    batch_exe_param_json : dict
        バッチ起動パラメータ
    exe_batch_type : ExeBatchType
        バッチ区分列挙型
    logger : logging
        ログ出力オブジェクト
    """

    def __init__(self, batch_exe_param_json, exe_batch_type):
        """
        Parameters
        ----------
        batch_exe_param_json : dict
            バッチ起動パラメータ
        exe_batch_type : ExeBatchType
            バッチ区分列挙型
        """

        self.batch_setting = OnlineBatchSetting()
        self.batch_exe_param_json = batch_exe_param_json
        self.exe_batch_type = exe_batch_type
        self.logger = self.__setLogger()

    def jobExecute(self):
        """ バッチ実行
        """

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
        """ ログ出力オブジェクト設定
        """

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
    executer.jobExecute()

