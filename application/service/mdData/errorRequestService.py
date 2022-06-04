from abc import ABCMeta, abstractmethod

class ErrorRequestService(metaclass=ABCMeta):
    """ エラーファイル作成リクエストサービスインターフェース
    """

    @abstractmethod
    def mainLogic(self):
        """
        エラーファイル作成リクエスト実行

        Returns
        ----------
        userid : str
            ユーザーID
        """

        pass






