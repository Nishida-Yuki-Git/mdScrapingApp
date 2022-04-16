from application.repository.mdData.fileDownload_repository import FileDownloadRepository
from scrapingSystem.repositoryImple.mdData.fileDownload_repository import FileDownloadRepositoryImple
from application.service.mdData.fileDownloadService import FileDownloadService

class FileDownloadServiceImpl(FileDownloadService):
    def __init__(self, result_file_num):
        self.result_file_num = result_file_num

    def mainLogic(self):
        try:
            file_download_repo: FileDownloadRepository = FileDownloadRepositoryImple()
            user_file_obj = file_download_repo.getUserFileObject(self.result_file_num)

            return user_file_obj.create_file.name
        except:
            raise


