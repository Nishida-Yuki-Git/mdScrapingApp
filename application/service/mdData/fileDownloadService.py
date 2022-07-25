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
        list
            int変換後バイナリデータ
        """

        pass


