'''
Created on 2021/11/06

@author: nishidayuki
'''

##採番サービス
from scrapingSystem.models import SaibanMT

class SaibanService():
    def __init__(self, key):
        self.saibanKety = key
        self.saiban_count = None
        self.saiban_ketasu = None

    def saibanMethod(self):
        self.__getSaibanData()
        saiban_str = self.__mainSaibanProcessor()
        return saiban_str

    ##採番管理マスタからキーを元に情報を取得
    def __getSaibanData(self):
        saiban_data_obj = SaibanMT.objects.get(pk=self.saibanKety)
        self.saiban_count = saiban_data_obj.saiban_count
        self.saiban_ketasu = saiban_data_obj.saiban_ketasu

    ##採番処理
    def __mainSaibanProcessor(self):
        ##採番処理
        create_str = ''
        create_str += str(self.saiban_count)
        padding_count = (self.saiban_ketasu - len(str(self.saiban_count)))
        roop_count = 0
        for i in range(self.saiban_ketasu):
            roop_count += 1
            create_str = list(create_str)
            create_str.insert(0, '0')
            create_str = ''.join(create_str)
            if roop_count == padding_count:
                break

        ##DBの採番カウントアップ
        saiban_data_obj = SaibanMT.objects.get(pk=self.saibanKety)
        saiban_data_obj.saiban_count = (self.saiban_count + 1)
        saiban_data_obj.save()

        return create_str













