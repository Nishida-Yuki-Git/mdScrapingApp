from application.service.mdData.mainBusinessService import FileCreateService
from application.service.mdData.Impl.mainBusinessServiceImpl import FileCreateServiceImpl
from application.service.dto.mainBusinessServiceDto import MainBusinessServiceDto

class FileCreateCommunicater():
    """
    新規ファイル作成セリアライズクラス

    Attributes
    ----------
    user_id : str
        ユーザーID
    start_year : str
        気象データ収集開始年
    end_year : str
        気象データ収集終了年
    start_month : str
        気象データ収集開始月
    end_month : str
        気象データ収集終了月
    ken_name_list : list
        気象データ収集対象県名称リスト
    md_item_list : list
        収集対象気象データ項目名称リスト
    """

    def __init__(self, request):
        """
        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト
        """

        self.user_id = request.data['userid']
        self.start_year = request.data['start_year']
        self.end_year = request.data['end_year']
        self.start_month = request.data['start_month']
        self.end_month = request.data['end_month']

        self.ken_name_list = request.data['ken']
        self.md_item_list = request.data['md_item']

    def checkMainBusinessParam(self):
        """
        POSTデータチェック

        Returns
        ----------
        check_message : str
            チェックエラーメッセージ
        """

        if (int(self.start_year) - int(self.end_year)) > 0:
            check_message = "開始年が終了年より未来です"
            return check_message
        elif (int(self.start_month) - int(self.end_month)) > 0:
            check_message = "開始月が終了月より未来です"
            return check_message
        elif len(self.ken_name_list) == 0:
            check_message = "「県」が選択されていません"
            return check_message
        elif len(self.md_item_list) == 0:
            check_message = "「気象データ項目」が選択されていません"
            return check_message
        else:
            return None

    def serveDto(self):
        """ サービス層へのデータ受け渡し
        """

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









