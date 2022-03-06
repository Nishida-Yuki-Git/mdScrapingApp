import dataclasses

@dataclasses.dataclass
class MainBusinessServiceDto:
    user_id: str
    start_year: int
    end_year: int
    start_month: int
    end_month: int
    ken_list: list = dataclasses.field(default_factory=list)
    md_item_list: list = dataclasses.field(default_factory=list)

    def getUserId(self):
        return self.user_id
    def getStartYear(self):
        return self.start_year
    def getEndYear(self):
        return self.end_year
    def getStartMonth(self):
        return self.start_month
    def getEndMonth(self):
        return self.end_month
    def getKenList(self):
        return self.ken_list
    def addKenList(self, ken_name):
        self.ken_list.append(ken_name)
    def getMdItemList(self):
        return self.md_item_list
    def addMdItemList(self, md_item_name):
        return self.md_item_list.append(md_item_name)