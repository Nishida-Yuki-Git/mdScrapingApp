from application.domainLayer.mdData.fileDownload_repository import FileDownloadRepository
from scrapingSystem.repositoryImple.mdData.fileDownload_repository import FileDownloadRepositoryImple

class FileDownloadService():
    def __init__(self, result_file_num):
        self.sheet_name = 'sheet1'
        self.result_file_num = result_file_num

    def mainLogic(self):
        try:
            file_download_repo: FileDownloadRepository = FileDownloadRepositoryImple()
            user_file_obj = file_download_repo.getUserFileObject(self.result_file_num)

            url = user_file_obj.create_file.name

            file_url = {
                'file_url': url
            }
            return file_url
        except:
            raise


