from application.repository.util.generalCode_repository import generalCodeRepository
from scrapingSystem.models import GeneralCodeMT

class generalCodeRepositoryImple(generalCodeRepository):
    """ 汎用コード取得レポジトリインターフェース
    """

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

        status_obj = GeneralCodeMT.objects.get(
            general_group_key = general_group_key,
            general_key = general_key)
        status = status_obj.general_code
        return status




