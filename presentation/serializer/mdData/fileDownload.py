from application.service.mdData.fileDownloadService import FileDownloadService
from application.service.mdData.fileDownloadService import FileDownloadService
from application.service.mdData.Impl.fileDownloadServiceImpl import FileDownloadServiceImpl

class FileDownloadCommunicater():
    """
    ファイルダウンロードセリアライズクラス

    Attributes
    ----------
    result_file_num : str
        ファイル番号
    """

    def __init__(self, result_file_num):
        """
        Parameters
        ----------
        result_file_num : str
            ファイル番号
        """
        self.result_file_num = result_file_num

    def getFile(self):
        """
        サービス層への受け渡し

        Returns
        ----------
        str
            ファイル格納パス
        """

        try:
            file_download_service : FileDownloadService = FileDownloadServiceImpl(self.result_file_num)
            return file_download_service.mainLogic()
        except:
            raise

