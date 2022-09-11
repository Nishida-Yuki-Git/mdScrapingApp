from abc import ABCMeta, abstractmethod

class MdScrapingXlWriteService(metaclass=ABCMeta):
    """ 気象データ中間コミット書き込みサービス基底インターフェース
    """

    @abstractmethod
    def xlMiddleCommit(self, output_data):
        """
        気象データ中間コミット書き込み実装

        Parameters
        ----------
        output_data : list
            書き込み気象データ
        """

        pass




