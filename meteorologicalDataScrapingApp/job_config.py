import os
from pathlib import Path

##バッチ基盤用設定クラス
class OnlineBatchSetting():
    def __init__(self):
        ##開発環境用Database設定
        '''
        self.host_id = 'localhost'
        self.port_num = '3306'
        self.db_user = 'root'
        self.db_password = 'gyudon176'
        self.database_name = 'mdsystemdb'
        '''

        ##本番環境用Databse設定
        self.host_id = 'apidb'
        self.port_num = '3306'
        self.db_user = 'yuki'
        self.db_password = 'gyudon176'
        self.database_name = 'mdsystemdb'

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.MEDIA_URL = '/media/'
        self.MEDIA_ROOT = os.path.join(self.BASE_DIR, 'media')
        self.FILE_SAVE_DIR = '/file/'

    def getHostId(self):
        return self.host_id
    def getPortNum(self):
        return self.port_num
    def getDbUser(self):
        return self.db_user
    def getDbPassWord(self):
        return self.db_password
    def getDatabaseName(self):
        return self.database_name
    def getBaseDir(self):
        return self.BASE_DIR
    def getMediaUrl(self):
        return self.MEDIA_URL
    def getMediaRoot(self):
        return self.MEDIA_ROOT
    def getFileSaveDir(self):
        return self.FILE_SAVE_DIR