from application.repository.mdData.fileDownload_repository import FileDownloadRepository
from scrapingSystem.models import *

class FileDownloadRepositoryImple(FileDownloadRepository):
    def getUserFileObject(self, result_file_num):
        user_file_obj = FileManageData.objects.get(
            result_file_num = result_file_num)
        return user_file_obj

