from application.service.mdData.mainBusinessService import FileCreateService
from application.service.mdData.Impl.mainBusinessServiceImpl import FileCreateServiceImpl
from application.service.dto.mainBusinessServiceDto import MainBusinessServiceDto

class FileCreateCommunicater():
    def __init__(self, request):
        self.user_id = request.data['userid']
        self.start_year = request.data['start_year']
        self.end_year = request.data['end_year']
        self.start_month = request.data['start_month']
        self.end_month = request.data['end_month']

        self.ken_name_list = request.data['ken']
        self.md_item_list = request.data['md_item']

    def serveDto(self):
        service_dto = MainBusinessServiceDto(
            self.user_id,
            self.start_year,
            self.end_year,
            self.start_month,
            self.end_month)

        for ken_name in self.ken_name_list:
            service_dto.addKenList(ken_name)
        for md_item in self.md_item_list:
            service_dto.addMdItemList(md_item)

        try:
            my_service : FileCreateService = FileCreateServiceImpl(service_dto)
            my_service.mainLogic()
        except:
            raise









