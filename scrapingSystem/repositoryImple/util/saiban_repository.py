from application.repository.util.saiban_repository import saibanRepository
from scrapingSystem.models import SaibanMT

class saibanRepositoryImple(saibanRepository):
    def getSaibanCode(self, saibanKey):
        saiban_data_obj = SaibanMT.objects.get(pk=saibanKey)
        saiban_count = saiban_data_obj.saiban_count
        saiban_ketasu = saiban_data_obj.saiban_ketasu

        create_str = ''
        create_str += str(saiban_count)
        padding_count = (saiban_ketasu - len(str(saiban_count)))
        roop_count = 0
        for i in range(saiban_ketasu):
            roop_count += 1
            create_str = list(create_str)
            create_str.insert(0, '0')
            create_str = ''.join(create_str)
            if roop_count == padding_count:
                break

        saiban_data_obj = SaibanMT.objects.get(pk=saibanKey)
        saiban_data_obj.saiban_count = (saiban_count + 1)
        saiban_data_obj.save()

        return create_str





