from abc import ABCMeta, abstractmethod

##気象データ収集&ファイル作成ビジネスロジックインターフェース
class MeteorologicaldataScrapingService(metaclass=ABCMeta):
    @abstractmethod
    def mainSoup(self):
        pass

    @abstractmethod
    def MDOutput(self):
        pass




