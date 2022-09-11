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
        list
            int変換後バイナリデータ
        """

        try:
            file_download_service : FileDownloadService = FileDownloadServiceImpl(self.result_file_num)
            ret_byte_data = file_download_service.mainLogic()
            file_download_service.xl_byte_data = None
            file_download_service.tree_list = None
            file_download_service.process_index_que = None
            file_download_service.start_index_list = None
            file_download_service.last_index_list = None
            return ret_byte_data
        except:
            raise

