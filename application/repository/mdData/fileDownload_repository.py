from abc import ABCMeta, abstractmethod

class FileDownloadRepository(metaclass=ABCMeta):
    """ ファイルダウンロードレポジトリインターフェース
    """

    @abstractmethod
    def getUserFileObject(self, result_file_num):
        """
        ダウンロード対象ファイル情報取得

        Returns
        ----------
        dict
            ダウンロード対象ファイル情報
        """

        pass
