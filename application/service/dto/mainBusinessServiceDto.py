import dataclasses

@dataclasses.dataclass
class MainBusinessServiceDto:
    """
    新規ファイル作成サービスDto

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
    ken_list : list
        気象データ収集対象県リスト
    md_item_list : list
        収集対象気象データ項目リスト
    """

    user_id: str
    start_year: int
    end_year: int
    start_month: int
    end_month: int
    ken_list: list = dataclasses.field(default_factory=list)
    md_item_list: list = dataclasses.field(default_factory=list)

    def getUserId(self):
        """
        ユーザーIDの返却

        Returns
        ----------
        userid : str
            ユーザーID
        """

        return self.user_id

    def getStartYear(self):
        """
        気象データ収集開始年の返却

        Returns
        ----------
        start_year : str
            気象データ収集開始年
        """

        return self.start_year

    def getEndYear(self):
        """
        気象データ収集終了年の返却

        Returns
        ----------
        end_year : str
            気象データ収集終了年
        """

        return self.end_year

    def getStartMonth(self):
        """
        気象データ収集開始月の返却

        Returns
        ----------
        start_month : str
            気象データ収集開始月
        """

        return self.start_month

    def getEndMonth(self):
        """
        気象データ収集終了月の返却

        Returns
        ----------
        end_month : str
            気象データ収集終了月
        """

        return self.end_month

    def getKenList(self):
        """
        気象データ収集対象県リストの返却

        Returns
        ----------
        ken_list : str
            気象データ収集対象県リスト
        """

        return self.ken_list

    def addKenList(self, ken_name):
        """
        気象データ収集対象県リストへの、県名称の追加

        Parameters
        ----------
        ken_name : str
            県名称
        """

        self.ken_list.append(ken_name)

    def getMdItemList(self):
        """
        収集対象気象データ項目リストの返却

        Returns
        ----------
        md_item_list : list
            収集対象気象データ項目リスト
        """

        return self.md_item_list

    def addMdItemList(self, md_item_name):
        """
        収集対象気象データ項目リストへの、気象データ項目名称の追加

        Parameters
        ----------
        md_item_name : str
            気象データ項目名称
        """

        return self.md_item_list.append(md_item_name)