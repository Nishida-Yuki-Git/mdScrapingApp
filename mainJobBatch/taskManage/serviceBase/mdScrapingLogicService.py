from abc import ABCMeta, abstractmethod

class MeteorologicaldataScrapingService(metaclass=ABCMeta):
    """ 気象データ収集&ファイル作成ビジネスサービス基底インターフェース
    """

    @abstractmethod
    def mainSoup(self):
        """
        Webスクレイピング及びファイル出力処理

        Returns
        ----------
        end : str
            ビジネスロジック処理終了サイン
        """

        pass

    @abstractmethod
    def MDOutput(self):
        """ 気象データ収集後のファイル作成処理
        """

        pass




