from application.system_application.mdData.fileDownloadService import FileDownloadService

class FileDownloadCommunicater():
    def __init__(self, request):
        self.result_file_num = request.data['result_file_num']

    def getFile(self):
        try:
            file_download_service = FileDownloadService(self.result_file_num)
            return file_download_service.mainLogic()
        except:
            raise









