from application.repository.mdData.fileDownload_repository import FileDownloadRepository
from scrapingSystem.models import *

class FileDownloadRepositoryImple(FileDownloadRepository):
    """ ファイルダウンロードレポジトリインターフェース
    """

    def getUserFileObject(self, result_file_num):
        """
        ダウンロード対象ファイル情報取得

        Returns
        ----------
        dict
            ダウンロード対象ファイル情報
        """

        user_file_obj = FileManageData.objects.get(
            result_file_num = result_file_num)
        return user_file_obj

