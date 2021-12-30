from application.domainLayer.util.generalCode_repository import generalCodeRepository
from scrapingSystem.models import GeneralCodeMT

class generalCodeRepositoryImple(generalCodeRepository):
    def getGeneralCode(self, general_group_key, general_key):
        status_obj = GeneralCodeMT.objects.get(
            general_group_key = general_group_key,
            general_key = general_key)
        status = status_obj.general_code
        return status




