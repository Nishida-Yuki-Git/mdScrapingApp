import os
from pathlib import Path
from commonUtils.cryptUtils.decrypt import Decrypt

##バッチ基盤用設定クラス
class OnlineBatchSetting():
    def __init__(self):
        self.decryptInstance = Decrypt.get_instance()

        ##開発環境用Database設定
        '''
        self.host_id = 'localhost'
        self.port_num = self.decryptInstance.decryptMethod('0CTDx9fP37x8RH8nVFPyNQ==')
        self.db_user = self.decryptInstance.decryptMethod('kuY/GS/nKi760mPD0BcjVA==')
        self.db_password = self.decryptInstance.decryptMethod('Y8PzaXzIQ0JQ8nnrk1RrCQ==')
        self.database_name = self.decryptInstance.decryptMethod('VOhRpoC6ceWlWpXMHb5Rdg==')
        '''

        ##本番環境用Databse設定
        self.host_id = self.decryptInstance.decryptMethod('fRAQORH+jxycZpvuPRgouQ==')
        self.port_num = self.decryptInstance.decryptMethod('0CTDx9fP37x8RH8nVFPyNQ==')
        self.db_user = self.decryptInstance.decryptMethod('UDjr0GudoYMQ+h1gm5QsfQ==')
        self.db_password = self.decryptInstance.decryptMethod('Y8PzaXzIQ0JQ8nnrk1RrCQ==')
        self.database_name = self.decryptInstance.decryptMethod('VOhRpoC6ceWlWpXMHb5Rdg==')

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