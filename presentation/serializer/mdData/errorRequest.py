from application.service.mdData.errorRequestService import ErrorRequestService
from application.service.mdData.Impl.errorRequestServiceImpl import ErrorRequestServiceImpl

class ErrorRequestCommunicater():
    def __init__(self, request):
        self.result_file_num = request.data['result_file_num']

    def serveParam(self):
        try:
            error_request_service: ErrorRequestService = ErrorRequestServiceImpl(self.result_file_num)
            return error_request_service.mainLogic()
        except:
            raise









