from abc import ABCMeta, abstractmethod

class UserInputItemGetService(metaclass=ABCMeta):
    """ 画面表示ユーザーデータ取得サービスインターフェース
    """

    @abstractmethod
    def getYearManageMTModel(self):
        """ 気象データ収集対象年管理マスタモデル取得
        """

        pass

    @abstractmethod
    def getYearManageMTObj(self):
        """ 気象データ収集対象年管理マスタ全レコードセット取得
        """

        pass

    @abstractmethod
    def getMonthManageMTModel(self):
        """ 気象データ収集対象月管理マスタモデル取得
        """

        pass

    @abstractmethod
    def getMonthManageMTObj(self):
        """ 気象データ収集対象月管理マスタ全レコードセット取得
        """

        pass

    @abstractmethod
    def getKenParamMTModel(self):
        """ 県管理マスタモデル取得
        """

        pass

    @abstractmethod
    def getKenParamMTObj(self):
        """ 県管理マスタ全レコードセット取得
        """

        pass

    @abstractmethod
    def getMDItemMTModel(self):
        """ 気象データ項目名称管理マスタモデル取得
        """

        pass

    @abstractmethod
    def getMDItemMTObj(self):
        """ 気象データ項目名称管理マスタ全レコードセット取得
        """

        pass

    @abstractmethod
    def getProcessResultDataModel(self):
        """ ユーザー処理結果情報管理データモデル取得
        """

        pass

    @abstractmethod
    def getProcessResultDataObj(self):
        """ ユーザー処理結果情報管理データ全レコードセット取得
        """

        pass






