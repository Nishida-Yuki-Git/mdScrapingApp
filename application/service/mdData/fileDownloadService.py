from abc import ABCMeta, abstractmethod

class FileDownloadService(metaclass=ABCMeta):
    """ ファイルダウンロードサービスインターフェース
    """

    @abstractmethod
    def mainLogic(self):
        """
        ファイルダウンロード実行

        Returns
        ----------
        str
            ファイル格納パス
        """

        pass


