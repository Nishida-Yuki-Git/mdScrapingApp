from application.system_application.mdData.errorRequestService import ErrorRequestService

class ErrorRequestCommunicater():
    def __init__(self, request):
        self.user_id = request.data['userid']
        self.result_file_num = request.data['result_file_num']

    def serveParam(self):
        try:
            error_request_service = ErrorRequestService(self.user_id, self.result_file_num)
            error_request_service.mainLogic()
        except:
            raise









