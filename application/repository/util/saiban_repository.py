from abc import ABCMeta, abstractmethod

class saibanRepository(metaclass=ABCMeta):
    """ 採番レポジトリインターフェース
    """

    @abstractmethod
    def getSaibanCode(self, saibanKey):
        """
        採番値取得

        Parameters
        ----------
        saibanKey : str
            採番管理キー

        Returns
        ----------
        create_str : str
            採番値
        """

        pass



