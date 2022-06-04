from application.service.mdData.errorRequestService import ErrorRequestService
from application.service.mdData.Impl.errorRequestServiceImpl import ErrorRequestServiceImpl

class ErrorRequestCommunicater():
    """
    エラーファイル作成セリアライズクラス

    Attributes
    ----------
    result_file_num : str
        ファイル番号
    """

    def __init__(self, request):
        """
        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト
        """

        self.result_file_num = request.data['result_file_num']

    def serveParam(self):
        """
        サービス層への受け渡し

        Returns
        ----------
        userid : str
            ユーザーID
        """

        try:
            error_request_service: ErrorRequestService = ErrorRequestServiceImpl(self.result_file_num)
            return error_request_service.mainLogic()
        except:
            raise









