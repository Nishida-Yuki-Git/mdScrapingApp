from abc import ABCMeta, abstractmethod

class FileCreateService(metaclass=ABCMeta):
    """ 新規ファイル作成サービスインターフェース
    """

    @abstractmethod
    def mainLogic(self):
        """ 新規ファイル作成リクエスト実行
        """

        pass






