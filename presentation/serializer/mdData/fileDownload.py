from application.service.mdData.fileDownloadService import FileDownloadService
from application.service.mdData.fileDownloadService import FileDownloadService
from application.service.mdData.Impl.fileDownloadServiceImpl import FileDownloadServiceImpl

class FileDownloadCommunicater():
    def __init__(self, result_file_num):
        self.result_file_num = result_file_num

    def getFile(self):
        try:
            file_download_service : FileDownloadService = FileDownloadServiceImpl(self.result_file_num)
            return file_download_service.mainLogic()
        except:
            raise

