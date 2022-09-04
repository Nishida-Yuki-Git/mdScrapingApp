from abc import ABCMeta, abstractmethod

class ErrorRequestRepository(metaclass=ABCMeta):
    """ エラーファイル作成リクエストレポジトリインターフェース
    """

    @abstractmethod
    def getErrorUserId(self, result_file_num):
        pass
