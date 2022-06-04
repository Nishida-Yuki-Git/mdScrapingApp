from abc import ABCMeta, abstractmethod

class UserInputItemGetRepository(metaclass=ABCMeta):
    """ 画面表示ユーザーデータ取得レポジトリインターフェース
    """

    @abstractmethod
    def getYearManageMTModel(self):
        """
        気象データ収集対象年管理マスタモデル取得

        Returns
        ----------
        YearManageMT
            気象データ収集対象年管理マスタモデル
        """

        pass

    @abstractmethod
    def getYearManageMTObj(self):
        """
        気象データ収集対象年管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ収集対象年管理マスタ全レコード
        """

        pass

    @abstractmethod
    def getMonthManageMTModel(self):
        """
        気象データ収集対象月管理マスタモデル取得

        Returns
        ----------
        MonthManageMT
            気象データ収集対象月管理マスタモデル
        """

        pass

    @abstractmethod
    def getMonthManageMTObj(self):
        """
        気象データ収集対象月管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ収集対象月管理マスタ全レコード
        """

        pass

    @abstractmethod
    def getKenParamMTModel(self):
        """
        県管理マスタモデル取得

        Returns
        ----------
        KenParamMT
            県管理マスタモデル
        """

        pass

    @abstractmethod
    def getKenParamMTObj(self):
        """
        県管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            県管理マスタ全レコード
        """

        pass

    @abstractmethod
    def getMDItemMTModel(self):
        """
        気象データ項目名称管理マスタモデル取得

        Returns
        ----------
        MDItemMT
            気象データ項目名称管理マスタモデル
        """

        pass

    @abstractmethod
    def getMDItemMTObj(self):
        """
        気象データ項目名称管理マスタ全レコードセット取得

        Returns
        ----------
        dict
            気象データ項目名称管理マスタ全レコード
        """

        pass

    @abstractmethod
    def getProcessResultDataModel(self):
        """
        ユーザー処理結果情報管理データモデル取得

        Returns
        ----------
        ProcessResultData
            ユーザー処理結果情報管理データモデル
        """

        pass

    @abstractmethod
    def getProcessResultDataObj(self, user_id):
        """
        ユーザー処理結果情報管理データ全レコードセット取得

        Returns
        ----------
        dict
            ユーザー処理結果情報管理データ全レコード
        """

        pass



