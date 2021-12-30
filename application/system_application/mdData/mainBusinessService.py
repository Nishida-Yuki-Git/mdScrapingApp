from application.domainLayer.util.generalCode_repository import generalCodeRepository
from application.domainLayer.util.saiban_repository import saibanRepository
from application.domainLayer.mdData.mainBusiness_repository import MainBusinessRepository
from scrapingSystem.repositoryImple.util.generalCode_repository import generalCodeRepositoryImple
from scrapingSystem.repositoryImple.util.saiban_repository import saibanRepositoryImple
from scrapingSystem.repositoryImple.mdData.mainBusiness_repository import MainBusinessRepositoryImple
import datetime
from mainJobBatch.taskManage.job import jobExecute
import threading

class FileCreateService():
    def __init__(self, service_dto):
        self.service_dto = service_dto
        self.saiban_key = 'jobKey'

    def mainLogic(self):
        try:
            saiban_repository: saibanRepository = saibanRepositoryImple()
            saiban_job_num = saiban_repository.getSaibanCode(self.saiban_key)

            file_num_date_time = (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

            general_code_repository: generalCodeRepository = generalCodeRepositoryImple()
            first_status_code = general_code_repository.getGeneralCode('GR000001', '01')

            main_repository: MainBusinessRepository = MainBusinessRepositoryImple()
            main_repository.jobQueRegister(saiban_job_num, self.service_dto.getUserId(), file_num_date_time)
            main_repository.jobParamRegister(saiban_job_num, self.service_dto)
            main_repository.userProcessResultRegister(file_num_date_time, first_status_code, self.service_dto)
            main_repository.fileManageDataRegister(file_num_date_time, self.service_dto)

            thread = threading.Thread(target=jobExecute.goFlow, args=(self.service_dto.getUserId(),))
            thread.start()
        except:
            raise






