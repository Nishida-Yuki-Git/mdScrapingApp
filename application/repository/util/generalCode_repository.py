from abc import ABCMeta, abstractmethod

class generalCodeRepository(metaclass=ABCMeta):
    """ 汎用コード取得レポジトリインターフェース
    """

    @abstractmethod
    def getGeneralCode(self, general_group_key, general_key):
        """
        汎用コード取得

        Parameters
        ----------
        general_group_key : str
            汎用グループキー
        general_key : str
            汎用キー

        Returns
        ----------
        status : str
            ステータス名称
        """

        pass



