from application.repository.mdData.errorRequest_repository import ErrorRequestRepository
from scrapingSystem.models import *

class ErrorRequestRepositoryImple(ErrorRequestRepository):
    """ エラーファイル作成リクエストレポジトリ実装クラス
    """

    def getErrorUserId(self, result_file_num):
        """
        エラーファイル作成ユーザーID取得

        Returns
        ----------
        error_userid : str
            エラーファイル作成ユーザーID
        """

        user_result_data = ProcessResultData.objects.get(
            result_file_num = result_file_num)
        error_user_id = user_result_data.user_id
        return error_user_id